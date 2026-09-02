# Pizza Place Sales — Data Engineering & Analytics Pipeline

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![SQL Server](https://img.shields.io/badge/SQL_Server-2022-red.svg)](https://www.microsoft.com/en-us/sql-server)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://www.docker.com/)

 **Repository:** [https://github.com/aldalisgomes/pizza-place-sales](https://github.com/aldalisgomes/pizza-place-sales)

## Project Overview
This case study covers a complete end-to-end data pipeline for a fictional **Pizza Place**, going from extracting denormalized CSV data to supporting advanced business decision-making.

The core objective was to restructure a relational database that suffered from redundancy and update anomalies. This was achieved by:
1. Applying **Normal Forms (1NF and 3NF)** to clean the data.
2. Automating the ETL data load into **SQL Server** using **Python** (Pandas, SQLAlchemy).
3. Extracting business intelligence using advanced **T-SQL**.

---

## Technologies & Tools
* **Languages:** Python (Pandas, SQLAlchemy, PyODBC), T-SQL
* **Database:** Microsoft SQL Server (Containerized)
* **Infrastructure:** Docker & Docker Compose
* **Automation:** Makefile
* **Modeling:** Peter Chen and Crow's Foot notations

---

## Project Structure
```text
pizza_sales/
├── data/
│   ├── data_dictionary.csv
│   ├── order_details.csv
│   ├── orders.csv
│   ├── pizza_types.csv
│   └── pizzas.csv
├── docker/
│   └── docker-compose.yml
├── src/
│   └── 03_normalization_and_new_tables.py
├── 01_create_tables.sql
├── 02_analysis_queries.sql
├── Dockerfile
├── Makefile
├── projeto 1 - pizzaria (2).pdf
├── README.md
└── requirements.txt
```

---

## Database Architecture & Data Modeling

### Normalization Process
1. **First Normal Form (1NF):** The original source data contained an `ingredients` column with multiple comma-separated values. These were decomposed into an atomic structure, creating the associative table `pizza_type_ingredients`.
2. **Third Normal Form (3NF):** Pizza categories were originally stored as redundant text. They were normalized into a separate dimension table (`categories`) with unique numeric identifiers.
3. **Data Quality & Business Rules (via Python):**
   * Default addition of *Mozzarella Cheese* to all pizzas to standardize recipes.
   * Default addition of *Tomato Sauce* for pizzas without a specified sauce.

### Entity Relationship Diagram (ERD)
```text
[ categories ]
      │ (1)
      │
      └───────< (N) [ pizza_types ] ───(1)───────< (N) [ pizzas ]
                         │                                  │ (1)
                         │ (1)                              │
                         │                                  └───────< (N) [ order_details ]
                         └───────< (N)                                         │ (N)
                                    [ pizza_type_ingredients ]                 │
                         ┌───────< (N)                                         │
                         │ (1)                                                 │ (1)
                  [ ingredients ]                                         [ orders ]
```

---

## How to Run This Project Locally

### 1. Prerequisites
* **Docker Desktop** installed and running.
* **Make** installed (optional, but recommended for ease of use).

### 2. Clone the Repository
```bash
git clone https://github.com/aldalisgomes/pizza-place-sales.git
cd pizza_sales
```

### 3. Start the Infrastructure (SQL Server)
Use the provided `Makefile` to quickly spin up the database container:
```bash
make db-up
```
*(Wait approximately 15 seconds for SQL Server to initialize).*

### 4. Run the ETL Pipeline
Build the Python application container and run the complete ETL pipeline. This step builds the image, connects to the Docker network, audits data, applies normalization rules, and loads the SQL Server database:
```bash
make run
```

### 5. Tear Down
Once finished, you can safely shut down and remove the containers:
```bash
make db-down
```

---

## Analytics Highlights
The project includes an advanced SQL script (`02_analysis_queries.sql`) containing:
* **Complex Filtering:** Usage of `BETWEEN`, `IN`, `LIKE`, and exclusions.
* **Joins:** `INNER`, `LEFT`, `RIGHT`, and `FULL OUTER` joins to combine normalized tables and identify data orphans.
* **Subqueries:** Identifying top-priced items and revenue percentage contributions.
* **Set Operations:** `UNION`, `INTERSECT`, and `EXCEPT` to cross-reference ingredient usage across pizza categories.