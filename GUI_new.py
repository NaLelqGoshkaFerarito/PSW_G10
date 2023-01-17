import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import tkintermapview
# connect to mysql
conn = mysql.connector.connect(host="139.144.177.81", user="ADMIN", password="", database="mydatabase")
if conn.is_connected():
    print("connected")
cursor = conn.cursor()

"""
Function to plot all metric data [Temperature, Humidity, Pressure, Light]
of a specific sensor given as arguments. It will return a plot of this data over a specific period.
In this case the period options are: day/week/month(not implemented)
Possible additions: last hour / last 3 days?
"""

#TODO:
# - update xlabels based on period of function
# - convert datetime to better format depending on period
# - Add Light as metric to function
# - Add month as period to function
# - Better GUI
# - Metadata per device
# - More buttons for metrics/period combos


###GEOGRAPHICAL POSITION

def mapviewsaxion(sensor):
    latitude, longitude = location(sensor)
    top = tk.Toplevel()
    top.title('Map view app - Saxion')
    top.geometry('600x400')
    my_label = tk.LabelFrame(top)
    my_label.pack(pady=20)
    map_widget = tkintermapview.TkinterMapView(top, width=800, height=600, corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    marker_saxion = map_widget.set_marker(float(longitude), float(latitude), text="Saxion Sensor")
    # set_position(latitude, longitude)
    map_widget.set_position(float(longitude), float(latitude), marker=True)
   # map_widget.set_address("Saxion Sensor", marker=True)



def mapviewgronau(sensor):
    latitude, longitude = location(sensor)
    top = tk.Toplevel()
    top.title('Map view app - Gronau')
    top.geometry('600x400')
    my_label = tk.LabelFrame(top)
    my_label.pack(pady=20)
    map_widget = tkintermapview.TkinterMapView(top, width=800, height=600, corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    marker_gronau = map_widget.set_marker(float(longitude), float(latitude), text="Gronau Sensor")
    # set_position(latitude, longitude)
    map_widget.set_position(float(longitude), float(latitude), marker=True)



def mapviewwierden(sensor):
    latitude, longitude = location(sensor)
    top = tk.Toplevel()
    top.title('Map view app - Wierden')
    top.geometry('600x400')
    my_label = tk.LabelFrame(top)
    my_label.pack(pady=20)
    map_widget = tkintermapview.TkinterMapView(top, width=800, height=600, corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    marker_wierden = map_widget.set_marker(float(longitude), float(latitude), text="Wierden Sensor")
    # set_position(latitude, longitude)
    map_widget.set_position(float(longitude), float(latitude), marker=True)


def mapviewlora(sensor):
    latitude, longitude = location(sensor)
    top = tk.Toplevel()
    top.title('Map view app - Lora')
    top.geometry('600x400')
    my_label = tk.LabelFrame(top)
    my_label.pack(pady=20)
    map_widget = tkintermapview.TkinterMapView(top, width=800, height=600, corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    marker_lora = map_widget.set_marker(float(longitude), float(latitude), text="Lora Sensor")
    #set_position(latitude, longitude)
    map_widget.set_position(float(longitude), float(latitude), marker=True)
    #marker_lora.set_address("Lora Sensor", marker=True)


def location(sensor):
    cursor.execute(
        "select longitude, latitude from device where name = %s", (sensor,))
    result = cursor.fetchall()
    return result[0]

def plot(metric, sensor, period):
    #Create new window to plot figure in
    root = create_window()
    # TEMPERATURE
    if metric == "Temperature":
        temp = []
        dates = []
        temp_lht_saxion = []
        dates_lht_saxion = []

        # Only these sensors read an inside temperature
        if sensor == "py-saxion" or sensor == "py-wierden" or sensor == "py-gronau" or sensor == "py-group9" or sensor == "lht-saxion":
            cursor.execute(
                "SELECT temp_in, time from status where time > DATE_SUB(CURRENT_DATE(), INTERVAL 1 {}) AND device_id = '{}'".format(period, sensor))

            result = cursor.fetchall()
            for r in result:
                temp.append(r[0])
                dates.append(r[1])
        # All other sensors read an outside temperature
        else:
            cursor.execute(
                "SELECT temp_out, time from status where time > DATE_SUB(CURRENT_DATE(), INTERVAL 1 {}) AND device_id = '{}'".format(period, sensor))
            result = cursor.fetchall()
            for r in result:
                temp.append(r[0])
                dates.append(r[1])

        # The sensor 'lht-saxion' reads both temp_out as temp_in.
        # Thus, in this case it will get extracted specifically for a subplot.
        if sensor == 'lht-saxion':
            cursor.execute(
                "SELECT temp_out, time from status where time > DATE_SUB(CURRENT_DATE(), INTERVAL 1 {}) AND device_id = '{}'".format(period, sensor))
            result = cursor.fetchall()
            for r in result:
                temp_lht_saxion.append(r[0])
                dates_lht_saxion.append(r[1])

        # If 'lht-saxion' make a subplot of both inside and outside temperature.
        if sensor == 'lht-saxion':
            fig, ax = plt.subplots(2, sharex=True)
            ax[0].plot(dates, temp)
            ax[0].set_title('Indoors Temperature detected by ' + sensor)
            ax[1].plot(dates_lht_saxion, temp_lht_saxion)
            ax[1].set_title('Exterior Temperature detected by ' + sensor)
            ax[0].set(ylabel='Temperature (Centigrade)')
            ax[1].set(xlabel='Time (Hours)', ylabel='Temperature (Centigrade)')

        # Else make a single plot of the temperature read indoors.
        else:
            fig, ax = plt.subplots()
            ax.plot(dates, temp)
            ax.set_title('Indoors Temperature detected by ' + sensor)
            ax.set(xlabel='Time (Hours)', ylabel='Temperature (Centigrade)')

    # HUMIDITY
    if metric == "Humidity":
        humidity = []
        dates = []
        # Read values from database
        cursor.execute(
            "SELECT humidity, time from status where time > DATE_SUB(CURRENT_DATE(), INTERVAL 1 {}) AND device_id = '{}'".format(period, sensor))
        result = cursor.fetchall()
        for r in result:
            humidity.append(r[0])
            dates.append(r[1])

        # Plot humidity
        fig, ax = plt.subplots()
        ax.plot(dates, humidity)
        ax.set_title('Relative humidity detected by ' + sensor)
        ax.set(xlabel='Time (Hours)', ylabel='Relative humidity')

    # PRESSURE
    if metric == "Pressure":
        pressure = []
        dates = []
        # read values from database.
        cursor.execute(
            "SELECT pressure, time from status where time > DATE_SUB(CURRENT_DATE(), INTERVAL 1 {}) AND device_id = '{}'".format(period, sensor))
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

    #Draw plot(s) in window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, root)
    toolbar.update()

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack()

def create_window():
    newwindow = tk.Toplevel(root)
    return newwindow


if __name__ == '__main__':
    root = tk.Tk()
    root.title('Weatherbase GUI')
    root.geometry("500x500")

    # GEOGRAPHICAL POSITION

    labelposition = tk.Label(root, text="Geographical Position")
    # Label1.grid(row=0, column=0)

    button_location_saxion = tk.Button(master=root,
                                       command=lambda: mapviewsaxion("py-saxion"),
                                       height=2,
                                       width=30,
                                       text="Saxion")

    button_location_wierden = tk.Button(master=root,
                                        command=lambda: mapviewwierden("py-wierden"),
                                        height=2,
                                        width=30,
                                        text="Wierden")

    button_location_gronau = tk.Button(master=root,
                                       command=lambda: mapviewgronau("lht-gronau"),
                                       height=2,
                                       width=30,
                                       text="Gronau")

    button_location_lora = tk.Button(master=root,
                                     command=lambda: mapviewlora("py-group9"),
                                     height=2,
                                     width=30,
                                     text="Lora")

    #TEMPERATURE
    button_temp_pysax = tk.Button(master=root,
                                  command=lambda: plot("Temperature", "py-saxion", "day"),
                                  height=2,
                                  width=30,
                                  text="Plot Temperature (last day) py-saxion ")
    button_temp_pywie = tk.Button(master=root,
                                  command=lambda: plot("Temperature", "py-wierden", "day"),
                                  height=2,
                                  width=30,
                                  text="Plot Temperature (last day) py-wierden")

    button_temp_pygrp10 = tk.Button(master=root,
                                    command=lambda: plot("Temperature", "py-group9", "day"),
                                    height=2,
                                    width=30,
                                    text="Plot Temperature (last day) py-group10")

    button_temp_lhtgro = tk.Button(master=root,
                                   command=lambda: plot("Temperature", "lht-gronau", "day"),
                                   height=2,
                                   width=30,
                                   text="Plot Temperature (last day) lht-gronau")
    button_temp_lhtsax = tk.Button(master=root,
                                   command=lambda: plot("Temperature", "lht-saxion", "day"),
                                   height=2,
                                   width=30,
                                   text="Plot Temperature (last day) lht-saxion")
    button_temp_lhtwie = tk.Button(master=root,
                                   command=lambda: plot("Temperature", "lht-wierden", "day"),
                                   height=2,
                                   width=30,
                                   text="Plot Temperature (last day) lht-wierden")
    #HUMIDITY
    button_hum_lhtgro = tk.Button(master=root,
                                  command=lambda: plot("Humidity", "lht-gronau", "day"),
                                  height=2,
                                  width=30,
                                  text="Plot Humidity (last day) lht-gronau")

    button_hum_lhtsax = tk.Button(master=root,
                                  command=lambda: plot("Humidity", "lht-saxion", "day"),
                                  height=2,
                                  width=30,
                                  text="Plot Humidity (last day) lht-saxion")

    button_hum_lhtwie = tk.Button(master=root,
                                  command=lambda: plot("Humidity", "lht-wierden", "day"),
                                  height=2,
                                  width=30,
                                  text="Plot Humidity (last day) lht-wierden")
    #PRESSURE

    button_pres_pysax = tk.Button(master=root,
                                  command=lambda: plot("Pressure", "py-saxion", "day"),
                                  height=2,
                                  width=30,
                                  text="Plot Pressure (last day) py-saxion ")
    button_pres_pywie = tk.Button(master=root,
                                  command=lambda: plot("Temperature", "py-wierden", "day"),
                                  height=2,
                                  width=30,
                                  text="Plot Pressure (last day) py-wierden")
    # TEMPERATURE WEEK
    button_temp_pysax_week = tk.Button(master=root,
                                  command=lambda: plot("Temperature", "py-saxion", "week"),
                                  height=2,
                                  width=30,
                                  text="Plot Temperature (last week) py-saxion ")
    button_temp_pywie_week = tk.Button(master=root,
                                  command=lambda: plot("Temperature", "py-wierden", "week"),
                                  height=2,
                                  width=30,
                                  text="Plot Temperature (last week) py-wierden")

    button_temp_pygrp10_week = tk.Button(master=root,
                                    command=lambda: plot("Temperature", "py-group9", "week"),
                                    height=2,
                                    width=30,
                                    text="Plot Temperature (last week) py-group10")

    button_temp_lhtgro_week = tk.Button(master=root,
                                   command=lambda: plot("Temperature", "lht-gronau", "week"),
                                   height=2,
                                   width=30,
                                   text="Plot Temperature (last week) lht-gronau")
    button_temp_lhtsax_week = tk.Button(master=root,
                                   command=lambda: plot("Temperature", "lht-saxion", "week"),
                                   height=2,
                                   width=30,
                                   text="Plot Temperature (last week) lht-saxion")
    button_temp_lhtwie_week = tk.Button(master=root,
                                   command=lambda: plot("Temperature", "lht-wierden", "week"),
                                   height=2,
                                   width=30,
                                   text="Plot Temperature (last week) lht-wierden")

    #Locations

    labelposition.pack(side="top", anchor="nw")
    button_location_saxion.pack(side="top", anchor="nw")
    button_location_wierden.pack(side="top", anchor="nw")
    button_location_gronau.pack(side="top", anchor="nw")
    button_location_lora.pack(side="top", anchor="nw")

    #Pack all temperature buttons
    button_temp_pysax.pack(side="top")
    button_temp_pywie.pack(side="top")
    button_temp_pygrp10.pack(side="top")
    button_temp_lhtgro.pack(side="top")
    button_temp_lhtsax.pack(side ="top")
    button_temp_lhtwie.pack(side ="top")

    #Pack all humidity buttons
    button_hum_lhtgro.pack(side="top")
    button_hum_lhtsax.pack(side="top")
    button_hum_lhtwie.pack(side="top")

    # Pack all pressure buttons
    button_pres_pysax.pack(side="top")
    button_pres_pywie.pack(side="top")

    # Pack all temperature buttons week
    button_temp_pysax_week.pack(side="top")
    button_temp_pywie_week.pack(side="top")
    button_temp_pygrp10_week.pack(side="top")
    button_temp_lhtgro_week.pack(side="top")
    button_temp_lhtsax_week.pack(side="top")
    button_temp_lhtwie_week.pack(side="top")

   
    root.mainloop()
