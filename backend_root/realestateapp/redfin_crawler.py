import sqlite3

SQLITE_DB_PATH = "housingdata.db"

def create_tables_if_not_exist():
   conn = sqlite3.connect(SQLITE_DB_PATH)
   conn.execute(
      '''
      CREATE TABLE IF NOT EXISTS URLS
      (URL                  TEXT NOT NULL,
      NUM_PROPOERTIES      INT,
      NUM_PAGES            INT,
      PER_PAGES_PROPERTIES INT);
      '''
   )
   conn.execute(
      '''
      CREATE TABLE IF NOT EXISTS LISTINGS
      URL                  TEXT NOT NULL,
      INFO                 TEXT);
      '''
   )
   conn.execute(
      '''
      CREATE TABLE IF NOT EXISTS LISTING_DETAILS(
      URL            TEXT    NOT NULL,
      NUMBER_OF_ROOMS INT,
      NAME           TEXT,
      COUNTRY        TEXT,
      REGION         TEXT,
      LOCALITY       TEXT,
      STREET         TEXT,
      POSTAL         TEXT,
      TYPE           TEXT,
      PRICE          REAL);
      '''
   )
   conn.close()
   