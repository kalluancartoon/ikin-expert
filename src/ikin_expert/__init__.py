"""
Ikin-Expert: Engine de Inferência e Sistemas Especialistas baseada em Algoritmo Rete Otimizado.
Implementa Alpha Network, Beta Network e Hash Joins (Indexação) para alta performance.

Copyright (c) 2026 Kalluan Cley Fiuza.
Licensed under MIT OR Apache-2.0.
"""

# =========================================================
# METADADOS DO PACOTE (Versão 2.0.2 - Stable Fix)
# =========================================================
__version__ = "2.0.2"
__author__ = "Kalluan Cley Fiuza"
__email__ = "kalluancartoon@gmail.com"
__license__ = "MIT OR Apache-2.0"

# =========================================================
# EXPORTAÇÃO DE CLASSES (API PÚBLICA)
# =========================================================
from .engine import (
    KnowledgeEngine,
    Rule,
    Fact,
    Pattern,
    Token,
    MATCH,
    AS,
    AND,
    OR,
    NOT
)

__all__ = [
    "KnowledgeEngine",
    "Rule",
    "Fact",
    "Pattern",
    "Token",
    "MATCH",
    "AS",
    "AND",
    "OR",
    "NOT",
]