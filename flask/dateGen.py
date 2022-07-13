from mimetypes import init
import time
from datetime import datetime, timedelta
import pandas as pd

class DateGen:
    def __init__(self):
        pass

    def date_df(self,hr,uID,initTime):
        # print(initTime)
        initTime = initTime.split(".")[0]
        # print("here "+initTime)
        dt_tuple=tuple([int(x) for x in initTime[:10].split('-')])+tuple([int(x) for x in initTime[11:].split(':')])
        initTime = datetime(*dt_tuple)
        time_t = []
        u_id = []
        for i in range(hr):
            time_t.append(initTime + timedelta( hours=i+1 ))
            u_id.append(uID)
        df = pd.DataFrame({'Time':time_t,'UserID':u_id})
        df.index = df['Time']
        df = df.drop(['Time'],axis=1)
        return df

