from flask import Flask, render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user
from flask_login import LoginManager
from models import db, Usuarios, entradaPonto, saidaPonto, justificativa
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_ponto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
db.init_app(app)

def hora_brasilia():
    fuso_brasilia = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_brasilia)


@app.route("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("funcionario"))
    else:
        return redirect(url_for("login"))   
                
@app.route("/templates/home.html")
def home():
        return render_template('home.html')

@app.route("/funcionario")
def funcionario():
    if current_user.is_authenticated and current_user.admin:
        return redirect(url_for("relatorio"))

    if current_user.is_authenticated:
        return redirect(url_for("entrada_ponto", user=current_user))
    else:
        return redirect(url_for("login"))

@app.route("/templates/admin.html", methods=['GET', 'POST'])
def admin():
    if current_user.is_authenticated and current_user.admin:
        if request.method == 'POST':
            nome = request.form.get("nome")
            email = request.form.get("email")
            senha = request.form.get("senha")
            admin = request.form.get("admin")

            if request.form.get("admin"):
                admin = True
            else:
                admin = False

            # Verifica se o usuário já existe
            if Usuarios.query.filter_by(email=email).first():
                return render_template("admin.html", user=current_user, error="Usuário já existe.")

            
            # Verifica se a Senha é Válida
            if len(senha) < 6:
                return render_template("admin.html", user=current_user, error="A senha deve ter pelo menos 6 caracteres.")
            
            # Verifica se o nome é válido
            if len(nome) < 3:
                return render_template("admin.html", user=current_user, error="O nome deve ter pelo menos 3 caracteres.")

            novo_usuario = Usuarios(nome=nome, email=email, senha=senha, admin=admin)
            db.session.add(novo_usuario)
            db.session.commit()
            return redirect(url_for("admin"))
        
        return render_template("admin.html", user=current_user)
    else:
        return redirect(url_for("index"))
    
@app.route("/templates/loginn.html", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get("email")
        senha = request.form.get("senha")

        Usuario = Usuarios.query.filter_by(email=email).first()
        if Usuario and Usuario.senha == senha:
            login_user(Usuario)
            return redirect(url_for("funcionario"))
        else:   
            return render_template("loginn.html", error="Email ou senha incorretos.")
    return render_template("loginn.html")


@app.route('/templates/entradaPonto.html', methods=['GET', 'POST'])
def entrada_ponto():
    if request.method == 'POST':
        nomeEntrada = request.form['nome']
        if nomeEntrada:
            novo_registro = entradaPonto(nome=nomeEntrada, usuario_id=1)
            db.session.add(novo_registro)
            db.session.commit()
            print(f'✅ {nomeEntrada} bateu ponto às {novo_registro.hora.strftime("%H:%M:%S")}')
        return redirect(url_for('home'))

    registrosE = entradaPonto.query.order_by(entradaPonto.hora.desc()).all()
    return render_template('entradaPonto.html', registrosEntrada=registrosE)

@app.route('/templates/saidaPonto.html', methods=['GET', 'POST'])
def saida_ponto():
    if request.method == 'POST':
        nomeSaida = request.form['nome']
        if nomeSaida:
            novo_registro = saidaPonto(nome=nomeSaida, usuario_id=1)
            db.session.add(novo_registro)
            db.session.commit()
            print(f'✅ {nomeSaida} bateu ponto às {novo_registro.hora.strftime("%H:%M:%S")}')
        return redirect(url_for('logout'))

    registrosS = saidaPonto.query.order_by(saidaPonto.hora.desc()).all()
    return render_template('saidaPonto.html', registrosSaida=registrosS)

@app.route('/templates/justificativa.html', methods=['GET', 'POST'])
def justificativas():
    if request.method == 'POST':
        textoJustificativa = request.form['nome']
        if textoJustificativa:
            novo_registro = justificativa(nome=textoJustificativa, usuario_id=1)
            db.session.add(novo_registro)
            db.session.commit()
        return redirect(url_for('justificativas'))

    registrosJ = justificativa.query.order_by(justificativa.hora.desc()).all()
    return render_template('justificativa.html', registrosJustificativa=registrosJ)

@app.route('/templates/relatorio.html', methods=['GET'])
def relatorio():
    if request.method == 'POST':
            nomeEntrada = request.form.get('nome')
            nomeSaida = request.form.get('nome')
            textoJustificativa = request.form.get('nome')
            entradaPonto(nome=nomeEntrada)
            saidaPonto(nome=nomeSaida)
            justificativa(nome=textoJustificativa)

            return redirect(url_for('relatorio'))
   
    registrosE = entradaPonto.query.order_by(entradaPonto.hora.desc()).all()
    registrosS = saidaPonto.query.order_by(saidaPonto.hora.desc()).all()
    registrosJ = justificativa.query.order_by(justificativa.hora.desc()).all()

    return render_template('relatorio.html', registrosEntrada = registrosE, registrosSaida = registrosS, registrosJustificativa = registrosJ)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@login_manager.user_loader
def load_user(user_id):
    return Usuarios.query.get(int(user_id))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True, port=5500)

