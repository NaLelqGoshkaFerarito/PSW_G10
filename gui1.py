import tkinter as tk
import pandas as pd
import math
import random
import matplotlib.pyplot as plt
from tkcalendar import Calendar
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from datetime import date, timedelta, datetime
import tkintermapview
import babel.numbers
from tkinter import ttk
import mysql.connector



sensors = ['sensor1', 'sensor2', 'sensor3']                      #sensor ids
metrics = ['Temperature', 'Humidity', 'Pressure', 'Light']       
colors = ['red', 'orange', 'green', 'cyan', 'blue', 'purple']    


numbet_of_points = 48

def datelist(n):
    dates = []
    count = 0
    today = date.today()
    for i in range(n):
        dates.append(datetime(today.year, today.month, today.day, i % 24))
        count += 1
        if count == 24:
            today = today + timedelta(1)
            count = 0
    return dates
    


            

def randomlist(n, metric):
    rand_list=[]                                                   
    if metric == 'Temperature':
        for i in range(n):
            rand_list.append(random.random() * 7 + 15 * math.sin(i/5))
        return rand_list
    elif metric == 'Humidity':
        for i in range(n):
            rand_list.append(random.random())
        return rand_list
    else:
        for i in range(n):
            rand_list.append(random.random() * 7 + 15 * math.sin(i/5))
        return rand_list


locations = {'Saxion':(52.221361, 6.886444), 'Gronau':(53.221361, 6.886444), 'Wierden' : (52.221361, 7.886444)}



    

def mapview(x):
    top = tk.Toplevel()
    location = list(locations)[x]
    top.title(f'Map view app - {location}')
    coords = locations[location]
    top.geometry('800x600')
    my_label = tk.LabelFrame(top)
    my_label.pack(pady=20)
    map_widget = tkintermapview.TkinterMapView(top, width=800,height=600,corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    marker = map_widget.set_marker(coords[0], coords[1], text=f"{location} Sensor")
    map_widget.set_position(coords[0], coords[1], marker=True)


class SensorData:   #class that contains all values for given sensors in given period
    def __init__(self, period, sensorid):
        self.start = period[0]
        self.end = period[-1]
        self.sensor_id = sensorid
        self.dataframe = pd.DataFrame({'Time':datelist(numbet_of_points)})
        for metric in metrics:
            self.dataframe[metric] = randomlist(numbet_of_points, metric=metric)
    
def update_label(self):
    self.label.configure(text = (self.period[0] + " - " + self.period[-1]))


def onselect(window, evt = None):  #triggers when listbox choice is altered
    window.changeplot()
    window.changetext()
    
def grad_date(window, button, evt = None):
    if(button == 0):
        dt1 = datetime.strptime(window.period[-1], "%d/%m/%Y")
        dt2 = datetime.strptime(window.calendar.get_date(), "%d/%m/%Y")
        if(dt2 >= dt1):
            return
    elif(button == 1):
        dt1 = datetime.strptime(window.period[0], "%d/%m/%Y")
        dt2 = datetime.strptime(window.calendar.get_date(), "%d/%m/%Y")
        if(dt2 <= dt1):
            return
    if(button == 0):
        window.period[0] = window.calendar.get_date()
    elif(button == 1):
        window.period[-1] = window.calendar.get_date()
    update_label(window)


def clear_frame(frame): #deletes everything in frame
    for widgets in frame.winfo_children():
        widgets.destroy()


def callback(event, x):
    mapview(x)

class MyWindow:  #main window
    def __init__(self, master=None ,*args, **kwargs):
        #period
        self.period = [date.today().strftime("%d/%m/%Y"), (date.today() + timedelta(1)).strftime("%d/%m/%Y")]
        
        #sensor list
        self.sensors_last = []
        for sensor in sensors:
            self.sensors_last.append(SensorData(self.period, sensor))

        #tab manager
        tabControl = ttk.Notebook(master)

        #frames
        self.frame0 = tk.Frame(master=master)
        self.frame0.grid(row = 0, column = 0)

        self.frame1 = tk.Frame(master=master)
        self.frame1.grid(row=0, column=1, rowspan=2)

        self.frame2 = tk.Frame(master=master)
        self.frame2.grid(row=0, column=2)

        self.frame3 = tk.Frame(master)
        self.frame3.grid(row = 1, column = 0)

        self.frame4 = tk.Frame(master)
        self.frame4.grid(row = 1, column=1)

        self.frame5 = tk.Frame(self.frame0)
        self.frame5.grid(row = 0, column=1)
        
        #information text
        self.text = tk.Text(self.frame3, width = 40, height = 10)
        self.text.grid(row=0, column=0, sticky='s')

        #calendar
        self.calendar = Calendar(self.frame5, selectmode = 'day',
               year = date.today().year, month = date.today().month, date_pattern = 'dd/mm/yyyy',
               day = date.today().day)
 
        self.calendar.grid(row = 0, column = 0, columnspan =2)


        #button to specify period
        self.start_button = tk.Button(self.frame5, text = "Start date", command = lambda: grad_date(self, 0))
        self.start_button.grid(row = 1, column = 0)

        self.end_button = tk.Button(self.frame5, text = "End date", command = lambda:grad_date(self, 1))
        self.end_button.grid(row=1, column=1)

        #label that shows current period

        self.label = tk.Label(self.frame5, text = "")
        self.label.grid(row = 2, column = 0, columnspan=2)
        update_label(self)

  
        #scroll bar
        self.sb = tk.Scrollbar(self.frame3)
        self.sb.grid(row = 0, column = 1, sticky='ns')
        self.sb.config(command = self.text.yview)
        self.text.config(yscrollcommand = self.sb.set)

        #listbox
        self.lb = tk.Listbox(self.frame0, selectmode=tk.MULTIPLE)
        for i in range(len(self.sensors_last)):
            self.lb.insert('end', self.sensors_last[i].sensor_id)
        self.lb.grid(row=0, column=0, sticky='ns')
        self.lb.bind('<<ListboxSelect>>', lambda event: onselect(self, event))
        self.lb.selection_set(first = 0)
    

        #plot
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)###
        self.line = FigureCanvasTkAgg(self.figure, self.frame1)
        self.figure.set_tight_layout(True)  
        self.toolbar = NavigationToolbar2Tk(self.line, self.frame1, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.grid(row = 1, column = 0)
        
        self.line.get_tk_widget().grid(row=0, column=0, sticky = 'swen')

        #radio button
        self.r_button_val = tk.IntVar()
        for i in range(len(metrics)):
            tk.Radiobutton(self.frame1, text = f'{metrics[i]}', variable = self.r_button_val, value = i, command=lambda: onselect(self)).grid(row=i + 1 + 1, column=0)

        #tab


        #status bar
        self.status = tk.Label(master, text="Status bar that shows important information", bd = 1, relief='sunken', anchor = 'e')
        self.status.grid(row=2, column=0, columnspan=5, sticky='we')

        onselect(self)


        

    def changeplot(self): #updates plot
        sensors_ = []
        sensor_names = []
        self.ax.clear()
        clear_frame(self.frame2)
        for item in self.lb.curselection():
            sensors_.append(item)
            sensor_names.append(sensors[item])
        plt.clf()
        count = 0
        for sensor in sensors_:
            dff = self.sensors_last[sensor]
            dff = dff.dataframe[['Time', metrics[self.r_button_val.get()]]].groupby('Time').sum()#[dff.dataframe['Time'] > self.period[0] & dff.dataframe['Time'] < self.period[1]].groupby('Time').sum()          #['Time', metrics[self.r_button_val.get()]]].groupby('Time').sum()
            dff.plot(kind='line', legend=False, ax=self.ax, color=colors[sensor], marker='o', fontsize=10)
            self.ax.legend(sensor_names, loc=0, frameon=True)
            legend = tk.Label(self.frame2, text = self.sensors_last[sensor].sensor_id, fg = colors[sensor], font=20)
            legend.grid(row = count, column = 0)
            def make_lambda(x):
                return lambda ev:callback(ev, x)
            legend.bind("<Button-1>", make_lambda(sensor))
            count += 1
        self.ax.set_title(f'Time Vs. {metrics[self.r_button_val.get()]}')
        self.ax.grid(b = True)
        self.line.draw()
        
# for i in range(2):
#     root.bind("<KeyPress-%c>" % keys[i],lambda ev:SomeFunc(ev,i))

# for i in range(2):
#     def make_lambda(x):
#         return lambda ev:SomeFunc(ev,x)
#     root.bind("<KeyPress-%c>" % keys[i], make_lambda(i))

    def changetext(self):  #updates text
        self.text.config(state='normal')
        self.text.delete("1.0", tk.END)
        sensors_ = []
        for item in self.lb.curselection():
            sensors_.append(self.sensors_last[item].sensor_id)
        for i in sensors_:
            self.text.insert(tk.END, f"{i} last measures:\n")
            for j in metrics:
                df = self.sensors_last[sensors.index(i)].dataframe
                self.text.insert(tk.END, f"{j} - {df.iloc[-1, df.columns.get_loc(j)]}\n")#df.iloc[-1, df.columns.get_loc('City')]
            self.text.insert(tk.END, '------------------------------\n')
        self.text.config(state = 'disabled')

    


    
    
def main():
    # conn = mysql.connector.connect(host="139.144.177.81", user="jesse", password="Kaas@1234", database="mydatabase")
    # if conn.is_connected():
    #     print(1)
    root = tk.Tk()
    #second = tk.Tk()
    app = MyWindow(master = root)
    #app2 = MyWindow(master = second)
    root.mainloop()

if __name__ == '__main__':
    main()

