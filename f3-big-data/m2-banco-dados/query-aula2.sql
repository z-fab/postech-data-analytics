/*
Realizando consultas comuns no Big Query
*/
SELECT
  date,
  invoice_and_item_number,
  store_number
FROM
  `bigquery-public-data.iowa_liquor_sales.sales`
ORDER BY
  `date` DESC
LIMIT
  100;


/*
Realizando consultas com cláusula WHERE
*/
SELECT
  date,
  invoice_and_item_number,
  store_number
FROM
  `bigquery-public-data.iowa_liquor_sales.sales`
WHERE
  store_number LIKE '58%'

/*
Query para retornar a quantidade de vendas de uma loja agregado pela data
*/
SELECT
  date,
  store_number,
  COUNT(1) AS `n_vendas`
FROM
  `bigquery-public-data.iowa_liquor_sales.sales`
WHERE
  store_number = '5811'
GROUP BY date, store_number
ORDER BY date
