import pandas as pd
import numpy as np


import matplotlib.pyplot as plt

import csv
import random
import re
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.style import use
import numpy as np


temp = []
xpoints = []
ypoints = []
# random.seed(10)

for i in range(1,1000):
  a = random.randrange(i*10000, i*10000000)
  
  time_t = (datetime.now() + timedelta( hours=i ) )

  temp.append([ time_t, a, 1 ])
  temp.append([ time_t, a, 2 ]) 
  temp.append([ time_t, a, 3 ]) 
  temp.append([ time_t, a, 4 ]) 
  temp.append([ time_t, a, 5 ]) 



header = ['Time', 'Usage','UserID']
with open('random.csv', 'w', encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(header)

    # write the data
    writer.writerows(temp)
