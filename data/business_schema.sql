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
  subject TEXT NOT NULL,
  created_at DATE NOT NULL
);
