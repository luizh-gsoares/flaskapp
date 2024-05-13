from flask import Flask, render_template, session, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.secret_key = 'PaoDoceFrango2024'

UPLOAD_FOLDER = '/home/luizhgsoares/mysite/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///minhabase.sqlite3'

db = SQLAlchemy(app)

app.app_context().push()

# Definição da classe Usuario
class Usuario(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String, unique=True)
    senha = db.Column(db.String)

    def __init__(self, nome, senha):
        self.nome = nome
        self.senha = senha

# Criação do banco de dados
with app.app_context():
    db.create_all()

#
# Rotas
#

# Rota para a página inicial
@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', usuario_logado = session['username'], usuarios = Usuario.query.all())

    return render_template('index.html')

# Rota para a página de registro
@app.route("/register", methods=['GET'])
def usuario():
    return render_template('register.html')

# Rota para adicionar um usuário
@app.route("/usuario/create", methods=['POST'])
def addUsuario():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        if Usuario.query.filter_by(nome=nome).first():
            return render_template('register.html', mensagem = 'Usuário já existe, tente novamente.')
        else:
            user = Usuario(nome, senha)
            db.session.add(user)
            db.session.commit()
            return render_template('login.html', mensagem = 'Usuário criado com sucesso. Faça o login.')

# Rota do login do usuário
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nome = request.form['nome']
        senha = request.form['senha']
        user = Usuario.query.filter_by(nome=nome).first()
        if user and user.senha == senha:
            session['username'] = nome
            return render_template('index.html', usuario_logado = session['username'], usuarios = Usuario.query.all())
        return render_template('login.html', mensagem = 'Usuário ou senha inválidos, tente novamente.')
    return render_template('login.html')

# Rota para o logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return render_template('index.html')

# Rota para a página de upload
@app.route("/upload", methods=['POST', 'GET'])
def upload():
    if 'username' in session:
        if request.method == 'POST':
            file = request.files['arquivo']
            savePath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(savePath)
            return render_template('upload.html', mensagem = 'Arquivo enviado com sucesso.', usuario_logado = session['username'])
        return render_template('upload.html', usuario_logado = session['username'])
    return render_template('index.html', mensagem = 'Faça o login para acessar esta página.')

# Função principal
if __name__ == '__main__':
    db.create_all()
    app.run()