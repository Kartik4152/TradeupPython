#http://csgo.exchange/collection/view/{collection_id}/show/{1|2}/{0|1|2|3|4}

import requests
import json
from bs4 import BeautifulSoup
from multiprocessing import Process

#Controllers
stat_trak=False
minProfit=0
budget=9999999999
##################


def getCondition(fl):
    if(fl<=0.07):
        return 'fn'
    elif(fl<=0.15):
        return 'mw'
    elif(fl<=0.38):
        return 'ft'
    elif(fl<=0.45):
        return 'ww'
    elif(fl<=1.0):
        return 'bs'
    else:
        return 'wtf'
upper_fval={
    "fn":0.07,
    "mw":0.15,
    "ft":0.38,
    "ww":0.45,
    "bs":1.0
}
fval={
    "fn":0,
    "mw":0.07,
    "ft":0.15,
    "ww":0.38,
    "bs":0.45
    }
qualities={"Contraband":6,
           "Covert":5,
           "Classified":4,
           "Restricted":3,
           "Mil-Spec Grade":2,
           "Consumer Grade":1
           }
condition={"Factory New":0,
           "Minimal Wear":1,
           "Field-Tested":2,
           "Well-Worn":3,
           "Battle-Scarred":4,
           "Not Available":5
           }

class skin:
    def __init__(self,name,quality,maxwear,minwear):
        self._name=name
        self._quality=quality
        self._maxwear=float(maxwear)
        self._minwear=float(minwear)
        #float=req*(maxwear-minwear)+minwear
        #req=(float-minwear)/(maxwear-minwear)
        self._req={
            'fn':(0.07-self._minwear)/(self._maxwear-self._minwear),
            'mw':(0.15-self._minwear)/(self._maxwear-self._minwear),
            'ft':(0.38-self._minwear)/(self._maxwear-self._minwear),
            'ww':(0.45-self._minwear)/(self._maxwear-self._minwear),
            'bs':(1.00-self._minwear)/(self._maxwear-self._minwear)
        }
    def __repr__(self):
        return f"""
        Name = {self.name}
        Quality = {self.quality}
        MaxWear = {self.maxwear}
        MinWear = {self.minwear}
        """
    @property
    def name(self):
        return self._name
    @property
    def quality(self):
        return self._quality
    @property
    def maxwear(self):
        return self._maxwear
    @property
    def minwear(self):
        return self._minwear
    @property
    def req(self):
        return self._req

# class price:
#     def __init__(self,fn=0,mw=0,ft=0,ww=0,bs=0):
#         self._fn=fn
#         self._mw=mw
#         self._ft=ft
#         self._ww=ww
#         self._bs=bs
#     def __repr__(self):
#         return f"""
#         FN={self._fn if self._fn >=0 else 'Not Available'}
#         MW={self._mw if self._mw >=0 else 'Not Available'}
#         FT={self._ft if self._ft >=0 else 'Not Available'}
#         WW={self._ww if self._ww >=0 else 'Not Available'}
#         BS={self._bs if self._bs >=0 else 'Not Available'}
#         """
#     @property
#     def fn(self):
#         return self._fn
#     @fn.setter
#     def fn(self,x):
#         self._fn=x
#     @property
#     def mw(self):
#         return self._mw
#     @mw.setter
#     def mw(self,x):
#         self._mw=x
#     @property
#     def ft(self):
#         return self._ft
#     @ft.setter
#     def ft(self,x):
#         self._ft=x
#     @property
#     def ww(self):
#         return self._ww
#     @ww.setter
#     def ww(self,x):
#         self._ww=x
#     @property
#     def bs(self):
#         return self._bs
#     @bs.setter
#     def bs(self,x):
#         self._bs=x
    
#collections go from 1 to 67 
f=open('output.txt','w',encoding='utf-8')
for collection_id in range(1,67):
    if(collection_id==54):
        continue
    r=requests.get(f"http://csgo.exchange/collection/view/{collection_id}/show/{int(stat_trak)+1}/0")
    soup=BeautifulSoup(r.text,'html.parser')
    skins=""
    title=BeautifulSoup(requests.get(f"http://csgo.exchange/collection/view/{collection_id}").text,'html.parser').find('h1').text
    print(f'Processing {title}...')
    if not stat_trak:
        skins=soup.find_all('div',{"class":"vItem Normal"})
    else:
        skins=soup.find_all('div',{"class":"vItem StatTrak"})
    result_list=[]
    weapon_list=[]
    price_list=[]
    temp_plist=[]
    temp_list=[]
    cur_price=-1.0
    cur_qual=skins[-1]["data-quality"]
    for j in skins[::-1]:
        if(j["data-quality"]!=cur_qual):
            cur_qual=j["data-quality"]
            weapon_list.append(temp_list.copy())
            price_list.append(temp_plist.copy())
            temp_plist.clear()
            temp_list.clear()
        temp_plist.append({"fn":0,"mw":0,"ft":0,"ww":0,"bs":0})
        temp_list.append(skin(j["data-name"],j["data-quality"],j["data-maxwear"],j["data-minwear"]))
    weapon_list.append(temp_list.copy())    
    price_list.append(temp_plist.copy())  
    for i in range(0,5):
        r=requests.get(f"http://csgo.exchange/collection/view/{collection_id}/show/{int(stat_trak)+1}/{i}")
        soup=BeautifulSoup(r.text,'html.parser')
        skins=""
        if not stat_trak:
            skins=soup.find_all('div',{"class":"vItem Normal"})
        else:
            skins=soup.find_all('div',{"class":"vItem StatTrak"})
        cur_qual=skins[-1]["data-quality"]
        row=0
        col=0
        for j in skins[::-1]:
            if(j["data-quality"]!=cur_qual):
                cur_qual=j["data-quality"]
                row=row+1
                col=0
            if(j["data-exterior"]!='Not Available'):
                cur_price=float(j.find('div',{"class":"priceItem"}).text)
            if(i==0):
                price_list[row][col]['fn']=cur_price
            elif(i==1):
                price_list[row][col]['mw']=cur_price
            elif(i==2):
                price_list[row][col]['ft']=cur_price
            elif(i==3):
                price_list[row][col]['ww']=cur_price
            else:
                price_list[row][col]['bs']=cur_price
            col=col+1            
            cur_price=-1.0

    rows=len(price_list)
    cols=[len(x) for x in price_list]
    profit_list=[]
    for row in range(0,rows-1):
        for col in range(0,cols[row]):
            #cycle through all conditions of current skin
            for condition,value in price_list[row][col].items():
                #check if current skin exists, if not then continue
                if(value==-1):
                    continue
                if(value*10>budget):
                    continue
                minfl=max(weapon_list[row][col].minwear,fval[condition])
                #if it exists, then cycle through all the skins it can trade up to
                #lowest we can go with current skin = max(weapon_list[row][col].minwear,fval[condition])
                for col2 in range(0,cols[row+1]):
                    for condition2,value2 in price_list[row+1][col2].items():
                        if(value==-1):
                            continue
                        if(minfl<=weapon_list[row+1][col2].req[condition2]):
                            result_list.append(f"""
Collection : {title};
Skin : {weapon_list[row+1][col2].name};
Condition : {condition2};
CostOfSkin : {value2};
TradeUpSkins (req 10) : {weapon_list[row][col].name};
CostOfTradeup : {value*10};
Profit (after tax): {value2*0.87-value*10};
FloatRequired : {weapon_list[row+1][col2].req[condition2]};
ConditionRequired: {condition};
                            """)
                            profit_list.append(value2*0.87-value*10)
                            break
                if(len(profit_list)>0):
                    if(min(profit_list)<=minProfit):
                        profit_list.clear()
                        result_list.clear()
                    else:              
                        print('*****************************************************************')    
                        for res in result_list:
                            print(res)
                            f.write(res)       
                        print(f'Max Profit = {max(profit_list)} ; Min Profit = {min(profit_list)}')
                        print('*****************************************************************')
                        profit_list.clear()
                        result_list.clear()
f.close()   
