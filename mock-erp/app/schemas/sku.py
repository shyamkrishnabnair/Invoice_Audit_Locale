from pydantic import BaseModel


class SKU(BaseModel):
    sku_code: str
    description: str | None = None
    default_unit_price: float | None = None
    currency: str | None = None
    active: bool = True