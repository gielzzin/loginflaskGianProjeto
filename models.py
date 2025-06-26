from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
import pytz

db = SQLAlchemy()


def hora_brasilia():
    fuso_brasilia = pytz.timezone('America/Sao_Paulo')
    return datetime.now(fuso_brasilia)


class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False) 
    email = db.Column(db.String(250), unique=True, nullable=False)  
    senha = db.Column(db.String(250), nullable=False)
    admin = db.Column(db.Boolean, nullable=False)
    registrosEntrada = db.relationship('entradaPonto', backref='usuario', lazy=True)
    registrosSaida = db.relationship('saidaPonto', backref='usuario', lazy=True)
    textoJustificativa = db.relationship('justificativa', backref='usuario', lazy=True)

class entradaPonto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    hora = db.Column(db.DateTime, default=hora_brasilia)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)


class saidaPonto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    hora = db.Column(db.DateTime, default=hora_brasilia)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class justificativa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    hora = db.Column(db.DateTime, default=hora_brasilia)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)


