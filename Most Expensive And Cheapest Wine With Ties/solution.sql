-- Combine region_1 and region_2 into a single column `region`
WITH combine_region AS(
    SELECT region_1 AS region,
        variety, price
    FROM winemag_pd
    WHERE price IS NOT NULL and region_1 IS NOT NULL
    UNION ALL
    SELECT region_2 AS region,
        variety, price
    FROM winemag_pd
    WHERE price IS NOT NULL and region_2 IS NOT NULL),
    
-- Rank wines within each region by price
ranked_cte AS(
    SELECT region, variety,
        DENSE_RANK() OVER(PARTITION BY region ORDER BY price DESC) as expensive_rank,
        DENSE_RANK() OVER(PARTITION BY region ORDER BY price) as cheapest_rank
    FROM combine_region)
    
-- Self-join to combine the most expensive and cheapest varieties for each region
SELECT
    DISTINCT t1.region,
    t1.variety AS expensive_variety,
    t2.variety AS cheapest_variety
FROM ranked_cte t1 
JOIN ranked_cte t2
ON t1.region = t2.region AND t1.expensive_rank = t2.cheapest_rank
WHERE t1.expensive_rank = 1 and t2.cheapest_rank = 1;




-- Note: The self-join on ranked_cte is used to bring together the variety with the highest price and the variety with the lowest price for each region into one row. Here’s how this works:
-- t1 refers to the subquery instance for the most expensive variety.
-- t2 refers to the subquery instance for the cheapest variety.
-- The join condition ON t1.region = t2.region AND t1.expensive_rank = t2.cheapest_rank ensures that we are matching the region and rank properly.
