-- =========================================================
-- Audit Schema
-- =========================================================

CREATE SCHEMA IF NOT EXISTS audit;


-- =========================================================
-- Invoice Audit
-- =========================================================

CREATE TABLE IF NOT EXISTS audit.invoice_audit (
    invoice_id UUID PRIMARY KEY,

    file_path VARCHAR(512) NOT NULL,
    file_checksum VARCHAR(64) NOT NULL UNIQUE,

    extraction_method VARCHAR(32),

    raw_extracted_text TEXT,
    translated_text TEXT,

    source_language VARCHAR(8),
    translation_confidence NUMERIC(4,3),

    invoice_number VARCHAR(64),
    vendor_name VARCHAR(255),
    po_number VARCHAR(64),

    invoice_date DATE,
    currency CHAR(3),

    total_amount NUMERIC(14,2),

    validation_status VARCHAR(32),
    recommendation VARCHAR(32),

    extracted_raw JSONB,

    thread_id VARCHAR(128),

    processed_at TIMESTAMPTZ DEFAULT now(),

    CONSTRAINT chk_validation_status
        CHECK (
            validation_status IS NULL
            OR validation_status IN ('passed', 'failed', 'partial')
        ),

    CONSTRAINT chk_recommendation
        CHECK (
            recommendation IS NULL
            OR recommendation IN ('approve', 'review', 'reject')
        )
);


-- =========================================================
-- Invoice Line Items
-- =========================================================

CREATE TABLE IF NOT EXISTS audit.invoice_line_items (
    id BIGSERIAL PRIMARY KEY,

    invoice_id UUID NOT NULL,

    line_number INTEGER NOT NULL,

    item_code VARCHAR(64),
    description TEXT,

    quantity NUMERIC(12,3),
    unit_price NUMERIC(14,4),
    line_total NUMERIC(14,2),

    CONSTRAINT fk_invoice_line_invoice
        FOREIGN KEY (invoice_id)
        REFERENCES audit.invoice_audit(invoice_id),

    CONSTRAINT uq_invoice_line
        UNIQUE (invoice_id, line_number)
);


-- =========================================================
-- Discrepancies
-- =========================================================

CREATE TABLE IF NOT EXISTS audit.discrepancies (
    id BIGSERIAL PRIMARY KEY,

    invoice_id UUID NOT NULL,

    field_name VARCHAR(64) NOT NULL,

    invoice_value TEXT,
    erp_value TEXT,

    deviation_pct NUMERIC(8,4),

    severity VARCHAR(16),

    detected_at TIMESTAMPTZ DEFAULT now(),

    CONSTRAINT fk_discrepancy_invoice
        FOREIGN KEY (invoice_id)
        REFERENCES audit.invoice_audit(invoice_id)
);


-- =========================================================
-- Human Feedback
-- =========================================================

CREATE TABLE IF NOT EXISTS audit.human_feedback (
    id BIGSERIAL PRIMARY KEY,

    invoice_id UUID NOT NULL,

    field_name VARCHAR(64) NOT NULL,

    original_value TEXT,
    corrected_value TEXT,

    corrected_by VARCHAR(128),

    corrected_at TIMESTAMPTZ DEFAULT now(),

    revalidated BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_feedback_invoice
        FOREIGN KEY (invoice_id)
        REFERENCES audit.invoice_audit(invoice_id)
);


-- =========================================================
-- Indexes
-- =========================================================

CREATE INDEX IF NOT EXISTS idx_invoice_vendor
    ON audit.invoice_audit(vendor_name);

CREATE INDEX IF NOT EXISTS idx_invoice_po
    ON audit.invoice_audit(po_number);

CREATE INDEX IF NOT EXISTS idx_invoice_status
    ON audit.invoice_audit(validation_status);

CREATE INDEX IF NOT EXISTS idx_invoice_recommendation
    ON audit.invoice_audit(recommendation);

CREATE INDEX IF NOT EXISTS idx_invoice_processed_at
    ON audit.invoice_audit(processed_at);

CREATE INDEX IF NOT EXISTS idx_discrepancy_invoice
    ON audit.discrepancies(invoice_id);

CREATE INDEX IF NOT EXISTS idx_feedback_invoice
    ON audit.human_feedback(invoice_id);