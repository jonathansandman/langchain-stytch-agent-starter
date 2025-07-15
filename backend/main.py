from app_factory import create_app
from api.routes import router as api_router

app = create_app()
app.include_router(api_router)
