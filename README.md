# p5-openfoodfacts

**How does the application work?**
The user can decide whether they want to find a substitue for one specific product or browse the already substituted products.

1. Find substitute
The user first needs to select a product category in the categories fetched from the Open Food Facts database.
This list is kept locally, and updated each time the user wants to substitute a product.

The user then selects a product from the products in the selected category, fetched from the Open Food Facts database.
The product list is kept locally, and updated each time the user wants to substitue a product.

A substitute product is suggested by the application. A  substitute product has got a higher score than the product selected by the user.

The user can save the result of the susbtitution.

2. Browse existing substitutions
The user can browse the list of products they decided to save locally.
The user can select one of this product and see the substitute product details.
