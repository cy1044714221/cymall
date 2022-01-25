import json
import requests
from faker import Faker

fake = Faker(locale='zh_CN')

headers = {
    'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/',
    'Content-Type': 'application/json',
}
import asyncio


def createuser(i):
    pwd = fake.password()
    data = {
        "username": fake.user_name()+fake.user_name(),
        "password": pwd,
        "password2": pwd,
        "sms_code": 926052,
        "mobile": fake.phone_number(),
        "allow": 'true'
    }
    response = requests.post('http://127.0.0.1:8000/users', headers=headers, data=json.dumps(data))
    if response.status_code != 201:
        print(response.text)


# 导入线程池模块对应的类
from multiprocessing.dummy import Pool

# 实例化一个线程池对象
pool = Pool(60)
# 将列表中每一个列表元素传递给get_page进行处理。
pool.map(createuser, [i for i in range(1, 10000)])
pool.close()
pool.join()
