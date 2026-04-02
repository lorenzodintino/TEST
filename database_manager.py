from sqlmodel import SQLModel, create_engine, Session, select
from typing import Type, List, Optional, Any, Dict
from datetime import datetime


class DatabaseManager:
    """
    Classe per la gestione del database.
    Si occupa di creare il connection pool, creare tabelle, 
    eseguire query CRUD e gestire le sessioni.
    """
    
    def __init__(self, database_url: str = "sqlite:///database.db"):
        """
        Inizializza il DatabaseManager con l'URL del database.
        
        Args:
            database_url: URL di connessione al database (es. sqlite:///database.db)
        """
        self.database_url = database_url
        self.engine = create_engine(
            database_url,
            echo=False,  # Imposta a True per vedere le query SQL eseguite
            connect_args={"check_same_thread": False} if "sqlite" in database_url else {}
        )
    
    def crea_tutte_le_tabelle(self):
        """
        Crea tutte le tabelle nel database basandosi sui modelli SQLModel registrati.
        Da chiamare una volta all'avvio dell'applicazione.
        """
        SQLModel.metadata.create_all(self.engine)
        print(f"Tabelle create con successo nel database: {self.database_url}")
    
    def crea_tabella(self, modello: Type[SQLModel]):
        """
        Crea una singola tabella nel database per il modello specificato.
        
        Args:
            modello: La classe del modello SQLModel (es. Utente)
        """
        modello.metadata.create_all(self.engine)
        print(f"Tabella '{modello.__tablename__}' creata con successo")
    
    def get_session(self) -> Session:
        """
        Restituisce una nuova sessione del database.
        Va usata con un context manager o chiusa manualmente.
        
        Returns:
            Una sessione SQLModel
        """
        return Session(self.engine)
    
    def salva(self, oggetto: SQLModel) -> SQLModel:
        """
        Salva un oggetto nel database (insert o update).
        
        Args:
            oggetto: L'istanza del modello da salvare
            
        Returns:
            L'oggetto salvato con gli eventuali campi aggiornati dal DB
        """
        with self.get_session() as session:
            session.add(oggetto)
            session.commit()
            session.refresh(oggetto)
            print(f"Oggetto salvato: {oggetto}")
            return oggetto
    
    def ottieni(self, modello: Type[SQLModel], id_valore: Any) -> Optional[SQLModel]:
        """
        Recupera un oggetto dal database per ID (primary key).
        
        Args:
            modello: La classe del modello
            id_valore: Il valore della primary key
            
        Returns:
            L'oggetto trovato o None se non esiste
        """
        with self.get_session() as session:
            risultato = session.get(modello, id_valore)
            return risultato
    
    def ottieni_tutti(self, modello: Type[SQLModel]) -> List[SQLModel]:
        """
        Recupera tutti gli oggetti di un certo tipo dal database.
        
        Args:
            modello: La classe del modello
            
        Returns:
            Lista di oggetti trovati
        """
        with self.get_session() as session:
            risultati = session.exec(select(modello)).all()
            return list(risultati)
    
    def cerca(self, modello: Type[SQLModel], **filtri) -> List[SQLModel]:
        """
        Cerca oggetti nel database con filtri dinamici.
        
        Args:
            modello: La classe del modello
            **filtri: Parametri nome=valore per filtrare la ricerca
            
        Returns:
            Lista di oggetti che corrispondono ai filtri
        """
        with self.get_session() as session:
            query = select(modello)
            for campo, valore in filtri.items():
                query = query.where(getattr(modello, campo) == valore)
            risultati = session.exec(query).all()
            return list(risultati)
    
    def aggiorna(self, oggetto: SQLModel, dati_da_aggiornare: Dict[str, Any]) -> SQLModel:
        """
        Aggiorna i campi di un oggetto esistente.
        
        Args:
            oggetto: L'oggetto da aggiornare (deve essere già recuperato dal DB)
            dati_da_aggiornare: Dizionario con i campi da aggiornare
            
        Returns:
            L'oggetto aggiornato
        """
        with self.get_session() as session:
            for campo, valore in dati_da_aggiornare.items():
                setattr(oggetto, campo, valore)
            oggetto.data_ultima_modifica = datetime.now()
            session.add(oggetto)
            session.commit()
            session.refresh(oggetto)
            print(f"Oggetto aggiornato: {oggetto}")
            return oggetto
    
    def elimina(self, oggetto: SQLModel) -> bool:
        """
        Elimina un oggetto dal database.
        
        Args:
            oggetto: L'oggetto da eliminare
            
        Returns:
            True se l'eliminazione è andata a buon fine
        """
        with self.get_session() as session:
            session.delete(oggetto)
            session.commit()
            print(f"Oggetto eliminato: {oggetto}")
            return True
    
    def esegui_query(self, query: str, parametri: Optional[Dict] = None) -> List[Dict]:
        """
        Esegue una query SQL grezza (utile per operazioni avanzate).
        
        Args:
            query: La query SQL da eseguire
            parametri: Eventuali parametri per la query
            
        Returns:
            Lista di dizionari con i risultati
        """
        from sqlalchemy import text
        
        with self.engine.connect() as connection:
            if parametri:
                risultato = connection.execute(text(query), parametri)
            else:
                risultato = connection.execute(text(query))
            
            if risultato.returns_rows:
                colonne = risultato.keys()
                return [dict(zip(colonne, riga)) for riga in risultato.fetchall()]
            connection.commit()
            return []
    
    def chiudi(self):
        """
        Chiude il connection pool del database.
        Da chiamare alla chiusura dell'applicazione.
        """
        self.engine.dispose()
        print("Connessione al database chiusa")
