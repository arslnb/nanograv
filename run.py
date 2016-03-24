from flask import Flask, render_template, jsonify
import numpy as np
import json, os

# Read the given JSON file
with open('static/data.json') as data_file:
    data = json.load(data_file)

# Initialize Flask
app = Flask(__name__)

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Pulsar Data')

# This route serves the HTML template, loads up script.js in the browser.
# The script.js file contains code that makes an AJAX call to retrieve the data
# This keeps the system asynchronous

@app.route("/")
def home():
    return render_template("output.html")

# This is the route that serves the data to feed the scatterplot
@app.route('/api/data')
def get_all_data():
    # Stores the cursor labels for pulsars without a binary companion
    no_binary_names = []
    # Stores period value for pulsars without a binary companion
    no_binary_periods = []
    # Stores period derivative value for pulsars without a binary companion
    no_binary_period_derivative = []
    # Stores raw files value for pulsars without a binary companion
    no_binary_raw = []
    # Stores the cursor labels for pulsars with a binary companion
    binary_names = []
    # Stores period value for pulsars with a binary companion
    binary_periods = []
    # Stores period derivative value for pulsars with a binary companion
    binary_period_derivative = []
    # Stores raw files value for pulsars with a binary companion
    binary_raw = []

    # I experimented with using the mean number of raw files for the median size
    # This didn't work because of the large standard deviation in the data set
    # This can be fixed, on Plotlys end by taking deviation into account while
    # calculating a sizeref value.

    #bmean_raw = np.mean(np.array([binary_raw]))
    #mean_raw = np.mean(np.array([no_binary_raw]))

    for i in data:
        if i["Binary"] == "Y":
            binary_names.append("Pulsar Name: " + i["Pulsar"])
            binary_periods.append(i["Period"])
            binary_period_derivative.append(i["Period Derivative"])
            binary_raw.append(i["Raw Profiles"])
        else:
            no_binary_names.append("Pulsar Name: " + i["Pulsar"])
            no_binary_periods.append(i["Period"])
            no_binary_period_derivative.append(i["Period Derivative"])
            no_binary_raw.append(i["Raw Profiles"])

    # Parse this pythonic data to JSON and push to the frontend
    return jsonify(names = no_binary_names, p = no_binary_periods, pd = no_binary_period_derivative, raw = no_binary_raw, b_names = binary_names, b_p = binary_periods, b_pd = binary_period_derivative, b_raw = binary_raw)

@app.route('/getdata/<field>')
def get_data(field):
    ret_arr = []
    for i in data:
        ret_arr.append(i[field])
    return ret_arr

if __name__ == "__main__":
    app.run(port = int(os.environ.get('PORT', 5000)))
