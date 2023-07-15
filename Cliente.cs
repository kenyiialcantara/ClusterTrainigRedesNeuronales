using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Net.Sockets;
using System.Diagnostics;
using System.IO;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace Sockets
{
    internal class Cliente
    {
        private string IP = "10.10.0.225";
        //private string IP = "127.0.0.1";
        private int PORT = 3000;
        TcpClient tcpClient;
        StreamWriter output;
        double RESULTADO = 0;

        public static void Main(string[] args)
        {
            Cliente c = new Cliente();
            c.iniciar();
        }
        public void iniciar()
        {
            Thread t = new Thread(new ThreadStart(ThreadProc));
            t.Start();
            string mensaje = "n";
            //Console.Write("Ingrese mensaje (s para salir): ");
            /*
            while (!mensaje.Equals("s"))
            {
                mensaje = Console.ReadLine();
            }*/
            Console.WriteLine("Esperando dataset de entrenamiento...");
        }

        public void ThreadProc()
        {
            tcpClient = new TcpClient(IP, PORT);
            Console.WriteLine("Conectado a " + IP + ":" + PORT);
            while (true)
            {
                try
                {
                    byte[] data = new byte[100000];
                    string responseData = string.Empty;
                    int bytes = tcpClient.GetStream().Read(data, 0, data.Length);
                    responseData = Encoding.ASCII.GetString(data, 0, bytes);
                    Console.WriteLine(responseData);
                    if (responseData.Contains("x"))
                    {
                        Red r = JsonSerializer.Deserialize<Red>(responseData);
                        Console.WriteLine("Epocas: {0}", r.epochs);
                        Console.WriteLine("Checks: {0}", r.checks);
                        //f.threads = 10;

                        RESULTADO = Operacion.entrenar(r);
                        Console.WriteLine("\n\nRESULTADO:");
                        Console.WriteLine(RESULTADO);
                        //ClienteEnvia(@"{""accuracy"": " + RESULTADO.ToString() + " }");
                        String w = @"{""result"": [";
                        foreach (double weight in Operacion.w_max)
                        {
                            w = String.Concat(w, weight.ToString(), ",");
                        }
                        w = String.Concat(w.Substring(0, w.Length -1), "]}");
                        ClienteEnvia(w);

                    }
                    
                    
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Adios");
                    break;
                }
            }
        }

        public void ClienteEnvia(string mensaje)
        {
            //Byte[] data = Encoding.ASCII.GetBytes(mensaje);
            //tcpClient.GetStream().Write(data, 0, data.Length);

            output = new StreamWriter(tcpClient.GetStream());
            output.WriteLine(mensaje);
            Console.WriteLine("Enviado: {0}", mensaje);
            output.Flush();
        }
    }
}
