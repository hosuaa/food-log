import sqlite3 as sl
import datetime
day = str(datetime.datetime.today())
print(day)
time = str(datetime.datetime.today()).split()[1]
hour = int(time[:2])
if hour<6:
    time='Night'
elif hour>=6 and hour<12:
    time='Morning'
elif hour>=12 and hour<18:
    time='Afternoon'
else:
    time='Evening'
con = sl.connect('foods.db')
cursor = con.cursor()
print("Connected to foods.db")
print('Food Journal')
print('Eaten today:')
cursor.execute("select food_eaten,portions from log where DATE(day)=DATE('now') ORDER BY DATE(day) ASC;")
rows = cursor.fetchall()
totalcal=0
totalfatcal=0
totalcarbcal=0
totalproteincal=0
for row in range(0, len(rows)):
    cursor.execute("select * from foods where foods.name=?",(str(rows[row][0]),))
    food = cursor.fetchall()
    portion=rows[row][1]
    totalcal=totalcal+food[0][1]*portion
    totalfatcal=totalfatcal+food[0][2]*portion*9
    totalcarbcal=totalcarbcal+food[0][3]*portion*4
    totalproteincal=totalproteincal+food[0][2]*portion*4
    #food[row][column]. food[0][0] is name of current food (on current row), food[0][1] is cal...
    print("Food",row+1,":",food[0][0], "x",portion,", Cal:",food[0][1]*portion,"cal, Fat:",food[0][2]*portion,"g, Carb:",food[0][3]*portion,"g, Protein:",food[0][4]*portion,"g")
print("Total calories this day:",totalcal)
print("Calories from fat:",totalfatcal,", Calories from carbs:",totalcarbcal,", Calories from protein:",totalproteincal)
#print("Fat/Carb/Protein ratio:",round(totalfatcal/totalcal,2),round(totalcarbcal/totalcal,2),round(totalproteincal/totalcal,2))
if totalcal==totalfatcal+totalcarbcal+totalproteincal and totalcal!=0:
    print("Fat/Carb/Protein ratio:",totalfatcal/totalcal,totalcarbcal/totalcal,totalproteincal/totalcal)
while True:
    food_name = input('Enter food:')
    cursor.execute("select * from foods where foods.name=?",(food_name,))
    exists = cursor.fetchall()
    if not exists:
        print(food_name, "not found. Did you mean:" )
        cursor.execute("select * from foods where name LIKE '%'||?||'%'",(food_name,))
        matches = cursor.fetchall()
        for match in range(0, len(matches)):
            print(matches[match][0])
        continue
    portions = input('Enter portion:')
    count = cursor.execute("""INSERT INTO Log(day,time,food_eaten,portions) VALUES (?,?,?,?);""", (day,time,food_name,portions))
    con.commit()
    print("Record inserted to foods.db")
cursor.close()