CREATE TABLE IF NOT EXISTS customers (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  industry TEXT NOT NULL,
  annual_value NUMERIC(12,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS sales (
  id SERIAL PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  amount NUMERIC(12,2) NOT NULL,
  sale_date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS support_tickets (
  id SERIAL PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  priority TEXT NOT NULL CHECK (priority IN ('low','medium','high')),
  status TEXT NOT NULL CHECK (status IN ('open','pending','closed')),
  created_at DATE NOT NULL
);

INSERT INTO customers (name, industry, annual_value) VALUES
('Nova Retail', 'Retail', 1800000),
('Vertex Health', 'Healthcare', 2400000),
('Orbit Logistics', 'Logistics', 950000),
('BluePeak Finance', 'Finance', 3200000),
('GreenGrid Energy', 'Energy', 1500000)
ON CONFLICT DO NOTHING;

INSERT INTO sales (customer_id, amount, sale_date)
SELECT id, amount, sale_date FROM (VALUES
((SELECT id FROM customers WHERE name='Nova Retail'), 420000, CURRENT_DATE-20),
((SELECT id FROM customers WHERE name='Nova Retail'), 180000, CURRENT_DATE-65),
((SELECT id FROM customers WHERE name='Vertex Health'), 600000, CURRENT_DATE-15),
((SELECT id FROM customers WHERE name='Vertex Health'), 510000, CURRENT_DATE-80),
((SELECT id FROM customers WHERE name='Orbit Logistics'), 120000, CURRENT_DATE-30),
((SELECT id FROM customers WHERE name='BluePeak Finance'), 800000, CURRENT_DATE-10),
((SELECT id FROM customers WHERE name='BluePeak Finance'), 720000, CURRENT_DATE-70),
((SELECT id FROM customers WHERE name='GreenGrid Energy'), 250000, CURRENT_DATE-25)
) AS x(customer_id, amount, sale_date)
WHERE NOT EXISTS (SELECT 1 FROM sales);

INSERT INTO support_tickets (customer_id, priority, status, created_at)
SELECT id, priority, status, CURRENT_DATE-days FROM (VALUES
((SELECT id FROM customers WHERE name='Nova Retail'),'high','open',8),
((SELECT id FROM customers WHERE name='Nova Retail'),'medium','pending',14),
((SELECT id FROM customers WHERE name='Vertex Health'),'low','closed',30),
((SELECT id FROM customers WHERE name='Orbit Logistics'),'high','open',5),
((SELECT id FROM customers WHERE name='BluePeak Finance'),'medium','pending',12)
) AS x(customer_id, priority, status, days)
WHERE NOT EXISTS (SELECT 1 FROM support_tickets);
