from fastapi import APIRouter, Depends, HTTPException
from models import Usuario, db
from dependencies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario: int, duracao_token: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    data_expiracao = datetime.now(timezone.utc) + timedelta(minutes=int(duracao_token))
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado


def autenticar_usuario(email: str, senha: str, session: Session) -> Optional[Usuario]:
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario:
        return None
    if not bcrypt_context.verify(senha, usuario.senha):
        return None
    return usuario


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
    
    
@auth_router.post( "/login" )
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado ou credenciais inválidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }

@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "bearer",  
        }


@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return {
            "acess_token": access_token,
            "token_type": "bearer",
        }
