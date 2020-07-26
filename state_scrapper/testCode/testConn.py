import mysql.connector

mydb = mysql.connector.connect(
    database='mobicrol_DB',
    host="mobicrol.heliohost.org",
    user="mobicrol_admin",
    password="X->e^QW%K{|v12~#"
)

mycursor = mydb.cursor()

mycursor.execute("Select * from states")
myresult = mycursor.fetchall()

for x in myresult:
    print(x)

#mycursor.execute("Delete from states")
#mycursor.execute("ALTER TABLE states ADD PRIMARY KEY (id_web)")
