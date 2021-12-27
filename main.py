from flask import Flask, render_template
from noteApi.note import note
from toDoApi.todo import todo


app = Flask(__name__)
app.register_blueprint(note, url_prefix='/note')
app.register_blueprint(todo, url_prefix='/todo')


@app.route('/')
def home():
    return render_template('home.html')


@app.errorhandler(404)
def error_404(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run()
