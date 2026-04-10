# [Favorite World Countries]

**CS178: Cloud and Database Systems — Project #1**
**Author:** Michael Castro
**GitHub:** mcastro2004

---

## Overview

Favorite World Countries is a Flask web application that allows users to browse country information from the MySQL world database and save their favorite countries in DynamoDB. It combines AWS RDS for structured country data with DynamoDB for user-created favorites and notes. This lets the user explore different world data and keep a personalized list of countries they are interested.

---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for [describe what you stored]
- **AWS DynamoDB** — non-relational database for [describe what you stored]
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
cs178-flask-app/
├── flaskapp.py               # Main Flask application — routes and app logic
├── dbCode.py                 # Database helper functions for MySQL and DynamoDB
├── creds_sample.py           # Credentials file
├── templates/
│   ├── home.html             # Landing page
│   ├── countries.html        # Displays country data from MySQL
│   ├── favorites.html        # Displays favorite countries from DynamoDB
│   ├── update_favorite.html  # Form to update notes for a saved favorite
├── .github/
│   └── workflows/
│       └── deploy.yml        # GitHub Actions deployment workflow
├── .gitignore                # Excludes creds.py and other sensitive files
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/mcastro2004/cs178-flask-app.git
   cd cs178-flask-app
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://98.93.254.130:8080
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

This project uses the `world` database hosted on AWS RDS. The main tables used in this project are:

- `country` — stores country information such as `Code`, `Name`, `Continent`, and `Population`; the primary key is `Code`
- `countrylanguage` — stores language information for each country; it links to the `country` table through `CountryCode`, which is a foreign key referencing `country.Code`

The app reads country data from MySQL and displays it on the `/countries` page.

The JOIN query used in this project connects the `country` table to the `countrylanguage` table using the country code. This allows the app to display one official language for each country along with its code, name, continent, and population.

### DynamoDB

This project also uses DynamoDB to store user-created favorite countries.

- **Table name:** `FavoriteCountries`
- **Partition key:** `Code`
- **Used for:** storing favorite countries selected by the user, along with attributes such as the country name, continent, and a note that can be updated later

Each item in the `FavoriteCountries` table includes:

- `Code`
- `Name`
- `Continent`
- `Note`

This connects to the rest of the app by allowing users to select countries from the MySQL `/countries` page and save them as favorites in DynamoDB. Users can then view, update, and delete those favorites through the app.

## CRUD Operations

| Operation | Route      | Description    |
| --------- | ---------- | -------------- |
| Create    | `/add-favorite` | Adds a selected country from the MySQL country list into the DynamoDB FavoriteCountries table |
| Read      | `/countries` | Displays country data from the MySQL world database |
| Update    | `/update-favorite` | Updates the note for a saved favorite country in DynamoDB |
| Delete    | `/delete-favorite` | Deletes a saved favorite country from DynamoDB |

---

## Challenges and Insights

One of the hardest parts of this project was deciding how to use the Update and Delete operations in a way that made sense for the overall design. Since the country data from the MySQL `world` database was being used mainly for browsing, I needed to think carefully about how DynamoDB could be used for user-created data instead. I decided to use DynamoDB to store favorite countries and editable notes, which made the CRUD features more practical and fit the project theme well.

Another challenge was troubleshooting smaller issues during development, especially with HTML templates and Flask routing. At different points, I ran into problems such as mistyping template file names, figuring out the correct page to redirect users to after different actions, and making sure form data was being passed correctly. Working through these problems helped me better understand how Flask routes, templates, and database operations all connect.

One of the biggest things I learned from this project was how to make two different database systems work together in the same application. MySQL through RDS was best for structured country data, while DynamoDB worked well for user-created favorites and notes. This helped me see how relational and non-relational databases can each serve different purposes within one web app.

---

## AI Assistance

I used ChatGPT when I ran into errors on the webpage to help me read through the errors it provided.