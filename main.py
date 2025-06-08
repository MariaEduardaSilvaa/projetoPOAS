from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_session
from models.models import Produto, Categoria, Fornecedor, Cliente, Movimentacao
from schemas import ProdutoCreate, ProdutoUpdate, Produto, CategoriaCreate, Categoria, FornecedorCreate, Fornecedor, MovimentacaoCreate, Movimentacao, ClienteCreate, Cliente
from typing import List
from datetime import datetime

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/produtos", response_model=Produto)
def criar_produto(produto: ProdutoCreate, session: Session = Depends(get_session)):
    try:
        if produto.pro_cat_id:
            categoria = session.query(Categoria).filter(Categoria.cat_id == produto.pro_cat_id).first()
            if not categoria:
                raise HTTPException(status_code=400, detail="Categoria não encontrada")

        db_produto = Produto(
            pro_nome=produto.pro_nome,
            pro_descricao=produto.pro_descricao,
            pro_custo=float(produto.pro_custo),
            pro_preco=float(produto.pro_preco),
            pro_quantidade=produto.pro_quantidade,
            pro_status=produto.pro_status,
            pro_marca=produto.pro_marca,
            pro_cat_id=produto.pro_cat_id,
            pro_data_cadastro=datetime.now()
        )

        session.add(db_produto)
        session.commit()
        session.refresh(db_produto)  

        return {
            "pro_id": db_produto.pro_id,
            "pro_nome": db_produto.pro_nome,
            "pro_descricao": db_produto.pro_descricao,
            "pro_custo": float(db_produto.pro_custo),
            "pro_preco": float(db_produto.pro_preco),
            "pro_quantidade": db_produto.pro_quantidade,
            "pro_status": db_produto.pro_status,
            "pro_marca": db_produto.pro_marca,
            "pro_cat_id": db_produto.pro_cat_id,
            "pro_data_cadastro": db_produto.pro_data_cadastro
        }

    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar produto: {str(e)}")

@app.delete("/produtos/{id}")
def deletar_produto(id: int, session: Session = Depends(get_session)):
    try:
        produto = session.get(Produto, id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")
        
        session.delete(produto)
        session.commit()
        return {"ok": True}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao deletar produto: {str(e)}")

@app.post("/categorias", response_model=Categoria)
def criar_categoria(categoria: CategoriaCreate, session: Session = Depends(get_session)):
    try:
        nova_categoria = Categoria(**categoria.dict())
        session.add(nova_categoria)
        session.commit()
        session.refresh(nova_categoria)
        return nova_categoria
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar categoria: {str(e)}")

@app.get("/categorias", response_model=List[Categoria])
def listar_categorias(session: Session = Depends(get_session)):
    try:
        return session.query(Categoria).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar categorias: {str(e)}")

@app.post("/fornecedores", response_model=Fornecedor)
def criar_fornecedor(fornecedor: FornecedorCreate, session: Session = Depends(get_session)):
    try:
        novo_fornecedor = Fornecedor(**fornecedor.dict())
        session.add(novo_fornecedor)
        session.commit()
        session.refresh(novo_fornecedor)
        return novo_fornecedor
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar fornecedor: {str(e)}")

@app.get("/fornecedores", response_model=List[Fornecedor])
def listar_fornecedores(session: Session = Depends(get_session)):
    try:
        return session.query(Fornecedor).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar fornecedores: {str(e)}")

@app.post("/clientes", response_model=Cliente)
def criar_cliente(cliente: ClienteCreate, session: Session = Depends(get_session)):
    try:
        novo_cliente = Cliente(**cliente.dict())
        session.add(novo_cliente)
        session.commit()
        session.refresh(novo_cliente)
        return novo_cliente
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar cliente: {str(e)}")

@app.get("/clientes", response_model=List[Cliente])
def listar_clientes(session: Session = Depends(get_session)):
    try:
        return session.query(Cliente).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar clientes: {str(e)}")

@app.post("/movimentacoes", response_model=Movimentacao)
def criar_movimentacao(movimentacao: MovimentacaoCreate, session: Session = Depends(get_session)):
    try:
        produto = session.get(Produto, movimentacao.mov_pro_id)
        if not produto:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

        if movimentacao.mov_quantidade <= 0:
            raise HTTPException(status_code=400, detail="Quantidade deve ser maior que zero")

        if movimentacao.mov_tipo == "saida":
            if produto.pro_quantidade < movimentacao.mov_quantidade:
                raise HTTPException(status_code=400, detail="Estoque insuficiente")
            produto.pro_quantidade -= movimentacao.mov_quantidade
        else:
            produto.pro_quantidade += movimentacao.mov_quantidade

        if movimentacao.mov_cli_id:
            cliente = session.get(Cliente, movimentacao.mov_cli_id)
            if not cliente:
                raise HTTPException(status_code=404, detail="Cliente não encontrado")

        nova_movimentacao = Movimentacao(
            mov_pro_id=movimentacao.mov_pro_id,
            mov_cli_id=movimentacao.mov_cli_id,
            mov_motivo=movimentacao.mov_motivo,
            mov_quantidade=movimentacao.mov_quantidade,
            mov_tipo=movimentacao.mov_tipo,
            mov_data=datetime.now()
        )
        
        session.add(nova_movimentacao)
        session.commit()
        session.refresh(nova_movimentacao)
        return nova_movimentacao
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar movimentação: {str(e)}")

@app.get("/movimentacoes", response_model=List[Movimentacao])
def listar_movimentacoes(session: Session = Depends(get_session)):
    try:
        return session.query(Movimentacao).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar movimentações: {str(e)}")