CREATE SCHEMA IF NOT EXISTS erp;


-- =========================================================
-- Vendors
-- =========================================================

CREATE TABLE IF NOT EXISTS erp.vendors (
    vendor_id VARCHAR(64) PRIMARY KEY,
    vendor_name VARCHAR(255) NOT NULL,
    currency CHAR(3),
    country VARCHAR(100),
    active BOOLEAN DEFAULT TRUE
);


-- =========================================================
-- SKU Master
-- =========================================================

CREATE TABLE IF NOT EXISTS erp.sku_master (
    sku_code VARCHAR(64) PRIMARY KEY,
    description TEXT,
    default_unit_price NUMERIC(14, 4),
    currency CHAR(3),
    active BOOLEAN DEFAULT TRUE
);


-- =========================================================
-- Purchase Orders
-- =========================================================

CREATE TABLE IF NOT EXISTS erp.purchase_orders (
    po_number VARCHAR(64) PRIMARY KEY,
    vendor_id VARCHAR(64) NOT NULL,
    currency CHAR(3) NOT NULL,
    order_date DATE,

    CONSTRAINT fk_po_vendor
        FOREIGN KEY (vendor_id)
        REFERENCES erp.vendors(vendor_id)
);


-- =========================================================
-- Purchase Order Line Items
-- =========================================================

CREATE TABLE IF NOT EXISTS erp.po_line_items (
    id BIGSERIAL PRIMARY KEY,

    po_number VARCHAR(64) NOT NULL,
    line_number INTEGER NOT NULL,

    sku_code VARCHAR(64) NOT NULL,
    description TEXT,

    quantity NUMERIC(12, 3) NOT NULL,
    unit_price NUMERIC(14, 4) NOT NULL,
    line_total NUMERIC(14, 2),

    CONSTRAINT fk_po_line_po
        FOREIGN KEY (po_number)
        REFERENCES erp.purchase_orders(po_number),

    CONSTRAINT fk_po_line_sku
        FOREIGN KEY (sku_code)
        REFERENCES erp.sku_master(sku_code),

    CONSTRAINT uq_po_line
        UNIQUE (po_number, line_number)
);


-- =========================================================
-- Indexes
-- =========================================================

CREATE INDEX IF NOT EXISTS idx_purchase_orders_vendor
    ON erp.purchase_orders(vendor_id);

CREATE INDEX IF NOT EXISTS idx_po_line_items_po
    ON erp.po_line_items(po_number);

CREATE INDEX IF NOT EXISTS idx_po_line_items_sku
    ON erp.po_line_items(sku_code);


-- =========================================================
-- Development Seed Data
-- =========================================================

INSERT INTO erp.vendors (
    vendor_id,
    vendor_name,
    currency,
    country
)
VALUES
    ('V001', 'Acme Logistics Supplies', 'USD', 'United States'),
    ('V002', 'Global Industrial GmbH', 'EUR', 'Germany'),
    ('V003', 'Iberia Components SL', 'EUR', 'Spain')
ON CONFLICT (vendor_id) DO NOTHING;


INSERT INTO erp.sku_master (
    sku_code,
    description,
    default_unit_price,
    currency
)
VALUES
    ('SKU001', 'Industrial Safety Gloves', 25.00, 'USD'),
    ('SKU002', 'Protective Helmet', 40.00, 'USD'),
    ('SKU003', 'Safety Boots', 75.00, 'USD'),
    ('SKU101', 'Hydraulic Filter', 32.50, 'EUR'),
    ('SKU102', 'Pressure Valve', 85.00, 'EUR')
ON CONFLICT (sku_code) DO NOTHING;


INSERT INTO erp.purchase_orders (
    po_number,
    vendor_id,
    currency,
    order_date
)
VALUES
    ('PO1001', 'V001', 'USD', '2026-09-01'),
    ('PO2001', 'V002', 'EUR', '2026-09-05'),
    ('PO3001', 'V003', 'EUR', '2026-09-10')
ON CONFLICT (po_number) DO NOTHING;


INSERT INTO erp.po_line_items (
    po_number,
    line_number,
    sku_code,
    description,
    quantity,
    unit_price,
    line_total
)
VALUES
    ('PO1001', 1, 'SKU001', 'Industrial Safety Gloves', 10, 25.00, 250.00),
    ('PO1001', 2, 'SKU002', 'Protective Helmet', 5, 40.00, 200.00),
    ('PO1001', 3, 'SKU003', 'Safety Boots', 2, 75.00, 150.00),

    ('PO2001', 1, 'SKU101', 'Hydraulic Filter', 20, 32.50, 650.00),
    ('PO2001', 2, 'SKU102', 'Pressure Valve', 4, 85.00, 340.00),

    ('PO3001', 1, 'SKU101', 'Hydraulic Filter', 10, 32.50, 325.00)
ON CONFLICT (po_number, line_number) DO NOTHING;