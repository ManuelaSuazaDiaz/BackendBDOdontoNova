from pymongo import MongoClient
from bson import ObjectId

class DB:
    def __init__(self):
        Mongo_URI = 'mongodb://localhost'
        client = MongoClient(Mongo_URI)
        self.__pacientes = client["pacientes_odontonova"]
        self.__inventario = client["controlInventario"]
    
    def agregar_pacientes(self, datos):
        results = self.__pacientes.pacientes.find_one({"documento":datos["documento"]})
        if results == None:
            self.__pacientes.pacientes.insert_one(datos)
            return True
        return False
    
    def recuperar_pacientes(self):
        results = self.__pacientes.pacientes.find({})
        pacientes = []
        for result in results:
            pacientes.append(result)
        return pacientes
    
    def buscar_paciente(self, doc):
        return self.__pacientes.pacientes.find_one({"documento":doc})
    
    def borrar_paciente(self, doc):
        self.__pacientes.pacientes.delete_one({"documento": doc})
        
    def agregar_citas(self, cita, doc, esp):
        print(cita, doc, esp)
        results_pac =  self.__pacientes.pacientes.find_one({"documento":doc})
        results_esp = self.__pacientes.especialistas.find_one({"nombreEspecialista":esp})
        cita["paciente"] = results_pac.get("_id")
        cita["especialista"] = results_esp.get("_id")
        self.__pacientes.citas.insert_one(cita)
    
    def agregar_articulo(self, datos):
        self.__inventario.articulo.insert_one(datos)
    
    def recuperar_productos(self):
        results = self.__inventario.articulo.find()
        productos = []
        for result in results:
            productos.append(result)
        return productos

    def recuperar_articulo(self, nombre):
        return self.__inventario.articulo.find_one({"nombre":nombre})     

    def delete_articulo(self, nombre):
        self.__inventario.articulo.delete_one({"nombre":nombre})       
        
        


            




        
        