from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas.sku import SKU


router = APIRouter(
    prefix="/sku",
    tags=["sku"],
)


@router.get("/{sku_code}", response_model=SKU)
def get_sku(sku_code: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    sku_code,
                    description,
                    default_unit_price,
                    currency,
                    active
                FROM erp.sku_master
                WHERE sku_code = %s
                """,
                (sku_code,),
            )

            sku = cursor.fetchone()

    if sku is None:
        raise HTTPException(
            status_code=404,
            detail=f"SKU '{sku_code}' not found",
        )

    return sku