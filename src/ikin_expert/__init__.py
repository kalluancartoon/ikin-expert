"""
Ikin-Expert: Engine de Inferência e Sistemas Especialistas baseada em Algoritmo Rete.
Desenvolvido para alta performance e rigor científico.

Copyright (c) 2026 Kalluan Cley Fiuza.
Licensed under MIT OR Apache-2.0.
"""

# Metadados do Projeto (Acessíveis via código)
__version__ = "0.1.0"
__author__ = "Kalluan Cley Fiuza"
__email__ = "kalluancartoon@gmail.com"
__license__ = "MIT OR Apache-2.0"

# Importando o Motor Rete e Componentes Principais
# Isso permite que o usuário faça: "from ikin_expert import KnowledgeEngine"
from .engine import (
    KnowledgeEngine,
    Rule,
    Fact,
    Pattern,
    Token
)

# Define o que será exportado quando alguém usar "from ikin_expert import *"
__all__ = [
    "KnowledgeEngine",
    "Rule",
    "Fact",
    "Pattern",
    "Token",
]