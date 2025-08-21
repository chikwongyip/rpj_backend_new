from fastapi import FastAPI
from routers import user, company, brands, product, product_image, product_attachments

app = FastAPI()
app.include_router(user.router)
app.include_router(company.router)
app.include_router(brands.router)
app.include_router(product.router)
app.include_router(product_image.router)
app.include_router(product_attachments.router)
