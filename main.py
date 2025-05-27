from fastapi import FastAPI, HTTPException, Depends, Query
from datetime import datetime
from sqlalchemy.orm import Session
from models.models import Produto, Categoria, Fornecedor, Movimentacao
from database import SessionLocal, engine, Base
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/produtos", response_model=schemas.Produto)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    db_prod = Produto(**produto.dict())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

@app.get("/produtos", response_model=list[schemas.Produto])
def listar_produto(db: Session = Depends(get_db)):
    return db.query(Produto).all()

@app.get("/produtos/{id}", response_model=schemas.Produto)
def listar_produto(id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.pro_id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.put("/produtos/{id}", response_model=schemas.Produto)
def atualizar_produto(id: int, produto: schemas.ProdutoUpdate, db: Session = Depends(get_db)):
    db_prod = db.query(Produto).filter(Produto.pro_id == id).first()
    if not db_prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for key, value in produto.dict().items():
        setattr(db_prod, key, value)
    db.commit()
    db.refresh(db_prod)
    return db_prod

@app.post("/categoria", response_model=schemas.Categoria)
def criar_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_cat = Categoria(**categoria.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@app.get("/categoria", response_model=list[schemas.Categoria])
def listar_categoria(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@app.post("/fornecedores", response_model=schemas.Fornecedor)
def criar_fornecedor(fornecedor: schemas.FornecedorCreate, db: Session = Depends(get_db)):
    db_forn = Fornecedor(**fornecedor.dict())
    db.add(db_forn)
    db.commit()
    db.refresh(db_forn)
    return db_forn

@app.get("/fornecedores", response_model=list[schemas.Fornecedor])
def listar_fornecedores(db: Session = Depends(get_db)):
    return db.query(Fornecedor).all()

@app.post("/movimentacoes", response_model=schemas.Movimentacao, status_code=201)
def registrar_movimentacao(mov: schemas.MovimentacaoCreate, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.pro_id == mov.mov_pro_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    # Validação de estoque para saída
    if mov.mov_tipo == "saida" and produto.pro_quantidade < mov.mov_quantidade:
        raise HTTPException(status_code=400, detail="Estoque insuficiente para saída")

    # Atualiza estoque
    if mov.mov_tipo == "entrada":
        produto.pro_quantidade += mov.mov_quantidade
    elif mov.mov_tipo == "saida":
        produto.pro_quantidade -= mov.mov_quantidade

    nova_mov = Movimentacao(**mov.dict())
    db.add(nova_mov)
    db.commit()
    db.refresh(nova_mov)
    return nova_mov

@app.get("/movimentacoes", response_model=list[schemas.Movimentacao])
def listar_movimentacoes(db: Session = Depends(get_db)):
    return db.query(Movimentacao).order_by(Movimentacao.mov_data.desc()).all()

@app.get("/movimentacoes/filtrar", response_model=list[schemas.Movimentacao])
def filtrar_movimentacoes_por_data(
    inicio: datetime = Query(..., description="Data inicial no formato YYYY-MM-DD"),
    fim: datetime = Query(..., description="Data final no formato YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    movimentacoes = db.query(Movimentacao).filter(
        Movimentacao.mov_data >= inicio,
        Movimentacao.mov_data <= fim
    ).order_by(Movimentacao.mov_data.desc()).all()

    return movimentacoes