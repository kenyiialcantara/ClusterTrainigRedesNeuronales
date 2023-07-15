using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

public class Red
{
    public DataObject data { get; set; }
    public List<int> rn { get; set; }
    public int epochs { get; set; }
    public int checks { get; set; } = 4;
    public List<double> w { get; set; }
}

public class DataObject
{
    public List<List<double>> x { get; set; }
    public List<List<double>> y { get; set; }
}