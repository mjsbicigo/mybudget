from pydantic import BaseModel

class GetCategories(BaseModel):
    tipo_categoria: str
    
class PostCategory(BaseModel):
    nome_categoria: str
    tipo_categoria: str

class DeleteCategory(BaseModel):
    nome_categoria: str
    tipo_categoria: str