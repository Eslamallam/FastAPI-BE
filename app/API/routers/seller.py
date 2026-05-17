from fastapi import APIRouter
from ..schemas.seller import SellerCreate

router = APIRouter(prefix="/api/v1/seller", tags=["Seller"])

@router.post("/signup")
def signup(seller: SellerCreate):
    pass