from utils import build_response, delete_note, load_database, load_template, add_note, delete_note, update_note
from urllib.parse import unquote_plus
from database import Note

def index(request):
    if request.startswith('POST'):
        print('\n\n', request)
        request = request.replace('\r', '') # remove caracteres indesejados
        # Cabeçalho e corpo estão sempre separados por duas quebras de linha
        sections = request.split('\n\n')
        body = sections[1]
        params = {}
        # Preenche o dicionário params com as informações do corpo da requisição
        # O dicionário conterá dois valores, o título e a descrição.
        # Posteriormente pode ser interessante criar uma função que recebe a
        # requisição e devolve os parâmetros para desacoplar esta lógica.
        for key_value in body.split('&'):
            # print(key_value)
            key_value = unquote_plus(key_value, encoding='utf-8', errors='replace')
            key_value = key_value.split('=')
            key = key_value[0]
            value = ''.join(key_value[1:])
            params[key] = value

        # Cria um objeto do tipo Note
        note = Note(title=params['titulo'], content=params['detalhes'])
        
        if ('create' in params.keys()):
            # adiciona a nova nota no banco de dados
            add_note(note)
        
        elif ('update' in params.keys()):
            # Pega informações da nota existente para atualizá-la
            previous_note = Note(title=params['prev_ttl'],content=params['prev_dtl'])
            update_note(previous_note, note)
        
        elif ('delete' in params.keys()):
            # Deleta a nota selecionada
            delete_note(note)

        return build_response(code=303, reason='See Other', headers='Location: /')

    # Cria uma lista de <li>'s para cada anotação
    note_template = load_template('components/note.html')
    notes_li = []
    for note in load_database():
        notes_li.append(note_template.format(title=note.title, details=note.content))
    notes = '\n'.join(notes_li)

    return build_response(load_template('index.html').format(notes=notes))