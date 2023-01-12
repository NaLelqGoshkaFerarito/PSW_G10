import mysql.connector
import matplotlib.pyplot as plt

# connect to mysql
conn = mysql.connector.connect(host="139.144.177.81", user="ADMIN", password="", database="mydatabase")
if conn.is_connected():
    print("connected")
cursor = conn.cursor()

"""
Function to plot all metric data [Temperature, Humidity, Pressure, Light]
of a specific sensor given as arguments. It will return a plot of this data.
This is over a time period of 1 day. (current day)
"""
def plot_day(metric, sensor):

    #TEMPERATURE
    if metric == "Temperature":
        temp = []
        dates = []
        temp_lht_saxion = []
        dates_lht_saxion = []

        #Only these sensors read an inside temperature
        if sensor == "py-saxion" or sensor == "py-wierden" or sensor == "py-gronau" or sensor == "py-group9" or sensor == "lht-saxion":
            cursor.execute(
                "SELECT temp_in, time from status where time > DATE_SUB(CURRENT_DATE(), INTERVAL 1 day) AND device_id = %s",
                (sensor,))
            result = cursor.fetchall()
            for r in result:
                temp.append(r[0])
                dates.append(r[1])
        # All other sensors read an outside temperature
        else:
            cursor.execute(
                "SELECT temp_out, time from status where time > DATE_SUB(CURRENT_DATE(), INTERVAL 1 day) AND device_id = %s",
                (sensor,))
            result = cursor.fetchall()
            for r in result:
                temp.append(r[0])
                dates.append(r[1])

        # The sensor 'lht-saxion' reads both temp_out as temp_in.
        # Thus, in this case it will get extracted specifically for a subplot.
        if sensor == 'lht-saxion':
            cursor.execute(
                "SELECT temp_out, time from status where time > DATE_SUB(CURRENT_DATE(), INTERVAL 1 day) AND device_id = 'lht-saxion'")
            result = cursor.fetchall()
            for r in result:
                temp_lht_saxion.append(r[0])
                dates_lht_saxion.append(r[1])

        #If 'lht-saxion' make a subplot of both inside and outside temperature.
        if sensor == 'lht-saxion':
            fig, ax = plt.subplots(2, sharex=True)
            ax[0].plot(dates, temp)
            ax[0].set_title('Indoors Temperature detected by ' + sensor)
            ax[1].plot(dates_lht_saxion, temp_lht_saxion)
            ax[1].set_title('Exterior Temperature detected by ' + sensor)
            ax[0].set(ylabel='Temperature (Centigrade)')
            ax[1].set(xlabel='Time (Hours)', ylabel='Temperature (Centigrade)')

        #Else make a single plot of the temperature read indoors.
        else:
            fig, ax = plt.subplots()
            ax.plot(dates, temp)
            ax.set_title('Indoors Temperature detected by ' + sensor)
            ax.set(xlabel='Time (Hours)', ylabel='Temperature (Centigrade)')

        plt.show()

    # HUMIDITY
    if metric == "Humidity":
        humidity = []
        dates = []
        #Read values from database
        cursor.execute(
            "SELECT humidity, time from status where time > DATE_SUB(CURRENT_DATE(), INTERVAL 1 day) AND device_id = %s",
            (sensor,))
        result = cursor.fetchall()
        for r in result:
            humidity.append(r[0])
            dates.append(r[1])

        #Plot humidity
        fig, ax = plt.subplots()
        ax.plot(dates, humidity)
        ax.set_title('Relative humidity detected by ' + sensor)
        ax.set(xlabel='Time (Hours)', ylabel='Relative humidity')
        plt.show()

    # PRESSURE
    if metric == "Pressure":
        pressure = []
        dates = []
        #read values from database.
        cursor.execute(
            "SELECT pressure, time from status where time > DATE_SUB(CURRENT_DATE(), INTERVAL 1 day) AND device_id = %s",
            (sensor,))
        result = cursor.fetchall()
        for r in result:
            pressure.append(r[0])
            dates.append(r[1])

        # Plot Pressure
        fig, ax = plt.subplots()
        ax.plot(dates, pressure)
        ax.set_title('Pressure detected by ' + sensor)
        ax.set(xlabel='Time (Hours)', ylabel='Pressure (Pascal)')
        plt.show()