from dataclasses import dataclass
import sqlite3

@dataclass
class Note:
    id: int = None
    title: str = None
    content: str = ''

class Database:
    def __init__(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name + '.db')
            self.cursor = self.conn.cursor()
            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS note (
                    id INTEGER PRIMARY KEY,
                    title STRING,
                    content STRING NOT NULL
                );
                """
            )
            print("Tabela criada com sucesso")
        except sqlite3.Error:
            print("Erro ao abrir o banco de dados")


    def add(self, note):
        try:
            self.cursor.execute(
                f"""
                INSERT INTO note (
                    title, content
                )
                VALUES (
                    '{note.title}',
                    '{note.content}'
                );
                """
            )
            self.conn.commit()
            print("Nota adicionada com sucesso")
        except sqlite3.Error:
            print("Erro ao adicionar a nota no banco de dados")


    def get_all(self):
        try:
            cursor = self.conn.execute(
                """
                SELECT id, title, content FROM note
                """
            )

            notes = []
            for linha in cursor:
                notes.append(
                    Note(
                        id=linha[0],
                        title=linha[1],
                        content=linha[2]
                    )
                )
            print("Notas carregadas com sucesso!")

            return notes
        except sqlite3.Error:
            print("Não foi possível buscar as informações solicitadas")
            return None
    

    def update(self, entry):
        try:
            self.cursor.execute(
                f"""
                UPDATE note SET title = '{entry.title}', content = '{entry.content}'
                WHERE id = {entry.id}
                """
            )

            self.conn.commit()

            print("Dados atualizados com sucesso!")
        except sqlite3.Error:
            print("Erro ao atualizar a nota")


    def delete(self, note_id):
        try:
            self.cursor.execute(
                """
                DELETE FROM note
                WHERE id = ?
                """,
                (note_id,)
            )

            self.conn.commit()

            print("Nota deletada com sucesso!")
        except sqlite3.Error:
            print("Ocorreu um erro ao deletar a nota.")
