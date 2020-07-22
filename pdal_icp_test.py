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

dt = []
dx = []
dy = []
dz = []

x = 556627
y = 4238930
t_thresh = [9e-3, 9e-4, 9e-5, 9e-6, 9e-7, 9e-8, 9e-9, 9e-10, 9e-11]

for tt in t_thresh:
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
            'type':'filters.icp',
            'tt':tt,
            'max_iter':200,
            # 'rt':0.999999999,
            'mse_abs':1e-20,
            'max_similar':100
        }
    ]
    p = pdal.Pipeline(json.dumps(pipeline))
    p.validate()
    p.execute()
    m = json.loads(p.metadata)
    t = m.get('metadata').get('filters.icp')[0].get('transform')
    print(t)
    e = time.time()
    tm = e-s
    print(tm)
    t = [float(val) for val in t.split()]
    dx.append(t[3])
    dy.append(t[7])
    dz.append(t[11])
    dt.append(tm)

dx = np.asarray(dx)
dy = np.asarray(dy)
tt = np.asarray(tt)
cmb = np.vstack((dt, t_thresh, dx, dy, dz))
np.savetxt('tt.txt', cmb)


