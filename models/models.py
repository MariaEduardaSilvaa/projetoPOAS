from sqlalchemy import Column, Integer, String, DateTime, Enum, Text, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class Categoria(Base):
    __tablename__ = 'tb_categorias'

    cat_id = Column(Integer, primary_key=True, autoincrement=True)
    cat_nome = Column(String(50), nullable=False)

class Produto(Base):
    __tablename__ = 'tb_produtos'

    pro_id = Column(Integer, primary_key=True, autoincrement=True)
    pro_nome = Column(String(100), nullable=False)
    pro_descricao = Column(Text)
    pro_custo = Column(DECIMAL(10, 2), nullable=False)
    pro_preco = Column(DECIMAL(10, 2), nullable=False)
    pro_quantidade = Column(Integer, nullable=False)
    pro_data_cadastro = Column(DateTime, default=datetime.datetime.utcnow)
    pro_status = Column(Enum('disponível', 'indisponível'), default='disponível')
    pro_marca = Column(String(50))
    pro_cat_id = Column(Integer, ForeignKey('tb_categorias.cat_id'))

    categoria = relationship('Categoria')

class Fornecedor(Base):
    __tablename__ = 'tb_fornecedores'

    for_id = Column(Integer, primary_key=True, autoincrement=True)
    for_nome = Column(String(100), nullable=False)
    for_cnpj = Column(String(18))
    for_contato = Column(String(20))

class Cliente(Base):
    __tablename__ = 'tb_clientes'

    cli_id = Column(Integer, primary_key=True, autoincrement=True)
    cli_cpf = Column(String(18))
    cli_nome = Column(String(45))

class Movimentacao(Base):
    __tablename__ = 'tb_movimentacoes'

    mov_id = Column(Integer, primary_key=True, autoincrement=True)
    mov_pro_id = Column(Integer, ForeignKey('tb_produtos.pro_id', ondelete='CASCADE'))
    mov_cli_id = Column(Integer, ForeignKey('tb_clientes.cli_id'), nullable=True)
    mov_motivo = Column(String(500))
    mov_data = Column(DateTime, default=datetime.datetime.utcnow)
    mov_quantidade = Column(Integer)

    produto = relationship('Produto')
    cliente = relationship('Cliente')