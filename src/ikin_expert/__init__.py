"""
Ikin-Expert: Engine de Inferência e Sistemas Especialistas baseada em Algoritmo Rete Otimizado.
Implementa Alpha Network, Beta Network e Hash Joins (Indexação) para alta performance.

Copyright (c) 2026 Kalluan Cley Fiuza.
Licensed under MIT OR Apache-2.0.
"""

# Metadados do Projeto
__version__ = "2.0.0"
__author__ = "Kalluan Cley Fiuza"
__email__ = "kalluancartoon@gmail.com"
__license__ = "MIT OR Apache-2.0"

# Importando os componentes principais da Engine
# Isso permite que o usuário faça: "from ikin_expert import KnowledgeEngine, MATCH"
from .engine import (
    KnowledgeEngine,
    Rule,
    Fact,
    Pattern,
    Token,
    MATCH  # <--- Essencial para a v2.0 (Hash Joins)
)

# Define o que será exportado publicamente quando alguém usar "from ikin_expert import *"
__all__ = [
    "KnowledgeEngine",
    "Rule",
    "Fact",
    "Pattern",
    "Token",
    "MATCH",
]