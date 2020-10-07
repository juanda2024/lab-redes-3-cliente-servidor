import socket
import hashlib
import time

s = socket.socket()
s.bind(("localhost", 5000))
s.listen(1)
print("- - - - - - - - - - - - - - - - Servidor corriendo en localhost puerto 5000 - - - - - - - - - - - - - - -")
conectado = True;
contador_clientes_conectados = 0

def enviar_data(filetosend):
    c.send(str.encode(filetosend.name))
    data = filetosend.read(1024*1000)
    i = 0
    while data:
        i += 1
        print("Enviando...", i)
        if(i == 1):
            start = time.time()
            c.send(str.encode(str(start) + "TIEMPO"))
        c.send(data)
        c.send(str.encode("#PAQUETES" + str(i)))
        data = filetosend.read(1024*10000)
    getsha256str(data.decode())

def getsha256str(stexto):
    hashsha = hashlib.sha256()
    hashsha.update(stexto.encode())
    print("hash del archivo enviado: ", hashsha.hexdigest())
    return hashsha.hexdigest()

while conectado:
    c, a = s.accept()
    info = c.recv(2024)
    if(info != b"recibido"):
        contador_clientes_conectados+=1;
        print("\n")
        print("Conexión exitosa con el cliente", contador_clientes_conectados,"...")
    if info == b"1":
        filetosend = open("test0.txt", "rb")
        enviar_data(filetosend)
        c.shutdown(2)
        c.close()
    if info == b"2":
        filetosend = open("test2.txt", "rb")
        enviar_data(filetosend)
        c.shutdown()
        c.close()
    if info == b"recibido":
        print("Archivo recibido con exito por el usuario")
        c.close()

s.close()



