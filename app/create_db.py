import asyncio
from app.database import engine, Base
from app.models import Place

# Create tables
async def init_db():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())
