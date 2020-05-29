import math
import numpy as np
import matplotlib.pyplot as plt

def controllerFitFunc(k):
    # model
    M = np.array([1.995908286, -0.996008084, 0.000024949, 0.000049899, 0.000024949])

    # simulation time
    tsim = 30 # [s]

    # sample time
    ts = 0.01 # [s]

    # time vector
    t = np.arange(0, tsim, ts) # [s]

    # model output signal
    y = np.zeros(t.size)

    # model input signal
    u = np.zeros(t.size)

    # model reference signal
    r = np.ones(t.size)

    # controller gains
    Kp = k[0]
    Ki = k[1]
    ei = 0

    # simulation loop
    for i in range(2,t.size):
        e = r[i-1] - y[i-1]
        ei = ei + e
        u[i] = Kp*e + Ki*ei*ts
        y[i] = M.dot(np.array([y[i-1], y[i-2], u[i], u[i-1], u[i-2]]).transpose())

    q = math.sqrt(np.sum(np.square(r-y))/t.size)

    # plot results - disable for optimization !!!
    fig = plt.figure()
    ax = fig.gca()
    ax.grid(True)
    ax.set_ylabel('Output signal [-]')
    ax.set_xlabel('Time [s]')
    plt.plot(t,y)
    plt.show()
    
    return q

print(controllerFitFunc([1.04267,0.36508]))
        

    
    
    
    
