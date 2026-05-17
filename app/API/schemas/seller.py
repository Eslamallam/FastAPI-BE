from pydantic import BaseModel, EmailStr


class SellerBase(BaseModel):
    name: str
    email: EmailStr

class SellerRead(BaseModel):
   pass

class SellerCreate(BaseModel):
    password: str
