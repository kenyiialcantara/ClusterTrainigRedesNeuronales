import socket
from multiprocessing import Pool
import json
import NetworkNeuron
import numpy as np

class Client:
    def __init__(self) -> None:
        self.host = 'localhost'
        self.port = 3000
        self.client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.ingreso = []
        self.salida = []
        self.rn = []
        self.epochs = 0
        self.w = []
        
      
        
    def entrena(self):
   
        my_rn = NetworkNeuron.RNA(*self.rn,self.w)
        return my_rn.entrenamiento(self.ingreso, self.salida, self.epochs)
       

    def start(self):

        #conectando
        self.client_socket.connect((self.host,self.port))
        print('Esperando al que envie los datos ...')

        #Resibiendo la respuesta del servidor
        while True:
            print('\nEsperando ...')
            data_json = {}
            data_json= self.client_socket.recv(16384).decode()
            data_obj ={}
            print('El servidor envio:',data_json)
            data_obj = json.loads(data_json)

            if data_obj['data'] == 'finish':
                print("Finalizado :'v")
                message = {"result":'Bye!'}
                message_json = json.dumps(message)
                self.client_socket.sendall((message_json.strip()).encode())
                self.client_socket.close()
                break

            self.ingreso = data_obj['data']['x']
            self.salida = data_obj['data']['y']
            self.rn = data_obj['rn']
            self.epochs = data_obj['epochs']
            self.w = data_obj['w']
            result_w = self.entrena()
            #Enviando al servidor
            message = {"result":result_w}
            print('Enviando al servidor los pesos:',np.round(result_w,decimals=3))
            message_json = json.dumps(message)
            print(message_json,'a')
            self.client_socket.sendall((message_json.strip()).encode())
            
        
        
        
def main():
    current_client = Client()
    current_client.start()

if __name__=="__main__":
    main()
