import os
import sys

from flask import Flask
from flask import render_template
from flask import request

import fastai
from fastai.vision.all import *
from fastai.vision.widgets import *

fastai.layers.CrossEntropyLossFlat = fastai.losses.CrossEntropyLossFlat

app = Flask(__name__)

learner = load_learner('./birds_model.pkl', cpu=True)


@app.route('/', methods=['GET', 'POST'])


def upload_predict():
    if request.method == "POST":
        image_file = request.files["image"]
        if image_file:
            img = PILImage.create(image_file)

            pred, pred_idx, probs = learner.predict(img)

            pourcent = probs[pred_idx] * 100.0
            proba = f"{pourcent:.04f} %"

            return render_template("index.html", prediction=proba, pred=pred)

    return render_template("index.html", prediction=0)


if __name__ == "__main__":
    app.run(port=12000, debug=True)
    print("fin")