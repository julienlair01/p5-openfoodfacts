DROP TABLE IF EXISTS Product_has_category, Product_has_substitute, User_favorite_product, Category, Store, Product_has_store, Country, Product_has_country, Brand, Product_has_brand, Product;

CREATE TABLE Product (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    barcode VARCHAR(13) NOT NULL,
    name_fr VARCHAR(100) NOT NULL,
    generic_name VARCHAR(100),
    nutrition_grade_fr CHAR,
    off_url VARCHAR(200),
    PRIMARY KEY (id),
    UNIQUE KEY barcode (barcode)
)
ENGINE=InnoDB;


CREATE TABLE Category (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    off_id VARCHAR(250) NOT NULL,
    name VARCHAR(250),
    PRIMARY KEY (id),
    UNIQUE KEY off_id (off_id)
)
ENGINE=InnoDB;


CREATE TABLE Product_has_category (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_id INT UNSIGNED NOT NULL,
    category_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY product_category (product_id, category_id),
    CONSTRAINT fk_product_cat_id
        FOREIGN KEY (product_id)
        REFERENCES Product(id),
    CONSTRAINT fk_category_prod_id
        FOREIGN KEY (category_id)
        REFERENCES Category(id)
)
ENGINE=InnoDB;


CREATE TABLE Brand (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(45),
    PRIMARY KEY (id),
    UNIQUE KEY brand (name)
)
ENGINE=InnoDB;


CREATE TABLE Product_has_brand (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_id INT UNSIGNED NOT NULL,
    brand_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY product_category (product_id, brand_id),
    CONSTRAINT fk_brand_product
        FOREIGN KEY (product_id)
        REFERENCES Product(id),
    CONSTRAINT fk_brand_brand
        FOREIGN KEY (brand_id)
        REFERENCES Brand(id)
)
ENGINE=InnoDB;


CREATE TABLE Country (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(45),
    PRIMARY KEY (id),
    UNIQUE KEY country (name)
)
ENGINE=InnoDB;


CREATE TABLE Product_has_country (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_id INT UNSIGNED NOT NULL,
    country_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY product_country (product_id, country_id),
    CONSTRAINT fk_product_country
        FOREIGN KEY (product_id)
        REFERENCES Product(id),
    CONSTRAINT fk_country_country
        FOREIGN KEY (country_id)
        REFERENCES Country(id)
)
ENGINE=InnoDB;


CREATE TABLE Store (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(45),
    city VARCHAR(45),
    country_id INT UNSIGNED,
    PRIMARY KEY (id),
    UNIQUE KEY store (city, name),
    CONSTRAINT fk_store_country
        FOREIGN KEY (country_id)
        REFERENCES Country(id)
)
ENGINE=InnoDB;


CREATE TABLE Product_has_store (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_id INT UNSIGNED NOT NULL,
    store_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY product_store (product_id, store_id),
    CONSTRAINT fk_product_store
        FOREIGN KEY (product_id)
        REFERENCES Product(id),
    CONSTRAINT fk_store_store
        FOREIGN KEY (store_id)
        REFERENCES Store(id)
)
ENGINE=InnoDB;


CREATE TABLE User_favorite_product (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY product_id (product_id),
    CONSTRAINT fk_favorite_product_id
        FOREIGN KEY (product_id)
        REFERENCES Product(id)
)
ENGINE=InnoDB;


CREATE TABLE Product_has_substitute (
    id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    product_id INT UNSIGNED NOT NULL,
    substitute_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY product_substitute (product_id, substitute_id),
    CONSTRAINT fk_product_id
        FOREIGN KEY (product_id)
        REFERENCES Product(id),
    CONSTRAINT fk_substitute_id
        FOREIGN KEY (substitute_id)
        REFERENCES Product(id)
)
ENGINE=InnoDB;
