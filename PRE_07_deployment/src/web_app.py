import pickle

import pandas as pd  # type: ignore
from flask import Flask, render_template, request  # type: ignore

app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"

FOLDER = "PRE_07_deployment"


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=("GET", "POST"))
#función para obtención de datos
#desde la app web
def index():

    if request.method == "POST":

        user_values = {}

        # Lee los valores de las cajas de texto de la interfaz
        # usamos le nombre de las columnas en user_values
        # y en reques.form para obtener la entrada
        # de la app web para esa entrada específica. 
        user_values["bedrooms"] = float(request.form["bedrooms"])
        user_values["bathrooms"] = float(request.form["bathrooms"])
        user_values["sqft_living"] = float(request.form["sqft_living"])
        user_values["sqft_lot"] = float(request.form["sqft_lot"])
        user_values["floors"] = float(request.form["floors"])

        # valore sde waterfront
        if request.form.get("waterfront") == "Yes":
            user_values["waterfront"] = 0
        else:
            user_values["waterfront"] = 1

        #
        # Valore entre 1 y 5
        if request.form.get("condition") == "1":
            user_values["condition"] = 1
        elif request.form.get("condition") == "2":
            user_values["condition"] = 2
        elif request.form.get("condition") == "3":
            user_values["condition"] = 3
        elif request.form.get("condition") == "4":
            user_values["condition"] = 4
        else:
            user_values["condition"] = 5

        df = pd.DataFrame.from_dict(user_values, orient="index").T

        # importar el modelo
        # cada vez que na persona da un submitt
        # en la aplicación se llama, el modelo, y 
        # si al persona que entrena el modelo encuentra
        # uno mejor, entonces solo hay que cambiar el 
        # archivo .pkl
        with open(f"{FOLDER}/submission/house_predictor.pkl", "rb") as file:
            loaded_model = pickle.load(file)

        # hacer predicciones, que normalmente 
        # devuelve una array columna, es decir
        # vecotr columna
        prediction = round(loaded_model.predict(df)[0][0], 2)

    else:
        prediction = None

    # retornar el valor del pronóstico
    return render_template("index.html", prediction=prediction)

# Notese que con esto empieza el debug e indica
# el lugar donde se tiene la aplicación 
# 
if __name__ == "__main__":
    app.run(debug=True)

