"""
Modulo per la gestione della struttura gerarchica dei documenti nel sistema.

DB_Tree rappresenta una struttura ad albero per organizzare i documenti
basata su categorie, utenze, anni, tipi di documenti e documenti specifici.
Questa classe viene utilizzata per mantenere una rappresentazione in memoria
dei dati esistenti nel file system o nel database.

Autore: Valerio
Data: 2025-03-11
"""


class DB_Tree:
    """
    Struttura dati che rappresenta la gerarchia dei documenti nel sistema.

    La struttura segue un'organizzazione basata su cinque livelli:
    - category (Categoria)
    - utility (Utenza)
    - year (Anno)
    - document_type (Tipo di documento)
    - document (Documento)

    Oltre ai livelli di struttura, tiene traccia anche dei percorsi completi (`paths`).

    Attributes:
        category (set): Insieme di tutte le categorie presenti.
        utility (set): Insieme delle utenze registrate.
        year (set): Insieme degli anni trovati nei documenti.
        document_type (set): Insieme dei tipi di documento.
        document (set): Insieme dei documenti registrati.
        paths (set): Insieme dei percorsi completi generati a partire dai livelli.
    """

    structure = ['category', 'utility', 'year', 'document_type', 'document']

    def __init__(self):
        """Inizializza un oggetto DB_Tree vuoto con insiemi per ogni livello gerarchico."""
        self.category = set()
        self.utility = set()
        self.year = set()
        self.document_type = set()
        self.document = set()
        self.paths = set()

    def __str__(self):
        """Restituisce una rappresentazione in stringa della struttura dati."""
        return (
            f'categories: {self.category}\n'
            f'utilities: {self.utility}\n'
            f'years: {self.year}\n'
            f'document_types: {self.document_type}\n'
            f'documents: {self.document}\n'
            f'paths: {self.paths}'
        )

    def __repr__(self):
        """Restituisce la rappresentazione testuale dell'oggetto."""
        return self.__str__()

    def __getitem__(self, key):
        """
        Permette di accedere direttamente agli insiemi interni tramite chiavi.

        Args:
            key (str): Nome dell'attributo richiesto.

        Returns:
            set: L'insieme corrispondente alla chiave.
        """
        return getattr(self, key)

    def dict(self):
        """
        Restituisce un dizionario che rappresenta la struttura corrente del DB_Tree.

        Returns:
            dict: Dizionario contenente gli insiemi organizzati per livello gerarchico.
        """
        return {k: getattr(self, k) for k in self.structure}

    def __sub__(self, other):
        """
        Esegue la differenza tra due strutture DB_Tree.

        La differenza è calcolata su tutti gli insiemi interni (categorie, utenze, anni, ecc.),
        permettendo di individuare elementi presenti in un albero e assenti nell'altro.

        Args:
            other (DB_Tree): L'oggetto DB_Tree con cui confrontare.

        Returns:
            dict: Dizionario con la differenza tra gli insiemi di `self` e `other`.
        """
        keys = [
            k for k, v in vars(self).items()
            if isinstance(v, set)
        ]  # Considera solo gli insiemi dell'oggetto
        return {k: getattr(self, k) - getattr(other, k) for k in keys}

    def add(self, key: str, value: str):
        """
        Aggiunge un elemento a uno dei livelli della struttura.

        Args:
            key (str): Il nome del livello in cui aggiungere l'elemento.
            value (str): Il valore da inserire nel livello specificato.

        Raises:
            AttributeError: Se il livello specificato non esiste.
        """
        if key in vars(self):
            self[key].add(value)
        else:
            raise AttributeError(f"Il livello '{key}' non esiste in DB_Tree.")

    @property
    def sorted_paths(self):
        """
        Restituisce un elenco ordinato dei percorsi salvati.

        Returns:
            list: Lista ordinata dei percorsi completi.
        """
        return sorted(self.paths)
