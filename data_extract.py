import MySQLdb
import json

conn = MySQLdb.connect(host="139.144.177.81", user="jesse", password="Kaas@1234", database="mydatabase")
cursor = conn.cursor()

#first device:
cursor.execute("SELECT * from device")
rows_device = cursor.fetchall()

rowarray_list_device = []
for row in rows_device:
    t = (row[0], row[1], row[2], row[3])
    rowarray_list_device.append(t)

j = json.dumps(rowarray_list_device)

with open('device_rowarrays.js', 'w') as f:
    f.write(j)


#then status:
cursor.execute("SELECT * from status")
rows_status = cursor.fetchall()

rowarray_list_status = []
print(rows_status)
for row in rows_status:
    t = (row[0], row[1], row[2], row[3], row[4], row[5], row[6].strftime("%Y-%m-%d %H:%M:%S"))
    rowarray_list_status.append(t)

k = json.dumps(rowarray_list_status)

with open('status_rowarrays.js', 'w') as g:
    g.write(k)
conn.commit()
cursor.close()
print('Done')