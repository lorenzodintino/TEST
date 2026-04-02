from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

import streamlit as st
from pydantic import Field


@dataclass
class Result:
    stato: bool = Field(default=True)
    risultato: Optional[Any] = Field(default=None)
    errore: Optional[str] = Field(default=None)
    info: Optional[str] = Field(default=None)
    timestamp: datetime = Field(default_factory=datetime.now)

    @classmethod
    def success(cls, risultato, info=None):
        return cls(stato=True, risultato=risultato, info=info)

    @classmethod
    def failure(cls, errore, info=None):
        return cls(stato=False, errore=errore, info=info)

    def is_success(self) -> bool:
        return self.stato

    def is_failure(self) -> bool:
        return not self.stato