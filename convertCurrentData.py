import numpy as np
import waterLevelScripts as WaterLevel
import pdb
from datetime import datetime
import os
import pandas as pd

now = datetime.now()
scriptWD = os.path.dirname(os.path.realpath(__file__))
wLevel = pd.read_csv(scriptWD+'/data/waterLevel_%s.data' % now.strftime("%Y-%m"),sep='\t',header=None)
#print(wLevel.tail(3))
#wLevel.info()
wLevel = wLevel.rename(columns={1:'WaterLevel'})
wLevel['Time'] = pd.to_datetime(wLevel[0], format='%Y-%m-%d %H-%M-%S') 
    
#data = np.readcsv("%s/data/waterLevel_%s.data" % (scriptWD,now.strftime("%Y-%m")))

nEntries = len(wLevel)
dFile = open("%s/data/waterLevel2_%s.data" % (scriptWD,now.strftime("%Y-%m")),"a")

for n in range(nEntries):
    #pdb.set_trace()
    currentH20Content = WaterLevel.getWaterContentFromDistance(wLevel['WaterLevel'][n],wd=scriptWD)
    dFile.write("%s\t%s\t%s\n" % (str(wLevel['Time'][n]),wLevel['WaterLevel'][n],currentH20Content))

dFile.close()
