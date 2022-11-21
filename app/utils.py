from passlib.context import CryptContext # For hashing passwprds


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto') # to hashing passwords

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):        # >>>>>>>>>> Take password from payload and verify that it is match up with hashed password from DB
    return pwd_context.verify(plain_password, hashed_password)