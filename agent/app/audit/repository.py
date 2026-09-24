import os
import uuid

import psycopg


def get_connection():
    return psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
    )


def checksum_exists(file_checksum: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT 1
                FROM audit.invoice_audit
                WHERE file_checksum = %s
                LIMIT 1
                """,
                (file_checksum,),
            )

            return cursor.fetchone() is not None


def create_invoice_record(file_path: str, file_checksum: str, ) -> str:
    invoice_id = str(uuid.uuid4())

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO audit.invoice_audit (
                    invoice_id,
                    file_path,
                    file_checksum,
                    validation_status
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    invoice_id,
                    file_path,
                    file_checksum,
                    "partial",
                ),
            )

        conn.commit()

    return invoice_id