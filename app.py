from flask import Flask, redirect, render_template, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import BytesIO
from flask import Response, make_response, session
from alch_conn import increment_data, fetch_data, show_graph, decrement_data

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/data/", methods=["POST"])
def update_data():
    past_choices = get_past(request.cookies)
    if past_choices == None:
        past_choices = []
    choices = form_data(request.form.to_dict(), past_choices)
    increment_data(choices)

    resp = make_response(redirect("/"))
    for val in choices:
        resp.set_cookie(str(val), 'true')
    return resp

@app.route("/remove/", methods=["POST"])
def remove_data():
    past_choices = get_past(request.cookies)
    choices = form_data(request.form.to_dict(), eval(past_choices))
    decrement_data(choices)

    resp = make_response(redirect("/"))
    for val in choices:
        resp.set_cookie(str(val), 'true')
    return resp

@app.route("/graph" )
def get_graph():
    fig = show_graph()
    output = BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route("/current")
def show_data():
    return fetch_data()

# Helper function to translate form data into list if the choice is not in the past choices
def form_data(form_dict, past_choices):
    choices = []
    if form_dict.get('date1') == '1' and 'date1' not in past_choices:
        choices.append(0)
    if form_dict.get('date2') == '1' and 'date2' not in past_choices:
        choices.append(1)
    if form_dict.get('date3') == '1' and 'date3' not in past_choices:
        choices.append(2)
    return choices

def set_true(choices):
    past = {0: False, 1: False, 2: False}
    for val in choices:
        past[val] = True
    return str(past)

def set_false(choices):
    past = {0: True, 1: True, 2: True}
    for val in choices:
        past[val] = False
    return str(past)

def get_past(cookie_dict):
    past = []
    if 'date1' in cookie_dict.keys():
        past.append('date1')
    if 'date2' in cookie_dict.keys():
        past.append('date2')
    if 'date3' in cookie_dict.keys():
        past.append('date3')