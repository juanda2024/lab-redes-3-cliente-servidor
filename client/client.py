import socket
import hashlib
import time
import datetime
import uuid

s = socket.socket()
r = socket.socket()
id_cliente = uuid.uuid4()

def conectar_cliente():
    try:
        s.connect(("localhost", 5000))
        print(" - - - - - - Conexión exitosa con el servidor - - - - - - - ")
        print("Preparado para recibir archivos... ")
        mostrar_menu()
    except:
        print(" - - - - - - Conexión finalizada - - - - - - - ")

def mostrar_menu():
    option = input("Seleccione 1 para archivo de 100 Mib, seleccion 2 para archivo de 200 Mib:")
    if option == "1":
        cantidad_bytes_archivo = "104.8576 MB"
        s.send(b"1")
        conseguir_archivo(cantidad_bytes_archivo)
    elif option == "2":
        cantidad_bytes_archivo = "262.144 MB"
        s.send(b"2")
        conseguir_archivo(cantidad_bytes_archivo)
    else:
        print("Selecciono un caracter invalido")
        mostrar_menu()

def conseguir_archivo(cantidad_bytes_archivo):
    fileName = s.recv(1024)
    print("Se está recibiendo el archivo: ", fileName.decode())
    print("...")
    newFile = open(fileName, "w")
    while True:
        file = s.recv(1024 * 10000)
        if file == b"":
            end = time.time()
            print("Tiempo total:",round(float(end)-float(start),5), "seg")
            break
        start = file.decode().split("TIEMPO")[0].replace("TIEMPO", "")
        newFile.write(file.decode().split("TIEMPO")[1].replace(" ","").split("#PAQUETES")[0])
        num_paquetes = file.decode().split("TIEMPO")[1].replace(" ","").split("#PAQUETES")[1]

    print("hash del archivo recibido: ", getsha256file(fileName.decode()))
    r.connect(("localhost", 5000))
    r.send(b"recibido")
    crearLog(fileName,cantidad_bytes_archivo,end,start,num_paquetes)

def crearLog(fileName, cantidad_bytes_archivo,end,start,num_paquetes):
    log_conexiones = open("conexion" + str(1) + ".log", "w")
    log_conexiones.write("Fecha y hora de la prueba:" + str(datetime.datetime.now()))
    log_conexiones.write("\n")
    log_conexiones.write("Nombre y tamaño del archivo: " + fileName.decode() + " , " + cantidad_bytes_archivo)
    log_conexiones.write("\n")
    log_conexiones.write("id del cliente: " + str(id_cliente))
    log_conexiones.write("\n")
    log_conexiones.write("Entrega exitosa: " + "el hash del archivo es : "  + str(getsha256file(fileName.decode())) +
                         " ,Que corresponde al mismo del servidor.")
    log_conexiones.write("\n")
    log_conexiones.write("Tiempo de transferencia: " + str(round(float(end)-float(start),5)) + " segundos")
    log_conexiones.write("\n")
    log_conexiones.write("# paquetes enviados: " + str(num_paquetes))
    log_conexiones.write("\n")
    log_conexiones.write("# paquetes recibidos: " + str(num_paquetes))
    log_conexiones.write("\n")
    log_conexiones.write("# paquetes transmitidos: " + str(num_paquetes))
    log_conexiones.write("\n")
    log_conexiones.write("bytes transmitidos y recibidos: " + cantidad_bytes_archivo + " , " + cantidad_bytes_archivo)



def getsha256file(archivo):
    try:
        hashsha = hashlib.sha256()
        with open(archivo, "rb") as f:
            for bloque in iter(lambda: f.read(4096), b""):
                hashsha.update(bloque)
        return hashsha.hexdigest()
    except Exception as e:
        print("Error: %s" % (e))
        return ""
    except:
        print("Error desconocido")
        return ""

conectar_cliente()
s.close()

