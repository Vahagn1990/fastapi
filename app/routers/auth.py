from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm # instead of get email get username, we should pass credential in BODY-> form-data 
                                                              # username = , password = 


router = APIRouter(tags=['authentication'])

@router.post('/login', response_model=schemas.Token)                      # >>>>> 
def login(user_credentials: OAuth2PasswordRequestForm = Depends() ,db: Session = Depends(get_db)):
# def login(user_credentials: schemas.UserLogin ,db: Session = Depends(get_db)): To pass email & password in body->raw->json

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    # user = db.query(models.User).filter(models.User.email == user_credentials.email).first() : To pass email & password in body->raw->json
    if not user: # Verify if that user is exists 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    if not utils.verify(user_credentials.password, user.password): # Take password from payload and verify that it is match up with hashed password from DB
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    access_token = oauth2.create_access_token(data={'user_id': user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}