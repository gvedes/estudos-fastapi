from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType


# cria a conexão com o banco de dados SQLite
db = create_engine("sqlite:///banco.db")

# cria a classe base para os modelos do SQLAlchemy
Base = declarative_base()


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column("id", Integer, nullable=False, primary_key=True,index=True, autoincrement=True)
    nome = Column("nome", String, nullable=False)
    email = Column("email", String, unique=True, index=True, nullable=False)
    senha = Column("senha", String, nullable=False)
    ativo = Column("ativo", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)
    
    def __init__(self, nome: str, email: str, senha: str, ativo: bool = True, admin: bool = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin
        
        
# Pedido

class Pedido(Base):
    __tablename__ = "pedidos"
    
    """
    STATUS_PEDIDOS = (
        ("PENDENTE", "Pendente"),
        ("EM_ANDAMENTO", "Em Andamento"),
        ("CONCLUIDO", "Concluído"),
        ("CANCELADO", "Cancelado")
    )
    """
    
    id = Column("id", Integer, nullable=False, primary_key=True,index=True, autoincrement=True)      
    status = Column("status", String, nullable=False) # pendente, em andamento, concluído, cancelado
    usuario = Column("usuario", Integer, ForeignKey("usuarios.id"), nullable=False)
    preco = Column("preco", Float, nullable=False)
    
    def __init__(self, usuario: int, status: str = "PENDENTE", preco: float = 0.0):
        self.usuario = usuario
        self.preco = preco
        self.status = status
        
        
# Itens do Pedido

class ItemPedido(Base):
    __tablename__ = "itens_pedido"
    
    id = Column("id", Integer, nullable=False, primary_key=True,index=True, autoincrement=True)      
    quantidade = Column("quantidade", Integer, nullable=False)
    sabor = Column("sabor", String, nullable=False)
    tamanho = Column("tamanho", String, nullable=False)
    preco_unitario = Column("preco_unitario", Float, nullable=False)
    pedidos = Column("pedidos", Integer, ForeignKey("pedidos.id"), nullable=False)
    
    def __init__(self, pedidos: int, sabor: str, tamanho: str, quantidade: int, preco_unitario: float):
        self.pedidos = pedidos
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario