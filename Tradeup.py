#http://csgo.exchange/collection/view/{collection_id}/show/{1|2}/{0|1|2|3|4}

import requests
import json
from bs4 import BeautifulSoup
from multiprocessing import Process

#Controllers
stat_trak=False
##################



qualities={"Covert":5,
           "Classified":4,
           "Restricted":3,
           "Mil-Spec Grade":2,
           "Consumer Grade":1
           }
condition={"Factory New":0,
           "Minimal Wear":1,
           "Field-Tested":2,
           "Well-Worn":3,
           "Battle-Scarred":4
           }

class skin:
    def __init__(self,name,quality,maxwear,minwear):
        self.name=name
        self.quality=quality
        self.maxwear=maxwear
        self.minwear=minwear
    def __repr__(self):
        return f"""
        Name = {self.name}
        Quality = {self.quality}
        MaxWear = {self.maxwear}
        MinWear = {self.minwear}
        """ 


for collection_id in range(1,2):
    r=requests.get(f"http://csgo.exchange/collection/view/{collection_id}/show/{int(stat_trak)+1}/{condition['Factory New']}")
    soup=BeautifulSoup(r.text,'html.parser')
    skins=""
    if not stat_trak:
        skins=soup.find_all('div',{"class":"vItem Normal"})
    else:
        skins=soup.find_all('div',{"class":"vItem StatTrak"})
    lowestQual=skins[-1]["data-quality"]
    highestQual=skins[0]["data-quality"]
    weapon_list=[]
    temp_list=[]
    cur_qual=skins[-1]["data-quality"]
    for j in skins[::-1]:
        if(j["data-quality"]!=cur_qual):
            cur_qual=j["data-quality"]
            weapon_list.append(temp_list.copy())
            temp_list.clear()
        temp_list.append(skin(j["data-name"],j["data-quality"],j["data-maxwear"],j["data-minwear"]))
    weapon_list.append(temp_list.copy())    
    print(weapon_list[0])
    