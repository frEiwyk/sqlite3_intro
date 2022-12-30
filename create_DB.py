import sqlite3

# connect to a database (create one, if it doesn't exist)
connection = sqlite3.connect("gta.db")

# in charge of all communication with the database
cursor = connection.cursor()

# all SQL commandy are done via this cursor interface
cursor.execute("CREATE TABLE IF NOT EXISTS gta (release_year INTEGER, release_name TEXT, city TEXT)")

release_list = [
    (1997, "Grand Theft Auto", "state of New Guernsey"),
    (1999, "Grand Theft Auto 2", "Anywhere, USA"),
    (2001, "Grand Theft Auto III", "Liberty City"),
    (2002, "Grand Theft Auto: Vice City", "Vice City"),
    (2004, "Grand Theft Auto: San Andreas", "state of San Andreas"),
    (2008, "Grand Theft Auto IV", "Liberty City"),
    (2013, "Grand Theft Auto V", "Los Santos")
]    

# adding multiple entries can be done using executemany function with the following syntax
cursor.executemany("INSERT INTO gta VALUES (?,?,?)", release_list)
# this is to commit the changes we made in the databaase
connection.commit()

# print what is added to the database (bc if we open the database in a text editor, it cannot be read)
for row in cursor.execute("SELECT * FROM gta"):
    print(row)
print("*************")

# if a row with city == Liberty City is found, print it
cursor.execute("SELECT * FROM gta WHERE city=:c", {"c": "Liberty City"})
gta_search = cursor.fetchall()
print(gta_search)
print("*************")

# create an additional table within the same database
cursor.execute("CREATE TABLE IF NOT EXISTS cities (gta_city TEXT, real_city TEXT)")
cursor.execute("INSERT INTO cities VALUES (?,?)", ("Liberty City", "New York"))
cursor.execute("SELECT * FROM cities WHERE gta_city=:c", {"c": "Liberty City"})
cities_search = cursor.fetchall()
print(cities_search)
print("*************")

# exchange data between the two tables
for i in gta_search:
    adjusted = [cities_search[0][1] if value == cities_search[0][0] else value for value in i]
    print(adjusted)



# close a connection to the database
connection.close()