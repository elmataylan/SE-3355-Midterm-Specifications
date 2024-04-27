import mysql.connector

myDB = mysql.connector.connect(
    host="localhost",
    user="root",
    password="00000000",
    database="products",
    auth_plugin='mysql_native_password'
)


with open("C:\\Users\\elma\\Desktop\\SamsungKurutma.jfif", "rb") as file:

    image_data = file.read()

cursor = myDB.cursor()
cursor.execute("INSERT INTO products_1 (id, urunismi, urunfiyati, urunkategori, yarinkapimda, urunsehir, image) VALUES (%s, %s, %s, %s, %s, %s, %s)",
               (10,"Hava Temizleyici", 13300, "Elektronik", 0, "İstanbul", image_data))  
myDB.commit()
cursor.close()

myDB.close()