insert_category = ("INSERT IGNORE INTO Category (off_id, name) "
                    "VALUES (%(off_id)s, %(name)s)")

insert_brand = ("INSERT IGNORE INTO Brand (name) "
                    "VALUES (%s)")

insert_product = ("INSERT IGNORE INTO Product (barcode, name_fr, nutrition_grade_fr, url) "
                    "VALUES (%(barcode)s, %(name_fr)s, %(nutrition_grade_fr)s, %(url)s)")

insert_store = ("INSERT IGNORE INTO Store (name) "
                    "VALUES (%s)")

insert_product_category = ("INSERT IGNORE INTO Product_category ("
                                    "product_id, "
                                    "category_id"
                                    ") "
                                "VALUES (%(product_id)s, (SELECT id FROM Category WHERE off_id = %(category)s))")

insert_product_brand = ("INSERT IGNORE INTO Product_brand ("
                                    "product_id, "
                                    "brand_id"
                                    ") "
                                "VALUES (%(product_id)s, (SELECT id FROM Brand WHERE name = %(brand)s))")

insert_product_store = ("INSERT IGNORE INTO Product_store ("
                                    "product_id, "
                                    "store_id"
                                    ") "
                                "VALUES (%(product_id)s, (SELECT id FROM Store WHERE name = %(store)s))")

insert_product_substitute = ("INSERT IGNORE INTO Product_substitute ("
                                    "product_id, "
                                    "substitute_id, "
                                    "score"
                                ")"
                                "VALUES ("
                                    "%(product_id)s, "
                                    "%(substitute_id)s, "
                                    "%(score)s"
                                ")")

insert_user_favorite_product = ("INSERT IGNORE INTO User_favorite_product (product_id) "
                                "VALUES ("
                                    "%(product_id)s"
                                ")")

get_categories = ("SELECT id, name, off_id FROM Category "
                    "ORDER BY name ")

count_brands = ("SELECT COUNT(*) as total FROM Brand")

get_category_off_id = ("SELECT off_id FROM Category "
                    "WHERE id = %(id)s")

get_products = ("SELECT p.id, p.name_fr, p.nutrition_grade_fr, p.url, p.barcode FROM Product p "
                "INNER JOIN Product_category pc ON p.id = pc.product_id "
                "WHERE pc.category_id = %(cat_id)s AND p.name_fr != '' "
                "ORDER BY p.name_fr ASC")

get_product_categories = ("SELECT c.name as 'category name' FROM Category c "
                            "INNER JOIN Product_category pc ON pc.category_id = c.id "
                            "INNER JOIN Product p ON p.id = pc.product_id "
                            "WHERE p.id = %(id)s")

get_product_brands = ("SELECT b.name as 'brand name' FROM Brand b "
                        "INNER JOIN Product_brand pb ON pb.brand_id = b.id "
                        "INNER JOIN Product p ON p.id = pb.product_id "
                        "WHERE p.id = %(id)s")

get_product_details = ("SELECT barcode, name_fr, nutrition_grade_fr, url, b.name, c.name FROM Product p " 
                        "INNER JOIN Product_category pc ON pc.product_id = p.id "
                        "INNER JOIN Category c ON c.id = pc.category_id "
                        "INNER JOIN Product_brand pb ON pc.product_id = pb.product_id "
                        "INNER JOIN Brand b ON pb.brand_id = b.id "
                        "WHERE p.id = %(id)s")

get_product_stores = ("SELECT s.name as 'store name' FROM Store s "
                        "INNER JOIN Product_store ps ON ps.store_id = s.id "
                        "INNER JOIN Product p ON p.id = ps.product_id "
                        "WHERE p.id = %(id)s")

get_product_substitutes = ("SELECT ps.substitute_id, p.name_fr, p.nutrition_grade_fr, p.url, p.barcode FROM Product_substitute ps "
                            "INNER JOIN Product p ON p.id = ps.substitute_id "
                            "WHERE product_id = %(id)s "
                            "ORDER BY ps.score DESC, p.nutrition_grade_fr ASC "
                            "LIMIT 1")

find_substitute = ( "SELECT p.id FROM Product p "
                    "WHERE p.nutrition_grade_fr != '' "
                    "AND p.id != %(id)s "
                    "AND p.nutrition_grade_fr < (SELECT p2.nutrition_grade_fr FROM Product p2 WHERE p2.id = %(id)s) "
                    "ORDER BY p.nutrition_grade_fr ")
