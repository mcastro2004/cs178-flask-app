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
    """Executes a SELECT query and returns all rows as dictionaries."""
    cur = get_conn().cursor(pymysql.cursors.DictCursor)
    cur.execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def get_countries():
    query = """
        SELECT Code, Name, Continent, Population
        FROM country
        ORDER BY Name
        LIMIT 20
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