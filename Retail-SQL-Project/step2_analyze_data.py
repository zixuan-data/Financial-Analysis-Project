import sqlite3
import pandas as pd

# 设置 pandas 显示选项，让控制台打印出来不要折叠列
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

conn = sqlite3.connect('retail_sales.db')

# ==========================================
# 任务 1：计算每个城市的月度总销售额（日期截取、GROUP BY 聚合）
# ==========================================
sql_task1 = """
SELECT 
    city AS 城市,
    SUBSTR(order_date, 1, 7) AS 月份, 
    SUM(amount) AS 月销售额
FROM sales_data
GROUP BY city, SUBSTR(order_date, 1, 7)
ORDER BY 月销售额 DESC
LIMIT 5;
"""
print("\n--- 任务 1：各城市单月最高销售额 Top 5 ---")
print(pd.read_sql_query(sql_task1, conn))

# ==========================================
# 任务 2：找出每个城市销售额最高的商品（RANK/DENSE_RANK）
# ==========================================
sql_task2 = """
WITH ProductSales AS (
    SELECT 
        city AS 城市,
        product_name AS 商品,
        SUM(amount) AS 总销售额,
        RANK() OVER(PARTITION BY city ORDER BY SUM(amount) DESC) as rnk
    FROM sales_data
    GROUP BY city, product_name
)
SELECT 城市, 商品, 总销售额
FROM ProductSales
WHERE rnk = 1;
"""
print("\n--- 任务 2：各城市销售额 Top 1 的商品（窗口函数） ---")
print(pd.read_sql_query(sql_task2, conn))

# ==========================================
# 任务 3：计算各销售渠道的转化率/客单价（COUNT DISTINCT 去重）
# ==========================================
sql_task3 = """
SELECT 
    channel AS 渠道,
    COUNT(order_id) AS 订单总数,
    COUNT(DISTINCT user_id) AS 购买人数,
    ROUND(SUM(amount) / COUNT(DISTINCT user_id), 2) AS 客单价
FROM sales_data
GROUP BY channel
ORDER BY 客单价 DESC;
"""
print("\n--- 任务 3：各渠道客单价与购买人数 ---")
print(pd.read_sql_query(sql_task3, conn))

# ==========================================
# 任务 4：找出复购用户（消费次数 >= 2 的用户），提取他们的消费明细（子查询/HAVING）
# ==========================================
sql_task4 = """
SELECT 
    user_id AS 用户ID,
    COUNT(order_id) AS 购买次数,
    SUM(amount) AS 累计消费金额
FROM sales_data
GROUP BY user_id
HAVING COUNT(order_id) >= 2
ORDER BY 累计消费金额 DESC
LIMIT 5;
"""
print("\n--- 任务 4：复购用户 Top 5 ---")
print(pd.read_sql_query(sql_task4, conn))

# ==========================================
# 任务 5：把复购用户 Top 10 画成柱状图，并保存到本地
# ==========================================
import matplotlib.pyplot as plt
import matplotlib

# 设置中文字体（Windows 系统）
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 修改一下刚才的 sql_task4，只取前 10 名
sql_chart = """
SELECT user_id, 
       SUM(amount) AS total_amount
FROM sales_data
GROUP BY user_id
HAVING COUNT(order_id) >= 2
ORDER BY total_amount DESC
LIMIT 10;
"""
df_chart = pd.read_sql_query(sql_chart, conn)

# 画图
plt.figure(figsize=(10, 6))
plt.bar(df_chart['user_id'], df_chart['total_amount'], color='skyblue')
plt.title('Top 10 复购用户累计消费金额')
plt.xlabel('用户 ID')
plt.ylabel('累计消费金额 (元)')
plt.xticks(rotation=45)#45度防重叠

# 保存图片，紧凑边缘把白边裁掉
plt.savefig('retail_top_users.png', bbox_inches='tight')
print("\n图表已保存为 retail_top_users.png")

conn.close()