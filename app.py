from flask import Flask, redirect, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
from flask import Response
from data_connection import insert_data, display_data, show_graph, delete_data

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/data/", methods=["POST"])
def update_data():
    if request.form.get('date1') == '1':
        insert_data(0)
    if request.form.get('date2') == '1':
        insert_data(1)
    if request.form.get('date3') == '1':
        insert_data(2)
    
    return redirect("/")

@app.route("/remove/", methods=["POST"])
def remove_data():
    if request.form.get('date1') == '1':
        delete_data(0)
    if request.form.get('date2') == '1':
        delete_data(1)
    if request.form.get('date3') == '1':
        delete_data(2)
    
    return redirect("/")

@app.route("/graph" )
def get_graph():
    fig = show_graph()
    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route("/current")
def show_data():
    return display_data()