import time
from datetime import datetime, timedelta
import pandas as pd

class DateGen:
    def __init__(self):
        pass

    def date_df(self,hr,uID):
        time_t = []
        u_id = []
        for i in range(hr):
            # print(datetime.now())
            time_t.append(datetime.now() + timedelta( hours=i ) )
            u_id.append(uID)
        df = pd.DataFrame({'Time':time_t,'UserID':u_id})
        df.index = df['Time']
        df = df.drop(['Time'],axis=1)
        return df

# dg = DateGen()
# print(dg.date_df(5,1))
