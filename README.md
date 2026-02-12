# Ikin-Expert 🧠 v2.0.2

**A High-Performance Rete Engine with Hash Joins for Python.**

[![PyPI version](https://img.shields.io/pypi/v/ikin-expert?color=blue&style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/ikin-expert/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-black?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT%20OR%20Apache--2.0-black?style=for-the-badge)](LICENSE-MIT)
[![INPI](https://img.shields.io/badge/INPI-Registrado-green?style=for-the-badge)](https://www.gov.br/inpi/pt-br)

> **"A ciência é feita de dados, mas a sabedoria é feita de inferências."**

---

## 🚀 O que há de novo na v2.0.2?

Esta versão consolida o motor para uso em **Sistemas Críticos (HealthTech)**:

* **✅ Correção de Memória:** O método `.reset()` agora garante a limpeza total da `WorkingMemory`, permitindo o processamento seguro de múltiplos pacientes/casos em sequência.
* **✅ Novos Operadores Lógicos:** Suporte nativo para `AND`, `OR`, `NOT` e `AS` (Alias) para regras complexas.
* **✅ Hash Joins O(1):** Cruzamento de dados instantâneo entre fatos diferentes utilizando tabelas hash indexadas.

---

## 📋 Sobre o Projeto

O **Ikin-Expert** é uma biblioteca de Sistemas Especialistas projetada para substituir ferramentas legadas no ecossistema Python moderno (3.10+).

Diferente de antecessores que utilizavam estruturas de dados lentas, o Ikin-Expert implementa **Indexação Automática** e tipagem forte com Pydantic.

### Principais Diferenciais
* **⚡ Hash Joins (O(1)):** Se você cruzar 10.000 Pacientes com 10.000 Exames, o sistema usa índices hash para encontrar pares instantaneamente, evitando o produto cartesiano lento.
* **🛡️ Type Safety:** Integração nativa com **Pydantic**.
* **🔗 Sintaxe Poderosa:** Use `MATCH` para ligar variáveis e `AND`/`OR` para lógica condicional aninhada.
* **🏥 Medical-Grade:** Projetado para suportar o projeto **NephroIA** (Diagnóstico Renal), garantindo estabilidade e precisão.

---

## 🛠 Instalação

Agora disponível oficialmente no PyPI:

```bash
pip install ikin-expert

```

*Requisitos: Python 3.10 ou superior.*

---

## 💻 Exemplo de Uso: Automação Residencial (IoT)

Veja como criar um "cérebro" para uma casa inteligente que toma decisões baseadas em sensores:

```python
from ikin_expert import KnowledgeEngine, Rule, Fact, MATCH, OR

# 1. Definindo os Sensores (Fatos)
class Sensor(Fact):
    tipo: str     # "movimento", "temperatura", "fumaca"
    local: str    # "sala", "cozinha", "quarto"
    ativo: bool

class Ambiente(Fact):
    periodo: str  # "dia", "noite"

# 2. Criando o Cérebro da Casa
class HomeAssistant(KnowledgeEngine):

    # REGRA: Iluminação Inteligente
    # SE detectar movimento em um local (MATCH.loc) E for noite...
    # ... ENTÃO acenda a luz DAQUELE local específico.
    @Rule(
        Sensor(tipo="movimento", local=MATCH.loc, ativo=True),
        Ambiente(periodo="noite")
    )
    def acender_luzes(self, loc):
        print(f"💡 AÇÃO: Movimento detectado! Acendendo luzes da {loc}.")

    # REGRA: Segurança Crítica (Incêndio)
    # SE detectar fumaça OU temperatura muito alta (> 60 graus)...
    # ... ENTÃO dispare o alarme geral.
    @Rule(
        OR(
            Sensor(tipo="fumaca", ativo=True),
            Sensor(tipo="temperatura", valor__gt=60.0)
        ),
        salience=100  # Prioridade máxima! Executa antes de tudo.
    )
    def alarme_incendio(self):
        print("🔥 EMERGÊNCIA: Risco de Incêndio! Ativando sprinklers e sirene.")

# 3. Execução
jarvis = HomeAssistant()
jarvis.reset()

# Cenário: É noite, houve movimento na sala e a cozinha está pegando fogo
jarvis.declare(Ambiente(periodo="noite"))
jarvis.declare(Sensor(tipo="movimento", local="sala", ativo=True))
jarvis.declare(Sensor(tipo="temperatura", local="cozinha", valor=85.0))

jarvis.run()

```

---

## 🆚 Comparativo de Performance

| Tecnologia | Método de Junção | Resultado (1k x 1k dados) |
| --- | --- | --- |
| **Legado / Naive** | Loop Aninhado | 🐌 Lento / Trava CPU |
| **Ikin-Expert v2.0** | **Hash Join Indexado** | 🚀 **Instantâneo** |

---

## ⚖️ Propriedade Intelectual

* **Registro de Software (INPI):** BR 51 2026 000822-0
* **Licença:** Dual License (MIT + Apache 2.0)

---

## 👨🏿‍🔬 Autor e Pesquisador

Desenvolvido por **Kalluan Cley Fiuza**.

* 🔬 **Foco de Pesquisa:** HealthTech, IA Simbólica, Nefrologia Computacional.
* 🏢 **Mantenedor:** Projeto incubado no ecossistema **Kalluan Cartoon™**.
* 📧 **Email:** kalluancartoon@gmail.com
* 🔗 **LinkedIn:** [Kalluan C. Fiuza](https://www.linkedin.com/in/kalluan-c-fiuza-b5a17b221/)
* 🆔 **ORCID:** [0009-0005-2693-6477](https://orcid.org/0009-0005-2693-6477)
* 📚 **Currículo Lattes:** [Acessar Lattes](https://lattes.cnpq.br/7267245059752858)

---

```

```