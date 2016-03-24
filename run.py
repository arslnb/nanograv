from flask import Flask, render_template, jsonify
import json
import numpy as np

with open('static/data.json') as data_file:
    data = json.load(data_file)

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template("output.html")

@app.route('/getalldata')
def get_alldata():
    names = []
    p = []
    pd = []
    raw = []

    b_names = []
    b_p = []
    b_pd = []
    b_raw = []
    for i in data:
        if i["Binary"] == "Y":
            b_names.append("Pulsar Name: " + i["Pulsar"])
            b_p.append(i["Period"])
            b_pd.append(i["Period Derivative"])
            b_raw.append(i["Raw Profiles"])
        else:
            names.append("Pulsar Name: " + i["Pulsar"])
            p.append(i["Period"])
            pd.append(i["Period Derivative"])
            raw.append(i["Raw Profiles"])
    return jsonify(names = names, p = p, pd = pd, raw = raw, b_names = b_names, b_p = b_p, b_pd = b_pd, b_raw = b_raw, bmean_raw = np.mean(np.array([b_raw])), mean_raw = np.mean(np.array([raw])))

@app.route('/getdata/<field>')
def get_data(field):
    ret_arr = []
    for i in data:
        ret_arr.append(i[field])
    return ret_arr

if __name__ == "__main__":
    app.run(debug = True)
