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