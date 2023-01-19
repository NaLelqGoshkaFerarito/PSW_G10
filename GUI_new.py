import tkinter as tk
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from mapview import *

# connect to mysql
conn = mysql.connector.connect(host="139.144.177.81", user="ADMIN", password="", database="mydatabase")
if conn.is_connected():
    print("connected")
cursor = conn.cursor()


#TODO:
# - convert datetime to better format depending on period
# - Better GUI
# - Metadata per device

###GEOGRAPHICAL POSITION

TIME = "day"


def time_period(time="day"):
    if time == "day" or time == "week" or time == "month":
        TIME = time
    else:
        TIME = "day"

"""
Function to perform a specific SQL query
"""
def SQLquery(sql_metric,sensor, period):
    metric =[]
    time = []

    cursor.execute(
        "SELECT {}, time from status where time > DATE_SUB(CURRENT_DATE(), INTERVAL 1 {}) AND device_id = '{}'".format(sql_metric,
            period, sensor))

    result = cursor.fetchall()
    for r in result:
        metric.append(r[0])
        time.append(r[1])
    return metric, time


"""
Function to plot all metric data [Temperature, Humidity, Pressure, Light]
of a specific sensor given as arguments. It will return a plot of this data over a specific period.
In this case the period options are: day/week/month(not implemented)
Possible additions: last hour / last 3 days?
"""
def plot(metric, sensor, period):
    #Create new window to plot figure in
    root = create_window()
    # TEMPERATURE
    if metric == "Temperature":
                # Only these sensors read an inside temperature
        if sensor == "py-saxion" or sensor == "py-wierden" or sensor == "py-gronau" or sensor == "py-group9" or sensor == "lht-saxion":
            temp, dates = SQLquery("temp_in", sensor, period)
        # All other sensors read an outside temperature
        else:
            temp, dates = SQLquery("temp_out", sensor, period)

        # The sensor 'lht-saxion' reads both temp_out as temp_in.
        # Thus, in this case it will get extracted specifically for a subplot.
        if sensor == 'lht-saxion':
            temp_out, dates2 = SQLquery("temp_out", "lht-saxion", period)

        # If 'lht-saxion' make a subplot of both inside and outside temperature.
            fig, ax = plt.subplots(2, sharex=True)
            plt.xticks(rotation=90)
            ax[0].plot(dates, temp)
            ax[0].set_title('Indoors Temperature detected by ' + sensor)
            ax[1].plot(dates2, temp_out)
            ax[1].set_title('Exterior Temperature detected by ' + sensor)
            ax[0].set(ylabel='Temperature (Centigrade)')
            ax[1].set(ylabel='Temperature (Centigrade)')
            if period == 'day': ax[1].set(xlabel='Time (hours)')
            elif period == 'week': ax[1].set(xlabel='Time (days)')
            elif period == 'month': ax[1].set(xlabel='Time (days)')

        # Else make a single plot of the temperature read indoors.
        else:
            fig, ax = plt.subplots()
            ax.plot(dates, temp)
            plt.xticks(rotation=90)
            ax.set_title('Indoors Temperature detected by ' + sensor)
            ax.set(ylabel='Temperature (Centigrade)')
            if period == 'day': ax.set(xlabel='Time (hours)')
            elif period == 'week': ax.set(xlabel='Time (days)')
            elif period == 'month': ax.set(xlabel='Time (days)')


    # HUMIDITY
    if metric == "Humidity":

        ### IF NOT ALL SENSORS:
        humidity, dates = SQLquery("humidity", sensor, period)

        # Plot humidity
        fig, ax = plt.subplots()
        ax.plot(dates, humidity)
        plt.xticks(rotation=90)
        ax.set_title('Relative humidity detected by ' + sensor)
        ax.set(ylabel='Relative humidity')
        if period == 'day':
            ax.set(xlabel='Time (hours)')
        elif period == 'week':
            ax.set(xlabel='Time (days)')
        elif period == 'month':
            ax.set(xlabel='Time (days)')

    # PRESSURE
    if metric == "Pressure":
        pressure, dates = SQLquery("pressure", sensor, period)

        # Plot Pressure
        fig, ax = plt.subplots()
        ax.plot(dates, pressure)
        plt.xticks(rotation=90)
        ax.set_title('Pressure detected by ' + sensor)
        ax.set(ylabel='Pressure (Pascal)')
        if period == 'day':
            ax.set(xlabel='Time (hours)')
        elif period == 'week':
            ax.set(xlabel='Time (days)')
        elif period == 'month':
            ax.set(xlabel='Time (days)')


    # LIGHT
    if metric == "Light":
       light, dates = SQLquery("light", sensor, period)

       # Plot Light
       fig, ax = plt.subplots()
       ax.plot(dates, light)
       plt.xticks(rotation=90)
       ax.set_title('Light detected by ' + sensor)
       ax.set(ylabel='Light (Lux?)')
       if period == 'day':
           ax.set(xlabel='Time (hours)')
       elif period == 'week':
           ax.set(xlabel='Time (days)')
       elif period == 'month':
           ax.set(xlabel='Time (days)')

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
    #LIGHT
    button_light_pysax = tk.Button(master=root,
                                  command=lambda: plot("Light", "py-saxion", "day"),
                                  height=2,
                                  width=30,
                                  text="Plot Light (last day) py-saxion ")
    button_light_pywie = tk.Button(master=root,
                                  command=lambda: plot("Temperature", "py-wierden", "day"),
                                  height=2,
                                  width=30,
                                  text="Plot Light (last day) py-wierden")

    button_light_pygrp10 = tk.Button(master=root,
                                    command=lambda: plot("Light", "py-group9", "day"),
                                    height=2,
                                    width=30,
                                    text="Plot Light (last day) py-group10")

    button_light_lhtgro = tk.Button(master=root,
                                   command=lambda: plot("Light", "lht-gronau", "day"),
                                   height=2,
                                   width=30,
                                   text="Plot Light (last day) lht-gronau")

    button_light_lhtwie = tk.Button(master=root,
                                   command=lambda: plot("Light", "lht-wierden", "day"),
                                   height=2,
                                   width=30,
                                   text="Plot Light (last day) lht-wierden")


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

    #HUMIDITY WEEK
    button_hum_lhtgro_week = tk.Button(master=root,
                                  command=lambda: plot("Humidity", "lht-gronau", "week"),
                                  height=2,
                                  width=30,
                                  text="Plot Humidity (last week) lht-gronau")

    button_hum_lhtsax_week = tk.Button(master=root,
                                  command=lambda: plot("Humidity", "lht-saxion", "week"),
                                  height=2,
                                  width=30,
                                  text="Plot Humidity (last week) lht-saxion")

    button_hum_lhtwie_week = tk.Button(master=root,
                                  command=lambda: plot("Humidity", "lht-wierden", "week"),
                                  height=2,
                                  width=30,
                                  text="Plot Humidity (last week) lht-wierden")
    #PRESSURE WEEK
    button_pres_pysax_week = tk.Button(master=root,
                                  command=lambda: plot("Pressure", "py-saxion", "week"),
                                  height=2,
                                  width=30,
                                  text="Plot Pressure (last week) py-saxion ")
    button_pres_pywie_week = tk.Button(master=root,
                                  command=lambda: plot("Pressure", "py-wierden", "week"),
                                  height=2,
                                  width=30,
                                  text="Plot Pressure (last week) py-wierden")
    #LIGHT WEEK
    button_light_pysax_week = tk.Button(master=root,
                                   command=lambda: plot("Light", "py-saxion", "week"),
                                   height=2,
                                   width=30,
                                   text="Plot Light (last week) py-saxion ")
    button_light_pywie_week = tk.Button(master=root,
                                   command=lambda: plot("Light", "py-wierden", "week"),
                                   height=2,
                                   width=30,
                                   text="Plot Light (last week) py-wierden")

    button_light_pygrp10_week = tk.Button(master=root,
                                     command=lambda: plot("Light", "py-group9", "week"),
                                     height=2,
                                     width=30,
                                     text="Plot Light (last week) py-group10")

    button_light_lhtgro_week = tk.Button(master=root,
                                    command=lambda: plot("Light", "lht-gronau", "week"),
                                    height=2,
                                    width=30,
                                    text="Plot Light (last week) lht-gronau")

    button_light_lhtwie_week = tk.Button(master=root,
                                    command=lambda: plot("Light", "lht-wierden", "week"),
                                    height=2,
                                    width=30,
                                    text="Plot Light (last week) lht-wierden")

    #TEMPERATURE MONTH
    button_temp_pysax_month = tk.Button(master=root,
                                  command=lambda: plot("Temperature", "py-saxion", "month"),
                                  height=2,
                                  width=30,
                                  text="Plot Temperature (last month) py-saxion ")
    button_temp_pywie_month = tk.Button(master=root,
                                  command=lambda: plot("Temperature", "py-wierden", "month"),
                                  height=2,
                                  width=30,
                                  text="Plot Temperature (last month) py-wierden")

    button_temp_pygrp10_month = tk.Button(master=root,
                                    command=lambda: plot("Temperature", "py-group9", "month"),
                                    height=2,
                                    width=30,
                                    text="Plot Temperature (last month) py-group10")

    button_temp_lhtgro_month = tk.Button(master=root,
                                   command=lambda: plot("Temperature", "lht-gronau", "month"),
                                   height=2,
                                   width=30,
                                   text="Plot Temperature (last month) lht-gronau")
    button_temp_lhtsax_month = tk.Button(master=root,
                                   command=lambda: plot("Temperature", "lht-saxion", "month"),
                                   height=2,
                                   width=30,
                                   text="Plot Temperature (last month) lht-saxion")
    button_temp_lhtwie_month = tk.Button(master=root,
                                   command=lambda: plot("Temperature", "lht-wierden", "month"),
                                   height=2,
                                   width=30,
                                   text="Plot Temperature (last month) lht-wierden")

    #HUMIDITY MONTH
    button_hum_lhtgro_month = tk.Button(master=root,
                                  command=lambda: plot("Humidity", "lht-gronau", "month"),
                                  height=2,
                                  width=30,
                                  text="Plot Humidity (last month) lht-gronau")

    button_hum_lhtsax_month = tk.Button(master=root,
                                  command=lambda: plot("Humidity", "lht-saxion", "month"),
                                  height=2,
                                  width=30,
                                  text="Plot Humidity (last month) lht-saxion")

    button_hum_lhtwie_month = tk.Button(master=root,
                                  command=lambda: plot("Humidity", "lht-wierden", "month"),
                                  height=2,
                                  width=30,
                                  text="Plot Humidity (last month) lht-wierden")
    #PRESSURE MONTH
    button_pres_pysax_month = tk.Button(master=root,
                                  command=lambda: plot("Pressure", "py-saxion", "month"),
                                  height=2,
                                  width=30,
                                  text="Plot Pressure (last month) py-saxion ")
    button_pres_pywie_month = tk.Button(master=root,
                                  command=lambda: plot("Temperature", "py-wierden", "month"),
                                  height=2,
                                  width=30,
                                  text="Plot Pressure (last month) py-wierden")
    #LIGHT MONTH
    button_light_pysax_month = tk.Button(master=root,
                                   command=lambda: plot("Light", "py-saxion", "month"),
                                   height=2,
                                   width=30,
                                   text="Plot Light (last month) py-saxion ")
    button_light_pywie_month = tk.Button(master=root,
                                   command=lambda: plot("Temperature", "py-wierden", "month"),
                                   height=2,
                                   width=30,
                                   text="Plot Light (last month) py-wierden")

    button_light_pygrp10_month = tk.Button(master=root,
                                     command=lambda: plot("Light", "py-group9", "month"),
                                     height=2,
                                     width=30,
                                     text="Plot Light (last month) py-group10")

    button_light_lhtgro_month = tk.Button(master=root,
                                    command=lambda: plot("Light", "lht-gronau", "month"),
                                    height=2,
                                    width=30,
                                    text="Plot Light (last month) lht-gronau")

    button_light_lhtwie_month = tk.Button(master=root,
                                    command=lambda: plot("Light", "lht-wierden", "month"),
                                    height=2,
                                    width=30,
                                    text="Plot Light (last month) lht-wierden")

   # #Pack all temperature buttons
   # button_temp_pysax.pack(side="top")
   # button_temp_pywie.pack(side="top")
   # button_temp_pygrp10.pack(side="top")
   # button_temp_lhtgro.pack(side="top")
   # button_temp_lhtsax.pack(side ="top")
   # button_temp_lhtwie.pack(side ="top")

   # #Pack all humidity buttons
   # button_hum_lhtgro.pack(side="top")
   # button_hum_lhtsax.pack(side="top")
   # button_hum_lhtwie.pack(side="top")

   # # Pack all pressure buttons
   # button_pres_pysax.pack(side="top")
   # button_pres_pywie.pack(side="top")

   # # Pack all light buttons
   # button_light_pywie.pack(side="top")
   # button_light_pysax.pack(side="top")
   # button_light_pygrp10.pack(side="top")
   # button_light_lhtwie.pack(side="top")
   # button_light_lhtgro.pack(side="top")
#
   # # Pack all temperature buttons week
   # button_temp_pysax_week.pack(side="top")
   # button_temp_pywie_week.pack(side="top")
   # button_temp_pygrp10_week.pack(side="top")
   # button_temp_lhtgro_week.pack(side="top")
   # button_temp_lhtsax_week.pack(side="top")
   # button_temp_lhtwie_week.pack(side="top")
#
   # # Pack all humidity buttons week
   # button_hum_lhtgro_week.pack(side="top")
   # button_hum_lhtsax_week.pack(side="top")
   # button_hum_lhtwie_week.pack(side="top")
#
   # # Pack all pressure buttons week
   # button_pres_pysax_week.pack(side="top")
   # button_pres_pywie_week.pack(side="top")
#
   # # pack all light week
   # button_light_pysax_week.pack(side="top")
   # button_light_pywie_week.pack(side="top")
   # button_light_pygrp10_week.pack(side="top")
   # button_light_lhtwie_week.pack(side="top")
   # button_light_lhtgro_week.pack(side="top")

    # Pack all temperature buttons month
    button_temp_pysax_week.pack(side="top")
    button_temp_pywie_week.pack(side="top")
    button_temp_pygrp10_week.pack(side="top")
    button_temp_lhtgro_week.pack(side="top")
    button_temp_lhtsax_week.pack(side="top")
    button_temp_lhtwie_week.pack(side="top")

    # Pack all humidity buttons month
    button_hum_lhtgro_month.pack(side="top")
    button_hum_lhtsax_month.pack(side="top")
    button_hum_lhtwie_month.pack(side="top")

    # Pack all pressure buttons month
    button_pres_pysax_month.pack(side="top")
    button_pres_pywie_month.pack(side="top")

    # pack all light month
    button_light_pysax_month.pack(side="top")
    button_light_pywie_month.pack(side="top")
    button_light_pygrp10_month.pack(side="top")
    button_light_lhtwie_month.pack(side="top")
    button_light_lhtgro_month.pack(side="top")

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

    button_day = tk.Button(master=root,
                           command=lambda: time_period("day"),
                           height=2,
                           width=30,
                           text="Day"
                           )
    button_week = tk.Button(master=root,
                            command=lambda: time_period("week"),
                            height=2,
                            width=30,
                            text="Week"
                            )
    button_month = tk.Button(master=root,
                             command=lambda: time_period("month"),
                             height=2,
                             width=30,
                             text="Month"
                             )

    # Locations

    labelposition.pack(side="top", anchor="nw")
    button_location_saxion.pack(side="top", anchor="nw")
    button_location_wierden.pack(side="top", anchor="nw")
    button_location_gronau.pack(side="top", anchor="nw")
    button_location_lora.pack(side="top", anchor="nw")
    button_day.pack(side="top", anchor="nw")
    button_week.pack(side="top", anchor="nw")
    button_month.pack(side="top", anchor="nw")

    root.mainloop()
