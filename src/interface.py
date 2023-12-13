# Fichier app.py

from flask import Flask, jsonify, render_template
from threading import Thread
import time
import psutil
from pydantic import BaseModel

app = Flask(__name__)

class RAMInfo(BaseModel):
    total: float
    available: float
    used: float
    percent: float

class Hdd(BaseModel):
    total: float
    used: float 
    free: float
    percent: float

max_points = 100

cpu_usages = []
cpu_times = []
ram_usages = []
ram_times = []
hdd_usages = []
hdd_times = []

def get_cpu_usage():
    return psutil.cpu_percent()

def get_ram_info():
    ram = psutil.virtual_memory()
    ram_data = RAMInfo(
        total=ram.total / (1024 ** 3),  # Converti en Go
        available=ram.available / (1024 ** 3),
        used=ram.used / (1024 ** 3),
        percent=ram.percent
    )
    return ram_data

def get_hdd_info():
    hdd = psutil.disk_usage('/')
    hdd_data = Hdd(
        total=hdd.total / (1024 ** 3),  # Converti en Go
        used=hdd.used / (1024 ** 3),
        free=hdd.free / (1024 ** 3),
        percent=hdd.percent
    )
    return hdd_data

def update_cpu_data():
    global cpu_usages, cpu_times
    while True:
        cpu_usage = get_cpu_usage()
        cpu_usages.append(cpu_usage)
        cpu_times.append(time.time())

        if len(cpu_usages) > max_points:
            cpu_usages = cpu_usages[-max_points:]
            cpu_times = cpu_times[-max_points:]

        time.sleep(1)

def update_ram_data():
    global ram_usages, ram_times
    while True:
        ram_info = get_ram_info()
        ram_usages.append(ram_info.percent)
        ram_times.append(time.time())

        if len(ram_usages) > max_points:
            ram_usages = ram_usages[-max_points:]
            ram_times = ram_times[-max_points:]

        time.sleep(1)

def update_hdd_data():
    global hdd_usages, hdd_times
    while True:
        hdd_info = get_hdd_info()
        hdd_usages.append(hdd_info.percent)
        hdd_times.append(time.time())

        if len(hdd_usages) > max_points:
            hdd_usages = hdd_usages[-max_points:]
            hdd_times = hdd_times[-max_points:]

        time.sleep(1)

@app.route('/cpu/graph')
def plot_cpu_graph():
    return render_template('cpu_graph.html', max_points=max_points)

@app.route('/ram/graph')
def plot_ram_graph():
    return render_template('ram_graph.html', max_points=max_points)

@app.route('/hdd/graph')
def plot_hdd_graph():
    return render_template('hdd_graph.html', max_points=max_points)

@app.route('/cpu/data')
def get_cpu_data():
    global cpu_usages, cpu_times
    return jsonify(usages=cpu_usages, times=cpu_times)

@app.route('/ram/data')
def get_ram_data():
    global ram_usages, ram_times
    return jsonify(usages=ram_usages, times=ram_times)

@app.route('/hdd/data')
def get_hdd_data():
    global hdd_usages, hdd_times
    return jsonify(usages=hdd_usages, times=hdd_times)

# Fichier app.py

from flask import Flask, jsonify, render_template
from threading import Thread
import time
import psutil
from pydantic import BaseModel

app = Flask(__name__)

class RAMInfo(BaseModel):
    total: float
    available: float
    used: float
    percent: float

class Hdd(BaseModel):
    total: float
    used: float 
    free: float
    percent: float

max_points = 100

cpu_usages = []
cpu_times = []
ram_usages = []
ram_times = []
hdd_usages = []
hdd_times = []

def get_cpu_usage():
    return psutil.cpu_percent()

def get_ram_info():
    ram = psutil.virtual_memory()
    ram_data = RAMInfo(
        total=ram.total / (1024 ** 3),  # Converti en Go
        available=ram.available / (1024 ** 3),
        used=ram.used / (1024 ** 3),
        percent=ram.percent
    )
    return ram_data

def get_hdd_info():
    hdd = psutil.disk_usage('/')
    hdd_data = Hdd(
        total=hdd.total / (1024 ** 3),  # Converti en Go
        used=hdd.used / (1024 ** 3),
        free=hdd.free / (1024 ** 3),
        percent=hdd.percent
    )
    return hdd_data

def update_cpu_data():
    global cpu_usages, cpu_times
    while True:
        cpu_usage = get_cpu_usage()
        cpu_usages.append(cpu_usage)
        cpu_times.append(time.time())

        if len(cpu_usages) > max_points:
            cpu_usages = cpu_usages[-max_points:]
            cpu_times = cpu_times[-max_points:]

        time.sleep(1)

def update_ram_data():
    global ram_usages, ram_times
    while True:
        ram_info = get_ram_info()
        ram_usages.append(ram_info.percent)
        ram_times.append(time.time())

        if len(ram_usages) > max_points:
            ram_usages = ram_usages[-max_points:]
            ram_times = ram_times[-max_points:]

        time.sleep(1)

def update_hdd_data():
    global hdd_usages, hdd_times
    while True:
        hdd_info = get_hdd_info()
        hdd_usages.append(hdd_info.percent)
        hdd_times.append(time.time())

        if len(hdd_usages) > max_points:
            hdd_usages = hdd_usages[-max_points:]
            hdd_times = hdd_times[-max_points:]

        time.sleep(1)

@app.route('/cpu/graph')
def plot_cpu_graph():
    return render_template('cpu_graph.html', max_points=max_points)

@app.route('/ram/graph')
def plot_ram_graph():
    return render_template('ram_graph.html', max_points=max_points)

@app.route('/hdd/graph')
def plot_hdd_graph():
    return render_template('hdd_graph.html', max_points=max_points)

@app.route('/cpu/data')
def get_cpu_data():
    global cpu_usages, cpu_times
    return jsonify(usages=cpu_usages, times=cpu_times)

@app.route('/ram/data')
def get_ram_data():
    global ram_usages, ram_times
    return jsonify(usages=ram_usages, times=ram_times)

@app.route('/hdd/data')
def get_hdd_data():
    global hdd_usages, hdd_times
    return jsonify(usages=hdd_usages, times=hdd_times)

# Votre code Flask précédent

@app.route('/ram/stats')
def display_ram_stats():
    ram_info = get_ram_info()  # Obtention des données de RAM (peut être remplacé par votre fonction)
    ram_stats = {
        'total': ram_info.total,
        'available': ram_info.available,
        'used': ram_info.used,
        'percent': ram_info.percent
    }
    return render_template('ram_stats.html', ram_stats=ram_stats)  # Passer les données à ram_stats.html



if __name__ == '__main__':
    cpu_thread = Thread(target=update_cpu_data)
    cpu_thread.daemon = True
    cpu_thread.start()

    ram_thread = Thread(target=update_ram_data)
    ram_thread.daemon = True
    ram_thread.start()

    hdd_thread = Thread(target=update_hdd_data)
    hdd_thread.daemon = True
    hdd_thread.start()

    app.run(debug=True)