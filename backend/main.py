from fastapi import FastAPI
from routers import user, company, brands, product, product_image, product_attachments
from middleware.verify_token import jwt_middleware
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(jwt_middleware)
app.include_router(user.router)
app.include_router(company.router)
app.include_router(brands.router)
app.include_router(product.router)
app.include_router(product_image.router)
app.include_router(product_attachments.router)
