from pydantic import BaseModel
from datetime import datetime

class PostReceive(BaseModel):
    valor: float
    recebido: bool
    fixo: bool
    data: datetime
    categoria: str
    descricao: str

class PostExpense(BaseModel):
    valor: float
    recebido: bool
    fixo: bool
    data: datetime
    categoria: str
    descricao: str
