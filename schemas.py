from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class CategoriaBase(BaseModel):
    cat_nome: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    cat_id: int
    class Config:
        orm_mode = True

class ProdutoBase(BaseModel):
    pro_nome: str
    pro_descricao: Optional[str] = None
    pro_custo: Decimal
    pro_preco: Decimal
    pro_quantidade: int
    pro_status: Optional[str] = "disponível"
    pro_marca: Optional[str] = None
    pro_cat_id: Optional[int] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(ProdutoBase):
    pass

class Produto(ProdutoBase):
    pro_id: int
    pro_data_cadastro: datetime
    categoria: Optional[Categoria] = None
    class Config:
        orm_mode = True

class FornecedorBase(BaseModel):
    for_nome: str
    for_cnpj: Optional[str] = None
    for_contato: Optional[str] = None

class FornecedorCreate(FornecedorBase):
    pass

class Fornecedor(FornecedorBase):
    for_id: int
    class Config:
        orm_mode = True

class ClienteBase(BaseModel):
    cli_cpf: str
    cli_nome: str

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    cli_id: int
    class Config:
        orm_mode = True

class MovimentacaoBase(BaseModel):
    mov_pro_id: int
    mov_cli_id: Optional[int] = None
    mov_motivo: str
    mov_quantidade: int

class MovimentacaoCreate(MovimentacaoBase):
    pass

class Movimentacao(MovimentacaoBase):
    mov_id: int
    mov_data: datetime
    class Config:
        orm_mode = True
