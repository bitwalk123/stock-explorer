import psycopg2
connection = psycopg2.connect("host=localhost dbname=postgres user=<your db username> password=<your db password>")

# カーソルをオープンします
cursor = connection.cursor()