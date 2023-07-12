import os
import io
import zipfile
import pandas as pd
import numpy as np

df = pd.DataFrame({'No.':[], 
                    'Part No.':[], 
                    'Back':[], 
                    'No':[], 
                    'Q\'ty/KANBAN':[], 
                    'Total':[], 
                    'Check':[], 
                    'Comment':[],
                    'Supplier Code':[],
                    'Supplier Name':[],
                    'Supplv Area':[],
                    'Delivery Date':[],
                    'Truck No':[],
                    'JIT Call No':[],
                    'Date of issue':[],
                    'Cycle':[],
                    'File Name':[]})
datapl = [[1,0],[1,1],[1,2],[1,3],[4,3],[7,1],[7,2],[7,3]]

# 读取数据
data = pd.read_excel("test.xlsx", header=None)

# 数据预处理
for i in range(0,8,1):
    data.insert(data.shape[1], data.shape[1], data[datapl[i][0]][datapl[i][1]])

# 数据合并
for i in range(7,len(data.index),1):
    df.loc[len(df.index)] = np.array(data.loc[i])