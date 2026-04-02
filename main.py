"""
Esempio di utilizzo della struttura Utente e del DatabaseManager.

Questo script mostra:
1. Come creare un'istanza del modello Utente
2. Come inizializzare il database e creare le tabelle
3. Come salvare, leggere, aggiornare ed eliminare utenti dal database
"""

from datetime import date, datetime
from utente import Utente, Sesso, Ruolo, Servizio
from database_manager import DatabaseManager


def main():
    # ============================================
    # 1. CREAZIONE DI UN UTENTE (STRUTTURA DATI)
    # ============================================
    print("=" * 60)
    print("1. CREAZIONE DI UN NUOVO UTENTE")
    print("=" * 60)
    
    # Creiamo un nuovo utente utilizzando il modello
    nuovo_utente = Utente(
        username="mario_rossi",
        email="mario.rossi@example.com",
        password="password_sicura_123",
        nome="Mario",
        cognome="Rossi",
        via="Via Roma",
        civico="10",
        cap="00100",
        citta="Roma",
        provincia="RM",
        nazione="Italia",
        data_nascita=date(1985, 5, 15),
        telefono="+39 333 1234567",
        sesso=Sesso.M,
        ruolo=Ruolo.UTENTE,
        servizio=[Servizio.GACEP],
        primo_accesso=True,
        note="Utente creato per dimostrazione"
    )
    
    print(f"\nUtente creato in memoria:")
    print(f"  UUID: {nuovo_utente.uuid}")
    print(f"  Username: {nuovo_utente.username}")
    print(f"  Email: {nuovo_utente.email}")
    print(f"  Nome: {nuovo_utente.nome} {nuovo_utente.cognome}")
    print(f"  Ruolo: {nuovo_utente.ruolo.value}")
    print(f"  Data registrazione: {nuovo_utente.data_registrazione}")
    
    # ============================================
    # 2. INIZIALIZZAZIONE DEL DATABASE
    # ============================================
    print("\n" + "=" * 60)
    print("2. INIZIALIZZAZIONE DEL DATABASE")
    print("=" * 60)
    
    # Creiamo il DatabaseManager con un database SQLite
    db_manager = DatabaseManager(database_url="sqlite:///test_database.db")
    
    # Creiamo la tabella per il modello Utente
    # (in alternativa si può usare db_manager.crea_tutte_le_tabelle())
    db_manager.crea_tabella(Utente)
    
    # ============================================
    # 3. SALVATAGGIO DELL'UTENTE NEL DATABASE
    # ============================================
    print("\n" + "=" * 60)
    print("3. SALVATAGGIO DELL'UTENTE NEL DATABASE")
    print("=" * 60)
    
    # Salviamo l'utente nel database
    utente_salvato = db_manager.salva(nuovo_utente)
    print(f"\nUtente salvato con UUID: {utente_salvato.uuid}")
    
    # ============================================
    # 4. LETTURA DAL DATABASE
    # ============================================
    print("\n" + "=" * 60)
    print("4. LETTURA DAL DATABASE")
    print("=" * 60)
    
    # Recuperiamo l'utente per UUID
    print("\nRecupero utente per UUID...")
    utente_recuperato = db_manager.ottieni(Utente, utente_salvato.uuid)
    if utente_recuperato:
        print(f"  Trovato: {utente_recuperato.username} - {utente_recuperato.email}")
    
    # Creiamo un secondo utente per dimostrare altre funzionalità
    print("\nCreazione di un secondo utente...")
    secondo_utente = Utente(
        username="luigi_bianchi",
        email="luigi.bianchi@example.com",
        password="altra_password_456",
        nome="Luigi",
        cognome="Bianchi",
        sesso=Sesso.M,
        ruolo=Ruolo.GUEST
    )
    db_manager.salva(secondo_utente)
    
    # Recupero tutti gli utenti
    print("\nRecupero di tutti gli utenti...")
    tutti_utenti = db_manager.ottieni_tutti(Utente)
    print(f"  Totale utenti nel database: {len(tutti_utenti)}")
    for u in tutti_utenti:
        print(f"    - {u.username} ({u.ruolo.value})")
    
    # Ricerca per filtro
    print("\nRicerca utenti per ruolo 'UTENTE'...")
    utenti_utente = db_manager.cerca(Utente, ruolo=Ruolo.UTENTE)
    print(f"  Trovati {len(utenti_utente)} utenti con ruolo UTENTE:")
    for u in utenti_utente:
        print(f"    - {u.username}")
    
    # ============================================
    # 5. AGGIORNAMENTO DI UN UTENTE
    # ============================================
    print("\n" + "=" * 60)
    print("5. AGGIORNAMENTO DI UN UTENTE")
    print("=" * 60)
    
    # Aggiorniamo alcuni campi dell'utente
    print(f"\nAggiornamento utente '{utente_recuperato.username}'...")
    utente_aggiornato = db_manager.aggiorna(
        utente_recuperato,
        {
            "telefono": "+39 333 9999999",
            "citta": "Milano",
            "ruolo": Ruolo.ADMIN
        }
    )
    print(f"  Nuovo telefono: {utente_aggiornato.telefono}")
    print(f"  Nuova città: {utente_aggiornato.citta}")
    print(f"  Nuovo ruolo: {utente_aggiornato.ruolo.value}")
    print(f"  Data ultima modifica: {utente_aggiornato.data_ultima_modifica}")
    
    # ============================================
    # 6. ESECUZIONE QUERY SQL GREZZA
    # ============================================
    print("\n" + "=" * 60)
    print("6. ESECUZIONE QUERY SQL GREZZA")
    print("=" * 60)
    
    # Esempio di query SQL diretta
    print("\nEsecuzione query SQL per contare gli utenti...")
    risultato = db_manager.esegui_query("SELECT COUNT(*) as conteggio FROM utenti")
    print(f"  Numero totale di utenti: {risultato[0]['conteggio']}")
    
    # ============================================
    # 7. ELIMINAZIONE DI UN UTENTE
    # ============================================
    print("\n" + "=" * 60)
    print("7. ELIMINAZIONE DI UN UTENTE")
    print("=" * 60)
    
    # Eliminiamo il secondo utente
    print(f"\nEliminazione utente '{secondo_utente.username}'...")
    db_manager.elimina(secondo_utente)
    
    # Verifichiamo che sia stato eliminato
    utenti_rimasti = db_manager.ottieni_tutti(Utente)
    print(f"  Utenti rimanenti nel database: {len(utenti_rimasti)}")
    
    # ============================================
    # CONCLUSIONE
    # ============================================
    print("\n" + "=" * 60)
    print("DIMOSTRAZIONE COMPLETATA!")
    print("=" * 60)
    print("\nRiassunto delle operazioni eseguite:")
    print("  ✓ Creato un modello Utente con SQLModel")
    print("  ✓ Inizializzato il database SQLite")
    print("  ✓ Creata la tabella 'utenti' automaticamente")
    print("  ✓ Salvato un utente nel database")
    print("  ✓ Letto utenti dal database (singolo, tutti, con filtri)")
    print("  ✓ Aggiornato i dati di un utente")
    print("  ✓ Eseguita una query SQL grezza")
    print("  ✓ Eliminato un utente dal database")
    
    # Chiudiamo la connessione al database
    db_manager.chiudi()


if __name__ == "__main__":
    main()
