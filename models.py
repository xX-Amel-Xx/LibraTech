from flask_sqlalchemy import SQLAlchemy
from datetime import date

#conexão com o banco de dados
db=SQLAlchemy ()

class Livro(db.Model):

    __tablename__= 'livro'
    id=db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    autor = db.Column(db.String(100), nullable=False)
    editora = db.Column(db.String(100), nullable=False)
    ano_publicacao = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'),nullable=False)
    emprestimo = db.relationship('Emprestimo', backref='livro')

class Usuario(db.Model):
    __tablename__="usuario"
    id=db.Column(db.Integer,primary_key=True)
    nome=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),unique=True,nullable=False)
    senha=db.Column(db.String(50),nullable=False)
    telefone=db.Column(db.String(20),unique=True,nullable=False)

class Categoria(db.Model):
    __tablename__= 'categoria'
    id=db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    livros = db.relationship('Livro', backref='categoria')
   

class Leitor(db.Model):
    __tablename__="leitor"
    id=db.Column(db.Integer,primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefone = db.Column(db.Integer, nullable=False)
    data_cadastro = db.Column(db.Date, nullable=False)
    emprestimo = db.relationship('Emprestimo', backref='leitor')

class Emprestimo(db.Model):
    __tablename__="emprestimo"
    id=db.Column(db.Integer,primary_key=True)
    livro_id = db.Column(db.Integer, db.ForeignKey('livro.id'),nullable=False)
    leitor_id = db.Column(db.Integer, db.ForeignKey('leitor.id'),nullable=False)
    data_emprestimo=db.Column(db.Date, nullable=False)
    data_prevista=db.Column(db.Date, nullable=False)
    data_devolucao=db.Column(db.Date,nullable=True)



    
