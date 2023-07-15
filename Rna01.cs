using System;
using System.Collections.Generic;

public class Rna01
{
    private static readonly Random rand = new Random();
    private int ci;
    private int co;
    private int cs;

    private double[][] xin;
    private double[][] xout;

    private double[] y;
    private double[] s;
    private double[] g;
    private double[] w;
    private List<double> y_pred = new List<double>();

    private int[] c;

    public List<double> getWeights()
    {
        return new List<double>(w);
    }

    public Rna01(int ci_, int co_, int cs_)
    {
        ci = ci_;
        co = co_;
        cs = cs_;

        y = new double[co + cs];
        s = new double[co + cs];
        g = new double[co + cs];
        w = new double[ci * co + co * cs];

        c = new int[3];
        c[0] = ci;
        c[1] = co;
        c[2] = cs;

        for (int i = 0; i < y.Length; i++)
        {
            y[i] = 0;
            s[i] = 0;
            g[i] = 0;
        }

        for (int i = 0; i < w.Length; i++)
        {
            w[i] = GetRandom();
        }
    }

    public Rna01(int ci_, int co_, int cs_, List<double> weights)
    {
        ci = ci_;
        co = co_;
        cs = cs_;

        y = new double[co + cs];
        s = new double[co + cs];
        g = new double[co + cs];
        w = new double[ci * co + co * cs];

        c = new int[3];
        c[0] = ci;
        c[1] = co;
        c[2] = cs;

        for (int i = 0; i < y.Length; i++)
        {
            y[i] = 0;
            s[i] = 0;
            g[i] = 0;
        }

        for (int i = 0; i < w.Length; i++)
        {
            w[i] = weights[i] + GetRandom()*0.5;
        }
    }

    public void setWeights(List<double> weights)
    {
        for (int i = 0; i < w.Length; i++)
        {
            w[i] = weights[i];
        }
    }

    public double Fun(double d)
    {
        return 1 / (1 + Math.Exp(-d));
    }

    public void PrintXIngreso()
    {
        for (int i = 0; i < xin.Length; i++)
        {
            for (int j = 0; j < xin[i].Length; j++)
            {
                Console.WriteLine("xingreso[{0},{1}]={2}", i, j, xin[i][j]);
            }
        }
        Console.WriteLine();
    }

    public void PrintXYSalida()
    {
        for (int i = 0; i < xout.Length; i++)
        {
            for (int j = 0; j < xout[i].Length; j++)
            {
                Console.WriteLine("xsalida[{0},{1}]={2}", i, j, xout[i][j]);
            }
        }
    }

    public void PrintY()
    {
        for (int i = 0; i < y.Length; i++)
        {
            Console.WriteLine("y[{0}]={1}", i, y[i]);
        }
    }

    public void PrintW()
    {
        for (int i = 0; i < w.Length; i++)
        {
            Console.Write("w[{0}]={1}", i, w[i]);
        }
    }

    public void PrintS()
    {
        for (int i = 0; i < s.Length; i++)
        {
            Console.WriteLine("s[{0}]={1}", i, s[i]);
        }
    }

    public void PrintG()
    {
        for (int i = 0; i < g.Length; i++)
        {
            Console.WriteLine("g[{0}]={1}", i, g[i]);
        }
    }

    public double GetRandom()
    {
        return (rand.NextDouble() * 2 - 1); // [-1;1[
    }

    public void Entrenamiento(double[][] ingreso, double[][] salida, int veces)
    {
        xin = ingreso;
        xout = salida;
        
        for (int v = 0; v < veces; v++)
        {
            for (int i = 0; i < xin.Length; i++)
            {
                Entreno(i);
            }
        }
    }

    public void Entreno(int cii)
    {
        int ii;
        double pls;
        int ci;

        // Entrenamiento

        // Ida
        // Capa 1
        ci = cii;
        ii = 0; // capa0 * capa1
        pls = 0;
        for (int i = 0; i < c[1]; i++)
        {
            for (int j = 0; j < c[0]; j++)
            {
                pls += w[ii] * xin[ci][j];
                ii++;
            }
            s[i] = pls; // i = i + capa0
            y[i] = Fun(s[i]); // i = i + capa0
            pls = 0;
        }

        // Capa 2
        pls = 0;
        ii = c[0] * c[1]; // capa1 * capa2
        for (int i = 0; i < c[2]; i++)
        {
            for (int j = 0; j < c[1]; j++)
            {
                pls += w[ii] * y[j];
                ii++;
            }
            s[i + c[1]] = pls; // i = i + capa1
            y[i + c[1]] = Fun(s[i + c[1]]); // i = i + capa1
            pls = 0;
        }

        // Vuelta
        // Capa 2 - g
        for (int i = 0; i < c[2]; i++)
        {
            g[i + c[1]] = (xout[ci][i] - y[i + c[1]]) * y[i + c[1]] * (1 - y[i + c[1]]);
        }

        // Capa 1 - g
        pls = 0;
        for (int i = 0; i < c[1]; i++)
        {
            for (int j = 0; j < c[2]; j++)
            {
                pls += w[c[0] * c[1] + j * c[1] + i] * g[c[1] + j];
            }
            g[i] = y[i] * (1 - y[i]) * pls;
            pls = 0;
        }

        // Capa 2 - w
        ii = c[0] * c[1]; // capa1 * capa2
        for (int i = 0; i < c[2]; i++)
        {
            for (int j = 0; j < c[1]; j++)
            {
                w[ii] += g[i + c[1]] * y[j];
                ii++;
            }
        }

        // Capa 1 - w
        ii = 0; // capa0 * capa1
        for (int i = 0; i < c[1]; i++)
        {
            for (int j = 0; j < c[0]; j++)
            {
                w[ii] += g[i] * xin[ci][j];
                ii++;
            }
        }
    }

    public void Prueba(double[][] pruebas)
    {
        foreach (var prueba in pruebas)
        {
            Usored(prueba);
        }
    }

    public void Usored(double[] datatest)
    {
        int ii;
        double pls;

        // Ida
        // Capa 1
        ii = 0; // capa0 * capa1
        pls = 0;
        for (int i = 0; i < c[1]; i++)
        {
            for (int j = 0; j < c[0]; j++)
            {
                pls += w[ii] * datatest[j];
                ii++;
            }
            s[i] = pls; // i = i + capa0
            y[i] = Fun(s[i]); // i = i + capa0
            pls = 0;
        }

        // Capa 2
        pls = 0;
        ii = c[0] * c[1]; // capa1 * capa2
        for (int i = 0; i < c[2]; i++)
        {
            for (int j = 0; j < c[1]; j++)
            {
                pls += w[ii] * y[j];
                ii++;
            }
            s[i + c[1]] = pls; // i = i + capa1
            y[i + c[1]] = Fun(s[i + c[1]]); // i = i + capa1
            pls = 0;
        }

        //Console.WriteLine("-----------Inicio Test----------");
        //Console.Write("prueba");
        //foreach (var value in datatest)
        //{
        //    Console.Write("[{0}] ", value);
        //}
        //Console.WriteLine();
        //Console.Write("salida");
        for (int i = c[1]; i < c[1] + c[2]; i++)
        {
            //Console.Write("[{0}] ", y[i]);
            this.y_pred.Add(y[i]);
        }
        //Console.WriteLine();
        //Console.WriteLine("-----------Fin Test----------");
    }

    public double getAccuracy()
    {
        double sum=0;
        Prueba(xin);
        Console.WriteLine(y_pred.Count);
        //Console.WriteLine("Obteniendo accuracy:");
        for(int i=0; i<y_pred.Count; ++i)
        {
            //Console.Write(y_pred[i]);
            sum += (y_pred[i] - xout[i][0]) * (y_pred[i] - xout[i][0]);
            //Console.Write(",");
        }
        
        sum /= y_pred.Count;
        y_pred.Clear();
        return sum;
    }
}

