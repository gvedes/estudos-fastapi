from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from dependencies import pegar_sessao
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario: int):
    token = f"sdSAAKDHFEUWEYcubvdsbsudife32{id_usuario}"
    return token



@auth_router.post("/")
async def home():
    """
    Essa é a rota de autenticação, onde você pode fazer login no sistema.
    """
    
    
    return {"message": "Você está na rota de autenticação!", "autenticado": False}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado!")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(nome=usuario_schema.nome, email=usuario_schema.email, senha=senha_criptografada, ativo=usuario_schema.ativo or False, admin=usuario_schema.admin or False)
        session.add(novo_usuario)
        session.commit()
        return {"message": f"Conta criada com sucesso {usuario_schema.nome}!"}
    
    
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")
    else:
        acess_token = criar_token(usuario.id)
        return {
            "acess_token": acess_token,
            "token_type": "bearer",
            
        }