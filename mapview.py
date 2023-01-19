import tkintermapview
import tkinter as tk
import mysql

conn = mysql.connector.connect(host="139.144.177.81", user="ADMIN", password="", database="mydatabase")
if conn.is_connected():
    print("connected")
cursor = conn.cursor()


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
    # set_position(latitude, longitude)
    map_widget.set_position(float(longitude), float(latitude), marker=True)
    # marker_lora.set_address("Lora Sensor", marker=True)


def location(sensor):
    cursor.execute(
        "select longitude, latitude from device where name = %s", (sensor,))
    result = cursor.fetchall()
    return result[0]
