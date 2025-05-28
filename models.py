from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz


db = SQLAlchemy()

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False) 
    registros = db.relationship('RegistroPonto', backref='usuario', lazy=True)

def hora_brasilia():
    fuso_brasilia = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_brasilia)

class RegistroPonto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.DateTime, default=hora_brasilia)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
