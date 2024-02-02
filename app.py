from flask import Flask, render_template, request
import os
import numpy as np
import pandas as pd
from ml_ops.pipeline.prediction import PredictionPipeline

app = Flask(__name__)  # Flask app initialization


@app.route("/", methods=["GET"])  # Route to display home page
def homepage():
    return render_template("index.html")


# @app.route("/")
# def hello_world():
#     return "<p>Hello, World!</p>"


@app.route("/train", methods=["GET"])  # Route to train the pipeline
def training():
    os.system("python main.py")
    return "Training Successfull"


@app.route(
    "/predict", methods=["POST", "GET"]
)  # Route to display the model predictions on UI
def prediction():
    if request.method == "POST":
        try:
            # Read the inputs given by the user
            fixed_acidity = float(request.form["fixed_acidity"])
            volatile_acidity = float(request.form["volatile_acidity"])
            citric_acid = float(request.form["citric_acid"])
            residual_sugar = float(request.form["residual_sugar"])
            chlorides = float(request.form["chlorides"])
            free_sulfur_dioxide = float(request.form["free_sulfur_dioxide"])
            total_sulfur_dioxide = float(request.form["total_sulfur_dioxide"])
            density = float(request.form["density"])
            pH = float(request.form["pH"])
            sulphates = float(request.form["sulphates"])
            alcohol = float(request.form["alcohol"])

            data = [
                fixed_acidity,
                volatile_acidity,
                citric_acid,
                residual_sugar,
                chlorides,
                free_sulfur_dioxide,
                total_sulfur_dioxide,
                density,
                pH,
                sulphates,
                alcohol,
            ]
            data = np.array(data).reshape(1, 11)

            obj = PredictionPipeline()
            predict = obj.predict(data)

            return render_template("results.html", prediction=str(predict))

        except Exception as e:
            print("The exception is: ", e)
            return "Please fix the above issue & try again."

    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
