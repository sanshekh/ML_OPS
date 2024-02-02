from flask import Flask, render_template, request
import os
import numpy as np
import pandas as pd
from ml_ops.pipeline.prediction import PredictionPipeline

app = Flask(__name__)  # Flask app initialization

@app.route('/', methods=["GET"]) # Route to display home page
def homepage():
    return render_template("index.html")


@app.route('/train', methods=["GET"]) # Route to train the pipeline
def training():
    os.system("python main.py")
    return "Training Successfull"