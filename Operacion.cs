using System;
using System.Drawing;
using System.Text.Json;

public class Operacion
{
    public static int max_acc = 0;
    public static List<double> w_max = new List<double>();
    //public static void Main(string[] args)
    //{
    //    double[][] ingreso = new double[][]
    //    {
    //        new double[] {0, 1, 0, 1},
    //        new double[] {0, 1, 1, 0},
    //        new double[] {1, 0, 0, 1},
    //        new double[] {1, 0, 1, 1}
    //    };
    //    double[][] salida = new double[][]
    //    {
    //        new double[] {1},
    //        new double[] {0},
    //        new double[] {1},
    //        new double[] {0}
    //    };
    //    double[][] evaluar = new double[][]
    //    {
    //        new double[] {0, 1, 0, 1},
    //        new double[] {0, 1, 1, 0},
    //        new double[] {1, 0, 0, 1},
    //        new double[] {1, 0, 1, 1},
    //        new double[] {1, 1, 1, 1},
    //        new double[] {0, 0, 0, 1},
    //        new double[] {1, 1, 0, 0}
    //    };
    //    Rna01 rn = new Rna01(4, 10, 1);
    //    rn.Entrenamiento(ingreso, salida, 1000);
    //    rn.Prueba(evaluar);
    //}

    public static double entrenar(Red r)
    {
        double[][] ingreso = new double[r.data.x.Count][];
        for(int i=0; i<r.data.x.Count;i++)
        {
            ingreso[i] = new double[r.data.x[i].Count];
            for(int j=0; j < r.data.x[i].Count; ++j)
            {
                ingreso[i][j] = r.data.x[i][j];
            }
        }

        double[][] salida = new double[r.data.x.Count][];
        for (int i = 0; i < r.data.y.Count; i++)
        {
            salida[i] = new double[r.data.y[i].Count];
            for (int j = 0; j < r.data.y[i].Count; ++j)
            {
                salida[i][j] = r.data.y[i][j];
            }
        }

        Thread[] T = new Thread[4*r.checks];
        Rna01[] redes = new Rna01[4];
        double[] accuracy = new double[4];
        
        Console.WriteLine(T.Length);
        for(int c=0; c<r.checks; c++)
        {
            Console.WriteLine("Check # {0}", c);
            for (int i = 0; i < 4; ++i)
            {
                
                if (c == 0)
                {
                    Console.WriteLine("Inicia train de red # {0}", i);
                    T[c*4 + i] = new Thread((index) =>
                    {
                        int i = (int)index;
                        redes[i] = new Rna01(r.rn[0], r.rn[1], r.rn[2], r.w);
                        redes[i].Entrenamiento(ingreso, salida, r.epochs);
                    });
                    
                }
                else 
                {
                    if (i != Operacion.max_acc)
                    {
                        Console.WriteLine("Inicia train de red # {0}", i);
                        T[c * 4 + i] = new Thread((index) =>
                        {
                            int i = (int)index;
                            redes[i] = new Rna01(r.rn[0], r.rn[1], r.rn[2], w_max);
                            redes[i].Entrenamiento(ingreso, salida, r.epochs);
                        });

                    }
                    else
                    {
                        Console.WriteLine("Continua train de red # {0}", i);
                        //T[i].Abort();
                        T[c * 4 + i] = new Thread((index) =>
                        {
                            int i = (int)index;
                            
                            redes[i].Entrenamiento(ingreso, salida, r.epochs);
                            redes[i].PrintW();
                        });
                    }
                        
                    
                }
                T[c * 4 + i].Start(i);
                
            }

            

            for (int i = 0; i < 4; i++)
            {
                T[c*4 + i].Join();
            }

            for (int i = 0; i < 4; ++i)
            {
                //redes[i].PrintW();
                accuracy[i] = redes[i].getAccuracy();
                Console.WriteLine("Accuracy red {0}", i);
                Console.WriteLine(accuracy[i]);
            }


            Operacion.max_acc = Array.IndexOf(accuracy, accuracy.Min());
            Operacion.w_max = redes[Operacion.max_acc].getWeights();
            Console.WriteLine("Min Perdida: {0}",accuracy[Operacion.max_acc]);
            Console.WriteLine("Correspondiente a red #: {0}", Operacion.max_acc);
            
            
        }

        return accuracy[max_acc];

    }
}