from pydantic import BaseModel

class Vendor(BaseModel):
    vendor_id: str
    vendor_name: str
    currency: str | None = None
    country: str | None = None
    active: bool = True
