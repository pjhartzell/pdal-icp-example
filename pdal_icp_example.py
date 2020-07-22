import json
import re
import numpy as np
import matplotlib.pyplot as plt
import pdal
import time

window_size = 200
step_size = 100
pre_event_index = './BrownsValley_06_2014/ept.json'
post_event_index = './BrownsValley_09_2014/ept.json'

X = []
Y = []
dx = []
dy = []
for x in np.arange(556627, 558726, step_size):
    for y in np.arange(4238930, 4240977, step_size):
        s = time.time()
        pipeline = [
            {
                'type':'readers.ept',
                'filename':post_event_index,
                'bounds':'([{},{}],[{},{}])'.format(x - 2,
                                                    x + window_size + 2,
                                                    y - 2,
                                                    y + window_size + 2)
            },
            {
                'type':'readers.ept',
                'filename':pre_event_index,
                'bounds':'([{},{}],[{},{}])'.format(x,
                                                    x + window_size,
                                                    y,
                                                    y + window_size)
            },
            {
                'type':'filters.icp'
            }
        ]
        p = pdal.Pipeline(json.dumps(pipeline))
        p.validate()
        p.execute()
        m = json.loads(p.metadata)
        t = m.get('metadata').get('filters.icp')[0].get('transform')
        t = [float(val) for val in t.split()]
        X.append(x + window_size/2)
        Y.append(y + window_size/2)
        dx.append(t[3])
        dy.append(t[7])

plt.figure()
plt.quiver(X, Y, dx, dy, angles='xy', scale_units='xy')
plt.axis('equal')
plt.show()
