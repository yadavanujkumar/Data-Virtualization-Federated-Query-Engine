-- Create schema for customer data
CREATE SCHEMA IF NOT EXISTS customers;

-- Create customer table
CREATE TABLE customers.customer (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create order_summary table (simulating S3/external data source)
CREATE TABLE customers.order_summary (
    id SERIAL PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    total_orders INTEGER NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    last_order_date DATE
);

-- Insert dummy customer data
INSERT INTO customers.customer (customer_id, first_name, last_name, email) VALUES
('CUST001', 'John', 'Doe', 'john.doe@example.com'),
('CUST002', 'Jane', 'Smith', 'jane.smith@example.com'),
('CUST003', 'Robert', 'Johnson', 'robert.johnson@example.com'),
('CUST004', 'Emily', 'Williams', 'emily.williams@example.com'),
('CUST005', 'Michael', 'Brown', 'michael.brown@example.com'),
('CUST006', 'Sarah', 'Davis', 'sarah.davis@example.com'),
('CUST007', 'David', 'Miller', 'david.miller@example.com'),
('CUST008', 'Lisa', 'Wilson', 'lisa.wilson@example.com'),
('CUST009', 'James', 'Moore', 'james.moore@example.com'),
('CUST010', 'Jennifer', 'Taylor', 'jennifer.taylor@example.com');

-- Insert dummy order summary data
INSERT INTO customers.order_summary (customer_id, total_orders, total_amount, last_order_date) VALUES
('CUST001', 15, 1250.50, '2024-01-15'),
('CUST002', 8, 890.25, '2024-01-10'),
('CUST003', 22, 3100.00, '2024-01-18'),
('CUST004', 5, 425.75, '2024-01-05'),
('CUST005', 12, 1875.30, '2024-01-12'),
('CUST006', 18, 2200.00, '2024-01-20'),
('CUST007', 3, 150.00, '2023-12-28'),
('CUST008', 9, 980.50, '2024-01-08'),
('CUST009', 25, 4500.25, '2024-01-22'),
('CUST010', 7, 650.00, '2024-01-03');
