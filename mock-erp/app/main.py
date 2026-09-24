from fastapi import FastAPI

from app.routes.vendor import router as vendor_router
from app.routes.purchase_order import router as po_router
from app.routes.sku import router as sku_router

app = FastAPI(
    title = "mock-erp",
)

@app.get("/health")
def get_health():
    return{
        "status" : "healthy",
        "service" : "mock-erp"
    }

app.include_router(vendor_router)
app.include_router(po_router)
app.include_router(sku_router)