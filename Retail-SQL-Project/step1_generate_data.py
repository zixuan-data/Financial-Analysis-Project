import pandas as pd
import numpy as np
import random
import sqlite3
from datetime import datetime, timedelta

# 1. 设置随机种子，保证每次生成的数据一样，方便后面调错
np.random.seed(42)
random.seed(42)

# 2. 定义基础信息
num_records = 5000
cities = ['上海', '苏州', '南京', '杭州', '无锡']
categories = ['数码', '家电', '服饰', '美妆', '食品']
products = {
    '数码': ['手机', '平板', '耳机'],
    '家电': ['冰箱', '洗衣机', '空调'],
    '服饰': ['T恤', '牛仔裤', '外套'],
    '美妆': ['口红', '面膜', '香水'],
    '食品': ['零食大礼包', '饮料', '生鲜']
}
channels = ['线上APP', '微信小程序', '线下门店']

# 3. 生成随机数据
data = []
start_date = datetime(2025, 1, 1)

for i in range(1, num_records + 1):
    # 随机时间（2025年全年）
    random_days = random.randint(0, 364)
    order_date = start_date + timedelta(days=random_days)

    # 随机商品信息
    category = random.choice(categories)
    product = random.choice(products[category])
    price = round(random.uniform(50, 8000), 2)  # 价格在50到8000之间
    quantity = random.randint(1, 5)
    amount = round(price * quantity, 2)

    # 随机客户（模拟复购，让部分用户ID重复）
    user_id = f"U{random.randint(1000, 2500)}"

    # 构造一条记录
    data.append({
        'order_id': f"O{10000 + i}",
        'order_date': order_date.strftime('%Y-%m-%d'),
        'user_id': user_id,
        'city': random.choice(cities),
        'channel': random.choice(channels),
        'category': category,
        'product_name': product,
        'price': price,
        'quantity': quantity,
        'amount': amount
    })

# 4. 转 DataFrame 并保存
df = pd.DataFrame(data)

# 看前5行
print("生成的原始数据示例：")
print(df.head())

# 5. 写入 SQLite 数据库
conn = sqlite3.connect('retail_sales.db')
df.to_sql('sales_data', conn, if_exists='replace', index=False)
conn.close()

print(f"\n成功!共生成 {num_records} 条数据，已存入 SQLite 数据库 'retail_sales.db' 的 'sales_data' 表。")