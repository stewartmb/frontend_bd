from configparser import ConfigParser
import psycopg2
import os

def get_connection():
    db_config = get_config()
    db = psycopg2.connect(**db_config)
    db.autocommit = True
    cur = db.cursor()
    return db, cur

def get_config(filename="properties.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    db_config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in the {filename} file")
    return db_config
