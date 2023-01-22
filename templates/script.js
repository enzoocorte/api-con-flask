// Aca creamos la logica

document.addEventListener('DOMContentLoaded', init); //Cuando inicie la pagina, ejecuta la funcion search
const URL_API= "http://localhost:3000/api/"

var costumers=[]

function init(){
    search()
}

async function search(){      
    var url= URL_API + "costumers"
    var response= await fetch(url,{      //esta es la respuesta que se recibe a traves de GET
        "method" : "GET",
        "headers":{
             "Content-Type": "application/json" 
        }
    })
    costumers=await response.json();     //Para que el resultado se convierta a JSON en la vble global costumers
    //Estamos trayendo lo que creamos en el backend
    
    var html = "" // aca iremos guardando las filas de la base de datos pasadas a html

    for (costumer of costumers){
        var row = //Aca tendriamos que convertir la info que nos brinda la variable resultado en html, se guarda en un string
        `<tr>
                <td>${costumer.Nombre}</td>
                <td>${costumer.Apellido}</td>
                <td>${costumer.Email}</td>
                <td>${costumer.Telefono}</td>
                <td>
                    <button type="button" onclick="edit(${costumer.Id})" class="button">Editar</button>
                    <a href="#" onclick="remove(${costumer.Id})" class="myButton">Eliminar</a>
                </td>
           </tr>`
        html= html + row;
    }

    document.querySelector("#customers > tbody").outerHTML = html //Esto es para poner lo que esta en la var row en el cuerpo de la tabla costumers

    }

function edit(Id){
    abrirFormulario()
    //tenemos que buscar el costumer a partir del Id
    var costumer= costumers.find(x => x.Id == Id) //buscamos el id que seleccionamos con sus datos
    //Con esto mostramos los datos en el formulario
    document.getElementById("txtId").value= costumer.Id
    document.getElementById("txtlastname").value= costumer.Apellido
    document.getElementById("txtemail").value= costumer.Email       
    document.getElementById("txtfirstname").value =costumer.Nombre
    document.getElementById("txtphone").value =costumer.Telefono


}

async function remove(Id) {
    respuesta = confirm("Seguro lo quiere eliminar?")
        if (respuesta) {
            //Llamado al servidor
            var url= URL_API + "costumers/" + Id
            await fetch(url,{    
                "method" : "DELETE",
                "headers":{
                     "Content-Type": "application/json" 
                }
            })
            window.location.reload();
            alert("Se elimino")
            
        }
    }

function abrirFormulario(){
        htmlModal= document.getElementById("modal") //Aca agarro el id:Modal que esta escrito en html
        htmlModal.setAttribute("class", "modale opened") //Aca cambio la class antigua por modale opened
    }
    
function cerrarModal(){
        htmlModal= document.getElementById("modal") //Aca agarro el id:Modal que esta escrito en html
        htmlModal.setAttribute("class", "modale") //Aca cambio la class antigua por modale
        window.location.reload();
    }    



async function save() {

    var data =  //objeto JSON que enviamos al servidor
        {
            "Apellido": document.getElementById("txtlastname").value, 
            "Email": document.getElementById("txtemail").value,            
            "Nombre": document.getElementById("txtfirstname").value, 
            "Telefono": document.getElementById("txtphone").value,
        }

        var Id = document.getElementById("txtId").value 
        if (Id != ""){
            data.Id=Id
        }

            //Llamado al servidor
        var url= URL_API + "costumers" 
        await fetch(url,{    
                "method" : "POST",
                "body":JSON.stringify(data), //Convertimos la variable data a string con JSON.stringify
                "headers":{
                "Content-Type": "application/json" 
                }
                })
            window.location.reload();
          
            
    }
    
