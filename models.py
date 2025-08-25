from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# Usuários
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Relatórios enviados pelo formulário principal
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    data = db.Column(db.String(20), nullable=False)
    fazenda = db.Column(db.String(100))
    talhao = db.Column(db.String(100))
    turno = db.Column(db.String(50))
    status = db.Column(db.String(50))
    maquina = db.Column(db.String(100))
    operador = db.Column(db.String(100))
    horimetro_inicial = db.Column(db.String(20))
    horimetro_final = db.Column(db.String(20))
    horas_trabalhadas = db.Column(db.String(20))
    producao_ha = db.Column(db.String(50))
    equipe_transporte = db.Column(db.String(50))
    dds_cafe = db.Column(db.String(50))
    transporte_pracha = db.Column(db.String(50))
    manutencoes = db.Column(db.Text)  # JSON em texto

# Relatórios simplificados para o dashboard
class Relatorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(20), nullable=False)
    fazenda = db.Column(db.String(100))
    talhao = db.Column(db.String(100))
    maquina = db.Column(db.String(100))
    operador = db.Column(db.String(100))
    horas_trabalhadas = db.Column(db.Float)
    producao_ha = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', backref=db.backref('relatorios', lazy=True))
