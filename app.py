from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco_ponto.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class RegistroPonto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    hora = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/', methods=['GET', 'POST'])
def registrar_ponto():
    if request.method == 'POST':
        nome = request.form['nome']
        if nome:
            novo_registro = RegistroPonto(nome=nome)
            db.session.add(novo_registro)
            db.session.commit()
            print(f'✅ {nome} bateu ponto às {novo_registro.hora.strftime("%H:%M:%S")}')  # Terminal
        return redirect(url_for('registrar_ponto'))

    registros = RegistroPonto.query.order_by(RegistroPonto.hora.desc()).all()
    return render_template('registro.html', registros=registros)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5500)

