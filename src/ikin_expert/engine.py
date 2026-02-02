import inspect
from typing import Any, Callable, Dict, List, Optional, Type, Set, Union
from pydantic import BaseModel

# =============================================================================
# 1. ESTRUTURA DE DADOS (Pydantic & Memória)
# =============================================================================

class Fact(BaseModel):
    """
    A unidade atômica de informação.
    Imutável e hashable para funcionar dentro do Algoritmo Rete.
    """
    model_config = {'frozen': True}

# =============================================================================
# 2. DEFINIÇÃO DE PADRÕES (A Linguagem da Regra)
# =============================================================================

class Pattern:
    """ Define o que a regra procura na memória. """
    def __init__(self, model_class: Type[Fact], **constraints):
        self.model_class = model_class
        self.constraints = constraints

# =============================================================================
# 3. COMPONENTES DO ALGORITMO RETE (O Grafo)
# =============================================================================

class ReteNode:
    """Classe base para todos os nós da rede."""
    def __init__(self):
        self.children: List['ReteNode'] = []

    def add_child(self, node: 'ReteNode'):
        self.children.append(node)
        return node

class Agenda:
    """Gerencia a fila de execução baseada em Prioridade (Salience)."""
    def __init__(self):
        self.activations: List['Activation'] = []

    def add_activation(self, activation: 'Activation'):
        self.activations.append(activation)
        # Ordena: Maior prioridade (Salience) no topo (índice 0)
        self.activations.sort(key=lambda x: x.priority, reverse=True)

    def pop(self) -> Optional['Activation']:
        if not self.activations:
            return None
        return self.activations.pop(0)

    def clear(self):
        self.activations.clear()

class Activation:
    """Representa uma regra pronta para disparar."""
    def __init__(self, node: 'TerminalNode', fact: Fact):
        self.node = node
        self.fact = fact
        self.priority = node.salience 

class TerminalNode(ReteNode):
    """
    O fim da linha. Se o dado chegou aqui, a regra deve ser ativada.
    """
    def __init__(self, rule_name: str, action: Callable, salience: int):
        super().__init__()
        self.rule_name = rule_name
        self.action = action
        self.salience = salience

    def activate(self, fact: Fact, agenda: Agenda):
        # Adiciona a regra na Agenda para ser executada depois
        agenda.add_activation(Activation(self, fact))

class AlphaNode(ReteNode):
    """
    O Filtro. Verifica UMA condição específica (Ex: idade > 18).
    """
    def __init__(self, field: str, op: str, value: Any):
        super().__init__()
        self.field = field
        self.op = op
        self.value = value

    def test(self, fact: Fact) -> bool:
        # Extrai o valor do fato com segurança
        if not hasattr(fact, self.field):
            return False
        
        fact_val = getattr(fact, self.field)
        
        # Lógica de Comparação Otimizada
        if self.op == "eq": return fact_val == self.value
        if self.op == "gt": return fact_val > self.value
        if self.op == "gte": return fact_val >= self.value
        if self.op == "lt": return fact_val < self.value
        if self.op == "lte": return fact_val <= self.value
        if self.op == "neq": return fact_val != self.value
        return False

    def propagate(self, fact: Fact, agenda: Agenda):
        """Se passar no teste, manda para os filhos."""
        if self.test(fact):
            for child in self.children:
                if isinstance(child, TerminalNode):
                    child.activate(fact, agenda)
                elif isinstance(child, AlphaNode):
                    child.propagate(fact, agenda)

class TypeNode(ReteNode):
    """
    Indexação por Tipo. O primeiro filtro da rede.
    Separa Pacientes de Exames, etc.
    """
    def __init__(self, model_class: Type[Fact]):
        super().__init__()
        self.model_class = model_class

    def propagate(self, fact: Fact, agenda: Agenda):
        # Só processa se o fato for do tipo correto
        if isinstance(fact, self.model_class):
            for child in self.children:
                if isinstance(child, AlphaNode):
                    child.propagate(fact, agenda)
                elif isinstance(child, TerminalNode):
                    child.activate(fact, agenda)

# =============================================================================
# 4. O MOTOR DE INFERÊNCIA (Ikin Engine)
# =============================================================================

def Rule(*patterns: Pattern, salience: int = 0):
    def decorator(func):
        func._is_rule = True
        func._patterns = patterns
        func._salience = salience
        return func
    return decorator

class KnowledgeEngine:
    def __init__(self):
        self.facts: Set[Fact] = set()
        self.agenda = Agenda()
        
        # A REDE RETE (Raiz)
        # Mapeia TipoDoFato -> TypeNode
        self.rete_root: Dict[Type[Fact], TypeNode] = {}
        
        # Inicializa construindo a rede
        self._build_network()

    def _build_network(self):
        """
        Compila as regras Python em um Grafo Rete.
        Isso roda apenas UMA VEZ na inicialização.
        """
        # 1. Coleta os métodos decorados
        for name, method in inspect.getmembers(self):
            if getattr(method, "_is_rule", False):
                self._compile_rule(method)

    def _compile_rule(self, method):
        """Transforma uma regra em nós na memória."""
        patterns = method._patterns
        salience = method._salience
        
        if not patterns: return

        # Para cada padrão na regra
        for pattern in patterns:
            # 1. Garante que existe um TypeNode para esse tipo de fato (Indexação)
            if pattern.model_class not in self.rete_root:
                self.rete_root[pattern.model_class] = TypeNode(pattern.model_class)
            
            current_node = self.rete_root[pattern.model_class]

            # 2. Cria ou reutiliza nós Alpha para cada restrição
            for field_op, value in pattern.constraints.items():
                if "__" in field_op:
                    field, op = field_op.split("__")
                else:
                    field, op = field_op, "eq"
                
                # OTIMIZAÇÃO: Procura se já existe um nó igual (Node Sharing)
                found_node = None
                for child in current_node.children:
                    if isinstance(child, AlphaNode) and \
                       child.field == field and \
                       child.op == op and \
                       child.value == value:
                        found_node = child
                        break
                
                if found_node:
                    current_node = found_node
                else:
                    new_node = AlphaNode(field, op, value)
                    current_node.add_child(new_node)
                    current_node = new_node
            
            # 3. No final da cadeia, adiciona o TerminalNode (Ação)
            terminal = TerminalNode(method.__name__, method, salience)
            current_node.add_child(terminal)

    def reset(self):
        self.facts.clear()
        self.agenda.clear()

    def declare(self, fact: Fact):
        """
        Insere o fato na rede.
        O fato viaja pelo grafo. Se chegar no final, ativa a regra na Agenda.
        """
        if fact in self.facts:
            return 
        
        self.facts.add(fact)
        
        # Passo 1: Indexação. Vai direto no TypeNode correto.
        fact_type = type(fact)
        if fact_type in self.rete_root:
            self.rete_root[fact_type].propagate(fact, self.agenda)

    def run(self):
        """Executa as regras que estão na Agenda."""
        # print("--- IKIN-EXPERT ENGINE RUNNING ---") # Comentado para limpar output
        steps = 0
        max_steps = 1000 
        
        while steps < max_steps:
            activation = self.agenda.pop()
            
            if not activation:
                break 
            
            # Injeta o fato nos argumentos da função
            try:
                sig = inspect.signature(activation.node.action)
                if len(sig.parameters) > 0:
                    activation.node.action(activation.fact)
                else:
                    activation.node.action()
            except Exception as e:
                print(f" [ERROR] Falha na regra {activation.node.rule_name}: {e}")
            
            steps += 1