import json
import pdal
import numpy as np
import matplotlib.pyplot as plt
import re


window_size = 200
step_size = 400

X = []
Y = []
u = []
v = []
for x in np.arange(556627 ,558726, step_size):
    for y in np.arange(4238930, 4240977, step_size):
        pipeline = [
            {
                'type':'readers.ept',
                'filename':'./BrownsValley_09_2014/ept.json',
                'bounds':'([{},{}],[{},{}])'.format(x,
                                                    x + window_size,
                                                    y,
                                                    y + window_size)
            },
            {
                'type':'readers.ept',
                'filename':'./BrownsValley_06_2014/ept.json',
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
        # Insert missing spaces between transform matrix rows
        t = re.sub(r'(\d)(\d\.)', r'\1 \2', t)
        t = re.sub(r'(\d)(\-\d)', r'\1 \2', t)
        t = [float(val) for val in t.split()]
        X.append(x + window_size/2)
        Y.append(y + window_size/2)
        u.append(t[3])
        v.append(t[7])

plt.figure()
plt.quiver(X, Y, u, v, angles='xy', scale_units='xy')
plt.axis('equal')
plt.show()
