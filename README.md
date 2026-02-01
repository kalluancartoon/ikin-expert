# Ikin-Expert 🧠

**A Modern, High-Performance Inference Engine for Python.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT%20OR%20Apache--2.0-green?style=for-the-badge)](LICENSE-MIT)
[![Code Style](https://img.shields.io/badge/Code%20Style-Pydantic-e92063?style=for-the-badge)](https://docs.pydantic.dev/)
[![Architecture](https://img.shields.io/badge/Algorithm-Rete%20Network-orange?style=for-the-badge)](https://en.wikipedia.org/wiki/Rete_algorithm)

> **"Democratizando a IA Simbólica com rigor científico e performance de escala."**

## 📋 Sobre o Projeto (About)

O **Ikin-Expert** é uma biblioteca de Sistemas Especialistas (Expert Systems) projetada para preencher a lacuna deixada por ferramentas legadas no ecossistema Python.

Diferente de antecessores que utilizavam estruturas de dados lentas e não tipadas, o Ikin-Expert foi reconstruído do zero sobre três pilares modernos:

1.  **Algoritmo Rete (Alpha Network):** Para processamento de regras em grafos, garantindo performance constante independentemente do volume de dados.
2.  **Pydantic V2:** Para validação de dados rigorosa (*Type Safety*) e performance em nível de sistema (Rust-core).
3.  **Alta Disponibilidade:** Arquitetura *stateless* e indexada, pronta para ambientes críticos como Saúde Pública (SUS) e Indústria 4.0.

Este projeto foi desenvolvido como parte de uma pesquisa em **HealthTech (NephroIA)** para diagnósticos de alta precisão.

---

## 🚀 Principais Diferenciais (Key Features)

* **⚡ Performance Algorítmica (Rete):** Utiliza grafos e compartilhamento de nós (*Node Sharing*) na memória. Se 1.000 regras verificam se a `idade > 60`, o teste é feito apenas uma vez.
* **🛡️ Type Safety & Validação:** Integração nativa com **Pydantic**. Dados inválidos são rejeitados antes de entrar no motor de inferência, garantindo a integridade do diagnóstico (*"Garbage In, Garbage Out"* mitigado).
* **🎯 Resolução de Conflitos (Saliência):** Suporte total a prioridade de execução via parâmetro `salience`. Regras de emergência sempre furam a fila de execução.
* **🔍 Indexação de Fatos:** O motor utiliza *Hashmaps* para indexar fatos por tipo. Regras de "Cardiologia" não perdem tempo processando dados de "Ortopedia" (Complexidade O(1)).
* **🐍 Pythonic Syntax:** Sintaxe limpa e moderna, inspirada no clássico CLIPS/Experta, mas adaptada para o Python 3.10+ (Decorators, Type Hints).

---

## 🛠 Instalação

Como o projeto está em fase Alpha (desenvolvimento ativo), instale diretamente do código fonte:

```bash
git clone [https://github.com/kalluan/ikin-expert.git](https://github.com/kalluan/ikin-expert.git)
cd ikin-expert
pip install -e .

```

*Requisitos: Python 3.10 ou superior.*

---

## 💻 Exemplo de Uso (Quick Start)

Veja como é simples criar um sistema de triagem médica com prioridades reais:

```python
from ikin_expert import KnowledgeEngine, Rule, Fact, Pattern

# 1. Definindo a Estrutura de Dados (Pydantic)
# O sistema garante que 'batimentos' seja sempre um número inteiro.
class Paciente(Fact):
    nome: str
    batimentos: int
    pressao: float

# 2. Criando o Especialista (Engine)
class TriagemHospitalar(KnowledgeEngine):

    # Regra de Emergência (Alta Prioridade: Salience 100)
    # Roda PRIMEIRO se ativada.
    @Rule(Pattern(Paciente, batimentos__gt=120), salience=100)
    def codigo_vermelho(self, p: Paciente):
        print(f"🚨 [URGENTE] Paciente {p.nome} com Taquicardia ({p.batimentos} bpm)!")

    # Regra de Rotina (Baixa Prioridade: Salience 10)
    @Rule(Pattern(Paciente, batimentos__lte=120), salience=10)
    def triagem_normal(self, p: Paciente):
        print(f"✅ [NORMAL] Paciente {p.nome} aguardando atendimento.")

# 3. Executando
engine = TriagemHospitalar()
engine.reset()

# O dado entra, o Algoritmo Rete processa e a Agenda ordena a execução.
engine.declare(Paciente(nome="João Silva", batimentos=145, pressao=14.8))
engine.run()

```

---

## 🆚 Comparativo: Ikin-Expert vs. Bibliotecas Legadas

| Recurso | 🐢 Bibliotecas Antigas (2019) | 🚀 Ikin-Expert (2026) |
| --- | --- | --- |
| **Algoritmo** | Busca Linear (Lento com muitas regras) | **Rete Network** (Grafo Otimizado) |
| **Validação** | Fraca (`dict` python puro) | **Forte** (Pydantic / Rust Core) |
| **Tipagem** | Dinâmica (Propenso a erros) | **Estática** (Type Hints + Autocomplete) |
| **Indexação** | Inexistente (Varre toda a memória) | **Hashmap** (Acesso O(1) por tipo) |
| **Licença** | MIT Simples | **Dual License** (Proteção de Patente) |

---

## ⚖️ Licenciamento Duplo (Dual License)

Este projeto é distribuído sob um modelo de licenciamento duplo para garantir máxima liberdade e segurança jurídica para adoção governamental e corporativa:

1. **MIT License** 
2. **Apache License 2.0** 

Veja os arquivos `LICENSE-MIT` e `LICENSE-APACHE` para detalhes completos.

---

## 👨‍🔬 Autor e Pesquisador

Desenvolvido por **Kalluan Cley Fiuza**.

* 🔬 **Foco de Pesquisa:** HealthTech, IA Simbólica, Nefrologia Computacional e Sistemas Críticos para o SUS.
* 🏢 **Mantenedor:** Projeto incubado no ecossistema criativo **Kalluan Cartoon™**.
* 📧 **Email:** kalluancartoon@gmail.com
* 🔗 **LinkedIn:** [Kalluan C. Fiuza](https://www.linkedin.com/in/kalluan-c-fiuza-b5a17b221/)
* 🆔 **ORCID:** [0009-0005-2693-6477](https://orcid.org/0009-0005-2693-6477)
* 📚 **Currículo Lattes:** [Acessar Lattes](https://lattes.cnpq.br/7267245059752858)
---

*"A ciência é feita de dados, mas a sabedoria é feita de inferências."*

```

```
