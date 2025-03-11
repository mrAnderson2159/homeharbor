# backend/app/paperless/models.py

"""
Definizione dei modelli SQLAlchemy per il modulo di gestione documenti.

Questi modelli rappresentano la struttura relazionale del database
all'interno dello schema `paperless`, che mappa le directory
e i documenti scansionati, insieme ai metadati e alle entità correlate.
"""


from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    """
    Rappresenta una categoria di documenti (es. 'Salute', 'Banca', ecc.).

    Attributi:
        id (int): Chiave primaria.
        name (str): Nome univoco della categoria.
        description (str): Descrizione opzionale.
        paths (relazione): Relazione con la tabella `Path`.
    """

    __tablename__ = "categories"
    __table_args__ = {"schema": "paperless"}  #

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String)

    paths = relationship("Path", back_populates="category_rel")


class Utility(Base):
    """
    Entità che rappresenta un'utenza, ovvero il mittente o destinatario del documento
    (es. 'Enel', 'Vodafone', 'Poste', ecc.).

    Attributi:
        id (int): Chiave primaria.
        name (str): Nome univoco dell'utenza.
        description (str): Descrizione opzionale.
        paths (relazione): Relazione con la tabella `Path`.
    """

    __tablename__ = "utilities"
    __table_args__ = {"schema": "paperless"}  #

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String)

    paths = relationship("Path", back_populates="utility_rel")


class Year(Base):
    """
    Rappresenta un anno di riferimento (es. 2022, 2019, ecc.).

    Attributi:
        id (int): Chiave primaria.
        name (int): Anno numerico, con vincolo ≥ 2000.
        paths (relazione): Relazione con la tabella `Path`.
    """

    __tablename__ = "years"
    __table_args__ = {"schema": "paperless"}  #

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Integer,
                  CheckConstraint("year >= 2000", name="check_year_range"),
                  nullable=False, unique=True, index=True)

    paths = relationship("Path", back_populates="year_rel")


class DocumentType(Base):
    """
    Specifica la tipologia del documento (es. 'Pagato', 'Non Pagato', 'Default').

    Attributi:
        id (int): Chiave primaria.
        name (str): Tipologia, con vincolo di valori ammessi.
        description (str): Descrizione opzionale.
        paths (relazione): Relazione con la tabella `Path`.
    """

    __tablename__ = "document_types"
    __table_args__ = {"schema": "paperless"}  #

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,
                  CheckConstraint("name IN ('paid', 'not_paid', 'default')", name="check_valid_document_type"),
                  nullable=False, unique=True, index=True)
    description = Column(String)

    paths = relationship("Path", back_populates="document_type_rel")


class Document(Base):
    """
    Descrive un documento specifico, come un file o una scansione.

    Attributi:
        id (int): Chiave primaria.
        name (str): Nome del documento.
        description (str): Descrizione opzionale.
        paths (relazione): Collegamento con i `Path`.
        tags (relazione): Relazione molti-a-molti con i `Tag`.
    """

    __tablename__ = "documents"
    __table_args__ = {"schema": "paperless"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)

    paths = relationship("Path", back_populates="document_rel")
    tags = relationship(
        "Tag",
        secondary="paperless.document_tags",
        back_populates="documents"
    )


class Path(Base):
    """
    Rappresenta un percorso completo nel filesystem, come relazione tra:
    Categoria → Utenza → Anno → Tipo Documento → Documento.

    Vincolo di unicità su tutte le colonne.

    Attributi:
        id (int): Chiave primaria.
        category, utility, year, document_type, document (int): Chiavi esterne.
        category_rel, utility_rel, year_rel, document_type_rel, document_rel: relazioni inverse.
    """

    __tablename__ = "paths"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Integer, ForeignKey("paperless.categories.id"), nullable=False)
    utility = Column(Integer, ForeignKey("paperless.utilities.id"), nullable=False)
    year = Column(Integer, ForeignKey("paperless.years.id"), nullable=False)
    document_type = Column(Integer, ForeignKey("paperless.document_types.id"), nullable=False)
    document = Column(Integer, ForeignKey("paperless.documents.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("category", "utility", "year", "document_type", "document",
                         name="unique_path_constraint"),
        {"schema": "paperless"}
    )

    category_rel = relationship("Category", back_populates="paths")
    utility_rel = relationship("Utility", back_populates="paths")
    year_rel = relationship("Year", back_populates="paths")
    document_type_rel = relationship("DocumentType", back_populates="paths")
    document_rel = relationship("Document", back_populates="paths")


class Tag(Base):
    """
    Tag semantici assegnabili ai documenti.

    Attributi:
        id (int): Chiave primaria.
        name (str): Nome univoco del tag.
        documents (relazione): Documenti associati.
    """

    __tablename__ = "tags"
    __table_args__ = {"schema": "paperless"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)

    documents = relationship(
        "Document",
        secondary="paperless.document_tags",
        back_populates="tags"
    )


class DocumentTag(Base):
    """
    Tabella ponte per la relazione molti-a-molti tra `Document` e `Tag`.

    Attributi:
        id (int): Chiave primaria.
        document_id (int): FK verso `documents`.
        tag_id (int): FK verso `tags`.
    """

    __tablename__ = "document_tags"
    __table_args__ = (
        UniqueConstraint("document_id", "tag_id", name="unique_document_tag"),
        {"schema": "paperless"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("paperless.documents.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("paperless.tags.id"), nullable=False)


class ExcludedPath(Base):
    """
    Elenco di cartelle da escludere dalla scansione.

    Attributi:
        id (int): Chiave primaria.
        path (str): Nome della cartella esclusa.
        reason (str): Motivazione opzionale.
    """

    __tablename__ = "excluded_paths"
    __table_args__ = {"schema": "paperless"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, nullable=False, unique=True, index=True)
    reason = Column(String)
