import pandas as pd
import matplotlib.pyplot as plt

# 1. 设置中文字体，防止图表里的中文变成方块
plt.rcParams['font.sans-serif'] = ['SimHei'] # Windows系统用黑体
plt.rcParams['axes.unicode_minus'] = False

print("正在读取最终干净的数据...")
# 读取刚才第二步生成的干净文件
df = pd.read_csv("maotai_final_clean.csv")

# 2. 开始画图
plt.figure(figsize=(12, 6)) # 设置画布大一点，因为茅台的历史数据很长

# 画折线图：X轴是日期，Y轴是净利润
plt.plot(df['Date'], df['净利润'], marker='o', color='#E63946', linewidth=2, markersize=4, label='净利润')

# 设置图表标题和坐标轴标签
plt.title('贵州茅台历年净利润趋势图', fontsize=18)
plt.xlabel('年份', fontsize=12)
plt.ylabel('净利润 (元)', fontsize=12)

# 把X轴的日期倾斜一下，防止字叠在一起
plt.xticks(rotation=45)

# 添加网格线，让图表看起来更专业
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()

# 3. 调整布局并保存图表
plt.tight_layout() # 自动调整布局防遮挡
plt.savefig("maotai_profit_trend.png", dpi=300)
print("🎉 大功告成！图表已保存为 maotai_profit_trend.png！")

# 在屏幕上显示图表
plt.show()