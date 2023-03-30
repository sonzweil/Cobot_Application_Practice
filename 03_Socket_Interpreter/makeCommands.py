import numpy as np
dist_X = 0.2
sample_num = 100
t = np.linspace(0, dist_X, sample_num)

amp = 0.08
freq = 8
theta = 0
y = amp * np.sin(2 * np.pi * freq * t + theta) # y = Asin(2*pi*f*t + theta)
startX = -0.160
startY = -0.550
startZ = 0.500
Rx = 0.047
Ry = -2.176
Rz = 2.309

with open('commands.txt', 'w') as f:
    for item in zip(t, y):
        f.write("movej(p[{},{},{},{},{},{}],a=1.05,v=1.2,t=0,r=0)\n"
                .format(item[0] + startX, startY, item[1] + startZ, Rx, Ry, Rz))
