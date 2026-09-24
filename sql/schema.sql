CREATE TABLE IF NOT EXISTS restaurant_sales (
    transaction_id INTEGER PRIMARY KEY,

    customer_name VARCHAR(100) NOT NULL,

    restaurant VARCHAR(100) NOT NULL,

    category VARCHAR(50) NOT NULL,

    country VARCHAR(50) NOT NULL,

    quantity INTEGER NOT NULL
        CHECK (quantity > 0),

    unit_price NUMERIC(10,2) NOT NULL
        CHECK (unit_price > 0),

    rating NUMERIC(2,1)
        CHECK (rating >= 1 AND rating <= 5),

    transaction_date DATE NOT NULL
);