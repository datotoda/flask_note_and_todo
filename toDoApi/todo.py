from flask import Blueprint, render_template, request, redirect, url_for

todo = Blueprint('todo', __name__, static_folder='static', template_folder='templates')


class Task:
    def __init__(self, task_id, task='', checked=False):
        self.checked = checked
        self.task = task
        self.task_id = task_id


class Todo:
    def __init__(self, todo_id_int, title=''):
        self.tasks = []
        self.task_ids = []

        self.title = title
        self.link = todo_id_int

    def add_task(self, text='', checked=False):
        if self.task_ids:
            self.task_ids.append(self.task_ids[-1] + 1)
        else:
            self.task_ids.append(1)
        self.tasks.append(Task(self.task_ids[-1], text, checked))

    def delete_task(self, task_id):
        task_id = int(task_id)
        self.tasks.pop(self.task_ids.index(task_id))
        self.task_ids.remove(task_id)


class Todos:
    todos = [Todo(1, 'First'),
             Todo(2, 'Second'),
             Todo(3, 'BYE'),
             Todo(4, 'long'),
             Todo(5, 'Really bye')]
    ids = [1, 2, 3, 4, 5]

    @classmethod
    def new_todo(cls, title=''):
        cls.ids.append(cls.ids[-1] + 1)
        cls.todos.append(Todo(cls.ids[-1], title))

    @classmethod
    def add_task_by_id(cls, todo_id_str, text='', checked=False):
        cls.todos[cls.ids.index(int(todo_id_str))].add_task(text, checked)

    @classmethod
    def remove_task_by_id(cls, todo_id_str, task_id):
        cls.todos[cls.ids.index(int(todo_id_str))].delete_task(task_id)

    @classmethod
    def getTodoById(cls, todo_id_str):
        try:
            todo_id_int = int(todo_id_str)
        except ValueError:
            return False

        if todo_id_int in cls.ids:
            for each in cls.todos:
                if todo_id_int == each.link:
                    return each
        return False


@todo.route('/')
def index():
    return render_template('todo_home.html')


@todo.route('/new', methods=["POST", "GET"])
def new_todo():
    if request.method == 'POST':
        if request.form['title'].strip() != '':
            Todos.new_todo(request.form['title'])
            return redirect(url_for('todo.todo_id', todo_id_str=str(Todos.ids[-1])))

    return render_template('todo_new.html')


@todo.route('/<todo_id_str>', methods=["POST", "GET"])
def todo_id(todo_id_str):
    if not (current := Todos.getTodoById(todo_id_str)):
        # abort(404)
        return redirect(url_for('todo.todo_error_404'))

    if request.method == 'POST':
        task_checked_ids = []
        task_content_ids = []
        task_contents = {}

        for key, value in request.form.items():
            if key.startswith('task'):
                task_content_ids.append(int(key.split('_')[1]))
                task_contents[int(key.split('_')[1])] = value
            if key.startswith('checkbox'):
                task_checked_ids.append(int(key.split('_')[1]))

        for task in current.tasks:
            if task.task_id in task_checked_ids:
                task.checked = True
            else:
                task.checked = False
            if task.task_id in task_content_ids:
                task.task = task_contents[task.task_id]
            else:
                task.task = ''

        if 'new_task_button' in request.form.keys():
            current.add_task()
            return redirect(request.referrer)

        return '', 204

    return render_template('todo_detail.html', todo=current)


@todo.route('/error_404')
def todo_error_404():
    return render_template('todo_404.html')


@todo.route('/list')
def list_view():

    if not Todos.todos[0].tasks:
        Todos.todos[0].add_task('hard work', False)
        Todos.todos[0].add_task('easy work', True)
        Todos.todos[0].add_task('there are true', True)
        Todos.todos[0].add_task('again flase', False)
        Todos.todos[0].delete_task(3)
        Todos.todos[2].add_task('gg', True)
        Todos.todos[3].add_task('ccna', False)

    return render_template('todo_list.html', todos=Todos.todos)
