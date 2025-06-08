from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Categoria(Base):
    __tablename__ = "categorias"
    cat_id = Column(Integer, primary_key=True, index=True)
    cat_nome = Column(String, nullable=False)
    produtos = relationship("Produto", back_populates="categoria")

class Produto(Base):
    __tablename__ = "produtos"
    pro_id = Column(Integer, primary_key=True, index=True)
    pro_nome = Column(String, nullable=False)
    pro_descricao = Column(String)
    pro_custo = Column(Float, nullable=False)  # Changed from Numeric to Float
    pro_preco = Column(Float, nullable=False)
    pro_quantidade = Column(Integer, nullable=False)
    pro_status = Column(String, default="disponível")
    pro_marca = Column(String)
    pro_cat_id = Column(Integer, ForeignKey("categorias.cat_id"))
    pro_data_cadastro = Column(DateTime, default=datetime.now)

    categoria = relationship("Categoria", back_populates="produtos")
    movimentacoes = relationship("Movimentacao", back_populates="produto")

class Fornecedor(Base):
    __tablename__ = "fornecedores"
    for_id = Column(Integer, primary_key=True, index=True)
    for_nome = Column(String, nullable=False)
    for_cnpj = Column(String)
    for_contato = Column(String)

class Cliente(Base):
    __tablename__ = "clientes"
    cli_id = Column(Integer, primary_key=True, index=True)
    cli_nome = Column(String, nullable=False)  # Made non-optional
    cli_cpf = Column(String)
    movimentacoes = relationship("Movimentacao", back_populates="cliente")

class Movimentacao(Base):
    __tablename__ = "movimentacoes"
    mov_id = Column(Integer, primary_key=True, index=True)
    mov_pro_id = Column(Integer, ForeignKey("produtos.pro_id"), nullable=False)
    mov_cli_id = Column(Integer, ForeignKey("clientes.cli_id"))
    mov_motivo = Column(String, nullable=False)
    mov_quantidade = Column(Integer, nullable=False)
    mov_tipo = Column(String, nullable=False)
    mov_data = Column(DateTime, default=datetime.now)

    produto = relationship("Produto", back_populates="movimentacoes")
    cliente = relationship("Cliente", back_populates="movimentacoes")