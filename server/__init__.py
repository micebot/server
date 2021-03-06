from fastapi import FastAPI

from server.env import env
from server.routes.auth import router as auth
from server.routes.heartbeat import router as heartbeat
from server.routes.orders import router as orders
from server.routes.products import router as products

app = FastAPI(
    title="MiceBot",
    version=env.VERSION,
    description="The MiceBot core.",
    debug=not env.PRODUCTION,
    docs_url="/docs" if not env.PRODUCTION else None,
    redoc_url="/redoc" if not env.PRODUCTION else None,
)
app.include_router(auth, prefix="/auth", tags=["authentication"])
app.include_router(products, prefix="/products", tags=["products"])
app.include_router(orders, prefix="/orders", tags=["orders"])
app.include_router(heartbeat, prefix="/hb", tags=["heartbeat"])
