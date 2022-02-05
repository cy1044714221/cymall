import json
import random
import threading
import time
import csv

import requests
from faker import Faker
import pandas as pd

fake = Faker(locale='zh_CN')
hosts = 'http://124.223.90.3:8000'
areas = pd.read_csv('./cy_areas.csv')
sku_id = [1, 2, 3]
f = open('./userinfo.csv', 'a+', encoding='utf-8')


def createuser():
    username = fake.user_name()
    pwd = fake.password()
    data = {
        "username": username,
        "password": pwd,
        "password2": pwd,
        "sms_code": 926052,
        'email': fake.ascii_company_email(),
        "mobile": fake.phone_number(),
        "allow": 'true'
    }

    """注册用户"""
    response = requests.post(hosts + '/users', headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    if response.status_code != 201:
        print(response.text)
    f_csv = csv.writer(f)
    f_csv.writerow([username, pwd])


def createorder():
    """JWT登陆"""
    usercsv = csv.reader(open('./userinfo.csv'))
    userinfo_list = []
    for i in usercsv:
        userinfo_list.append(i)
    userinfo = random.choice(userinfo_list)
    user_data = {"username": userinfo[0], "password": userinfo[1]}
    response = requests.post(hosts + '/authorizations', headers={'Content-Type': 'application/json'},
                             data=json.dumps(user_data))
    token = response.json()['token']
    headers = {
        'Authorization': 'JWT ' + token,
        'Content-Type': 'application/json',
    }

    """添加用户地址"""
    # 生成地址
    s1 = areas[areas['parent_id'].isnull()]['id'].values.tolist()
    province_id = random.choices(s1)[0]
    s2 = areas[areas['parent_id'] == province_id]['id'].values.tolist()
    city_id = random.choices(s2)[0]
    s3 = areas[areas['parent_id'] == city_id]['id'].values.tolist()
    district_id = random.choice(s3)
    place = fake.street_address()
    address_data = {
        "addressee": fake.name(),
        "province_id": province_id,
        "city_id": city_id,
        "district_id": district_id,
        "place": place,
        "mobile": fake.phone_number()
    }
    response = requests.post(hosts + '/addresses', headers=headers, data=json.dumps(address_data))
    address_id = response.json()['id']
    while True:
        """加入购物车"""
        carts_data = {"sku_id": random.choice(sku_id), "count": random.randint(1, 6)}
        response = requests.post(hosts + '/carts', headers=headers, data=json.dumps(carts_data))
        """查看购物车"""
        response = requests.get(hosts + '/carts', headers=headers).text
        print(response)
        if response:
            """提交订单"""
            pay_method = [1, 2]
            order_data = {"address": address_id, "pay_method": random.choice(pay_method)}
            response = requests.post(hosts + '/orders', headers=headers, data=json.dumps(order_data))
            print(response.json())
            break



def fun1():
    while True:
        try:
            createuser()
        except Exception:
            continue
        time.sleep(random.randint(120, 1200))


def fun2():
    while True:
        try:
            createorder()
        except Exception:
            continue
        time.sleep(random.randint(80, 800))


threads = []
threads.append(threading.Thread(target=fun1))
threads.append(threading.Thread(target=fun2))

for t in threads:
    t.start()
