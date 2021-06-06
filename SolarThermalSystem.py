import math as m
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import pyplot

#all quantities are in SI units (length = m, temp = K, etc.) unless otherwise 
#specified


###Temperature of absorber###

r, l, d = [float(x) for x in input("Enter the radius, length, and thickness (m) of the absorber material (separated by a space): ").split()]
A = 2*m.pi*(r*l)+m.pi*(r**2) #total surface area of absorber
I = 0.7*1000 #intensity of sunlight hitting absorber
ep = 0.8 #emissivity of absorber
sig = 5.67*(10**(-8)) #stefan-boltzmann constant
Ah = 2*m.pi*(r*l) #surface area of absorber hit by sun
T = ((I*Ah)/(ep*sig*A))**(1/4) #temp at surface of absorber
Tf = (T-273.15)*(9/5)+32 #conversion from K to F


###Rate of heat flow from absorber to water###

cpt = float(input("Enter thickness (m) of copper pipe: "))
Ta = float(input("Enter the inital temp (K) of the water flowing into the solar panel: ")) #temp of water
c = r #radius of absorber
b = r-d #radius of copper pipe
a = b-cpt #radius of water flowing through pipe
kc = 1 #thermal conductivity of absorber
kb = 385 #thermal conductivity of copper
Qdotab = 2*m.pi*l*(T-Ta)/((np.log(c/b)/kc)+(np.log(b/a)/kb))


###Temperature of tank###

Tw = 0.95*T #temp of heated water reaching tank
T0 = Ta #temp of tank water = temp of water flowing into absorber (Ta)
ht = 370 #heat transfer coefficient for steel tank with water on either side
R = 1 #radius of tank
H = 2 #height of tank
At = 2*m.pi*(R*H)+m.pi*(R**2) #surface area
t_array = [] #empty array for time values
t = 0.0 #initial time 
tmax = 60000 #max time
Tt_array = [] #empty array for temp of tank values
while t < tmax:
    t_array.append(t) #populate array with time values
    t += 1
for i in range(len(t_array)):
    Tt = Tw + (T0-Tw)*np.exp(-t_array[i]/(ht*At)) #use t_array values to determine temp of tank
    Ttf = (Tt-273.15)*(9/5)+32 #conversion from K to F
    Tt_array.append(Ttf)

###Print Tf, Qdottab, and Tt_array[tmax] values###
print("")
print("Temperature (F) at surface of absorber: "+ str(Tf))
print("Rate of heat flow (J/s) from absorber to water: " + str(Qdotab))
print("The maximum temperature (F) of the water tank is close to: " + str(Tt_array[tmax-1]))
print("")


###Plot of temperature of tank###

class SnapToCurveCursor: #create class that displays x,y values of curve that cursor is closest to

    def __init__(self, ax, x, y):
        self.ax = ax
        self.x = x
        self.y = y
        self.lx = ax.axhline(color = 'red')  #horizontal line for cursor
        self.ly = ax.axvline(color = 'red')  #vertical line


    def mouse_move(self, event):
        
        if not event.inaxes:
            return

        x = event.xdata
        y = event.ydata
        indx = min(np.searchsorted(self.x, x), len(self.x) - 1) 
        x = self.x[indx]
        y = self.y[indx]
        self.lx.set_ydata(y) #update horizontal line location
        self.ly.set_xdata(x) #update veritical line 

        self.ax.figure.canvas.draw()



fig, ax = plt.subplots()
ax.plot(t_array,Tt_array)
snap_cursor = SnapToCurveCursor(ax, t_array, Tt_array)
fig.canvas.mpl_connect('motion_notify_event', snap_cursor.mouse_move)


plt.title("Heating of Solar Thermal Tank")
plt.xlabel("$t$"+" "+"(s)")
plt.ylabel("$T_{t}$"+" "+"(F)")

pyplot.ylim(bottom = Tt_array[0] - 5)
pyplot.ylim(top = Tt_array[tmax-1] + 5)

plt.show()