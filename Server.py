import socket
import numpy as np
import json
import threading
import math
import random


class Server:
    def __init__(self) -> None:
        self.host = 'localhost'
        self.port = 3000
        self.serv_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.clients = {}
        self.threads_clients = []
        self.number_clients = 0
        self.accurancy = {}
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
        self.epochs = 1000
        self.checks = 3
        
        
    def resibe_clientes(self):
        
        
        class ManagementClient:
            def __init__(self,client_socket,client_address,rn) -> None:
                self.rand = random.Random()
                self.client_address = client_address
                self.client_socket = client_socket
                self.w= []
                self.SME = 0
                self.y = []
                self.s = []
                self.g = []
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
            
                
                

            def resibe_message_client(self):
                
                response_json = self.client_socket.recv(16384).decode('utf-8')
                response = json.loads(response_json)
                print('Recibiendo del cliente {}:'.format(self.client_address[0]),np.round(response['result'],decimals=3))
                self.w = response['result']


        


            
            def prueba(self,pruebas):
                prubs = [0] * self.c[0]
                
                for i in range(len(pruebas)):
                    for j in range(len(pruebas[i])):
                        prubs[j] = pruebas[i][j]
                    self.usored(prubs)
                return self.y
                


            def fun(self, d):
                return 1 / (1 + math.exp(-d))
            
            def get_random(self):
                return self.rand.random() * 2 - 1  # [-1;1[

    
            def usored(self, datatest):
                print("-----------****Inicio Test****----------")
                ii = 0
                pls = 0
                
                for i in range(self.c[1]):
                    for j in range(self.c[0]):
                        pls += self.w[ii] * datatest[j]
                        ii += 1
                    self.s[i] = pls
                    self.y[i] = self.fun(self.s[i])
                    pls = 0
                
                # Capa2
                pls = 0
                ii = self.c[0] * self.c[1]
                for i in range(self.c[2]):
                    for j in range(self.c[1]):
                        pls += self.w[ii] * self.y[j]
                        ii += 1
                    self.s[i + self.c[1]] = pls
                    self.y[i + self.c[1]] = self.fun(self.s[i + self.c[1]])
                    pls = 0
                
                print("prueba", end=" ")
                for i in range(len(datatest)):
                    print(f"[{datatest[i]}]", end=" ")
                print()
                
                print("salida", end=" ")
                for i in range(self.c[1], self.c[1] + self.c[2]):
                    print(f"[{self.y[i]}]", end=" ")
                print()
               
        
        id_available = 0
        while True:
            #Llega la conexion y acepta
            client_socket,client_address = self.serv_socket.accept()
            self.clients[id_available] = ManagementClient(client_socket,client_address,self.rn)
            
           
            print('Nuevo cliente con ip {}'.format(client_address[0]))
            print('cantida de clientes:',len(self.clients))

            id_available +=1
            self.number_clients = self.number_clients+1
            if self.number_clients > 0: 
                print('\nIngresa 1 para Iniciar y 0 para salir')
        
    
    def envia_message_cliente(self,finish =False):
        
        data = {}

        if finish:
            data = {}
            data['data'] = 'finish'
        else:
            data = {}
            data['data'] = {
                    "x": self.ingreso,
                    "y": self.salida
                }
            
            data ['rn'] = self.rn
            data['epochs'] = self.epochs
            

        i = 0
        for id in self.clients:
            data_json = {}
            if not finish:
                data['w'] = self.clients[id].w
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
                for check in range(self.checks):
                    print('|---------Check ',check+1,'-------- |')
                    self.threads_clients = []
                    for id in self.clients:
                         t = threading.Thread(target=self.clients[id].resibe_message_client)
                         self.threads_clients.append(t)
                         t.start()
                    self.envia_message_cliente()
                    for thread in self.threads_clients:
                        thread.join()

                    for id in self.clients:
                        print('\n\n Probando cliente ',self.clients[id].client_address[0],':')

                        aux = np.array(self.salida).flatten()
                        y= np.array(self.clients[id].prueba(self.evaluar))
                        SME = sum((aux-y)**2)/y.shape[0]
                        self.clients[id].SME = SME
                        print('SME:',SME)
                        print('\nIngresa 1 para Iniciar y 0 para salir')

                    #Buscando el cliente con menor SME
                    e = 1
                    index = 0
                    for id in self.clients:
                        if self.clients[id].SME<e:
                            index = id
                            e =self.clients[id].SME
                        
                    
                    #Modificando pesos
                    for id in self.clients:
                        if id == index:
                            continue
                        else:
                            aux_w = []
                            for i in range(len(self.clients[id].w)):
                                if self.clients[id].w[i] < self.clients[index].w[i]:
                                    aux_w.append(self.clients[id].w[i]+0.05)
                                else:
                                    aux_w.append(self.clients[id].w[i]-0.05)
                            
                            self.clients[id].w = aux_w

                    
        self.serv_socket.close()
                    

    def start(self):
        
    
        #Iniciando
        self.serv_socket.bind((self.host,self.port))
        #Experando conexion entrante
        self.serv_socket.listen()
        print('El servidor esta escuchando en la ip {} y puerto {} ...'.format(self.host,self.port))
        my_menu = threading.Thread(target=self.menu)
        my_menu.start()
        self.resibe_clientes()        
      
    
        
    
    
def main():
    current_server = Server()
    current_server.start()



if __name__=="__main__":
    main()
