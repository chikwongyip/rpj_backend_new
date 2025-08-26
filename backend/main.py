from fastapi import FastAPI
from routers import user, company, brands, product, product_image, product_attachments
from middleware.verify_token import jwt_middleware
app = FastAPI()
app.middleware("http")(jwt_middleware)
app.include_router(user.router)
app.include_router(company.router)
app.include_router(brands.router)
app.include_router(product.router)
app.include_router(product_image.router)
app.include_router(product_attachments.router)
