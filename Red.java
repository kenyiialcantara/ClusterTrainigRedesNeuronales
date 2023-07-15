package org.example;

import java.util.List;

public class Red {
    public DataObject data;
    public List<Integer> rn;
    public int epochs;
    public int checks = 4;
    public List<Double> w;
    class DataObject {
        public List<List<Double>> x;
        public List<List<Double>> y;
    }
}

