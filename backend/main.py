from fastapi import FastAPI
from routers import user, company, brands

app = FastAPI()
app.include_router(user.router)
app.include_router(company.router)
app.include_router(brands.router)
