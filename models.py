from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz


db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False) 
    registrosEntrada = db.relationship('entradaPonto', backref='usuario', lazy=True)
    registrosSaida = db.relationship('saidaPonto', backref='usuario', lazy=True)

def hora_brasilia():
    fuso_brasilia = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_brasilia)

class entradaPonto(db.Model):
    idEntrada = db.Column(db.Integer, primary_key=True)
    horarioEntrada = db.Column(db.DateTime, default=hora_brasilia)
    nomeEntrada = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class saidaPonto(db.Model):
    idSaida = db.Column(db.Integer, primary_key=True)
    nomeSaida = db.Column(db.String(100), nullable=False)
    horaSaida = db.Column(db.DateTime, default=hora_brasilia)    
