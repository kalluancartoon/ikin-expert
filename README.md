# Ikin-Expert 🧠 v2.0.3

**A High-Performance Rete Engine with Hash Joins for Python.**

[![PyPI version](https://img.shields.io/pypi/v/ikin-expert?color=blue&style=for-the-badge&logo=pypi&logoColor=white)](https://pypi.org/project/ikin-expert/)
[![Python](https://img.shields.io/badge/Python-3.10%2B-black?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT%20OR%20Apache--2.0-black?style=for-the-badge)](LICENSE-MIT)
[![INPI](https://img.shields.io/badge/INPI-Registrado-green?style=for-the-badge)](https://www.gov.br/inpi/pt-br)

> **"A ciência é feita de dados, mas a sabedoria é feita de inferências."**

---

## 🚀 O que há de novo na v2.0.3?

Esta versão eleva o motor, focando em estabilidade e integração profunda:

✅ Ponte Alfa-Beta (Hash-Join Layer): Correção crítica na propagação de fatos entre nós Alfa (filtros) e Beta (junções). Agora, a intersecção de múltiplos fatos é garantida via indexação por Hash.

✅ Resiliência de Memória: Validada em testes de estresse de 20 horas+ com ocupação de 100% de CPU e consumo estável de RAM (~4.5%), sem memory leaks.

✅ Dicionário de Operadores Estável: Padronização da sintaxe de comparação (ex: __gte, __contains, __eq) para garantir a manutenibilidade do código.
---

## 📋 Sobre o Projeto

O **Ikin-Expert** é uma biblioteca de Sistemas Especialistas esenvolvido pela Kalluan Cartoon para substituir motores legados, unindo IA Simbólica à robustez do **Pydantic v2.**

Diferente de antecessores que utilizavam estruturas de dados lentas, o Ikin-Expert implementa **Indexação Automática** e tipagem forte com Pydantic.

### Principais Diferenciais
* **⚡Complexidade Amortizada (O(1)):** Se você cruzar 10.000 Pacientes com 10.000 Exames, o sistema usa índices hash para encontrar pares instantaneamente, evitando o produto cartesiano lento.
* **🛡️ Engenharia de Dados:** Integração nativa com **Pydantic**.
* **🏗️ Arquitetura Rete Otimizada:** Separação clara entre Memória de Trabalho e Base de Conhecimento para maior previsibilidade temporal.

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
from ikin_expert import KnowledgeEngine, Rule, Fact, MATCH
from pydantic import Field

# 1. Definindo os Modelos de Dados (Fatos)
class Termostato(Fact):
    local: str
    temperatura: float = Field(gt=-50, lt=100)

class Presenca(Fact):
    local: str
    detectada: bool

# 2. Motor de Inferência (Gestão de Climatização)
class ClimaManager(KnowledgeEngine):

    # REGRA: Ativar Ar-Condicionado
    # SE houver presença no local (MATCH.loc) E a temperatura for > 25...
    @Rule(
        Presenca(local=MATCH.loc, detectada=True),
        Termostato(local=MATCH.loc, temperatura__gt=25.0)
    )
    def ligar_refrigeracao(self, loc):
        print(f"❄️ AÇÃO: Climatizando a {loc}. Conforto térmico ativado.")

# 3. Execução
sistema = ClimaManager()
sistema.reset() # Governança: Limpeza da Working Memory

# Simulando dados de sensores
sistema.declare(Presenca(local="sala", detectada=True))
sistema.declare(Termostato(local="sala", temperatura=28.5))

sistema.run()

```

---

## 🆚 Comparativo de Performance

|Métrica|Métodos Legados (Naive)|Ikin-Expert v2.0.3
|Complexidade de Junção|O(Nĸ) (Exponencial)|O(1) Amortizado
|Uso de Memória (Estresse)|Inconsistente / Leaks|Estável (~4.5% RAM)
|Variabilidade Temporal|Alta / Imprevisível|Baixa / Determinística
---

## ⚖️ Propriedade Intelectual

* **Registro de Software (INPI):** BR 51 2026 000822-0
* **Licença:** Dual License (MIT + Apache 2.0)

---

## 👨🏿‍🔬 Autor e Pesquisador

Desenvolvido por **Kalluan Cley Fiuza**.

* 🔬 **Foco de Pesquisa:** HealthTech, IA Simbólica, Sistemas Especialistas.
* 🏢 **Mantenedor:** Projeto incubado no ecossistema **Kalluan Cartoon™**.
* 📧 **Email:** contato@kalluancartoon.com.br
* 🔗 **LinkedIn:** [Kalluan C. Fiuza](https://www.linkedin.com/in/kalluan-c-fiuza-b5a17b221/)
* 🆔 **ORCID:** [0009-0005-2693-6477](https://orcid.org/0009-0005-2693-6477)
* 📚 **Currículo Lattes:** [Acessar Lattes](https://lattes.cnpq.br/7267245059752858)

---

```

```