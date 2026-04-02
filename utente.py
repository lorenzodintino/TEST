from enum import Enum
from sqlmodel import SQLModel, Field
from typing import Optional, List
import uuid
from datetime import date, datetime
from sqlalchemy import JSON, Column


class Sesso(str, Enum):
    M = 'Maschio'
    F = 'Femmina'
    X = 'Non specificato'


class Ruolo(str, Enum):
    SUPERADMIN = 'SUPERADMIN'
    ADMIN = 'ADMIN'
    UTENTE = 'UTENTE'
    GUEST = 'GUEST'


class Servizio(str, Enum):
    GACEP = 'GACEP'


class Utente(SQLModel, table=True):
    """
    Modello Utente che definisce sia la struttura dati (Pydantic) 
    che la tabella del database (SQLAlchemy/SQLModel).
    
    Il parametro table=True indica a SQLModel di creare una tabella
    nel database con questo schema.
    """
    __tablename__ = "utenti"
    
    uuid: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True, max_length=100)
    username: str = Field(..., min_length=3, max_length=30, index=True)
    codice_fiscale: Optional[str] = Field(default=None, min_length=16, max_length=16)
    email: str = Field(..., max_length=100, index=True)
    password: str = Field(...)
    nome: Optional[str] = Field(default=None)
    cognome: Optional[str] = Field(default=None)
    via: Optional[str] = Field(default=None)
    civico: Optional[str] = Field(default=None)
    cap: Optional[str] = Field(default=None)
    citta: Optional[str] = Field(default=None)
    provincia: Optional[str] = Field(default=None)
    nazione: Optional[str] = Field(default=None)
    data_nascita: Optional[date] = Field(default=None)
    telefono: Optional[str] = Field(default=None, max_length=100)
    sesso: Sesso = Field(default=Sesso.X)
    ruolo: Ruolo = Field(default=Ruolo.GUEST)
    data_registrazione: datetime = Field(default_factory=datetime.now)
    ultimo_accesso: Optional[datetime] = Field(default=None)
    data_ultima_modifica: Optional[datetime] = Field(default=None)
    stato_attivo: bool = Field(default=True)
    servizio: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    primo_accesso: bool = Field(default=True)
    note: Optional[str] = Field(default=None)
