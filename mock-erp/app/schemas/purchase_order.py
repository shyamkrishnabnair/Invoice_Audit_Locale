from pydantic import BaseModel


class POLineItem(BaseModel):
    line_number: int
    sku_code: str
    description: str | None = None
    quantity: float
    unit_price: float
    line_total: float | None = None


class PurchaseOrder(BaseModel):
    po_number: str
    vendor_id: str
    currency: str
    order_date: str | None = None
    line_items: list[POLineItem]