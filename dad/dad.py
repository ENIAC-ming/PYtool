import os
from sys import argv
import logging
from numpy import array
import zipfile
import pandas as pd
from shutil import rmtree
import warnings
from datetime import datetime

def extract(folder_path, exdir): ## 将folder_path下的.zip文件中的xlsx文件解压到exdir目录下
    if os.path.exists(exdir):
        rmtree(exdir)
    os.makedirs(exdir)
    if os.path.exists(folder_path):
        for f in os.listdir(folder_path):
            if f.endswith('.zip'):
                file_path = os.path.join(folder_path, f)
                if zipfile.is_zipfile(file_path):
                    zip_file = zipfile.ZipFile(file_path)
                    for i in zip_file.namelist():
                        if i.endswith('.xlsx'):
                            zip_file.extract(i, exdir)
                else:
                    log = f'错误: {f} 不是有效的zip文件。'
                    print(log)
                    logging.error(log)
    else:
        print('ERROR: Directory does not exist.')
        logging.error('ERROR: Directory does not exist.')
        os.system('pause')

def merge_xlsx_files(xlsx_files_path, output_file_path):
    cnt = 0
    df = pd.DataFrame({ 'No.':[], 
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
    for f in os.listdir(xlsx_files_path):
        # 读取数据
        file_path = os.path.join(xlsx_files_path, f)
        data = pd.read_excel(file_path, header=None, engine='openpyxl')
        if(data[0][0] != 'Supplier Code:'):
            log = f'错误： {f} 文件格式错误！不是有效文件！'
            print(log)
            logging.error(log)
            continue

        # 数据预处理
        for i in range(0,8,1):
            data.insert(data.shape[1], data.shape[1], data[datapl[i][0]][datapl[i][1]])
        data.insert(data.shape[1], data.shape[1], f)
        # 数据合并
        for i in range(7,len(data.index),1):
            df.loc[len(df.index)] = array(data.loc[i])
        cnt += 1
    df.to_excel(output_file_path, index = False)
    return cnt

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    logging.basicConfig(filename="log.txt",level=logging.INFO)
    print('运行时间：'+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logging.info('运行时间：'+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    try:
        warnings.filterwarnings('ignore')
        logging.basicConfig(filename='log.txt',level=logging.INFO)
        fn = '.\\'
        if len(argv) > 1: 
            fn = argv[1]
        extract(fn, 'extract')
        cnt = merge_xlsx_files('extract', 'output.xlsx')
        print(f'完成，合并了{cnt}个文件。')
        logging.info(f'完成，合并了{cnt}个文件。')
    except Exception as e:
        print(e)
        logging.error(e)
    os.system('pause')