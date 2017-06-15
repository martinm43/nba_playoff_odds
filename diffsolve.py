# coding: utf-8
from sympy import *
x,y,z,t=symbols('x y z t')
f = Function('f')
diffeq=Eq(f(x,y).diff(x)+9*f(x,y).diff(y),1)
# Sympy PDE solver is pdesolve 
# Sympy ODE solver is desolve 
soleq=pdsolve(diffeq,f(x,y))
print(soleq)
