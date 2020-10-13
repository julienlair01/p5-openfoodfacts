insert_category = ("INSERT IGNORE INTO Category (off_id, name) "
                    "VALUES (%(off_id)s, %(name)s)")

insert_product = ("INSERT IGNORE INTO Product (barcode, name_fr, generic_name, nutrition_grade_fr, off_url) "
                    "VALUES (%(barcode)s, %(name_fr)s, %(generic_name)s, %(nutrition_grade_fr)s, %(off_url)s)")

insert_product_category = ("INSERT IGNORE INTO Product_category ("
                                    "product_id, "
                                    "category_id"
                                    ") "
                                "VALUES (%(product_id)s, (SELECT id FROM Category WHERE off_id = %(category)s))")

insert_product_substitute = ("INSERT INTO Product_has_substitute ("
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

get_categories = ("SELECT id, name, off_id FROM Category "
                    "ORDER BY name "
                    "LIMIT 10")

get_category_off_id = ("SELECT off_id FROM Category "
                    "WHERE id = %(id)s")

get_products = ("SELECT p.name_fr FROM Product p "
                "INNER JOIN Product_category pc ON p.id = pc.product_id "
                "INNER JOIN Category c ON c.id = pc.category_id "
                "WHERE pc.category_id = %(cat_id)s "
                "GROUP BY p.name_fr "
                "ORDER BY p.name_fr ASC "
                "LIMIT 20")