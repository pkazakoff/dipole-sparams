# Wire Dipole S-Parameter Generator
A simple python script which calculates the impedance and scattering parameters of a dipole antenna. Can output to a Touchstone .s1p file.

##Notes

The approxmation used is only valid when the diameter of the wire is much less than the length. The approximation also assumes that the near field is only free space. Nearby metal objects will affect the feed impedance somewhat. If this an issue for you, you may want to move to a full-blown FEM simulation, or just build your system and measure S11 with a network analyzer.

S-parameter output assumes a 50 ohm system.

##Understanding the output

In the output table, "R" is the input resistance and "X" is the input reactance. |S11| (db) is a measure of the return loss at a 50 ohm feed - a good match will have a large negative number. For example, -1 dB is a poor match, and -10 dB is an excellent match.

## Example usage
Getting the feed impedance of a one meter long, 3mm wide dipole at 145 MHz:

```
peter@salish:~/scripts$ ./dipole-sparams.py -f1 145 -l 1 -d 3 -p 1

Wire dipole antenna S-parameter calculator
Written by Peter Kazakoff, University of Victoria

Based on eqns 8-60a, 8-60b, 8-61a, and 8-61b from
"Antenna Theory, 3rd ed." by Constantine A. Balanis

This program is BSD licensed and comes with ABSOLUTELY NO WARRANTY


  Frequency (MHz)    R (ohms)    X (j*ohms)    |S11| (db)  S11
-----------------  ----------  ------------  ------------  ---------------------------------
              145     66.3626       9.55313      -15.7945  (0.146371218253+0.0700811282789j)

```

Getting the feed impedance of the same 1m long, 3mm wide dipole from 100 - 200 MHz in 5 MHz increments, and saving the resulting S-parameters to a Touchstone file called dipole.s1p:

```
peter@salish:~/scripts$ ./dipole-sparams.py -f1 100 -f2 200 -l 1 -d 3 -p 20 -o dipole.s1p

Wire dipole antenna S-parameter calculator
Written by Peter Kazakoff, University of Victoria

Based on eqns 8-60a, 8-60b, 8-61a, and 8-61b from
"Antenna Theory, 3rd ed." by Constantine A. Balanis

This program is BSD licensed and comes with ABSOLUTELY NO WARRANTY


  Frequency (MHz)    R (ohms)    X (j*ohms)    |S11| (db)  S11
-----------------  ----------  ------------  ------------  ---------------------------------
              100     25.6966    -313.461       -0.220123  (0.927206464438-0.301439908996j)
              105     28.8326    -272.759       -0.322342  (0.902207149957-0.338360553181j)
              110     32.2425    -233.965       -0.481029  (0.866280199918-0.380409219811j)
              115     35.9508    -196.724       -0.736627  (0.81350635668-0.426845835977j)
              120     39.9856    -160.723       -1.16736   (0.73478431643-0.473700313886j)
              125     44.3789    -125.686       -1.93331   (0.617967654896-0.508760369683j)
              130     49.1675     -91.365       -3.3804    (0.45457701078-0.502509228135j)
              135     54.3937     -57.5285      -6.30228   (0.265225208221-0.404914097692j)
              140     60.1065     -23.9592     -12.7365    (0.132848357841-0.188692518539j)
              145     66.3626       9.55313    -15.7945    (0.146371218253+0.0700811282789j)
              150     73.2282      43.2167      -8.50279   (0.277375715621+0.253427802399j)
              155     80.7806      77.2426      -5.23327   (0.433113577981+0.33481848814j)
              160     89.1111     111.85        -3.55908   (0.563398533214+0.35104142771j)
              165     98.3275     147.271       -2.5973    (0.660497785847+0.33708319757j)
              170    108.558      183.758       -1.99676   (0.730835368721+0.31194189185j)
              175    119.958      221.589       -1.59664   (0.782070189873+0.284134378751j)
              180    132.712      261.08        -1.3158    (0.820070498297+0.257104145691j)
              185    147.047      302.59        -1.11008   (0.848876979596+0.232068638375j)
              190    163.24       346.54        -0.953903  (0.871201835958+0.209312293073j)
              195    181.635      393.426       -0.831678  (0.888871558878+0.188748799976j)

Wrote Touchstone File dipole.s1p

```

Generate S-parameters for a 10cm long dipole 1.5mm thick dipole in the range 500 MHz - 1 GHz, sweeping through 1000 points without writing the output to the screen:

```
peter@salish:~/scripts$ ./dipole-sparams.py -f1 500 -f2 1000 -l 0.1 -d 1.5 -p 1000 -o dipole.s1p --skip-output

Wire dipole antenna S-parameter calculator
Written by Peter Kazakoff, University of Victoria

Based on eqns 8-60a, 8-60b, 8-61a, and 8-61b from
"Antenna Theory, 3rd ed." by Constantine A. Balanis

This program is BSD licensed and comes with ABSOLUTELY NO WARRANTY


Wrote Touchstone File dipole.s1p
```


