
import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(database="random_picker",
                        host="localhost",
                        user="postgres",
                        password="postgres",
                        port="5432",
                        cursor_factory=RealDictCursor)

