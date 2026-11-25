import akshare as ak
import pandas as pd

print("正在抓取茅台财务数据，请稍等...")
df = ak.stock_financial_abstract(symbol="600519")

print("抓取成功，前5行数据如下：")
print(df.head())

df.to_csv("maotai_data.csv", index=False, encoding='utf-8-sig')
print("数据已保存为 maotai_data.csv！")