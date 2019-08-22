from urllib.request import urlretrieve
import requests.packages.urllib3
import pandas as pd
import time
import datetime
import csv
import sys

contract = sys.argv[1]

url = "http://info512ah.taifex.com.tw/Future/ImgChartDetail.ashx?type=1&contract=TX"+contract
goods = "臺指期" + contract 
date = datetime.datetime.now().strftime("%Y%m%d")

row_format = "%-8s %6s\n" + "%-8s %6s\n"*10
cvs_title = ['商品代號', '時間', '下一檔價格', '下一檔數量', '下兩檔價格', '下兩檔數量', '下三檔價格', '下三檔數量', '下四檔價格', '下四檔數量', '下五檔價格', '下五檔數量', '上一檔價格', '上一檔數量', '上兩檔價格', '上兩檔數量', '上三檔價格', '上三檔數量', '上四檔價格', '上四檔數量', '上五檔價格', '上五檔數量']

def download_data():
    requests.packages.urllib3.disable_warnings()
    urlretrieve(url, filename="hosts.csv")

def read_data(fileName="./hosts.csv"):
    data = pd.read_csv(fileName,encoding="big5",delimiter='\t')
    data = data[goods]
    return(data)

def split_data(data):
    down = []
    up = []
    for i in range(13,18,1):
        five_data  = data[data.index==i].values[0].split(',')
        down.extend([five_data[0],five_data[1]])
        up.extend([five_data[-2],five_data[-1]])
    down.extend(up)
    return down

def get_time(data):
    t_time = data[data.index==11].values[0].split(',')[-1]
    return t_time

def data_write(output_file):
    writer = csv.writer(output_file)
    writer.writerow(cvs_title)
    record_time = 0
    last_row = []
    yield
    while 1:
        write_data = yield
        if last_row != write_data:
            print(row_format%(*write_data,))
            last_row = write_data.copy()
            record_time = write_data[1]
            writer.writerow(write_data)

if __name__ == '__main__':
    fileName="./%s/%s_UpDn5.csv"%(contract,date)
    with open (fileName,'a',newline='') as output_file:
        write = data_write(output_file)
        next(write)
        while 1:
            download_data()
            data = read_data()
            t_time = get_time(data)
            UpDn5 = split_data(data)
            writeData = [goods,t_time]
            writeData.extend(UpDn5)
            write.send(writeData)
            time.sleep(5)
