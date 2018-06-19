#Install

``` bash
pip install numexpr
pip install sympy
``` bash

#Run the Code
``` bash
python2 bestFit.py -f data.txt -p b1 b2 b3 -t "b1/b2*exp(-(x-b3)**2/(2.*b2**2))" -i 1. 10. 500. -c 1 0 -d
``` bash