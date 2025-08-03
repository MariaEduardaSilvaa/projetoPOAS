from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models.models import Produto, Categoria, Fornecedor
from database import SessionLocal, engine, Base
import schemas
from models.models import Produto, Categoria, Fornecedor, Cliente, Movimentacao

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
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()

@app.get("/produtos/{id}", response_model=schemas.Produto)
def buscar_produto(id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.pro_id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.post("/produtos/{id}", response_model=schemas.Produto)
def atualizar_produto(id: int, produto: schemas.ProdutoUpdate, db: Session = Depends(get_db)):
    db_prod = db.query(Produto).filter(Produto.pro_id == id).first()
    if not db_prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for key, value in produto.dict().items():
        setattr(db_prod, key, value)
    db.commit()
    db.refresh(db_prod)
    return db_prod

@app.post("/categorias", response_model=schemas.Categoria)
def criar_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_cat = Categoria(**categoria.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@app.get("/categorias", response_model=list[schemas.Categoria])
def listar_categorias(db: Session = Depends(get_db)):
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

from models.models import Produto, Categoria, Fornecedor, Cliente, Movimentacao


@app.post("/clientes", response_model=schemas.Cliente)
def criar_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    db_cli = Cliente(**cliente.dict())
    db.add(db_cli)
    db.commit()
    db.refresh(db_cli)
    return db_cli

@app.get("/clientes", response_model=list[schemas.Cliente])
def listar_clientes(db: Session = Depends(get_db)):
    return db.query(Cliente).all()

@app.get("/clientes/{id}", response_model=schemas.Cliente)
def buscar_cliente(id: int, db: Session = Depends(get_db)):
    cli = db.query(Cliente).filter(Cliente.cli_id == id).first()
    if not cli:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    return cli

@app.post("/movimentacoes", response_model=schemas.Movimentacao)
def registrar_movimentacao(mov: schemas.MovimentacaoCreate, db: Session = Depends(get_db)):
    db_mov = Movimentacao(**mov.dict())
    db.add(db_mov)
    db.commit()
    db.refresh(db_mov)
    return db_mov

@app.get("/movimentacoes", response_model=list[schemas.Movimentacao])
def listar_movimentacoes(db: Session = Depends(get_db)):
    return db.query(Movimentacao).all()

@app.get("/movimentacoes/{id}", response_model=schemas.Movimentacao)
def buscar_movimentacao(id: int, db: Session = Depends(get_db)):
    mov = db.query(Movimentacao).filter(Movimentacao.mov_id == id).first()
    if not mov:
        raise HTTPException(status_code=404, detail="Movimentação não encontrada")
    return mov
