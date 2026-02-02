# Ikin-Expert 🧠 v2.0

**A High-Performance Rete Engine with Hash Joins for Python.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-black?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT%20OR%20Apache--2.0-black?style=for-the-badge)](LICENSE-MIT)
[![Code Style](https://img.shields.io/badge/Code%20Style-Pydantic-e92063?style=for-the-badge)](https://docs.pydantic.dev/)
[![Architecture](https://img.shields.io/badge/Algorithm-Rete%20Network%20(Alpha%2BBeta)-black?style=for-the-badge)](https://en.wikipedia.org/wiki/Rete_algorithm)

> **"A ciência é feita de dados, mas a sabedoria é feita de inferências."**

---

## 🚀 O que há de novo na v2.0?

A versão 2.0 introduz o **Algoritmo Rete Completo** (Alpha + Beta Networks) com otimização de **Hash Joins**.

* **Antes (v0.1):** Apenas filtros simples em fatos isolados.
* **Agora (v2.0):** Capacidade de cruzar dados (JOINS) entre fatos diferentes com performance $O(1)$ (tempo constante), utilizando a nova sintaxe `MATCH`.

Isso permite criar sistemas complexos (como Monitoramento de Saúde ou Detecção de Fraude) que processam milhares de eventos em tempo real sem degradação de performance.

---

## 📋 Sobre o Projeto

O **Ikin-Expert** é uma biblioteca de Sistemas Especialistas projetada para preencher a lacuna deixada por ferramentas legadas no ecossistema Python.

Diferente de antecessores que utilizavam estruturas de dados lentas ou loops aninhados (Produto Cartesiano), o Ikin-Expert implementa **Indexação Automática** nas regras de junção.

### Principais Diferenciais
* **⚡ Hash Joins (O(1)):** Se você cruzar 10.000 Pacientes com 10.000 Exames, o sistema **não** faz 100 milhões de comparações. Ele usa Tabelas Hash para encontrar o par exato instantaneamente.
* **🛡️ Type Safety:** Integração nativa com **Pydantic**. Dados inválidos são rejeitados antes de entrar no motor.
* **🔗 Variáveis de Ligação (`MATCH`):** Sintaxe declarativa e elegante para conectar regras.
* **🧠 Saliência:** Prioridade de execução real para sistemas críticos (Emergência > Rotina).

---

## 🛠 Instalação

```bash
git clone [https://github.com/kalluancartoon/ikin-expert.git](https://github.com/kalluancartoon/ikin-expert.git)
cd ikin-expert
pip install -e .

```

*Requisitos: Python 3.10 ou superior.*

---

## 💻 Exemplo de Uso (v2.0)

Veja como criar um sistema de **Detecção de Fraude** que cruza dados do Cliente com Transações em tempo real:

```python
from ikin_expert import KnowledgeEngine, Rule, Fact, Pattern, MATCH

# 1. Definindo os Dados (Pydantic)
class Cliente(Fact):
    id: int
    nome: str
    status: str  # "VIP" ou "Comum"

class Transacao(Fact):
    cliente_id: int # Foreign Key
    valor: float

# 2. Criando o Especialista
class AntiFraudeIA(KnowledgeEngine):

    # REGRA DE JOIN (Complexa):
    # "Se o Cliente é VIP (Fato 1) E fez transação acima de 5k (Fato 2)..."
    # O uso de MATCH.cid cria um índice Hash automático entre os dois fatos.
    @Rule(
        Pattern(Cliente, id=MATCH.cid, status="VIP"),
        Pattern(Transacao, cliente_id=MATCH.cid, valor__gt=5000.0),
        salience=100
    )
    def alerta_vip(self, c: Cliente, t: Transacao):
        print(f"🚨 ALERTA VIP: {c.nome} tentou gastar R$ {t.valor}!")

    # REGRA SIMPLES:
    @Rule(Pattern(Transacao, valor__gt=10000.0), salience=50)
    def alerta_geral(self, t: Transacao):
        print(f"⚠️ ALERTA GERAL: Transação suspeita de R$ {t.valor}")

# 3. Execução
engine = AntiFraudeIA()
engine.reset()

# O sistema indexa os clientes na memória (Beta Network)
engine.declare(Cliente(id=1, nome="Kalluan", status="VIP"))
engine.declare(Cliente(id=2, nome="Visitante", status="Comum"))

# Ao receber a transação, o sistema encontra o "Kalluan" instantaneamente (O(1))
engine.declare(Transacao(cliente_id=1, valor=6000.0))

engine.run()

```

---

## 🆚 Comparativo de Performance (Join)

Imagine um cenário cruzando **1.000 Clientes** com **1.000 Transações**.

| Tecnologia | Método de Junção | Operações Realizadas | Resultado |
| --- | --- | --- | --- |
| **Legado / Naive** | Loop Aninhado (Nested Loop) | 1.000.000 (1 Milhão) | 🐌 Lento / Trava |
| **Ikin-Expert v2.0** | **Hash Join Indexado** | ~2.000 | 🚀 **Instantâneo** |

---

## ⚖️ Licenciamento Duplo (Dual License)

Este projeto é distribuído sob um modelo de licenciamento duplo para garantir segurança jurídica:

1. **MIT License**
2. **Apache License 2.0** 

---

## 👨🏿‍🔬 Autor e Pesquisador

Desenvolvido por **Kalluan Cley Fiuza**.

* 🔬 **Foco de Pesquisa:** HealthTech, IA Simbólica, Nefrologia Computacional e Sistemas Críticos.
* 🏢 **Mantenedor:** Projeto incubado no ecossistema criativo **Kalluan Cartoon™**.
* 📧 **Email:** kalluancartoon@gmail.com
* 🔗 **LinkedIn:** [Kalluan C. Fiuza](https://www.linkedin.com/in/kalluan-c-fiuza-b5a17b221/)
* 🆔 **ORCID:** [0009-0005-2693-6477](https://orcid.org/0009-0005-2693-6477)
* 📚 **Currículo Lattes:** [Acessar Lattes](https://lattes.cnpq.br/7267245059752858)

---
