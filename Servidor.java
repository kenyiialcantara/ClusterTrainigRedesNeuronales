package org.example;

import org.json.*;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.*;
import java.util.concurrent.CountDownLatch;


public class Servidor {
    private static final int PUERTO = 3000;

    private double[][] funcion;
    private double a;
    private double b;
    private int segmentos;
    private int threads;
    private List<Double> sumasParciales;
    private int nodos;
    List<double[]> intervalosList;
    List<Thread> ThreadList;
    private CountDownLatch startSignal = new CountDownLatch(1);

    public Servidor() {
        this.funcion = new double[][]{{7, 1}, {8, 2}};
        this.a = 5;
        this.b = 10;
        this.segmentos = 10000;
        this.threads = 10;
        this.sumasParciales = new ArrayList<>();
        this.nodos = 3;
        this.ThreadList = new ArrayList<>();
    }

    public void start() {
        try {
            ServerSocket serverSocket = new ServerSocket(PUERTO);
            System.out.println("El servidor está escuchando en el puerto " + PUERTO + "...");
            intervalosList = this.generarIntervalos(this.a, this.b, this.nodos);
            int idActual = 0;
            while (idActual < nodos) {
                Socket socket = serverSocket.accept();
                System.out.println("Nuevo cliente conectado: " + socket.getInetAddress());
                System.out.println("Pasando ID: " + idActual);
                int finalIdActual = idActual;
                Thread thread = new Thread(() -> handleClient(socket, finalIdActual));
                thread.start();
                this.ThreadList.add(thread);
                idActual++;
            }
            while (sumasParciales.size() < nodos) {
                try {
                    Thread.sleep(1000); // Espera 1 segundo
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }
            serverSocket.close();

            double mejorAccuracy = Double.MIN_VALUE;
            JSONObject mejoresPesos = null;
            for (double sumaParcial : sumasParciales) {
                if (sumaParcial > mejorAccuracy) {
                    mejorAccuracy = sumaParcial;
                    mejoresPesos = pedirPesos(ThreadList.get(sumasParciales.indexOf(sumaParcial) + 1));
                }
            }

            System.out.println("Mejor Accuracy: " + mejorAccuracy);
            System.out.println("Mejores Pesos: " + mejoresPesos);
        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            throw new RuntimeException(e);
        }
    }

    private void handleClient(Socket socket, int clientID) {
        try {
            BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            PrintWriter output = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);

            try {
                startSignal.await();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            System.out.println("Enviar a cliente");
            // Enviar tarea al cliente
            System.out.println("Creando tarea para ID: " + clientID);
            JSONObject taskJSON = createTaskJSON(clientID); // Aqui empaqueto los hiperparametros que enviare a los nodos
            output.println(taskJSON);

            // Recibir resultado parcial del cliente
            String sumaParcialString = input.readLine();
            JSONObject sumaParcialJSON = new JSONObject(sumaParcialString);
            double resultadoJSON = sumaParcialJSON.getDouble("result");
            sumasParciales.add(resultadoJSON);

            // Obtener mejores pesos de acuerdo al nodo con mayor accuracy
            if (resultadoJSON == Collections.max(sumasParciales)) {
                output.println("{\"send\": 1}"); // Solicitar envío de pesos
                String pesosString = input.readLine();
                JSONObject pesosJSON = new JSONObject(pesosString);
                System.out.println("Pesos del nodo con mayor accuracy: " + pesosJSON);
            } else {
                output.println("{\"send\": 0}"); // No enviar pesos
            }

            socket.close();
        } catch (IOException e) {
            e.printStackTrace();
        } catch (JSONException e) {
            throw new RuntimeException(e);
        }
    }

    private JSONObject createTaskJSON(int clientID) throws JSONException {
        JSONObject taskJSON = new JSONObject();
        JSONObject dataJSON = new JSONObject();
        JSONArray xJSON = new JSONArray();
        JSONArray yJSON = new JSONArray();

        double[][] xData = {{0.5, 0.5, 0.0, 0.5, 1.0, 1.0, 1.0}, {0.5, 0.0, 0.0, 1.0, 1.0, 1.0, 0.5}, {0.5, 0.5, 0.0, 0.5, 0.0, 1.0, 0.0},
                {0.5, 0.5, 0.0, 1.0, 0.0, 1.0, 1.0}, {0.0, 0.0, 0.0, 0.5, 0.0, 1.0, 0.0}, {0.0, 0.0, 1.0, 0.5, 1.0, 1.0, 1.0},
                {0.0, 0.5, 0.0, 0.5, 0.0, 1.0, 1.0}};

        double[][] yData = {{0.5}, {0.5}, {1.0}, {0.5}, {1.0}, {0.5}, {1.0}};

        for (double[] x : xData) {
            JSONArray rowJSON = new JSONArray();
            for (double value : x) {
                rowJSON.put(value);
            }
            xJSON.put(rowJSON);
        }

        for (double[] y : yData) {
            JSONArray rowJSON = new JSONArray();
            for (double value : y) {
                rowJSON.put(value);
            }
            yJSON.put(rowJSON);
        }

        dataJSON.put("x", xJSON);
        dataJSON.put("y", yJSON);

        taskJSON.put("data", dataJSON);
        taskJSON.put("rn", new JSONArray(Arrays.asList(7, 6, 1)));
        taskJSON.put("epochs", 2);
        taskJSON.put("checks", 2);

        return taskJSON;
    }

    private JSONObject pedirPesos(Thread nodo) throws JSONException {
        nodo.interrupt();
        JSONObject requestJSON = new JSONObject();
        requestJSON.put("send", 1);

        // Aqui falta sacar el socket del nodo
        // para luego usarlo para mandar el pedido
        // PrintWriter output = new PrintWriter(new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())), true);
        // BufferedReader input = new BufferedReader(new InputStreamReader(socket.getInputStream()));
        // output.println(requestJSON);
        //String sumaParcialString = input.readLine();
        JSONObject pesosJSON = new JSONObject();

        return pesosJSON;
    }

    private static List<double[]> generarIntervalos(double a, double b, int nodos) {
        List<double[]> intervalos = new ArrayList<>();
        double delta = (b - a) / nodos;
        double x0 = a;

        for (int i = 0; i < nodos; i++) {
            double x1 = x0 + delta;
            intervalos.add(new double[]{x0, x1});
            x0 = x1;
        }

        return intervalos;
    }

    public static void main(String[] args) {
        Servidor servidor = new Servidor();
        Scanner scanner = new Scanner(System.in);
        String input = "";

        while (true) {
            System.out.print("Ingrese número de nodos: ");
            input = scanner.nextLine();
            try {
                servidor.nodos = Integer.parseInt(input);
                break;
            } catch (Exception e) {
                System.out.println("Ingresa un número entero");
            }
        }

        new Thread(() -> servidor.start()).start();

        // Esperar hasta que se ingrese "SALIR" por teclado
        while (true) {
            input = scanner.nextLine();
            if (input.equals("SALIR")) {
                break;
            }
        }

        while (true) {
            System.out.print("Ingrese número de threads por cliente: ");
            input = scanner.nextLine();
            try {
                servidor.threads = Integer.parseInt(input);
                break;
            } catch (Exception e) {
                System.out.println("Ingresa un número entero");
            }
        }

        servidor.startSignal.countDown();
    }
}
