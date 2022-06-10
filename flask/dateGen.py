import time
from datetime import datetime, timedelta
import pandas as pd

class DateGen:
    def __init__(self):
        pass

    def date_df(self,hr,uID):
        # global time_t
        for i in range(hr,uID):
            print(datetime.now())
            time_t=(datetime.now() + timedelta( hours=i ) )
            print(time_t)
        # df = pd.DataFrame({'time':time_t})
        return []

dg = DateGen()
print(dg.date_df(5,1))
