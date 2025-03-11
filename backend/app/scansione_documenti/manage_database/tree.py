# backend/app/scansione_documenti/manage_database/tree.py
class DB_Tree:
    structure = ['category', 'utility', 'year', 'document_type', 'document']

    def __init__(self):
        self.category = set()
        self.utility = set()
        self.year = set()
        self.document_type = set()
        self.document = set()

    def __str__(self):
        return (
            f'categories: {self.category}\n'
            f'utilities: {self.utility}\n'
            f'years: {self.year}\n'
            f'document_types: {self.document_type}\n'
            f'documents: {self.document}'
        )

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, key):
        return getattr(self, key)

    def dict(self):
        return {k: getattr(self, k) for k in self.structure}

    def __sub__(self, other):
        return {k: getattr(self, k) - getattr(other, k) for k in self.structure}

    def add(self, key: str, value: str):
        self[key].add(value)
