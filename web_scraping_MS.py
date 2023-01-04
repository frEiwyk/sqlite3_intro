import mechanicalsoup
import pandas as pd
import sqlite3

browser = mechanicalsoup.StatefulBrowser()
browser.open("https://en.wikipedia.org/wiki/Comparison_of_Linux_distributions")

# extract table headers (th = table head)
th = browser.page.find_all("th", attrs={"class": "table-rh"})

# only the text we need
distribution = [value.text.replace("\n", "") for value in th]
#print(distribution.index("Zorin OS"))

# separate only the first table
distribution = distribution[:98]
#print(distribution)

# extract table data (td)

td = browser.page.find_all("td")
columns = [value.text.replace("\n", "") for value in td]

# again, only the first table
columns = columns[8:1086]
#print(columns)

# table is 11 columns long, so we extract every 11th item and assign it to a given row

column_names = ["Founder", 
                "Maintainer", 
                "Initial_Release_Year", 
                "Current_Stable_Version", 
                "Security_Updates", 
                "Release_Date", 
                "System_Distribution_Commitment", 
                "Forked_From", 
                "Target_Audience", 
                "Cost", 
                "Status"]

dictionary = {"Distribution": distribution}

for idx, key in enumerate(column_names):
    dictionary[key] = columns[idx:][::11]
    
df = pd.DataFrame(data = dictionary)


# insert data into a database

connection = sqlite3.connect("linux_distribution.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE linux (Distribution, " + ",".join(column_names)+ ")")
for i in range(len(df)):
    cursor.execute("INSERT INTO linux VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", df.iloc[i])

# permanently save data in database file (otherwise data is deletef when program is stopped)
connection.commit()

connection.close()

