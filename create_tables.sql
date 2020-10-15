CREATE TABLE IF NOT EXISTS Product (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    barcode VARCHAR(13) NOT NULL,
    name_fr VARCHAR(100) NOT NULL,
    nutrition_grade_fr CHAR,
    url VARCHAR(200),
    PRIMARY KEY (id),
    UNIQUE KEY barcode (barcode)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Category (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    off_id VARCHAR(250) NOT NULL,
    name VARCHAR(250),
    PRIMARY KEY (id),
    UNIQUE KEY off_id (off_id)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Brand (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    off_id VARCHAR(250) NOT NULL,
    name VARCHAR(250),
    PRIMARY KEY (id),
    UNIQUE KEY off_id (off_id)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Product_category (
    product_id INT UNSIGNED NOT NULL,
    category_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (product_id, category_id),
    UNIQUE KEY product_category (product_id, category_id),
    CONSTRAINT fk_product_cat_id
        FOREIGN KEY (product_id)
        REFERENCES Product(id),
    CONSTRAINT fk_category_prod_id
        FOREIGN KEY (category_id)
        REFERENCES Category(id)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Product_brand (
    product_id INT UNSIGNED NOT NULL,
    brand_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (product_id, brand_id),
    UNIQUE KEY product_brand (product_id, brand_id),
    CONSTRAINT fk_product_brand_id
        FOREIGN KEY (product_id)
        REFERENCES Product(id),
    CONSTRAINT fk_brand_prod_id
        FOREIGN KEY (brand_id)
        REFERENCES Brand(id)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS User_favorite_product (
    product_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (product_id),
    UNIQUE KEY product_id (product_id),
    CONSTRAINT fk_favorite_product_id
        FOREIGN KEY (product_id)
        REFERENCES Product(id)
)
ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS Product_substitute (
    product_id INT UNSIGNED NOT NULL,
    substitute_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (product_id, substitute_id),
    UNIQUE KEY product_substitute (product_id, substitute_id),
    CONSTRAINT fk_product_id
        FOREIGN KEY (product_id)
        REFERENCES Product(id),
    CONSTRAINT fk_substitute_id
        FOREIGN KEY (substitute_id)
        REFERENCES Product(id)
)
ENGINE=InnoDB;