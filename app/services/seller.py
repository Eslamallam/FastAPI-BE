from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.database.models import Seller

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_seller(self, credentials: Seller):
        seller = Seller(
            **credentials.model_dump(exclude=["password"]),
            password_hash=password_context.hash(credentials.password),
        )

        self.session.add(seller)
        await self.session.commit()
        await self.session.refresh(seller)
        return seller
