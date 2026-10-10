# 🏡 DBT House Prices Project (Docker + Postgres)

This project is a minimal example to help you learn how to use [DBT](https://www.getdbt.com/) (Data Build Tool) with a PostgreSQL database using Docker Compose.

It includes:
- A preloaded seed dataset (`house_prices.csv`)
- A basic DBT model that calculates average sale price by neighborhood
- Docker containers for PostgreSQL and DBT

---

## 🚀 Quick Start

### 1. ✅ Clone the Repository

```bash
git clone https://github.com/vasuchettyphd/dbt_tutorial.git
cd dbt_tutorial
```

---

### 2. 🐳 Start the Environment

```bash
docker-compose up --build -d
```

This will:
- Start the PostgreSQL container (`dbt_postgres`)
- Start the DBT CLI container (`dbt_cli`)
- Run `dbt debug` and `dbt seed` automatically

---

### 3. 🧪 Run DBT Models and Tests

Enter the DBT container:

```bash
docker exec -it dbt_cli bash
```

Then inside the container:

```bash
dbt debug       # check config and connection
dbt run         # build models (e.g., create views)
```

When you're done using the container, **exit the bash session** with:

```bash
exit
```

If you started `docker-compose` with `up` (not `-d`), you can also stop it with `Ctrl + C`.

---

## 🗞 What's in the Project?

### 📂 Seed Datasets

#### `house_prices.csv`
A small, clean dataset for introductory exercises with fields:
- `id`, `neighborhood`, `lot_area`, `year_built`, `overall_qual`, `overall_cond`, `full_bath`, `bedroom_abvgr`, `sale_price`

#### `house_prices_large.csv`
A larger, messier dataset with:
- 500+ rows
- Missing values in numeric fields
- Duplicate rows
- Great for teaching data cleaning and validation techniques

#### `client_preferences.csv`
A synthetic dataset representing client preferences:
- `client_id`, `preferred_neighborhood`
- Ranges for `price`, `bedrooms`, `bathrooms`, and `year_built`
- Used to build models that match clients to houses

These CSVs are loaded using `dbt seed` and appear as tables in your database.

---

### 📂 `models/avg_sale_price.sql`

```sql
-- Calculates average sale price by neighborhood and overall quality
select
  neighborhood,
  overall_qual,
  avg(sale_price) as avg_price,
  count(*) as num_sales
from {{ ref('house_prices') }}
group by neighborhood, overall_qual
order by avg_price desc
```

---

## 🔍 Inspect the Results: Use `psql` from Docker

```bash
docker exec -it dbt_postgres psql -U dbt_user -d dbt_db
```

Then inside PostgreSQL:

```sql
\dt      -- List tables
\dv      -- List views
SELECT * FROM avg_sale_price;
```

When finished, **exit the PostgreSQL shell** with:

```sql
\q
```

---

## 🔌 Clean Up

If `docker-compose up` is running in the foreground, stop it with `Ctrl + C` first.

To stop and remove containers and volumes:

```bash
docker-compose down -v
```

---

## 🧠 Want to Learn More?

- [DBT Learn](https://docs.getdbt.com/docs/introduction)
- [DBT Command Reference](https://docs.getdbt.com/reference/dbt-commands)
