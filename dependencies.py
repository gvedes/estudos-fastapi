from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from models import db, Usuario
from jose import JWTError, jwt
from main import SECRET_KEY, ALGORITHM


def pegar_sessao():
    
    try:    
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    
    finally:
        session.close()
        
        
def verificar_token(token: str, session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido! Verifique a validade do token e tente novamente.")
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado!")
    return usuario