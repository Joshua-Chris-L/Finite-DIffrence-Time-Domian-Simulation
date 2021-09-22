#FDTD code
# Simulation in free space


import numpy as np
from math import exp
from matplotlib import pyplot as plt


ke = 200
ex = np.zeros(ke)
hy = np.zeros(ke)
# Pulse parameters
kc = int(ke / 2)
t0 = 40
spread = 12
nsteps = 100




# Main FDTD Loop
for time_step in range(1, nsteps + 1):
    for k in range(1, ke):                                # Calculate the Ex field
        ex[k] = ex[k] + 0.5 * (hy[k - 1] - hy[k])
    pulse = exp(-0.5 * ((t0 - time_step) / spread) ** 2)  # Put a Gaussian pulse at kc - 20
    ex[kc-20] = pulse
    pulse = exp(-0.5 * ((t0 - time_step) / spread) ** 2)  # Put a Gaussian pulse at kc + 20
    ex[kc+20] = pulse
    for k in range(ke - 1):                               # Calculate the Hy field
        hy[k] = hy[k] + 0.5 * (ex[k] - ex[k + 1])

       
       
# Plot of the Ex Field.      
plt.rcParams['font.size'] = 20
plt.figure(figsize=(8, 10))
plt.subplot(211)
plt.plot(ex, color='r', linewidth=2)
plt.ylabel('E$_x$', fontsize='14')
plt.xticks(np.arange(0, 201, step=20))
plt.xlim(0, 200)
plt.yticks(np.arange(-1, 1.2, step=1))
plt.ylim(-1.2, 1.2)
plt.text(100, 0.5, 'T = {}'.format(time_step), horizontalalignment='center')

# Plot of the Ey Field.
plt.subplot(212)
plt.plot(hy, color='b', linewidth=2)
plt.ylabel('H$_y$', fontsize='14')
plt.xlabel('FDTD cells')
plt.xticks(np.arange(0, 201, step=20))
plt.xlim(0, 200)
plt.yticks(np.arange(-1, 1.2, step=1))
plt.ylim(-1.2, 1.2)
plt.subplots_adjust(bottom=0.2, hspace=0.5)
plt.show()
