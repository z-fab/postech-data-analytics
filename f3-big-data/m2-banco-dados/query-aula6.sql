/*
Executando Clustering Kmeans nos resultados de um SELECT
*/
CREATE OR REPLACE MODEL
`postech-412612.model_cluster.store_cluster`
OPTIONS (model_type = 'kmeans', num_clusters = 6)
AS
SELECT
  date,
  store_name,
  COUNT(DISTINCT invoice_and_item_number) transaction,
  SUM(volume_sold_gallons) total_volume_sold_gallons,
  SUM(volume_sold_liters) total_volume_sold_liters,
  SUM(sale_dollars) total_revenue_sale,
  AVG(sale_dollars) avg_revenue_sale,
  MIN(sale_dollars) min_revenue_sale,
  MAX(sale_dollars) max_revenue_sale
FROM
  `bigquery-public-data.iowa_liquor_sales.sales`
GROUP BY date, store_name
ORDER BY date
