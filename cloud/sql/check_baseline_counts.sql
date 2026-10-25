-- Failing rows indicate drift from the repository's historical source snapshot.
SELECT 'orders' AS source_table, COUNT(*) AS actual_rows, 99441 AS expected_rows FROM `secret-drake-512620-i7.olist_raw.orders` HAVING COUNT(*) != 99441
UNION ALL
SELECT 'items' AS source_table, COUNT(*) AS actual_rows, 112650 AS expected_rows FROM `secret-drake-512620-i7.olist_raw.items` HAVING COUNT(*) != 112650
UNION ALL
SELECT 'reviews' AS source_table, COUNT(*) AS actual_rows, 99224 AS expected_rows FROM `secret-drake-512620-i7.olist_raw.reviews` HAVING COUNT(*) != 99224
UNION ALL
SELECT 'customers' AS source_table, COUNT(*) AS actual_rows, 99441 AS expected_rows FROM `secret-drake-512620-i7.olist_raw.customers` HAVING COUNT(*) != 99441
UNION ALL
SELECT 'products' AS source_table, COUNT(*) AS actual_rows, 32951 AS expected_rows FROM `secret-drake-512620-i7.olist_raw.products` HAVING COUNT(*) != 32951
UNION ALL
SELECT 'sellers' AS source_table, COUNT(*) AS actual_rows, 3095 AS expected_rows FROM `secret-drake-512620-i7.olist_raw.sellers` HAVING COUNT(*) != 3095
UNION ALL
SELECT 'translations' AS source_table, COUNT(*) AS actual_rows, 71 AS expected_rows FROM `secret-drake-512620-i7.olist_raw.translations` HAVING COUNT(*) != 71;
