from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_ponto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def hora_brasilia():
    fuso_brasilia = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_brasilia)

class RegistroPonto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    hora = db.Column(db.DateTime, default=hora_brasilia)

@app.route('/templates/entradaPonto.html', methods=['GET', 'POST'])
def entrada_ponto():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome:
            novo_registro = RegistroPonto(nome=nome)
            db.session.add(novo_registro)
            db.session.commit()
            print(f'✅ {nome} bateu ponto às {novo_registro.hora.strftime("%H:%M:%S")}')
        return redirect(url_for('saida_ponto'))

    registros = RegistroPonto.query.order_by(RegistroPonto.hora.desc()).all()
    return render_template('entradaPonto.html', registros=registros)

@app.route('/templates/saidaPonto.html', methods=['GET', 'POST'])
def saida_ponto():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome:
            novo_registro = RegistroPonto(nome=nome)
            db.session.add(novo_registro)
            db.session.commit()
            print(f'✅ {nome} bateu ponto às {novo_registro.hora.strftime("%H:%M:%S")}')
        return redirect(url_for('saida_ponto'))

    registros = RegistroPonto.query.order_by(RegistroPonto.hora.desc()).all()
    return render_template('saidaPonto.html', registros=registros)


@app.route('/templates/relatorio.html', methods=['GET'])
def relatorio():
   if request.method == 'POST':
        nome = request.form.get('nome')
        RegistroPonto(nome=nome)

        return redirect(url_for('relatorio'))
   
   registros = RegistroPonto.query.order_by(RegistroPonto.hora.desc()).all()
   return render_template('relatorio.html', registros=registros)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5500)

