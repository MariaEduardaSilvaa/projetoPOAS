from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models.models import Produto, Categoria, Fornecedor
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

@app.post("/products", response_model=schemas.Produto)
def create_product(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    db_prod = Produto(**produto.dict())
    db.add(db_prod)
    db.commit()
    db.refresh(db_prod)
    return db_prod

@app.get("/products", response_model=list[schemas.Produto])
def read_products(db: Session = Depends(get_db)):
    return db.query(Produto).all()

@app.get("/products/{id}", response_model=schemas.Produto)
def read_product(id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.pro_id == id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto

@app.put("/products/{id}", response_model=schemas.Produto)
def update_product(id: int, produto: schemas.ProdutoUpdate, db: Session = Depends(get_db)):
    db_prod = db.query(Produto).filter(Produto.pro_id == id).first()
    if not db_prod:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    for key, value in produto.dict().items():
        setattr(db_prod, key, value)
    db.commit()
    db.refresh(db_prod)
    return db_prod

@app.post("/categories", response_model=schemas.Categoria)
def create_category(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_cat = Categoria(**categoria.dict())
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

@app.get("/categories", response_model=list[schemas.Categoria])
def read_categories(db: Session = Depends(get_db)):
    return db.query(Categoria).all()

@app.post("/suppliers", response_model=schemas.Fornecedor)
def create_supplier(fornecedor: schemas.FornecedorCreate, db: Session = Depends(get_db)):
    db_forn = Fornecedor(**fornecedor.dict())
    db.add(db_forn)
    db.commit()
    db.refresh(db_forn)
    return db_forn

@app.get("/suppliers", response_model=list[schemas.Fornecedor])
def read_suppliers(db: Session = Depends(get_db)):
    return db.query(Fornecedor).all()
