package org.example;

import org.json.JSONArray;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.example.Red;

public class Cliente {
    private String IP = "10.10.0.225";
    private int PORT = 3000;
    private Socket socket;
    private PrintWriter output;
    private double RESULTADO = 0;

    public static void main(String[] args) {
        Cliente c = new Cliente();
        c.iniciar();
    }

    public void iniciar() {
        Thread t = new Thread(this::threadProc);
        t.start();
        String mensaje = "n";
        // System.out.print("Ingrese mensaje (s para salir): ");
        /*
        while (!mensaje.equals("s")) {
            mensaje = Console.ReadLine();
        }*/
        System.out.println("Esperando dataset de entrenamiento...");
    }

    public void threadProc() {
        try {
            socket = new Socket(IP, PORT);
            System.out.println("Conectado a " + IP + ":" + PORT);

            BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String responseData;

            while (true) {
                responseData = input.readLine();
                System.out.println("print retorno"+responseData);
                if (responseData.contains("x") || true) {
//                    Red r = JsonSerializer.deserialize(responseData, Red.class);
                    Red r = new ObjectMapper().readValue(responseData, Red.class);
                    System.out.println("Epocas: " + r.epochs);
                    System.out.println("Checks: " + r.checks);
                    // f.threads = 10;

                    RESULTADO = Operacion.entrenar(r);
                    System.out.println("\n\nRESULTADO:");
                    System.out.println(RESULTADO);
                    // ClienteEnvia("{\"accuracy\": " + RESULTADO + " }");
                    StringBuilder w = new StringBuilder("{\"result\": [");
                    for (double weight : Operacion.w_max) {
                        w.append(weight).append(",");
                    }
                    w.setLength(w.length() - 1);
                    w.append("]}");
                    clienteEnvia(w.toString());
                } else {
                    System.out.println("Esperando");
                }
            }
        } catch (IOException ex) {
            System.out.println("Adios");
        }
    }

    public void clienteEnvia(String mensaje) {
        try {
            output = new PrintWriter(socket.getOutputStream(), true);
            output.println(mensaje);
            System.out.println("Enviado: " + mensaje);
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }

    // Clase Red


    // Clase Operacion

}

