import asyncio
from redis.asyncio import Redis
from sqlalchemy import text

from vectorflow.core.config import get_settings
from vectorflow.db.session import engine, get_db_session

async def test_connection():
    settings = get_settings()
    print(f"Checking configuration for project: {settings.PROJECT_NAME}")
    print(f"Connecting to Postgres at: {settings.POSTGRES_SERVER}")

    async for session in get_db_session():
        result = await session.execute(
            text("SELECT extname FROM pg_extension WHERE extname = 'vector';")
        )
        ext = result.scalar()
        if ext == "vector":
            print("[SUCCESS] Connecnted to PostgresSQL. 'vector' extension is active")
        else:
            print("[WARNING] Connected to PostgresSQL, but 'vactor extension was not found")
        break

    print(f"Connecting to Redis at {settings.REDIS_HOST}")
    redis = Redis.from_url(settings.REDIS_URL)
    pong = await redis.ping()
    if pong:
        print("[SUCCESS] Conncted to Redis. PONG received!")
    await redis.aclose()

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(test_connection())