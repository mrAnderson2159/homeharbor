# backend/app/scansione_documenti/models.py
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy import ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from app.database import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"schema": "scansione_documenti"}  #

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String)

    paths = relationship("Path", back_populates="category_rel")


class Utility(Base):
    __tablename__ = "utilities"
    __table_args__ = {"schema": "scansione_documenti"}  #

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    description = Column(String)

    paths = relationship("Path", back_populates="utility_rel")


class Year(Base):
    __tablename__ = "years"
    __table_args__ = {"schema": "scansione_documenti"}  #

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Integer,
                  CheckConstraint("year >= 2000", name="check_year_range"),
                  nullable=False, unique=True, index=True)

    paths = relationship("Path", back_populates="year_rel")


class DocumentType(Base):
    __tablename__ = "document_types"
    __table_args__ = {"schema": "scansione_documenti"}  #

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String,
                  CheckConstraint("name IN ('paid', 'not_paid', 'default')", name="check_valid_document_type"),
                  nullable=False, unique=True, index=True)
    description = Column(String)

    paths = relationship("Path", back_populates="document_type_rel")


class Document(Base):
    __tablename__ = "documents"
    __table_args__ = {"schema": "scansione_documenti"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)

    paths = relationship("Path", back_populates="document_rel")
    tags = relationship(
        "Tag",
        secondary="scansione_documenti.document_tags",
        back_populates="documents"
    )


class Path(Base):
    __tablename__ = "paths"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(Integer, ForeignKey("scansione_documenti.categories.id"), nullable=False)
    utility = Column(Integer, ForeignKey("scansione_documenti.utilities.id"), nullable=False)
    year = Column(Integer, ForeignKey("scansione_documenti.years.id"), nullable=False)
    document_type = Column(Integer, ForeignKey("scansione_documenti.document_types.id"), nullable=False)
    document = Column(Integer, ForeignKey("scansione_documenti.documents.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("category", "utility", "year", "document_type", "document",
                         name="unique_path_constraint"),
        {"schema": "scansione_documenti"}
    )

    category_rel = relationship("Category", back_populates="paths")
    utility_rel = relationship("Utility", back_populates="paths")
    year_rel = relationship("Year", back_populates="paths")
    document_type_rel = relationship("DocumentType", back_populates="paths")
    document_rel = relationship("Document", back_populates="paths")


class Tag(Base):
    __tablename__ = "tags"
    __table_args__ = {"schema": "scansione_documenti"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)

    documents = relationship(
        "Document",
        secondary="scansione_documenti.document_tags",
        back_populates="tags"
    )


class DocumentTag(Base):
    __tablename__ = "document_tags"
    __table_args__ = (
        UniqueConstraint("document_id", "tag_id", name="unique_document_tag"),
        {"schema": "scansione_documenti"}
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("scansione_documenti.documents.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("scansione_documenti.tags.id"), nullable=False)


class ExcludedPath(Base):
    __tablename__ = "excluded_paths"
    __table_args__ = {"schema": "scansione_documenti"}

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, nullable=False, unique=True, index=True)
    reason = Column(String)
