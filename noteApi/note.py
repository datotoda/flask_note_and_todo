from flask import Blueprint, render_template, request, redirect, url_for

note = Blueprint('note', __name__, static_folder='static', template_folder='templates')


class Note:
    def __init__(self, note_id, title='', content=''):
        self.title = title
        self.content = content
        self.link = note_id


class Notes:
    notes = [Note(1, 'First', 'hello world!'),
             Note(2, 'Second', 'hello world again!'),
             Note(3, 'BYE', 'bye bye!'),
             Note(4, 'long', 'hello\n\nand\n\nworld!'),
             Note(5, 'Really bye', 'ok bye!')]
    ids = [1, 2, 3, 4, 5]

    @classmethod
    def new_note(cls, title='', content=''):
        cls.ids.append(cls.ids[-1] + 1)
        cls.notes.append(Note(cls.ids[-1], title, content))

    @classmethod
    def getNoteById(cls, _note_id):
        try:
            _note_id = int(_note_id)
        except Exception:
            return False

        if _note_id in cls.ids:
            for _note in cls.notes:
                if _note_id == _note.link:
                    return _note
        return False


@note.route('/')
def index():
    return render_template('note_home.html')


@note.route('/new', methods=["POST", "GET"])
def new_note():
    if request.method == 'POST':
        if request.form['title'].strip() != '':
            Notes.new_note(request.form['title'], request.form['data'])
            return redirect(url_for('.note_id', note_id_str=str(Notes.ids[-1])))

    return render_template('note_detail.html', new=True)


@note.route('/<note_id_str>', methods=["POST", "GET"])
def note_id(note_id_str):
    current_note = Notes.getNoteById(note_id_str)
    if not current_note:
        return redirect(url_for('.note_error_404'))
    if request.method == 'POST':
        current_note.title = request.form['title']
        current_note.content = request.form['data']
    return render_template('note_detail.html', note=current_note)


@note.route('/error_404')
def note_error_404():
    return render_template('note_404.html')


@note.route('/list')
def list_view():
    return render_template('note_list.html', notes=Notes.notes)
