from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request
from flask import jsonify

from db import DB
from datetime import date
from datetime import datetime

app = Flask(__name__)
db = DB()

@app.route("/")
def index():
    return render_template("main.html")

#%% Primer menú
@app.route("/pacientes")
def pacientes():
    return render_template("pacientes.html")  

@app.route("/volver_main")
def volver_main():
    return redirect(url_for("index"))

@app.route("/AgregarPaciente", methods=["GET", "POST"]) 
def agregar_pacientes():
    if request.method == "POST":
        if request.form.get("check", "") == "on":
            hoy = date.today()
            fnac = datetime.strptime(request.form.get("nacimiento", "No ingresado"),  "%Y-%m-%d")
            edad = hoy.year - fnac.year - ((hoy.month, hoy.day) < (fnac.month, fnac.day))
            datos = {
                "nombres": request.form.get("nombres", "No ingresado"),
                "apellidos": request.form.get("apellidos", "No ingresado"),
                "direccion": request.form.get("direccion", "No ingresado"),
                "documento": request.form.get("documento", "No ingresado"),
                "tratamiento": request.form.get("tratamiento", "No ingresado"),
                "nacimiento": request.form.get("nacimiento", "No ingresado"),
                "correo": request.form.get("correo", "No ingresado"),
                "genero": request.form.get("genero", "No ingresado"),
                "telefono": request.form.get("telefono", "No ingresado"),
                "tipoSangre": request.form.get("tipoSangre", "No ingresado"),
                "acudiente": request.form.get("acudiente", "No ingresado"),
                "telAcudiente": request.form.get("telAcudiente", "No ingresado"),
                "parentesco": request.form.get("parentesco", "No ingresado"),
                "edad": edad
            }
            bandera = db.agregar_pacientes(datos)
            return redirect(url_for("pacientes"))
        else: return render_template("agregar_pacientes.html")

    return render_template("agregar_pacientes.html")

@app.route("/EditarInfoPacientes", methods=["GET", "POST"])
def editar_pacientes():
    if request.method == "POST":
        doc = request.form.get("BuscarPaciente")
        datos = db.buscar_paciente(doc)
        return render_template("editar_paciente.html", pacientes = [datos], documento = doc )
    else:
        datos = db.recuperar_pacientes()
    return render_template("editar_paciente.html", pacientes = datos, doc = "0")

@app.route("/ModificarInfo", methods=["GET","POST"])
@app.route("/ModificarInfo/<string:doc>", methods=["GET","POST"])
def modificar(doc=None):
    if request.method == "POST":
        datos = {}
        for key, value in request.form.items():
            datos[key] = value
        db.borrar_paciente(datos["documento"])
        db.agregar_pacientes(datos)
        return redirect(url_for("editar_pacientes"))
    else: 
        datos = db.buscar_paciente(doc)
        return render_template("modificar_paciente.html", info=datos)

@app.route("/Eliminar/<string:doc>")
def eliminar(doc):
    db.borrar_paciente(doc)
    return redirect(url_for("editar_pacientes"))

@app.route("/AgregarCita", methods=["GET", "POST"])
def agregar_cita():
    if request.method == "POST":
        datos_cita = {
            "fecha": request.form.get("date", "No agregado"),
            "hora": request.form.get("time", "No agregado")
        }
        doc = request.form.get("documento", "No agregado")
        esp = request.form.get("appointmentfor", "No agregado")
        db.agregar_citas(datos_cita, doc, esp)
        return redirect(url_for("pacientes"))
    return render_template("agregar_cita.html")

@app.route("/ListaTratamientos")
def tratamientos():
    return render_template("lista_tratamientos.html")

@app.route("/ListaEspecialistas") 
def especialista():
    return render_template("lista_especialistas.html")

#%%Segundo menú
@app.route("/inventario")
def inventario():
    return render_template("inventario.html")

@app.route("/AgregarInsumoEnser", methods=["GET", "POST"])
def agregar_insumo():
    if request.method == "POST":
        datos = {
            "nombre": request.form.get("nombre", "No ingresado"),
            "registro": request.form.get("registro", "No ingresado"),
            "descripcion": request.form.get("descripcion", "No ingresado"),
            "stock": request.form.get("stock", "No ingresado"),
            "almacenamiento": request.form.get("almacenamiento", "No ingresado"),
            "fecha": request.form.get("fecha", "No ingresado"),
            "marca": request.form.get("marca", "No ingresado"),
            "categoria": request.form.get("categoria", "No ingresado"),
            "proveedor": request.form.get("proveedor", "No ingresado"),
            "nit": request.form.get("nit", "No ingresado"),
            "telefono": request.form.get("telefono", "No ingresado")
        }
        db.agregar_articulo(datos)
        return redirect(url_for("inventario"))
    return render_template("agregar_insumo.html")

@app.route("/ListaInsumos", methods=["GET", "POST"])
@app.route("/ListaInsumos/<string:nombre>")
def lista_insumos(nombre=None):
    if request.method == "POST":
        nombre = request.form.get("Buscar")
        producto = db.recuperar_articulo(nombre)
        return render_template("insumos.html", productos = [producto], nombre = nombre)
    else:
        productos = db.recuperar_productos()
        return render_template("insumos.html", productos = productos, nombre = "")
    
@app.route("/ModificarArticulo/<string:nombre>", methods=["GET", "POST"])
def modificar_articulo(nombre=None):
    if request.method == "POST":
        datos = {}
        for key, value in request.form.items():
            datos[key] = value
        db.delete_articulo(nombre)
        db.agregar_articulo(datos)
        return redirect(url_for("lista_insumos"))
    else:
        articulo = db.recuperar_articulo(nombre)
        return render_template("modificar_articulo.html", producto = articulo, nombre = nombre)

@app.route("/EliminarInsumos/<string:nombre>")
def eliminar_articulo(nombre=None):
    if nombre:
        db.delete_articulo(nombre)
        return redirect(url_for("lista_insumos"))
if __name__ == "__main__":
    app.run(debug=True, port=4000)


