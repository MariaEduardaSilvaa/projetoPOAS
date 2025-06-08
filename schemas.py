from pydantic import BaseModel
from typing import Optional, Literal
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
    pro_custo: float
    pro_preco: float
    pro_quantidade: int
    pro_status: Optional[Literal["disponível", "indisponível"]] = "disponível"
    pro_marca: Optional[str] = None
    pro_cat_id: Optional[int] = None

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoUpdate(BaseModel):
    pro_nome: Optional[str] = None
    pro_descricao: Optional[str] = None
    pro_custo: Optional[float] = None
    pro_preco: Optional[float] = None
    pro_quantidade: Optional[int] = None
    pro_status: Optional[Literal["disponível", "indisponível"]] = None
    pro_marca: Optional[str] = None
    pro_cat_id: Optional[int] = None

class Produto(ProdutoBase):
    pro_id: int
    pro_data_cadastro: datetime
    categoria: Optional[Categoria] = None  # Relacionamento com categoria
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

class ClienteBase(BaseModel):
    cli_nome: str
    cli_cpf: Optional[str] = None

class ClienteCreate(ClienteBase):
    pass

class Cliente(ClienteBase):
    cli_id: int
    class Config:
        from_attributes = True

class MovimentacaoBase(BaseModel):
    mov_pro_id: int
    mov_cli_id: Optional[int] = None
    mov_motivo: str
    mov_quantidade: int
    mov_tipo: Literal["entrada", "saida"]

class MovimentacaoCreate(MovimentacaoBase):
    pass

class Movimentacao(MovimentacaoBase):
    mov_id: int
    mov_data: datetime
    class Config:
        from_attributes = True