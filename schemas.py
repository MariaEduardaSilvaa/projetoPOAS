from pydantic import BaseModel
from typing import Optional, Literal
from decimal import Decimal
from datetime import datetime

class CategoriaBase(BaseModel):
    cat_nome: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    cat_id: int
    class Config:
        from_attributes = True

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
        from_attributes = True

class FornecedorBase(BaseModel):
    for_nome: str
    for_cnpj: Optional[str] = None
    for_contato: Optional[str] = None

class FornecedorCreate(FornecedorBase):
    pass

class Fornecedor(FornecedorBase):
    for_id: int
    class Config:
        from_attributes = True

class MovimentacaoBase(BaseModel):
    mov_pro_id: int
    mov_cli_id: Optional[int] = None
    mov_motivo: Optional[str] = None
    mov_quantidade: int
    mov_tipo: Literal["entrada", "saida"]

class MovimentacaoCreate(MovimentacaoBase):
    pass

class Movimentacao(MovimentacaoBase):
    mov_id: int
    mov_data: datetime

    class Config:
        from_attributes = True