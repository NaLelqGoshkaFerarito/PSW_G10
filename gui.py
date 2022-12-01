import tkinter as tk
import pandas as pd
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import webbrowser

sensor1 = []
sensor2 = []
sensor1humidity = []
time = []
for i in range(24):
    sensor1.append(math.sin(i/5) * 5 + 14)
    sensor2.append(math.cos(i/5) * 5 + 13)
    sensor1humidity.append(i * 4)
    time.append(i)


data = {'Temperature': sensor1,
         'Humidity' : sensor1humidity,        
         'Time': time
         }
df = pd.DataFrame(data)

data2 = {'Temperature': sensor2,
         'Humidity' : sensor1humidity,        
         'Time': time
         }
df2 = pd.DataFrame(data2)

dfs = [df, df2]
root = tk.Tk()

def changeplot(line, frame, number):

    if number == 0:
    
        plt.clf()
        dff = frame[['Time', 'Temperature']].groupby('Time').sum()
        dff.plot(kind='line', legend=True, ax=ax, color='r', marker='o', fontsize=10)
        
        ax.set_title('Time Vs. Temperature')
        line.draw()
        ax.clear()
    
    elif number == 1:
    
        plt.clf()
        dff = frame[['Time', 'Humidity']].groupby('Time').sum()
        dff.plot(kind='line', legend=True, ax=ax, color='g', marker='o', fontsize=10)
        ax.set_title('Time Vs. Humidity')
        line.draw()
        ax.clear()
    
def callback(url):
    webbrowser.open_new(url)

def onselect(evt):
    # Note here that Tkinter passes an event object to onselect()
    w = evt.widget
    index = int(w.curselection()[0])
    changeplot(line, dfs[index], r.get())


    


# figure = plt.Figure(figsize=(6,5), dpi=100)
# ax = figure.add_subplot(111)
# chart_type = FigureCanvasTkAgg(figure, root)
# chart_type.get_tk_widget().pack()
# df = df[['First Column','Second Column']].groupby('First Column').sum()
# df.plot(kind='Chart Type such as bar', legend=True, ax=ax)
# ax.set_title('The Title for your chart')


chosen = 0
items = ['sensor1', 'sensor2']



listbox = tk.Listbox(root)
listbox.insert('end', 'sensor1')
listbox.insert('end', 'sensor2')
listbox.grid(row=0, column=0)
listbox.bind('<<ListboxSelect>>', onselect)

#root.geometry('800x600+10+10')

frame = tk.Frame(root)
frame.grid(row=0, column=1, rowspan=2, sticky='e')

status = tk.Label(root, text="Updated 2 minutes ago (not really)", bd = 1, relief='sunken', anchor = 'e')
status.grid(row=2, column=0, columnspan=2, sticky='we')

figure = plt.Figure(figsize=(5, 4), dpi=100)
ax = figure.add_subplot(111)
line = FigureCanvasTkAgg(figure, frame)
line.get_tk_widget().grid(row=0, column=0)#pack(side=tk.LEFT, fill=tk.BOTH)
# df3 = df2[['Time', 'Temperature']].groupby('Time').sum()
# df3.plot(kind='line', legend=True, ax=ax2, color='r', marker='o', fontsize=10)
# ax2.set_title('Time Vs. Temperature')

r = tk.IntVar()
#r.set(0)
tk.Radiobutton(frame, text = 'Temperature', variable = r, value = 0, command=lambda: changeplot(line, dfs[items.index(listbox.get('anchor'))], r.get())).grid(row=1, column=0)
tk.Radiobutton(frame, text = 'Humidity', variable = r, value = 1, command=lambda: changeplot(line, dfs[items.index(listbox.get('anchor'))], r.get())).grid(row=2, column=0)

text = tk.Text(root, height = 3)
text.grid(row=1, column=0)
text.insert(tk.END, "Temperature - " + str(sensor1[-1]))

link1 = tk.Label(frame, text="Coordinates: 52°13'16.9\"N 6°53'11.2\"E", fg="blue", cursor="hand2")
link1.grid(row=3, column=0)
link1.bind("<Button-1>", lambda e: callback("https://www.google.com/maps/place/52°13'16.9\"N+6°53'11.2\"E/"))
root.mainloop()