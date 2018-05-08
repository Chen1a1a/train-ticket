# -*- coding:utf-8 -*-
import urllib.request
import json
import datetime

#自定义浏览器Header
my_headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36 LBBROWSER"
}

#站点信息 --- 构建字典 stationDict 站名:简称 opStationDict 简称:站点
versionUrl = "https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version"
versionReq = urllib.request.Request(versionUrl, headers = my_headers)
stationData = urllib.request.urlopen(versionReq).read().decode('utf-8').split("'")[1].split('|')
stationDict = {}
opStationDict = {}
i = 0
while i < len(stationData)-1:
    stationDict[stationData[i+1]] = stationData[i+2]
    opStationDict[stationData[i+2]] = stationData[i+1]
    i = i + 5
#print(stationDict)

#用户输入信息
trainDate = input("请输入出发日期：")
fromStation = input("请输入出发地：")
toStation = input("请输入目的地：")
tomorrow= (datetime.datetime.now() + datetime.timedelta(days = 1)).strftime('%Y-%m-%d')
if(trainDate == "") : trainDate = tomorrow

#请求数据库查询
queryUrl = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=" + trainDate + "&leftTicketDTO.from_station=" + stationDict[fromStation] +"&leftTicketDTO.to_station=" + stationDict[toStation] + "&purpose_codes=ADULT"
req = urllib.request.Request(queryUrl, headers = my_headers)
html = urllib.request.urlopen(req)
data = json.loads(html.read().decode('utf-8'))

#处理并输出数据
#始发站 4 终到站 5 出发站 6 到达站 7
#出发时间 8 到达时间 9 历时 10
#数据长度 37 商务座特等座 32 一等座 31 二等座 30
#高级软卧 软卧 23 动卧 硬卧 28 软座 硬座 29 无座 26 其他
#标题行 车次 车站 时间 历时 特等 一等  二等 软卧 硬卧 硬座 无座
print("车次\t车站        \t时间\t历时\t特等\t一等\t二等\t软卧\t硬卧\t硬座\t无座")
train_num = len(data['data']['result'])
for i in range(train_num) :
    train_info = data['data']['result'][i].split('|')
    #处理无票信息为--
    for n in range(23, 33) :
        if(train_info[n] == "") : train_info[n] = "--"
    star = opStationDict[train_info[6]]
    end = opStationDict[train_info[7]]
    #对齐处理
    if(len(star) < 6) : 
        for i in range(6 - len(star)) :
            star = star + "  "
    if(len(end) < 6) : 
        for i in range(6 - len(end)) :
            end = end + "  "
    print(train_info[3] + "\t"+ star + "\t" + train_info[8] + "\t" + train_info[10] + "\t" + train_info[32] + "\t" + train_info[31] + "\t" + train_info[30] + "\t" + train_info[23] + "\t" + train_info[28] + "\t" + train_info[29] + "\t" + train_info[26])
    print("\t" + end + "\t" +train_info[9])
    print("------------------------------------------------------------------------------------------")