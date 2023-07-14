import socket
import numpy as np
import json
import threading
import math
import random
import sys


class Server:
    def __init__(self) -> None:
        self.host = 'localhost'
        self.port = 3000
        self.serv_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clients = {}
        self.threads_clients = []
        self.number_clients = 0

        self.ingreso =  [
          [0.5, 0.5, 0.0, 0.5, 1.0, 1.0, 1.0],
          [0.5, 0.0, 0.0, 1.0, 1.0, 1.0, 0.5],
          [0.5, 0.5, 0.0, 0.5, 0.0, 1.0, 0.0],
          [0.5, 0.5, 0.0, 1.0, 0.0, 1.0, 1.0],
          [0.0, 0.0, 0.0, 0.5, 0.0, 1.0, 0.0],
          [0.0, 0.0, 1.0, 0.5, 1.0, 1.0, 1.0],
          [0.0, 0.5, 0.0, 0.5, 0.0, 1.0, 1.0]
        ]

        self.salida = [[0.5], [0.5], [1.0], [0.5], [1.0], [0.5], [1.0]]

        self.evaluar = [
                [0.5, 0.5, 0.0, 0.5, 1.0, 1.0, 1.0],
                [0.5, 0.0, 0.0, 1.0, 1.0, 1.0, 0.5],
                [0.5, 0.5, 0.0, 0.5, 0.0, 1.0, 0.0],
                [0.5, 0.5, 0.0, 1.0, 0.0, 1.0, 1.0],
                [0.0, 0.0, 0.0, 0.5, 0.0, 1.0, 0.0],
                [0.0, 0.0, 1.0, 0.5, 1.0, 1.0, 1.0],
                [0.0, 0.5, 0.0, 0.5, 0.0, 1.0, 1.0],
                [0.5, 0.0, 1.0, 0.5, 0.0, 1.0, 0.0],
                [0.0, 0.5, 1.0, 0.5, 1.0, 1.0, 0.0],
                [0.5, 0.5, 0.0, 0.5, 1.0, 1.0, 0.0],
                ]


        self.rn = [7, 6, 1]
        self.epochs = 2
        self.checks = 2


    
        
        
    def resibe_clientes(self):
        
        
        class ManagementClient:
            def __init__(self,client_socket,client_address,rn) -> None:
                self.rand = random.Random()
                self.client_address = client_address
                self.client_socket = client_socket
                self.w= []
                self.y = []
                self.s = []
                self.g = []
                self.w = []
                self.c = [0, 0, 0]  # capas de datos
                self.c[0] = rn[0]
                self.c[1] = rn[1]
                self.c[2] = rn[2]
                for _ in range(rn[1] + rn[2]):
                    self.y.append(0)
                    self.s.append(0)
                    self.g.append(0)
            
                for _ in range(rn[0] * rn[1] + rn[1] * rn[2]):
                    self.w.append(self.get_random())
                
            def get_random(self):
                return self.rand.random() * 2 - 1  # [-1;1[
            def resibe_message_client(self):
                response_json = self.client_socket.recv(1024).decode('utf-8')
                response = json.loads(response_json)
                print('Recibiendo del cliente {}:'.format(self.client_address[0]),np.round(response['result'],decimals=3))
                self.w = response['result']
            
            def prueba(self, pruebas):
               
                for i in range(len(pruebas)):
                    prubs = pruebas[i]
                    self.usored(prubs)

            def fun(self, d):
                return 1 / (1 + math.exp(-d))
    
            def usored(self, datatest):
                print("-----------****Inicio Test****----------")
                print("prueba", end=" ")
                for i in range(len(datatest)):
                    print("[{}]".format(datatest[i]), end=" ")
                print()
                print("salida", end=" ")
                for i in range(self.c[1], self.c[1] + self.c[2]):
                    print("[{}]".format(self.y[i]), end=" ")
                print()
                print("-----------****Fin Test****----------")
               
        
        id_available = 0
        while True:
            #Llega la conexion y acepta
            client_socket,client_address = self.serv_socket.accept()
            self.clients[id_available] = ManagementClient(client_socket,client_address,self.rn)
            t = threading.Thread(target=self.clients[id_available].resibe_message_client)
            self.threads_clients.append(t)
            t.start()
            print('Nuevo cliente con ip {}'.format(client_address[0]))
            print('cantida de clientes:',len(self.clients))
            id_available +=1
            self.number_clients = self.number_clients+1
            if self.number_clients > 0: 
                print('\nIngresa 1 para Iniciar y 0 para salir')
            
            
                
            
        
            
    
    
    def envia_message_cliente(self,finish =False):
        
        data = {
        "data": {
            "x": self.ingreso,
            "y": self.salida
        },
        "rn": self.rn,
        "epochs": self.epochs,
        "checks": self.checks
        }

        if finish:
            data = {
                "data":'finish'
            }

        i = 0
        for id in self.clients:
            data_json  = json.dumps(data)+"\n"
            print('Enviando al cliente con ip {}:'.format(self.clients[id].client_address[0]),data_json)
            #Enviando a todos los clientes
            self.clients[id].client_socket.sendall(data_json.encode())           
            i+=1

    def menu(self):
        while True:
            option = int(input())
            if option == 0:
                self.envia_message_cliente(finish=True)
                
                break
            if option == 1:
                self.envia_message_cliente()
                for thread in self.threads_clients:
                    thread.join()

                for id in self.clients:
                    print('\n\n Probando cliente ',self.clients[id].client_address[0],':')
                    self.clients[id].prueba(self.evaluar)
                    print('\nIngresa 1 para Iniciar y 0 para salir')
        self.serv_socket.close()
        # sys.exit()
                    

    def start(self):
        
        #Configurando el numero de clientes
        # self.number_clients = int(input('Ingresa el numero de clientes:'))
        #Iniciando
        self.serv_socket.bind((self.host,self.port))
        #Experando conexion entrante
        self.serv_socket.listen()
        print('El servidor esta escuchando en la ip {} y puerto {} ...'.format(self.host,self.port))
        my_menu = threading.Thread(target=self.menu)
        my_menu.start()
        self.resibe_clientes()        
        # self.serv_socket.close()
    
        
    
    
def main():
    current_server = Server()
    current_server.start()



if __name__=="__main__":
    main()
