import json
import random

import requests
from faker import Faker
import pandas as pd
from pandas import DataFrame

fake = Faker(locale='zh_CN')
hosts = 'http://127.0.0.1:8000'
areas = pd.read_csv('./cy_areas.csv')
sku_id = [1, 2, 3]


def createdata():
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

    """JWT登陆"""
    data = {"username": username, "password": pwd}
    response = requests.post(hosts + '/authorizations', headers={'Content-Type': 'application/json'},
                             data=json.dumps(data))
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
    data = {
        "addressee": fake.name(),
        "province_id": province_id,
        "city_id": city_id,
        "district_id": district_id,
        "place": place,
        "mobile": fake.phone_number()
    }
    response = requests.post(hosts + '/addresses', headers=headers, data=json.dumps(data))
    address_id = response.json()['id']

    """加入购物车"""
    data = {"sku_id": random.choice(sku_id), "count": random.randint(1, 6)}
    response = requests.post(hosts + '/carts', headers=headers, data=json.dumps(data))
    """提交订单"""
    pay_method = [1, 2]
    data = {"address": address_id, "pay_method": random.choice(pay_method)}
    response = requests.post(hosts + '/orders', headers=headers, data=json.dumps(data))
    print(response.json())


num = 0
while num < 10:
    try:
        createdata()
    except Exception:
        continue
    num += 1
