# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 09:35:34 2021

@author: SHAOQM
"""

import pandas as pd
from pathlib import Path
from zipfile import ZipFile
import time

tempalte = r"""!#=====DMCplus===DMCplus===DMCplus===DMCplus===DMCplus===DMCplus===DMCplus=====#
!# This file contains the information of DMCplus Model vector. Do not modify  #
!#=====DMCplus===DMCplus===DMCplus===DMCplus===DMCplus===DMCplus===DMCplus=====#
.VERsion   "1"
.VECtor   "{tag}"  "Raw Data"  "{unit}"  ""
.REMark   ""
.LENgth   {length:d}
.FREquency   5           !(sec)
.STArt   "01-Jan-2021 00:00:00"
.END
!========================================
!!!BEGIN RAW DATA
{data}
!!!END RAW DATA
!========================================"""

def csv2dpv(filename, csvfile = None):
    starttime = time.time()
    timestamp = f'{starttime:<19}'.replace(' ', '0')[:18].replace('.', '')
    exportpath = Path('../data') / timestamp
    exportpath.mkdir(parents=True, exist_ok=True)

    if csvfile:
        df = pd.read_csv(csvfile, skiprows=10, header=[0,1],dtype='unicode').dropna(axis=1)
    else: 
        df = pd.read_csv(filename, skiprows=10, header=[0,1],dtype='unicode').dropna(axis=1)
    
    df.drop(df.columns[0], axis=1, inplace=True)

    zipname =  Path(filename).name[:-4] + '-' +  timestamp + '.zip'
    
    length = len(df.index)
    with ZipFile('../downloads/' + zipname,'w') as zipf:
        for col in df:
            # skip empty columns
            try:
                float(df[col][0])
            except:
                continue
        
            tag,unit = col
            unit = unit[1:-1]
            data = '\n'.join(df[col].tolist())
            res = tempalte.format(tag=tag, unit=unit, length=length, data=data)
            pdvname = f'{tag}.dpv'
            exportfile = exportpath / pdvname
            exportfile.write_text(res)
            zipf.write(exportfile, arcname=pdvname)
    return zipname
