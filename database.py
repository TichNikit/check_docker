from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine("postgresql+asyncpg://USERNAME:PASSWORD@HOST:PORT/DATABASE")
new_session = async_sessionmaker(engine, expire_on_commit=False)
#
class Base(DeclarativeBase):
    pass

class Film_historic(Base):
    __tablename__ = 'historic'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    year: Mapped[int | None]  # Новый столбец года
    rating: Mapped[float]

class Film_horror(Base):
    __tablename__ = 'horror'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    year: Mapped[int | None]  # Новый столбец года
    rating: Mapped[float]

class Film_thriller(Base):
    __tablename__ = 'thriller'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    year: Mapped[int | None]  # Новый столбец года
    rating: Mapped[float]


async def create_table():
    async with engine.begin() as conn:
        # Создание всех таблиц, определённых в моделях
        await conn.run_sync(Base.metadata.create_all)