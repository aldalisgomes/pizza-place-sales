# Pizza Place Sales — Data Modeling, Ingestion, and Analysis

## Project Overview
This case study covers the data pipeline for the fictional **Pizza Place**, from extracting denormalized data to supporting decision-making.

The objective was to restructure a relational database that presented redundancy problems and update anomalies by applying **Normal Forms (1NF and 3NF)**, automating the data load into **SQL Server** via **Python**, and extracting business information using **T-SQL**.

---
## Technologies Used

* **Language / Libraries:** Python (Pandas, SQLAlchemy, PyODBC)
* **Database:** SQL Server (T-SQL)
* **Containerization:** Docker & Docker Compose
* **IDE / Tools:** VS Code (Extensions: SQL Server, Python)
* **Data Modeling:** Lucidchart (Peter Chen and Crow's Foot notations)
* **Version Control:** Git & GitHub

---

## Database Architecture & ER Modeling

### Data Governance and Quality
A **Data Dictionary** was developed for the physical modeling, ensuring database integrity through Constraints:
* **Primary Keys (PK) and Foreign Keys (FK):** To ensure correct relationships between orders, pizzas, categories, and ingredients.
* **CHECK Constraints:** For business rules in the database (e.g., `price > 0`, `quantity > 0`, validation of the limit year in `date`, and standardization of sizes `IN ('S', 'M', 'L', 'XL', 'XXL')`).

### Normalization Process
1. **First Normal Form (1NF):** The ingredients column contained multiple comma-separated values in the source file. These values were decomposed, and the associative table `pizza_type_ingredients` was created.
2. **Third Normal Form (3NF):** Pizza categories were stored redundantly as text in the types table. They were isolated into a new dimension table named `categories` with a unique numeric identifier.
3. **Business Rules Applied via Python:**
   * Addition of *Mozzarella Cheese* to all pizza types to standardize the ingredient list.
   * Addition of *Tomato Sauce* as a default for recipes without a specific sauce specified in the original description.

---

## Relational Schema (ER Diagram)

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

                  
## How to Run This Project Locally

If you want to clone and run this project on your machine, follow these steps:

### 1. Prerequisites
* Python (version 3.10+) installed.
* Docker Desktop installed and running.
* SQL Server ODBC Driver 17 (or compatible) installed.

### 2. Clone the Repository
```bash
git clone [https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git](https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git)
cd pizza_sales

### 3. Set Up the Environment
Install the required Python packages:
pip install -r requirements.txt

### 4. Start SQL Server via Docker
Run your SQL Server container using Docker Compose (or start your local instance):
docker-compose up -d

### 5. Run the Data Pipeline
Execute the main script to audit data, apply normalization rules, create the database structure, and load the data automatically:
python src/03_normalization_and_new_tables.py