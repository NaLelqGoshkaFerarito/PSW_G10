import tkinter as tk
import pandas as pd
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser


sensors = ['sensor1', 'sensor2'] 
metrics = ['Temperature', 'Humidity']
period = [0, 1]  #list of dates, measures between these dates gonna be plotted
number = 0    #represent chosen metrics if 0 it will plot temperature and so on



class SensorData:   #class that contains all values for given sensors in given period
    def __init__(self, period, sensorid):
        self.start = period[0]
        self.end = period[-1]
        self.sensor_id = sensorid
        self.dataframe = pd.DataFrame({'Temperature' : random.sample(range(15, 25), 4), 'Time' : range(1, 5)})


def onselect(evt, window):
    window.changeplot(number, period)
    window.changetext()
    



class MyWindow:  #main window
    def __init__(self, master=None ,*args, **kwargs):
        #frames
        self.frame0 = tk.Frame(master=master)
        self.frame0.grid(row = 0, column = 0)

        self.frame1 = tk.Frame(master=master)
        self.frame1.grid(row=0, column=1)
        #listbox

        self.lb = tk.Listbox(self.frame0, selectmode=tk.MULTIPLE)
        for i in range(len(sensors)):
            self.lb.insert('end', sensors[i])
        self.lb.grid(row=0, column=0, sticky='wnes')
        self.lb.bind('<<ListboxSelect>>', lambda event: onselect(event, self))

        #plot
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.line = FigureCanvasTkAgg(self.figure, self.frame1)
        self.line.get_tk_widget().grid(row=0, column=0)

        #radio button
        self.r_button_val = tk.IntVar()
        for i in range(len(metrics)):
            tk.Radiobutton(self.frame1, text = f'{metrics[i]}', variable = self.r_button_val, value = i).grid(row=i + 1, column=0)

        #status bar
        self.status = tk.Label(master, text="Updated 2 minutes ago (not really)", bd = 1, relief='sunken', anchor = 'e')
        self.status.grid(row=2, column=0, columnspan=2, sticky='we')


        #information text
        self.text = tk.Text(self.frame0, height = 3)
        self.text.grid(row=1, column=0, sticky='s')
    
    

    def changeplot(self, number, period):
        sensors_ = []
        for item in self.lb.curselection():
            sensors_.append(item)
            print(item)
        plt.clf()
        for sensor in sensors_:
            dff = SensorData(period, sensors[sensor])
            dff = dff.dataframe[['Time', metrics[number]]].groupby('Time').sum()
            dff.plot(kind='line', legend=True, ax=self.ax, color='r', marker='o', fontsize=10)
        self.ax.set_title(f'Time Vs. {metrics[number]}')
        self.line.draw()
        self.ax.clear()


    def changetext(self):
        self.text.config(state='normal')
        self.text.delete("1.0", tk.END)
        sensors_ = []
        for item in self.lb.curselection():
            sensors_.append(sensors[item])
        for i in sensors_:
            self.text.insert(tk.END, f"{i} last measures:\n")
            for j in metrics:
                self.text.insert(tk.END, f"{j} - TO DO LATER\n")


    
    
    


root = tk.Tk()
app = MyWindow(master = root)

root.mainloop()
