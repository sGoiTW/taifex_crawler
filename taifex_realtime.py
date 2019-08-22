import requests
import datetime,time
import csv
import sys
from bs4 import BeautifulSoup

url = "http://info512ah.taifex.com.tw/Future/FusaQuote_Norl.aspx"

contract = sys.argv[1]
goods = "臺指期" + contract 
date = datetime.datetime.now().strftime("%Y%m%d")

row_format = "%-8s %-10s %8s %6s %6s %10s %10s"
cvs_title = ["商品代號","時間","成交價","成交量","總量","最高價","最低價"]

def get_my_hope_data(goods_name=goods):
    data = requests.get(url)
    soup = BeautifulSoup(data.text, 'html.parser')
    tr_tags = soup.find_all("tr",class_ = "custDataGridRow")
    a = [tr_text.find_all("a")[0].string == goods_name for tr_text in tr_tags ]
    selected_information = [info[0] for info in zip(tr_tags,a) if info[1]==True][0]
    return selected_information

def split_data(data_selected):
    td_tags = data_selected.find_all("td")
    origin_data = [x.string for x in td_tags if x.string!=None]
    return origin_data

def operate_data(data):
    buy_price, buy_amout, sell_price, sell_amout, trade_price, up_down, Amplitude, trade_amout, star_price, max_price, min_price, ref_price, time = data
    return [goods,time,trade_price,buy_amout,trade_amout,max_price,min_price]

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
    fileName = "./%s/%s_Match.csv"%(contract,date)
    with open (fileName,'a',newline='') as output_file:
        write = data_write(output_file)
        next(write)
        while 1:
            origindata = get_my_hope_data()
            o_data = split_data(origindata)
            sort_data = operate_data(o_data)
            write.send(sort_data)
            time.sleep(1)

