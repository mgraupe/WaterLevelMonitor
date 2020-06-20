import numpy as np
import matplotlib.pyplot as plt
import os

scriptWD = os.path.dirname(os.path.realpath(__file__))

data = np.loadtxt(scriptWD+'/data/calibrationDistanceAmount.txt')

np.save(scriptWD+'/data/calibrationData.npy',data)
fig = plt.figure(figsize=(6,9))
fig.suptitle('Calibration : Water content vs. Height (20-june-2020)')
ax0 = fig.add_subplot(211)
ax0.plot(data[:,0],data[:,1],'o-')
ax0.set_ylabel('height to water surface (cm)',fontsize=12)

ax1 = fig.add_subplot(212)
ax1.plot(data[:,0][:-1],np.diff(data[:,1]),'o-')
ax1.set_ylabel('slope, increase (cm/l)',fontsize=12)

ax1.set_xlabel('water content (l)',fontsize=12)
plt.savefig(scriptWD+'/figures/calibrationData.pdf')
