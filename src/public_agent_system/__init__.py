"""Local validation utilities for the public human-gated agent system."""

from .core import ValidationResult, new_envelope, validate_envelope
from .registry import AGENTS, AGENTS_BY_ID

__all__ = [
    "AGENTS",
    "AGENTS_BY_ID",
    "ValidationResult",
    "new_envelope",
    "validate_envelope",
]

__version__ = "1.0.0"

