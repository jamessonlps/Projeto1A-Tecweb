import os
from database import Database

main_database = 'data/banco'

def extract_route(request):
    final = 0
    for j in range(4, len(request)):
        if request[j] == " ":
            final = j
            break
    return request[5 : final]


def read_file(path):
    main_types = ['txt', 'html', 'css', 'js']
    name, extension = os.path.splitext(path)
    # Lê arquivo como string
    if extension in main_types:
        with open(path, 'r', encoding='utf-8') as file:
            data = file.read()
    # Lê como bytes
    else:
        with open(path, 'rb') as file:
            data = file.read()
    return data


def load_template(template):
    """ Recebe um HTML e converte para string """
    
    path = f'templates/{template}'
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content


def build_response(body='', code=200, reason='OK', headers=''):
    # Se houver conteúdo no headers, deve ser passado entre reason e body
    if len(headers) > 0:
        return f'HTTP/1.1 {code} {reason}\n{headers}\n\n{body}'.encode()
    return f'HTTP/1.1 {code} {reason}\n\n{body}'.encode()


# =============================================================

def load_database(database=main_database):
    """
        Carrega base de dados retornando uma lista de notes
    """
    db = Database(database)
    return db.get_all()


def add_note(note, database=main_database):
    """
        Insere nova nota no banco de dados
    """
    db = Database(database)
    db.add(note)


def delete_note(note, database=main_database):
    """
        Remove nota do banco de dados
    """
    db = Database(database)
    notes = db.get_all()
    for nt in notes:
        if ((nt.title == note.title) and (nt.content == note.content)):
            db.delete(nt.id)
            break


def update_note(previous_note, new_note, database=main_database):
    """
        Atualiza nota do banco de dados
    """
    db = Database(database)
    notes = db.get_all()

    for nt in notes:
        if ((nt.title == previous_note.title) and (nt.content == previous_note.content)):
            new_note.id = nt.id #guarda id e encerra looping
            break
    db.update(new_note)
