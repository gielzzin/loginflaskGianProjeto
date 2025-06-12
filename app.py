from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_ponto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def hora_brasilia():
    fuso_brasilia = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_brasilia)

class entradaPonto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    hora = db.Column(db.DateTime, default=hora_brasilia)

class saidaPonto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    hora = db.Column(db.DateTime, default=hora_brasilia)

class justificativa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    hora = db.Column(db.DateTime, default=hora_brasilia)

@app.route('/templates/entradaPonto.html', methods=['GET', 'POST'])
def entrada_ponto():
    if request.method == 'POST':
        nomeEntrada = request.form['nome']
        if nomeEntrada:
            novo_registro = entradaPonto(nome=nomeEntrada)
            db.session.add(novo_registro)
            db.session.commit()
            print(f'✅ {nomeEntrada} bateu ponto às {novo_registro.hora.strftime("%H:%M:%S")}')
        return redirect(url_for('saida_ponto'))

    registrosE = entradaPonto.query.order_by(entradaPonto.hora.desc()).all()
    return render_template('entradaPonto.html', registrosEntrada=registrosE)

@app.route('/templates/saidaPonto.html', methods=['GET', 'POST'])
def saida_ponto():
    if request.method == 'POST':
        nomeSaida = request.form['nome']
        if nomeSaida:
            novo_registro = saidaPonto(nome=nomeSaida)
            db.session.add(novo_registro)
            db.session.commit()
            print(f'✅ {nomeSaida} bateu ponto às {novo_registro.hora.strftime("%H:%M:%S")}')
        return redirect(url_for('saida_ponto'))

    registrosS = saidaPonto.query.order_by(saidaPonto.hora.desc()).all()
    return render_template('saidaPonto.html', registrosSaida=registrosS)

@app.route('/templates/justificativa.html', methods=['GET', 'POST'])
def justificativas():
    if request.method == 'POST':
        textoJustificativa = request.form['nome']
        if textoJustificativa:
            novo_registro = justificativa(nome=textoJustificativa)
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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5500)

