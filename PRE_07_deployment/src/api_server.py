# exponer el modelo con un servidor
# via dirección web
# es un servidor que funciona
# en todo momento y funciona como 
# una página web, recibe 
# los datos y retorna el resultado
# usando el modelo 
"""API server example"""

#
# Usage from command line:
# curl http://127.0.0.1:5000 -X POST -H "Content-Type: application/json" \
# -d '{"bathrooms": "2", "bedrooms": "3", "sqft_living": "1800", \
# "sqft_lot": "2200", "floors": "1", "waterfront": "1", "condition": "3"}'
#

# Windows:
# curl http://127.0.0.1:5000 -X POST -H "Content-Type: application/json" -d "{\"bathrooms\": \"2\", \"bedrooms\": \"3\", \"sqft_living\": \"1800\", \"sqft_lot\": \"2200\", \"floors\": \"1\", \"waterfront\": \"1\", \"condition\": \"3\"}"

import pickle

import pandas as pd  # type: ignore
from flask import Flask, request  # type: ignore

app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"


FEATURES = [
    "bedrooms",
    "bathrooms",
    "sqft_living",
    "sqft_lot",
    "floors",
    "waterfront",
    "condition",
]


@app.route("/", methods=["POST"])
def index():
    """API function"""

    args = request.json
    # sacar los valores para cada clave equivalente
    # en la página.
    filt_args = {key: [int(args[key])] for key in FEATURES}
    df = pd.DataFrame.from_dict(filt_args)

    with open("PRE_07_deployment/submission/house_predictor.pkl", "rb") as file:
        loaded_model = pickle.load(file)

    prediction = loaded_model.predict(df)

    return str(prediction[0][0])


if __name__ == "__main__":
    app.run(debug=True)
    
    
    
    





























