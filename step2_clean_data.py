import pandas as pd

print("正在读取原始数据...")
# 读取原始抓下来的数据
df = pd.read_csv("maotai_data.csv")

# 前两列通常是 '选项' 和 '指标'，后面全是日期
# 我们直接定位到 '指标' 这一列
indicator_col = df.columns[1]

# 1. 精准抓取“净利润”这一行（排除带“归母”或“扣非”字眼的干扰项）
net_profit_row = df[df[indicator_col].astype(str).str.contains('净利润', na=False) &
                    ~df[indicator_col].astype(str).str.contains('归母|扣非', na=False)]

# 2. 提取日期（从第3列开始的所有表头）和对应的值
dates = df.columns[2:]
values = net_profit_row.iloc[0, 2:]

# 3. 组装成我们想要的干净两列：Date 和 净利润
clean_df = pd.DataFrame({
    'Date': dates,
    '净利润': values
})

# 4. 清洗：只要8位数的日期，把金额转成数字，排序
clean_df = clean_df[clean_df['Date'].astype(str).str.len() == 8]
clean_df['Date'] = pd.to_datetime(clean_df['Date'], format='%Y%m%d')
clean_df['净利润'] = pd.to_numeric(clean_df['净利润'], errors='coerce')
clean_df = clean_df.sort_values('Date')

# 5. 保存！
clean_df.to_csv("maotai_final_clean.csv", index=False, encoding='utf-8-sig')
print("终极清洗完成！预览如下：")
print(clean_df.head())