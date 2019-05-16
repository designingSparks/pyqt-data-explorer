import time
tstart=time.time()
npoints = 10
interval =0.01

for n in range(npoints):
    print('Elapsed time: {}'.format(time.time() - tstart))
    # time.sleep(0.005) #simulates processing delay

    #Option 1. Processing delay is accumulated
    # time.sleep(interval)
    
    #Option 2. Processing delay is not accumulated
    delay = (tstart + (n+1)*interval) - time.time()
    if (delay > 0):
        time.sleep(delay)

