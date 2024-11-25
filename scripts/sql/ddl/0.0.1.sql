CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    urn TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    description TEXT,
    sku TEXT,
    product_id TEXT,
    regular_price REAL,
    sale_price REAL,
    discount REAL,
    in_stock BOOLEAN NOT NULL DEFAULT TRUE,
    main_image_url TEXT,
    all_image_urls JSON,
    starting_price REAL
);