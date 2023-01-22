from flask import Flask , render_template, jsonify, request #render_template sirve para poder combinar codigos de distintos archivos, Es para conmbinar phyton con otros lenguajes
#la libreria request es para importar datos, jsonfy es para mandar datos en JSON
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin #Esta libreria sirve para que no solo funcione en el puerto 3000, le da mas utilidad   


app = Flask(__name__)   #Para iniciar flask, --name-- es el nombre por defecto
cors = CORS(app) #llamamos a la libreria CORS
app.config["MYSQL_HOST"]= "localhost"
app.config["MYSQL_USER"]= "root"
app.config["MYSQL_PASSWORD"]= ""
app.config["MYSQL_DB"]= "system" #Con esto llamamos a la base de datos "jugadores"
mysql=MySQL(app)


@app.route("/api/costumers") 
@cross_origin()  #Le indicamos con esto que se puede llamar desde webs diferentes, no solo el puerto 3000
def getAllCostumers(): #Funcion para obtener la informacion de todos los cliente
    cur = mysql.connection.cursor() #Esto crea un objeto que permite guardar en la base de datos
    cur.execute("SELECT Id, Nombre, Apellido, Email, Telefono FROM costumers") #Consulta a la base de datos
    data = cur.fetchall() #El fetchall trae toda la info
    result = []
    for fila in data: #Recorremos las filas de la info capturada en la variable data
        content = {
                    "Id":fila[0],
                    "Nombre":fila[1], 
                    "Apellido":fila[2], 
                    "Email":fila[3], 
                    "Telefono":fila[4] } #[0] es el Id, como estamos en un for, muestra todas las filas  
        result.append(content) #Vamos llenando el array de resultados con el contenido de las filas
    #Hay que pasar la informacion por JSON
    return jsonify(result) #Devuelve la info en JSON

@app.route("/api/costumers/<int:id>")  #el <int:id> es para buscar el id del cliente en la base de datos
@cross_origin()
def getCostumer(id): #Funcion para obtener la informacion de un cliente
    cur = mysql.connection.cursor() #Esto crea un objeto que permite guardar en la base de datos
    cur.execute("SELECT Id, Nombre, Apellido, Email, Telefono FROM costumers WHERE Id="+str(id)) #Consulta a la base de datos
    data = cur.fetchall() #El fetchall trae toda la info
    content = {}
    for fila in data: #Recorremos las filas de la info capturada en la variable data
        content = {
                    "Id":fila[0],
                    "Nombre":fila[1], 
                    "Apellido":fila[2], 
                    "Email":fila[3], 
                    "Telefono":fila[4] } #[0] es el Id, como estamos en un for, muestra todas las filas  
    #Hay que pasar la informacion por JSON
    return jsonify(content) #Devuelve la info en JSON

@app.route("/api/costumers", methods=["POST"]) #Utilizamos el POST para agregar clientes
@cross_origin()
def createCostumer(): #Para ver si se actualiza o se crea un cliente
    if "Id" in request.json:
        updateCostumer()
    else:
        createCostumer()    
    return "ok"    
  
def createCostumer(): #Funcion para crear clientes
    cur = mysql.connection.cursor() #Esto crea un objeto que permite guardar en la base de datos
    cur.execute ("INSERT INTO `costumers` (`Id`, `Nombre`, `Apellido`, `Email`, `Telefono`) VALUES (NULL, %s , %s , %s , %s);",
                (request.json["Nombre"],request.json["Apellido"],request.json["Email"],request.json["Telefono"])) #Aca le pasamos codigo SQL. %s significa que le pasaremos un str
    #el request.json sirve para mandar la info en formato json, mandamos la info para agregar un nuevo cliente
    mysql.connection.commit() #Para realizar completamente la ejecucion del comando, se pone una sola vez x funcion
    return "Cliente guardado"

def updateCostumer(): #Funcion para modificar clientes
    cur = mysql.connection.cursor() #Esto crea un objeto que permite guardar en la base de datos
    cur.execute ("UPDATE `costumers` SET `Nombre` = %s, `Apellido` = %s , `Email` = %s , `Telefono` = %s WHERE `costumers`.`Id` = %s;",
                (request.json["Nombre"],request.json["Apellido"],request.json["Email"],request.json["Telefono"], request.json["Id"])) #Aca le pasamos codigo SQL. %s significa que le pasaremos un str
    #el request.json sirve para mandar la info en formato json, mandamos la info para agregar un nuevo cliente
    mysql.connection.commit() #Para realizar completamente la ejecucion del comando, se pone una sola vez x funcion
    return "Cliente guardado"


@app.route("/api/costumers/<int:id>", methods=["DELETE"]) #Utilizamos el DELETE para borrar clientes
@cross_origin()
def removeCostumer(id): #Funcion para eliminar clientes
    cur = mysql.connection.cursor() #Esto crea un objeto que permite guardar en la base de datos
    cur.execute ("DELETE FROM `costumers` WHERE `costumers`.`Id` = "+str(id)+";") #Aca le pasamos codigo SQL para eliminar cliente, con el id concatenado, es el valor que le pasamos a la funcio 
    mysql.connection.commit() #Para realizar completame
    return "Cliente Eliminado"

@app.route("/") #Esto es para ver donde modificaremos la ruta, si ponemos solo la /, modificaremos en la pagina principal
@cross_origin()
def index(): #creamos una funcion
    return render_template("index.html")


@app.route("/<path:path>") #Esto es un comodin que permite aceptar cualquier cosa
@cross_origin()
def publicFiles(path): #creamos una funcion
    return render_template(path)

app.run(None, 3000, True) #corremos flask en el puerto 3000, el true es para modificar rapidamente los parametros, sin la necesidad de dar play siempre