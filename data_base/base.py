from .database import async_session, engine, Base


def connection(func):
    async def wrapper(*args, **kwargs):
        async with async_session() as session:  # Открывает асинхронную сессию с базой данных
            #  Передает открытую сессию в оборачиваемую функцию, чтобы она могла использовать её для выполнения запросо
            return await func(session, *args, **kwargs)

    return wrapper


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)





