# dbCode.py
# Author: Michael Castro
# Helper functions for database connection and queries


import pymysql
import creds
import boto3
from creds import *

def get_conn():
    """Returns a connection to the MySQL RDS instance."""
    conn = pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db,
    )
    return conn

def execute_query(query, args=()):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def get_countries():
    query = """
        SELECT country.Code, country.Name, country.Continent, country.Population, MIN(countrylanguage.Language) AS Language
        FROM country
        JOIN countrylanguage
            ON country.Code = countrylanguage.CountryCode
        WHERE countrylanguage.IsOfficial = 'T'
        GROUP BY country.Code, country.Name, country.Continent, country.Population
        ORDER BY country.Name
    """
    return execute_query(query)


dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('FavoriteCountries')


def get_favorites():
    response = table.scan()
    return response.get('Items', [])


def add_favorite_country(code, name, continent):
    table.put_item(
        Item={
            'Code': code,
            'Name': name,
            'Continent': continent,
            'Note': ''
        }
    )


def get_one_favorite(code):
    response = table.get_item(Key={'Code': code})
    return response.get('Item')


def update_favorite_note(code, note):
    table.update_item(
        Key={'Code': code},
        UpdateExpression='SET Note = :n',
        ExpressionAttributeValues={':n': note}
    )


def delete_favorite_country(code):
    table.delete_item(Key={'Code': code})