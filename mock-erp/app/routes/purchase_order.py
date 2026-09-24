from fastapi import APIRouter, HTTPException

from app.database import get_connection
from app.schemas.purchase_order import PurchaseOrder

router = APIRouter(
    prefix="/po",
    tags=["purchase-orders"],
)


@router.get("/{po_number}", response_model=PurchaseOrder)
def get_purchase_order(po_number: str):
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    po_number,
                    vendor_id,
                    currency,
                    order_date
                FROM erp.purchase_orders
                WHERE po_number = %s
                """,
                (po_number,),
            )

            po = cursor.fetchone()

            if po is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"Purchase order '{po_number}' not found",
                )

            cursor.execute(
                """
                SELECT
                    line_number,
                    sku_code,
                    description,
                    quantity,
                    unit_price,
                    line_total
                FROM erp.po_line_items
                WHERE po_number = %s
                ORDER BY line_number
                """,
                (po_number,),
            )

            line_items = cursor.fetchall()

    return {
        **po,
        "order_date": (
            po["order_date"].isoformat()
            if po["order_date"]
            else None
        ),
        "line_items": line_items,
    }