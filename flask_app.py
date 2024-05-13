import os
from flask import Flask, render_template, session, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.secret_key = '123456'
UPLOAD_FOLDER = '/home/luizhgsoares/mysite/upload'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minhabase.sqlite3'

db = SQLAlchemy(app)

class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True)
    senha = db.Column(db.String)

    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/usuario", methods=['POST', 'GET'])
def usuario():
    return render_template('usuario.html')

@app.route("/usuario/addUsuario", methods=['POST', 'GET'])
def addUsuario():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        user = Usuario(nome, senha)
        db.session.add(user)
        db.session.commit()
    users = Usuario.query.all()
    return render_template('usuario.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        user = Usuario.query.filter_by(nome=nome).first()
        if user and user.senha == senha:
            session['username'] = nome
            return 'Login feito com sucesso'
        return 'Falha no login'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if 'username' in session:
        if request.method == 'POST':
            file = request.files['arquivo']
            savePath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(savePath)
            return 'upload feito com sucesso'
        return render_template('upload.html')
    return 'Você não está logado'

if __name__ == '__main__':
    db.create_all()
    app.run()