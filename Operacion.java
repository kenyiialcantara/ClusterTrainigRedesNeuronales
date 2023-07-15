package org.example;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.apache.commons.lang3.ArrayUtils;
public class Operacion {
    public static int max_acc = 0;
    public static List<Double> w_max = new ArrayList<>();

    public static double entrenar(Red r) {
        double[][] ingreso = new double[r.data.x.size()][];
        for (int i = 0; i < r.data.x.size(); i++) {
            ingreso[i] = new double[r.data.x.get(i).size()];
            for (int j = 0; j < r.data.x.get(i).size(); ++j) {
                ingreso[i][j] = r.data.x.get(i).get(j);
            }
        }

        double[][] salida = new double[r.data.y.size()][];
        for (int i = 0; i < r.data.y.size(); i++) {
            salida[i] = new double[r.data.y.get(i).size()];
            for (int j = 0; j < r.data.y.get(i).size(); ++j) {
                salida[i][j] = r.data.y.get(i).get(j);
            }
        }

        Thread[] T = new Thread[4 * r.checks];
        Rna01[] redes = new Rna01[4];
        double[] accuracy = new double[4];

        System.out.println(T.length);
        for (int c = 0; c < r.checks; c++) {
            System.out.println("Check # " + c);
            for (int i = 0; i < 4; ++i) {

                if (c == 0) {
                    System.out.println("Inicia train de red # " + i);
                    int finalI = i;
                    T[c * 4 + i] = new Thread((Runnable) () -> {
                        int index = finalI;
                        redes[index] = new Rna01(r.rn.get(0), r.rn.get(1), r.rn.get(2), r.w);
                        redes[index].Entrenamiento(ingreso, salida, r.epochs);
                    });

                } else {
                    if (i != Operacion.max_acc) {
                        System.out.println("Inicia train de red # " + i);
                        int finalI1 = i;
                        T[c * 4 + i] = new Thread((Runnable) () -> {
                            int index = finalI1;
                            redes[index] = new Rna01(r.rn.get(0), r.rn.get(1), r.rn.get(2), w_max);
                            redes[index].Entrenamiento(ingreso, salida, r.epochs);
                        });

                    } else {
                        System.out.println("Continua train de red # " + i);
                        int finalI2 = i;
                        T[c * 4 + i] = new Thread((Runnable) () -> {
                            int index = finalI2;

                            redes[index].Entrenamiento(ingreso, salida, r.epochs);
                            redes[index].printw();
                        });
                    }


                }
                T[c * 4 + i].start();

            }


            for (int i = 0; i < 4; i++) {
                try {
                    T[c * 4 + i].join();
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
            }

            for (int i = 0; i < 4; ++i) {
                accuracy[i] = redes[i].getAccuracy();
                System.out.println("Accuracy red " + i);
                System.out.println(accuracy[i]);
            }


            Operacion.max_acc = ArrayUtils.indexOf(accuracy, Collections.min(Arrays.asList(ArrayUtils.toObject(accuracy) )));
            Operacion.w_max = redes[Operacion.max_acc].getWeights();
            System.out.println("Min Perdida: " + accuracy[Operacion.max_acc]);
            System.out.println("Correspondiente a red #: " + Operacion.max_acc);


        }

        return accuracy[max_acc];
    }
}
