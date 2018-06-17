from sqlite3 import connect

conn = connect('movie_club.db')
c = conn.cursor()
with open('createMovieTables.sql') as file:
    script = file.read()
    c.executescript(script)
conn.close()
