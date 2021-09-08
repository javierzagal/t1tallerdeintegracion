from flask import Flask, redirect, url_for, request, render_template
import requests
import json
import math
app = Flask(__name__)


canvasid = 15682


@app.route("/", methods = ["POST", "GET"])
def home():
    if request.method == "POST":
        print("BOTON")
        idPersona = request.form["submit_button"]
        return redirect(url_for("user", id = idPersona))
    else:
        return render_template("users.html", content = usuarios())

def usuarios():
    r = requests.get("https://us-central1-taller-integracion-310700.cloudfunctions.net/tarea-1-2021-2/15682/users")
    total = int(r.headers["X-Total-Count"])
    nIteraciones = math.ceil(total/10)


    texto = []
    for i in range(0,nIteraciones):
        r = requests.get("https://us-central1-taller-integracion-310700.cloudfunctions.net/tarea-1-2021-2/15682/users?_page=" + str(i + 1))
        jsonRequest = r.json()
        #print(jsonRequest)
        nElementos = len(r.json())
        for i in range(0,nElementos):
            lista = []
            lista.append(jsonRequest[i]["id"])
            lista.append(jsonRequest[i]["name"] + " " + jsonRequest[i]["lastName"])
            texto.append(lista)
    return texto

@app.route("/ciudades", methods = ["POST", "GET"])
def citiesHome():
    if request.method == "POST":
        idCity= request.form["submit_button"]
        return redirect(url_for("city", id = idCity))

    return render_template("cities.html", content = ciudades())

def ciudades():
    r = requests.get("https://us-central1-taller-integracion-310700.cloudfunctions.net/tarea-1-2021-2/15682/cities")
    total = int(r.headers["X-Total-Count"])
    nIteraciones = math.ceil(total/10)
    texto = []

    for i in range(0,nIteraciones):
        r = requests.get("https://us-central1-taller-integracion-310700.cloudfunctions.net/tarea-1-2021-2/15682/cities?_page=" + str(i + 1))
        jsonRequest = r.json()
        nElementos = len(r.json())
        for i in range(0,nElementos):
            lista = []
            lista.append(jsonRequest[i]["id"])
            lista.append(jsonRequest[i]["name"] + ", " + jsonRequest[i]["country"])
            lista.append(jsonRequest[i]["users"])
            texto.append(lista)

    return texto


@app.route("/user/<id>")
def user(id): # muestra la tarjeta y las direcciones
    r = requests.get("https://us-central1-taller-integracion-310700.cloudfunctions.net/tarea-1-2021-2/15682/users/" + str(id))
    jsonRequest = r.json()
    nombre = jsonRequest["name"] + " " + jsonRequest["lastName"]
    listaTarjeta = tarjeta(id) #lista tarjeta
    listaDirecciones = direccion(id)
    info = []
    info.append(listaTarjeta)
    info.append(listaDirecciones) #
    info.append(nombre)
    print(info)
    return render_template("user.html", content = info)
    #return str(textoTarjeta) + str(textoDirecciones) 

@app.route("/city/<id>", methods = ["POST", "GET"])
def city(id):
    if request.method == "POST":
        print("BOTON")
        idPersona = request.form["submit_button"]
        return redirect(url_for("user", id = idPersona))
    else:
        r = requests.get("https://us-central1-taller-integracion-310700.cloudfunctions.net/tarea-1-2021-2/15682/cities?q=" + str(id))
        jsonRequest = r.json()
        nombre = jsonRequest[0]["name"] + ", " + jsonRequest[0]["country"] 
        usersID = jsonRequest[0]["users"] 
        usersNames = []
        for usuario in usersID:
            usuarioNombreID = []
            r = requests.get("https://us-central1-taller-integracion-310700.cloudfunctions.net/tarea-1-2021-2/15682/users?q=" + str(usuario))
            jsonRequest = r.json()
            nombreUsuario = jsonRequest[0]["name"] + " " + jsonRequest[0]["lastName"] 
            usuarioNombreID.append(nombreUsuario) #nombre
            usuarioNombreID.append(usuario) #id

            usersNames.append(usuarioNombreID) #lista [ [nombre,id], [nombre1,id1] ... ]
        info = []
        info.append(nombre)
        #hacer que los users sean nombres y no ids
        info.append(usersNames)


        return render_template("city.html", content = info)


def tarjeta(id): # ojo que puede que sen mas de una sola tarjeta 
    r = requests.get("https://us-central1-taller-integracion-310700.cloudfunctions.net/tarea-1-2021-2/15682/users/" + id + "/credit-cards")
    jsonRequest = r.json()
    texto = []
    nElementos = len(r.json())
    for i in range(0,nElementos):
        lista = []
        lista.append("id : " + str(jsonRequest[i]["id"]))
        lista.append("Card number : " + str(jsonRequest[i]["creditCard"]))
        lista.append("CVV : " + str(jsonRequest[i]["CVV"]))

        texto.append(lista)
    return texto

def direccion(id):
    r = requests.get("https://us-central1-taller-integracion-310700.cloudfunctions.net/tarea-1-2021-2/15682/users/" + id + "/addresses")
    jsonRequest = r.json()
    texto = []
    nElementos = len(r.json())
    for i in range(0,nElementos):
        lista = []
        lista.append("address : " + str(jsonRequest[i]["address"]))
        lista.append("city : " + str(jsonRequest[i]["city"]["name"]) + ", " + str(jsonRequest[i]["city"]["country"]))
        lista.append("zip : " + str(jsonRequest[i]["zip"]))

        texto.append(lista)
    return texto



    
if __name__ == "__main__":
    app.run()