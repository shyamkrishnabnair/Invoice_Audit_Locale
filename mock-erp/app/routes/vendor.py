from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas.vendor import Vendor

router = APIRouter(
    prefix = "/vendor",
    tags = ["vendors"]
)

@router.get("/{vendor_id}", response_model = Vendor)
def get_vendor(vendor_id: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 
                    vendor_id,
                    vendor_name,
                    currency,
                    country,
                    active
                FROM erp.vendors
                WHERE vendor_id = %s
                """,
                (vendor_id,)
            )
            vendor = cursor.fetchone()

    if vendor is None:
        raise HTTPException(
            status_code = 404,
            detail = f"Vendor {vendor_id} not found!"
        )

    return vendor