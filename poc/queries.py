insert_brand = ("INSERT IGNORE INTO Brand (off_id, name) "
                    "VALUES (%(off_id)s, %(name)s)")

insert_category = ("INSERT IGNORE INTO Category (off_id, name) "
                    "VALUES (%(off_id)s, %(name)s)")

insert_country = ("INSERT INTO Country (name) "
                    "VALUES (%(name)s)")

insert_store = ("INSERT INTO Store (name, city, country_id) "
                    "VALUES ("
                        "%(name)s, " 
                        "%(city)s, "
                        "%(country_id)s"
                    ")")

insert_product = ("INSERT IGNORE INTO Product (barcode, name_fr, generic_name, nutrition_grade_fr, off_url) "
                    "VALUES (%(barcode)s, %(name_fr)s, %(generic_name)s, %(nutrition_grade_fr)s, %(off_url)s)")

insert_product_has_brand = ("INSERT INTO Product_has_brand (product_id, brand_id) "
                            "VALUES (%(product_id)s, %(brand_id)s)")

insert_product_has_category = ("INSERT INTO Product_has_category ("
                                    "product_id, "
                                    "category_id"
                                    ") "
                                "VALUES ("
                                    "%(product_id)s,"
                                    "%(category_id)s"
                                    ")")

insert_product_has_country = ("INSERT INTO Product_has_country ("
                                    "product_id, "
                                    "country_id"
                                ")"
                                "VALUES ("
                                    "%(product_id)s, "
                                    "%(country_id)s"
                                ")"
                                )

insert_product_has_store = ("INSERT INTO Product_has_store (product_id, product_id, store_id, store_id) "
                                "VALUES ("
                                    "%(product_id)s, "
                                    "%(store_id)s"
                                ")")

insert_product_has_substitute = ("INSERT INTO Product_has_substitute ("
                                    "product_id, "
                                    "substitute_id"
                                ")"
                                "VALUES ("
                                    "%(product_id)s, "
                                    "%(substitute_id)s"
                                ")")

insert_user_favorite_product = ("INSERT INTO User_favorite_product (product_id) "
                                "VALUES ("
                                    "%(product_id)s"
                                ")")