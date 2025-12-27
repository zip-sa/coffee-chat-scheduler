from fastapi import FastAPI
from appserver.apps.account.endpoints import router as account_router

app = FastAPI()

def include_routers(_app: FastAPI):
    _app.include_router(account_router)


include_routers(app)