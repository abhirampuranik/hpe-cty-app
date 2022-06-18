import time
import csv
import random
import re
from datetime import datetime, timedelta
import pandas as pd

class DateGenML:
    def __init__(self):
        pass

    def date_df(self,hr,uID):
        time_t = []
        u_id = []
        usage = []
        for i in range(hr):
            # print(datetime.now())
            usage.append(random.randrange(1000000000000, 1200000000000))
            time_t.append(datetime.now() + timedelta( hours=i ) )
            u_id.append(uID)
        df = pd.DataFrame({'Time':time_t,'Usage':usage,'UserID':u_id})
        #df.index = df['Time']
        # df = df.drop(['Time'],axis=1)
        df.to_csv('LR_Predict.csv',index=False)
        return "success"

# dg = DateGen()
# print(dg.date_df(5,1))
