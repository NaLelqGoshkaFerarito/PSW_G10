import tkinter as tk
import pandas as pd
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser
import tkintermapview


sensors = ['sensor1', 'sensor2', 'sensor3'] #sensor ids
metrics = ['Temperature', 'Humidity']
colors = ['red', 'orange', 'green', 'cyan', 'blue', 'purple']
period = [0, 1]  #list of dates, measures between these dates gonna be plotted
number = 0    #represent chosen metrics if 0 it will plot temperature and so on

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


class SensorData:   #class that contains all values for given sensors in given period
    def __init__(self, period, sensorid):
        self.start = period[0]
        self.end = period[-1]
        self.sensor_id = sensorid
        self.dataframe = pd.DataFrame({'Time':range(1, 25)})
        for metric in metrics:
            self.dataframe[metric] = randomlist(24, metric=metric)
    
def callback(event, count):
    count += 1
    if count == 1:
        mapviewSaxion()
    if count == 2:
        mapviewGronau()
    if count == 3:    
        mapviewWierden()
    if count == 4:    
        mapviewLora()

def onselect(window, evt = None):  #triggers when listbox choice is altered
    window.changeplot()
    window.changetext()
    
def clear_frame(frame): #deletes everything in frame
    for widgets in frame.winfo_children():
        widgets.destroy()


class MyWindow:  #main window
    def __init__(self, master=None ,*args, **kwargs):
        #period
        self.period = [0, 1]
        
        #sensor list
        self.sensors_last = []
        for sensor in sensors:
            self.sensors_last.append(SensorData(self.period, sensor))


        #frames
        self.frame0 = tk.Frame(master=master)
        self.frame0.grid(row = 0, column = 0)

        self.frame1 = tk.Frame(master=master)
        self.frame1.grid(row=0, column=1)

        self.frame2 = tk.Frame(master=master)
        self.frame2.grid(row=0, column=2)
        
        #information text
        self.text = tk.Text(self.frame0, height = 3)
        self.text.grid(row=1, column=0, sticky='s')

        #listbox
        self.lb = tk.Listbox(self.frame0, selectmode=tk.MULTIPLE)
        for i in range(len(self.sensors_last)):
            self.lb.insert('end', self.sensors_last[i].sensor_id)
        self.lb.grid(row=0, column=0, sticky='wnes')
        self.lb.bind('<<ListboxSelect>>', lambda event: onselect(self, event))

        #plot
        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)###
        self.line = FigureCanvasTkAgg(self.figure, self.frame1)
        
        self.line.get_tk_widget().grid(row=0, column=0)

        #radio button
        self.r_button_val = tk.IntVar()
        for i in range(len(metrics)):
            tk.Radiobutton(self.frame1, text = f'{metrics[i]}', variable = self.r_button_val, value = i, command=lambda: onselect(self)).grid(row=i + 1, column=0)

        #status bar
        self.status = tk.Label(master, text="Status bar that shows important information", bd = 1, relief='sunken', anchor = 'e')
        self.status.grid(row=2, column=0, columnspan=5, sticky='we')

        #mapview menu

        """""
        #mapview button Saxion
        locationbutton = tk.Button(
        self.frame2,        
        text='View',
        command=mapviewSaxion)
        locationbutton.pack(side='right')
        
"""
    def changeplot(self): #updates plot
        #global count
        print(self.r_button_val.get())
        sensors_ = []
        clear_frame(self.frame2)
        for item in self.lb.curselection():
            sensors_.append(item)
        plt.clf()
        count = 0
        for sensor in sensors_:
            dff = self.sensors_last[sensor]
            dff = dff.dataframe[['Time', metrics[self.r_button_val.get()]]].groupby('Time').sum()
            dff.plot(kind='line', legend=False, ax=self.ax, color=colors[sensor], marker='o', fontsize=10)
            legend = tk.Label(self.frame2, text = self.sensors_last[sensor].sensor_id, fg = colors[sensor], font=20)
            legend.grid(row = count, column = 0)
            def make_lambda(x):
                return lambda ev:callback(ev, x)
            legend.bind(f"<Button-{1}>", make_lambda(count))
            count += 1
        self.ax.set_title(f'Time Vs. {metrics[self.r_button_val.get()]}')
        self.ax.grid(b = True)
        self.line.draw()
        self.ax.clear()


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

###create mapview
    
def mapviewSaxion():
    top = tk.Toplevel()
    top.title('Map view app - Saxion')
    top.geometry('600x400')
    my_label = tk.LabelFrame(top)
    my_label.pack(pady=20)
    map_widget = tkintermapview.TkinterMapView(top, width=800,height=600,corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    marker_Saxion = map_widget.set_marker(52.221361,6.886444, text="Saxion Sensor")
    map_widget.set_address("Saxion Sensor", marker=True)
    print(marker_Saxion.position)
    

def mapviewGronau():
    top = tk.Toplevel()
    top.title('Map view app - Gronau')
    top.geometry('600x400')
    my_label = tk.LabelFrame(top)
    my_label.pack(pady=20)
    map_widget = tkintermapview.TkinterMapView(top, width=800,height=600,corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    marker_Gronau = map_widget.set_marker(52.221361,6.886444, text="Gronau Sensor")
    map_widget.set_address("Gronau Sensor", marker=True)
    print(marker_Gronau.position)
        
def mapviewWierden():
    top = tk.Toplevel()
    top.title('Map view app - Wierden')
    top.geometry('600x400')
    my_label = tk.LabelFrame(top)
    my_label.pack(pady=20)
    map_widget = tkintermapview.TkinterMapView(top, width=800,height=600,corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    marker_Wierden = map_widget.set_marker(52.221361,6.886444, text="Wierden Sensor")
    map_widget.set_position(52.221361,6.886444, marker=True)
   # print(marker_Wierden.position)

def mapviewLora():
    top = tk.Toplevel()
    top.title('Map view app - Lora')
    top.geometry('600x400')
    my_label = tk.LabelFrame(top)
    my_label.pack(pady=20)
    map_widget = tkintermapview.TkinterMapView(top, width=800,height=600,corner_radius=0)
    map_widget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    marker_Lora = map_widget.set_marker(52.221361,6.886444, text="Lora Sensor")
    marker_Lora.position(52.221361,6.886444, marker=True)
    print(marker_Lora.position)


    
    
    


root = tk.Tk()
app = MyWindow(master = root)

root.mainloop()

