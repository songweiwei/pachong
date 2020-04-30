# -*- coding: utf-8 -*-
# author: songwei
# place: Shenzhen Guangdong
# time: 2020/4/26 14:17
import os, re, json, traceback
import requests
import json
import time
import pandas as pd
import os


def fetchHotel(city, star, page):
    url = "https://hotels.ctrip.com/Domestic/Tool/AjaxHotelList.aspx"
    headers = {
        'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'https://hotels.ctrip.com',
        'Referer': 'https://hotels.ctrip.com/hotel/beijing1',
        'accept': '*/*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
        'cookie':'ga=GA1.2.652986780.1569503628; _RF1=218.17.112.191; _RSG=yPay3y7yxp4HArGzzPI8lB; _RDG=2823bb45aaf7372c592bb4a92864a49cb6; _RGUID=4cfbf07f-03f2-467c-bbc8-499f7d435291; UM_distinctid=16f8f8167d99dc-0f85f3d39f4677-6701b35-144000-16f8f8167da986; MKT_CKID=1578660623323.j4yam.v0hw; magicid=XKhxSMiRT2fD3hdzs3RFGPiESF04RUE8O3luuQcYVpPBaLSQv4yIN4/TI76Mhhde; ASP.NET_SessionId=mqqvojhw3clyzdwuqhhfnrw3; _abtest_userid=b1197616-2646-4871-91d4-ef131bb4b94e; hoteluuid=A0zFC5pm95q5CHbd; OID_ForOnlineHotel=15695036275483f32ow1587868823236102032; _gid=GA1.2.1105782744.1587868825; Session=SmartLinkCode=csdn&SmartLinkKeyWord=&SmartLinkQuary=_UTF.&SmartLinkHost=blog.csdn.net&SmartLinkLanguage=zh; MKT_CKID_LMT=1587868825572; MKT_Pagesource=PC; fcerror=113287591; _HGUID=T%03%06%02%06PW%06MPS%06RMTVW%03M%02%02%03XMTYY%06W%04TSURYQ; _zQdjfing=1336fa1336fa5fa4cc3365ac3a923a3165bbd5c08665b02e1336fa; HotelDomesticVisitedHotels1=56187715=0,0,4.9,37,/200l1c000001di36z3715.jpg,; appFloatCnt=15; GUID=09031130211312129809; Union=OUID=&AllianceID=66672&SID=1693366&SourceID=&AppID=&OpenID=&createtime=1587872328&Expires=1588477128412; login_uid=0ECFD7BB8984A976B4E6BAFFE73CA74D; login_type=6; cticket=B705FD64EC8BB5CFFCABA72D7E17B000AF3B5F4126168F3C2DBE63399F37772E; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; ticket_ctrip=bJ9RlCHVwlu1ZjyusRi+ypZ7X2r4+yojcAtLNjRoozV/vyFwtNrQInk251+UXHS8j2S/Na+2aCIzsKIH6mEpZEm9AWYFHqqVIE/AxGNATlZKbsIvcLUczAGMFx4JKYuaoJuc9bJnTZWTNK0HnWB4U/uVzRBSMzSRHq5r5SMGtYd65h6APGyMNRDDfKZT9ScV7ydiDgvaAQM1akJYsM7YcwOZq37oCiIdhoPdbZBG/K4RstPBeUxeZjUg+EwsjHcSvTM3bpvmNJrdvYKDl5XN32gggkQrqvAFWl7kydwfD54=; DUID=u=2E6BFC4CB8A2BC7E3C3F6F89B5C19DE9&v=0; IsNonUser=u=2E6BFC4CB8A2BC7E3C3F6F89B5C19DE9&v=0; UUID=49B8C1D34C544A15BCB097AB9ED26E58; IsPersonalizedLogin=F; _bfi=p1%3D102002%26p2%3D102003%26v1%3D38%26v2%3D30; _gat=1; _jzqco=%7C%7C%7C%7C1587868825793%7C1.427969904.1569503633559.1587871492719.1587882458919.1587871492719.1587882458919.undefined.0.0.18.18; __zpspc=9.4.1587882458.1587882458.1%233%7Cblog.csdn.net%7C%7C%7C%7C%23; hoteluuidkeys=QctJSQY1beplEfMW3Y5YNOY6qENYqY8UeUnEZHj4HWZYhY5pIQBe8QvSOj4Y1YHpinkwN4KUMjlY5YcBjg0wUfIG4j6YBY90yn7YL0y3Mv61wPbeb5Y0ljLgysYSY7sI84K1lxgowApI0DiHGi3diZYHYFYXYhqv4he5sYOoisdYlYDYcYoYdLEaUKkNwPci4QRP0jmrhzYdNJ57y6rGOYgOW6OvN7xoFeBUYmOxDPxU7YfXiqQw4zj5SES8JgFWNSjArdcJsdiFLwbmv38RU0jgfYd6jbrQOytFiUswaHRf9Enbjpdx3UxUME03EXDEAaWN8eh4wbcEdZjOteDniSaYcgrF4eZ7efdx14iz3iOmxH4WzQj46ezXw0XKsqwpziSXRDLjP3emfEcky61vUci35EHkynpva8K01Em0KHUwq7i3sRONjQraFYoFJb0yNrX7jaNePBjdMKMGj4QwZpx9bxdmxogxabEOlEcoEGoWPoe4GwGTETojZ3e0biU7YGprT1E1MyfNvbsiB5EZ9yFavFmK87WkpE3AjSGe0cx9MjorUoE7UWtpeP1j75Y1oj9sx09xzhxS3xt5E0PEPoEQ3WPHe5nwMTEaSj0Se3tiGsYUkrPle6Be9FYhlEcawNzW1GillKUmEcqE1GEqUW1Be7swFpENkjc6eATiqnYLArGBesDel7EUtY3SEhkwUtWdmiZY1YXnYs6i8XitLiT5jkYSYt4wnSEmbETdJLmjdbyOMjkpjLYDYMkR4BJ6DjhAyNDjp3jzHY34EMDw09WNojbLRZmEkY8YMnYcGW4Grzky3zE70JOPEslRsTv1DJPXJk5JTXEl3vLBJlAyQYGYhdRmaJDkwdPv05J6dWGSi9kwdcYA9yakJUDEc9j4YfY3HjzQwmbvb1; _bfa=1.1569503627548.3f32ow.1.1587876628550.1587882456221.6.39.212093; _bfs=1.2; hotelhst=2012709687'
    }

    formData = {
        'cityId': city,
        'star': star,
        'page': page,
    }

    # 发起网络请求
    r = requests.post(url, data=formData, headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding    #防止出现乱码现象

    # 解析 json 文件，提取酒店数据
    js=json.loads(r.text)
    json_data = json.loads(r.text)['hotelPositionJSON']

    hotelList = []
    for item in json_data:
        hotelId = item['id']
        hotelList.append(hotelId)

    return hotelList


print(fetchHotel("1","4","1"))



# def fetchCmts(hotel, page):
#     url = "https://m.ctrip.com/restapi/soa2/16765/gethotelcomment?&_fxpcqlniredt=09031074110034723384"
#     headers = {
#         'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
#         'Referer': 'https://m.ctrip.com/webapp/hotel/hoteldetail/dianping/' + hotel + '.html?&fr=detail&atime=20191027&days=1',
#         'Origin': 'https://m.ctrip.com',
#         'accept': '*/*',
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
#     }
#
#     formData = {
#         'groupTypeBitMap': '3',
#         'auth': "",
#         'cid': "09031074110034723384",
#         'ctok': "",
#         'cver': "1.0",
#         'extension': '[]',
#         'lang': "01",
#         'sid': "8888",
#         'syscode': "09",
#         'hotelId': str(hotel),
#         'needStatisticInfo': '0',
#         'order': '0',
#         'pageIndex': str(page),
#         'pageSize': '10',
#         'tagId': '0',
#         'travelType': '-1',
#     }
#
#     r = requests.post(url, data=formData, headers=headers)  # formData,
#     r.raise_for_status()
#     r.encoding = r.apparent_encoding
#
#     json_data = json.loads(r.text)
#
#     cmtsList = []
#     hotelName = json_data['hotelName']
#
#     for item in json_data['othersCommentList']:
#         cmt = []
#
#         userName = item['userNickName']
#         travelType = item['travelType']
#         baseRoomName = item['baseRoomName']
#         checkInDate = item['checkInDate']
#         postDate = item['postDate']
#         ratingPoint = item['ratingPoint']
#         content = item['content']
#
#         cmt.append(userName)
#         cmt.append(hotelName)
#         cmt.append(travelType)
#         cmt.append(baseRoomName)
#         cmt.append(checkInDate)
#         cmt.append(postDate)
#         cmt.append(ratingPoint)
#         cmt.append(content)
#
#         cmtsList.append(cmt)
#
#     return cmtsList
#
#
# def saveCmts(path, filename, data):
#     # 如果路径不存在，就创建路径
#     if not os.path.exists(path):
#         os.makedirs(path)
#
#     # 保存文件
#     dataframe = pd.DataFrame(data)
#     dataframe.to_csv(path + filename, encoding='utf_8_sig', mode='a', index=False, sep=',', header=False)
#
#
# if __name__ == '__main__':
#     hotel = '469055'  # 上海静安香格里拉大酒店
#     startPage = 1
#     endPage = 100
#     path = 'Data/'
#     filename = 'cmtTest.csv'
#
#     for p in range(startPage, endPage + 1):
#         cmts = fetchCmts(hotel, p)
#         saveCmts(path, filename, cmts)
#         time.sleep(0.5)










