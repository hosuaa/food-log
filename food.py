import sqlite3 as sl
con = sl.connect('foods.db')
cursor = con.cursor()
print("Connected to foods.db")
while True:
    food_name = input('Enter food:')
    food_cal = input('Enter cal:')
    food_fat = input('Enter fat:')
    food_carb = input('Enter carb:')
    food_protein = input('Enter protein')
    count = cursor.execute("""INSERT INTO Foods (name,cal,fat,carb,protein) VALUES (?,?,?,?,?);""", (food_name,food_cal,food_fat,food_carb,food_protein))
    con.commit()
    print("Record inserted to foods.db")

cursor.close()