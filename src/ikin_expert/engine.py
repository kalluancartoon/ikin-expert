import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Set, Tuple, Union
from collections import defaultdict
from pydantic import BaseModel

# =============================================================================
# 1. VARIÁVEIS DE LIGAÇÃO (BINDINGS)
# =============================================================================

class Match:
    """
    Representa uma variável de ligação.
    Ex: Pattern(Paciente, id=MATCH.p_id)
    """
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f"<Match {self.name}>"

    def __getattr__(self, name):
        # Permite sintaxe MATCH.qualquer_coisa
        return Match(name)

# Instância global para uso fácil
MATCH = Match("root")

# =============================================================================
# 2. ESTRUTURA DE DADOS (Facts & Tokens)
# =============================================================================

class Fact(BaseModel):
    """
    Unidade atômica de informação. Imutável e Hashable.
    """
    model_config = {'frozen': True}

class Token:
    """
    Representa um caminho parcial na rede.
    Carrega a lista de fatos que satisfazem as regras até aquele ponto.
    """
    
    def __init__(self, parent: Optional['Token'], fact: Optional[Fact]):
        self.parent = parent
        self.fact = fact
        # Cache da lista plana para performance em Joins
        self._flat_list = None
    
    def to_list(self) -> List[Fact]:
        if self._flat_list is None:
            facts = []
            current = self
            # Navega para trás até chegar no Token Raiz
            while current is not None:
                if current.fact is not None:
                    facts.append(current.fact)
                current = current.parent
            self._flat_list = list(reversed(facts))
        return self._flat_list

    def get_fact_by_index(self, index: int) -> Optional[Fact]:
        """Recupera um fato específico do histórico do token."""
        facts = self.to_list()
        if 0 <= index < len(facts):
            return facts[index]
        return None

# =============================================================================
# 3. PADRÕES
# =============================================================================

class Pattern:
    def __init__(self, model_class: Type[Fact], **constraints):
        self.model_class = model_class
        self.constraints = constraints

# =============================================================================
# 4. NÓS DA REDE (Alpha, Beta, HashJoin)
# =============================================================================

class ReteNode:
    def __init__(self):
        self.children: List['ReteNode'] = []

    def add_child(self, node: 'ReteNode'):
        self.children.append(node)
        return node

# --- ALPHA NETWORK ---

class AlphaNode(ReteNode):
    """Filtra fatos individuais (Ex: idade > 18)."""
    def __init__(self, field: str, op: str, value: Any):
        super().__init__()
        self.field = field
        self.op = op
        self.value = value
        self.items: Set[Fact] = set()

    def test(self, fact: Fact) -> bool:
        if not hasattr(fact, self.field): return False
        fact_val = getattr(fact, self.field)
        
        # Se o valor for um MATCH (variável), AlphaNode SEMPRE aprova.
        # A validação real acontecerá no HashJoinNode.
        if isinstance(self.value, Match):
            return True

        if self.op == "eq": return fact_val == self.value
        if self.op == "gt": return fact_val > self.value
        if self.op == "gte": return fact_val >= self.value
        if self.op == "lt": return fact_val < self.value
        if self.op == "lte": return fact_val <= self.value
        if self.op == "neq": return fact_val != self.value
        return False

    def activate(self, fact: Fact, engine):
        if self.test(fact):
            self.items.add(fact)
            for child in self.children:
                if isinstance(child, AlphaNode):
                    child.activate(fact, engine)
                elif isinstance(child, BetaNode):
                    child.right_activate(fact, engine)
                elif isinstance(child, RuleTerminalNode):
                    child.activate_single(fact, engine)

class TypeNode(ReteNode):
    def __init__(self, model_class: Type[Fact]):
        super().__init__()
        self.model_class = model_class
    
    def activate(self, fact: Fact, engine):
        if isinstance(fact, self.model_class):
            for child in self.children:
                if isinstance(child, AlphaNode):
                    child.activate(fact, engine)
                elif isinstance(child, BetaNode):
                    child.right_activate(fact, engine)
                elif isinstance(child, RuleTerminalNode):
                    child.activate_single(fact, engine)

# --- BETA NETWORK (O Coração da v2.0) ---

class BetaNode(ReteNode):
    """Classe base para nós Beta."""
    def __init__(self):
        super().__init__()
        self.left_memory: List[Token] = []
        self.right_memory: List[Fact] = []

    def left_activate(self, token: Token, engine):
        raise NotImplementedError

    def right_activate(self, fact: Fact, engine):
        raise NotImplementedError
    
    def propagate(self, parent_token: Token, new_fact: Fact, engine):
        new_token = Token(parent=parent_token, fact=new_fact)
        for child in self.children:
            if isinstance(child, BetaNode):
                child.left_activate(new_token, engine)
            elif isinstance(child, RuleTerminalNode):
                child.activate_token(new_token, engine)

class CartesianBetaNode(BetaNode):
    """
    Join Padrão (Sem índice). Faz o produto cartesiano.
    Usado quando não há variáveis compartilhadas.
    """
    def left_activate(self, token: Token, engine):
        self.left_memory.append(token)
        for fact in self.right_memory:
            self.propagate(token, fact, engine)

    def right_activate(self, fact: Fact, engine):
        self.right_memory.append(fact)
        for token in self.left_memory:
            self.propagate(token, fact, engine)

class HashJoinNode(BetaNode):
    """
    NOVO NA V2.0: Join Indexado (Hash Join).
    Usa Dicionários para O(1) lookups.
    """
    def __init__(self, left_idx: int, left_field: str, right_field: str):
        super().__init__()
        # Configuração do Join
        self.left_idx = left_idx    # Qual fato do histórico tem a chave?
        self.left_field = left_field # Qual campo é a chave?
        self.right_field = right_field # Qual campo do novo fato é a chave?
        
        # Memórias Indexadas (Hashmaps)
        # Chave -> Lista de Itens
        self.left_index: Dict[Any, List[Token]] = defaultdict(list)
        self.right_index: Dict[Any, List[Fact]] = defaultdict(list)

    def _get_key(self, obj: Any, field: str) -> Any:
        return getattr(obj, field, None)

    def left_activate(self, token: Token, engine):
        # 1. Descobre a chave de join no histórico
        target_fact = token.get_fact_by_index(self.left_idx)
        if not target_fact: return
        
        key = self._get_key(target_fact, self.left_field)
        
        # 2. Indexa
        self.left_index[key].append(token)
        
        # 3. Busca Instantânea na memória da direita
        if key in self.right_index:
            for fact in self.right_index[key]:
                self.propagate(token, fact, engine)

    def right_activate(self, fact: Fact, engine):
        # 1. Descobre a chave no fato novo
        key = self._get_key(fact, self.right_field)
        
        # 2. Indexa
        self.right_index[key].append(fact)
        
        # 3. Busca Instantânea na memória da esquerda
        if key in self.left_index:
            for token in self.left_index[key]:
                self.propagate(token, fact, engine)

class DummyBetaNode(ReteNode):
    """Iniciador da rede Beta."""
    def left_activate(self, engine):
        for child in self.children:
            if isinstance(child, BetaNode):
                # Token raiz (sem pai, sem fato)
                child.left_activate(Token(None, None), engine)

class RuleTerminalNode(ReteNode):
    """Ativador Final."""
    def __init__(self, rule_name: str, action: Callable, salience: int):
        super().__init__()
        self.rule_name = rule_name
        self.action = action
        self.salience = salience

    def activate_token(self, token: Token, engine):
        facts = token.to_list()
        engine.agenda.add_activation(self, facts)

    def activate_single(self, fact: Fact, engine):
        engine.agenda.add_activation(self, [fact])

# =============================================================================
# 5. MOTOR E COMPILADOR INTELIGENTE
# =============================================================================

class Activation:
    def __init__(self, node: RuleTerminalNode, facts: List[Fact]):
        self.node = node
        self.facts = facts
        self.priority = node.salience 

class Agenda:
    def __init__(self):
        self.activations: List[Activation] = []

    def add_activation(self, node: RuleTerminalNode, facts: List[Fact]):
        self.activations.append(Activation(node, facts))
        self.activations.sort(key=lambda x: x.priority, reverse=True)

    def pop(self) -> Optional[Activation]:
        if not self.activations: return None
        return self.activations.pop(0)

    def clear(self):
        self.activations.clear()

def Rule(*patterns: Pattern, salience: int = 0):
    def decorator(func):
        func._is_rule = True
        func._patterns = patterns
        func._salience = salience
        return func
    return decorator

class KnowledgeEngine:
    def __init__(self):
        self.agenda = Agenda()
        self.rete_root: Dict[Type[Fact], TypeNode] = {}
        self.dummy_beta = DummyBetaNode()
        self._build_network()

    def _build_network(self):
        for name, method in inspect.getmembers(self):
            if getattr(method, "_is_rule", False):
                self._compile_rule(method)

    def _get_or_create_alpha_chain(self, pattern: Pattern) -> ReteNode:
        if pattern.model_class not in self.rete_root:
            self.rete_root[pattern.model_class] = TypeNode(pattern.model_class)
        current = self.rete_root[pattern.model_class]
        
        for field_op, value in pattern.constraints.items():
            if "__" in field_op: field, op = field_op.split("__")
            else: field, op = field_op, "eq"
            
            # Se for MATCH (Binding), o AlphaNode apenas passa adiante (sucesso automático)
            # A filtragem real será no HashJoin
            
            found = None
            for child in current.children:
                if isinstance(child, AlphaNode) and \
                   child.field == field and child.op == op and child.value == value:
                    found = child
                    break
            
            if found:
                current = found
            else:
                new_node = AlphaNode(field, op, value)
                current.add_child(new_node)
                current = new_node
        return current

    def _compile_rule(self, method):
        patterns = method._patterns
        terminal = RuleTerminalNode(method.__name__, method, method._salience)

        if len(patterns) == 1:
            last_alpha = self._get_or_create_alpha_chain(patterns[0])
            last_alpha.add_child(terminal)
        else:
            # COMPILADOR BETA INTELIGENTE v2.0
            # Rastreia variáveis para decidir entre CartesianJoin ou HashJoin
            
            # Mapa de Variáveis: "var_name" -> (pattern_index, field_name)
            known_vars: Dict[str, Tuple[int, str]] = {}
            
            current_beta_input = self.dummy_beta
            
            # Analisa o padrão 0 (inicial) para popular variáveis
            first_pattern = patterns[0]
            for k, v in first_pattern.constraints.items():
                if isinstance(v, Match):
                    field = k.split("__")[0]
                    known_vars[v.name] = (0, field)

            # Começa a construir a cadeia a partir do padrão 1
            # O padrão 0 entra via Dummy -> Left Input do primeiro Beta
            
            for i, pattern in enumerate(patterns):
                alpha_tail = self._get_or_create_alpha_chain(pattern)
                
                # Se for o primeiro padrão, ele só alimenta o input, não cria join ainda
                if i == 0:
                    continue

                # Decisão: HashJoin ou CartesianJoin?
                join_var = None
                join_config = None # (left_idx, left_field, right_field)

                # Verifica se este padrão usa alguma variável já conhecida
                for k, v in pattern.constraints.items():
                    if isinstance(v, Match):
                        field_name = k.split("__")[0]
                        if v.name in known_vars:
                            # BINGO! Encontramos uma chave de join.
                            left_idx, left_field = known_vars[v.name]
                            join_config = (left_idx, left_field, field_name)
                            join_var = v.name
                            break # Por simplicidade, usamos a primeira chave que acharmos
                        else:
                            # Nova variável, registra
                            known_vars[v.name] = (i, field_name)

                if join_config:
                    # Cria nó Otimizado
                    join_node = HashJoinNode(*join_config)
                    # print(f" [COMPILER] Otimizando regra '{method.__name__}': HashJoin em {join_var.name}")
                else:
                    # Join Genérico
                    join_node = CartesianBetaNode()

                current_beta_input.add_child(join_node)
                alpha_tail.add_child(join_node)
                current_beta_input = join_node
            
            current_beta_input.add_child(terminal)
            self.dummy_beta.left_activate(self)

    def declare(self, fact: Fact):
        fact_type = type(fact)
        if fact_type in self.rete_root:
            self.rete_root[fact_type].activate(fact, self)

    def run(self):
        steps = 0
        while steps < 1000:
            activation = self.agenda.pop()
            if not activation: break
            try:
                sig = inspect.signature(activation.node.action)
                params = len(sig.parameters)
                if params == 0: activation.node.action()
                else: activation.node.action(*activation.facts[:params])
            except Exception as e:
                print(f" [ERROR] Rule {activation.node.rule_name}: {e}")
            steps += 1