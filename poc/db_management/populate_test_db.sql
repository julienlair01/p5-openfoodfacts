INSERT INTO Category (id, off_id, name, clean_name)
VALUES (NULL, 'fr:pates-a-tartiner', 'fr:Pâtes à tartiner', 'Pâtes à tartiner');

INSERT INTO Product (
    id,
    barcode,
    category_id,
    fr_category_tag,
    generic_name,
    name_fr,
    clean_name,
    nutrition_grade_fr,
    off_url
  )
VALUES (
    NULL,
    123643746,
    1,
    'fr_category_tag:varchar',
    'generic_name:varchar',
    'name_fr:varchar',
    'clean_name:varchar',
    'nutrition_grade_fr:varchar',
    'off_url:varchar'
  );