-- Average sale price by neighborhood and overall quality
select
  neighborhood,
  overall_qual,
  avg(sale_price) as avg_price,
  count(*) as num_sales
from {{ ref('house_prices') }}
group by neighborhood, overall_qual
order by avg_price desc