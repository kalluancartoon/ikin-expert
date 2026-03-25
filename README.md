````md
# Ikin-Expert 🧠 v2.0.3

**A High-Performance Rete Engine with Hash Joins for Python**

[![PyPI version](https://img.shields.io/pypi/v/ikin-expert?color=blue&style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/ikin-expert/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-black?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT%20OR%20Apache--2.0-black?style=for-the-badge)](LICENSE-MIT)
[![INPI](https://img.shields.io/badge/INPI-Registrado-green?style=for-the-badge)](https://www.gov.br/inpi/pt-br)

> **"A ciência é feita de dados, mas a sabedoria é feita de inferências."**

---

## 🚀 O que há de novo na v2.0.3?

Esta versão eleva o motor com foco em estabilidade, integração e previsibilidade operacional:

- ✅ **Ponte Alfa-Beta (Hash-Join Layer):** correção crítica na propagação de fatos entre nós Alfa (filtros) e Beta (junções). Agora, a interseção entre múltiplos fatos é realizada por meio de indexação por hash.
- ✅ **Resiliência de Memória:** validada em testes de estresse com mais de 20 horas de execução, ocupação de 100% de CPU e consumo estável de RAM (~4.5%), sem indícios de *memory leaks*.
- ✅ **Dicionário de Operadores Estável:** padronização da sintaxe de comparação (`__gte`, `__contains`, `__eq`, entre outros), favorecendo legibilidade, manutenção e consistência interna.

---

## 📋 Sobre o Projeto

O **Ikin-Expert** é uma biblioteca de sistemas especialistas desenvolvida pela **Kalluan Cartoon** para substituir motores legados, unindo **IA simbólica** à robustez do **Pydantic v2**.

Diferentemente de abordagens anteriores baseadas em estruturas menos eficientes, o Ikin-Expert implementa **indexação automática**, **tipagem forte** e uma arquitetura orientada à previsibilidade de execução.

### Principais Diferenciais

- **⚡ Junções otimizadas com Hash Indexing:** reduz o custo de cruzamento entre fatos em cenários comuns, evitando o produto cartesiano ingênuo.
- **🛡️ Engenharia de Dados:** integração nativa com **Pydantic**, promovendo validação forte e maior confiabilidade na modelagem dos fatos.
- **🏗️ Arquitetura Rete otimizada:** separação clara entre **Working Memory** e **Knowledge Base**, favorecendo organização, escalabilidade e previsibilidade temporal.
- **🔎 Regras mais expressivas:** suporte a operadores declarativos para construção de condições mais legíveis e fáceis de manter.

---

## 🛠 Instalação

Disponível oficialmente no **PyPI**:

```bash
pip install ikin-expert
````

**Requisitos:** Python 3.10 ou superior.

---

## 💻 Exemplo de Uso: Automação Residencial (IoT)

Veja como criar um "cérebro" para uma casa inteligente que toma decisões com base em sensores:

```python
from ikin_expert import KnowledgeEngine, Rule, Fact, MATCH
from pydantic import Field

# 1. Definição dos modelos de dados (fatos)
class Termostato(Fact):
    local: str
    temperatura: float = Field(gt=-50, lt=100)

class Presenca(Fact):
    local: str
    detectada: bool

# 2. Motor de inferência (gestão de climatização)
class ClimaManager(KnowledgeEngine):

    # REGRA:
    # Se houver presença no local (MATCH.loc)
    # e a temperatura for maior que 25 °C,
    # então o sistema ativa a refrigeração.
    @Rule(
        Presenca(local=MATCH.loc, detectada=True),
        Termostato(local=MATCH.loc, temperatura__gt=25.0)
    )
    def ligar_refrigeracao(self, loc):
        print(f"❄️ AÇÃO: Climatizando {loc}. Conforto térmico ativado.")

# 3. Execução
sistema = ClimaManager()
sistema.reset()  # Limpeza da Working Memory

# Simulação de dados de sensores
sistema.declare(Presenca(local="sala", detectada=True))
sistema.declare(Termostato(local="sala", temperatura=28.5))

sistema.run()
```

---

## 🆚 Comparativo de Performance

| Métrica                    | Métodos legados (naive)                       | Ikin-Expert v2.0.3                     |
| -------------------------- | --------------------------------------------- | -------------------------------------- |
| Estratégia de junção       | Produto cartesiano / varredura ingênua        | Indexação por hash                     |
| Escalabilidade             | Limitada em cenários com alto volume de fatos | Otimizada para cenários mais complexos |
| Uso de memória em estresse | Inconsistente / sujeito a vazamentos          | Estável (~4.5% de RAM)                 |
| Variabilidade temporal     | Alta / imprevisível                           | Baixa / mais previsível                |

> **Nota:** o ganho de desempenho depende do volume de fatos, do número de regras e do padrão de junção empregado no problema.

---

## ⚖️ Propriedade Intelectual

* **Registro de Software (INPI):** BR 51 2026 000822-0
* **Licença:** Dual License (**MIT** + **Apache 2.0**)

---

## 👨🏿‍🔬 Autor e Pesquisador

Desenvolvido por **Kalluan Cley Fiuza**.

* 🔬 **Foco de pesquisa:** HealthTech, IA simbólica e sistemas especialistas
* 🏢 **Mantenedor:** projeto incubado no ecossistema **Kalluan Cartoon™**
* 📧 **Email:** [contato@kalluancartoon.com.br](mailto:contato@kalluancartoon.com.br)
* 🔗 **LinkedIn:** [Kalluan C. Fiuza](https://www.linkedin.com/in/kalluan-c-fiuza-b5a17b221/)
* 🆔 **ORCID:** [0009-0005-2693-6477](https://orcid.org/0009-0005-2693-6477)
* 📚 **Currículo Lattes:** [Acessar Lattes](https://lattes.cnpq.br/7267245059752858)

---

## 📌 Observações

O Ikin-Expert foi projetado para aplicações que exigem **inferência simbólica**, **rastreabilidade lógica** e **controle explícito sobre regras de decisão**, sendo especialmente promissor em domínios como:

* sistemas especialistas médicos;
* automação inteligente;
* motores de decisão baseados em regras;
* validação e classificação simbólica de conhecimento.

---