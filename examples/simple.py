from fastapi import APIRouter, FastAPI
from pydantic import BaseSettings, RedisDsn

from fastapi_components.components import AIOHTTPSessionComponent, AIORedisComponent
from fastapi_components.state_manager import FastAPIStateManager

router = APIRouter()


@router.get("/redis_set")
async def redis_set(key: str, value: str, request):
    await request.app.state.redis.set(key, value)

    return "OK"


@router.post("/send_http")
async def send_http(request):
    async with request.app.state.session.get("http://wikipredia.org") as r:
        return await r.text()


class Settings(BaseSettings):
    redis_dsn: RedisDsn


def create_app() -> FastAPI:

    settings = Settings()

    state_manager = FastAPIStateManager(
        components=[
            AIORedisComponent(),
            AIOHTTPSessionComponent(),
        ],
        settings=settings,
    )

    app = FastAPI()
    app.include_router(router)

    state_manager.set_startup_hook(app)
    state_manager.set_shutdown_hook(app)

    return app
