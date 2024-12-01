# NYC Housing Schema Design
## Description
This project provides a well-structured database schema for managing New York City housing data. The schema can be used to analyze housing trends, manage building information, and support decision-making processes for housing-related projects.

Users can set up and interact with the schema using pgAdmin or Python for seamless integration into workflows.

## Table of Contents
Description
Schema Design
Installation
Usage
Features
Contributing
License
Schema Design
The schema is structured with the following key tables:

Buildings Table: Contains information about individual buildings, such as address, year built, and unit count.
Rent Data Table: Tracks rent details by unit and neighborhood.
Neighborhoods Table: Includes borough-specific demographic and geographic data.
Installation
Prerequisites
PostgreSQL and pgAdmin installed on your system.
Python (3.8 or higher) with psycopg2 library installed.
Steps
Clone this repository:

bash
Copy code
git clone https://github.com/your-username/nyc-housing-schema.git
Navigate to the project directory:

bash
Copy code
cd nyc-housing-schema
Set up the database in pgAdmin:

Open pgAdmin and create a new database (e.g., nyc_housing).
Execute the provided SQL scripts in the sql/ folder using the query editor in pgAdmin:
schema.sql to create the database schema.
data.sql to populate the database with sample data.
(Optional) Install Python dependencies:

bash
Copy code
pip install psycopg2
Usage
Using pgAdmin
Open pgAdmin and connect to your PostgreSQL instance.
Use the query editor to run SQL queries against the schema:
sql
Copy code
SELECT * FROM buildings WHERE borough = 'Brooklyn';
Using Python
Run the provided Python scripts to interact with the database. Example:
python
Copy code
import psycopg2

# Connect to the database
connection = psycopg2.connect(
    database="nyc_housing",
    user="your_username",
    password="your_password",
    host="127.0.0.1",
    port="5432"
)
cursor = connection.cursor()

# Execute a query
cursor.execute("SELECT * FROM buildings WHERE borough = 'Manhattan';")
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
connection.close()
Modify or create your own Python scripts to perform analyses or automate database operations.
Features
Easy-to-use schema for NYC housing data.
Supports integration with pgAdmin and Python for flexible workflows.
Designed for scalability and analytical efficiency.
Contributing
Contributions are welcome! To contribute:

Fork this repository.
Create a feature branch:
bash
Copy code
git checkout -b feature/your-feature
Commit your changes:
bash
Copy code
git commit -m "Add a new feature"
Push your branch:
bash
Copy code
git push origin feature/your-feature
Open a pull request.
License
This project is licensed under the MIT License. See the LICENSE file for more details.

Acknowledgments
NYC Open Data for providing housing datasets.
PostgreSQL and pgAdmin for database management.
Python’s psycopg2 library for database interaction.
