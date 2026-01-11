import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

def run_marine_visualization(csv_file):
    # 1. 加载数据
    print(f"正在加载数据: {csv_file}...")
    df = pd.read_csv(csv_file)
    df['date_start'] = pd.to_datetime(df['date_start'])
    
    # --- 视图 1: 全球物种分布交互地图 (对应 PPT GeoMap) ---
    print("生成地理分布视图...")
    fig_map = px.scatter_mapbox(
        df, 
        lat="decimalLatitude", 
        lon="decimalLongitude", 
        color="scientificName",
        hover_name="scientificName",
        hover_data={"depth": True, "date_start": "|%Y-%m-%d"},
        zoom=1, 
        height=600,
        title="<b>海洋生物全球观测分布图</b>",
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_map.update_layout(mapbox_style="open-street-map")
    fig_map.update_layout(margin={"r":0,"t":50,"l":0,"b":0})
    fig_map.write_html("map_distribution.html") # 保存为网页格式

    # --- 视图 2: 物种活动深度分布图 (环境因子分析) ---
    print("生成深度分析视图...")
    # 过滤掉深度为空的数据进行分析
    depth_df = df.dropna(subset=['depth'])
    fig_depth = px.box(
        depth_df, 
        x="scientificName", 
        y="depth", 
        color="scientificName",
        points="all", 
        title="<b>各物种活动深度分布对比</b>",
        labels={"depth": "深度 (Meters)", "scientificName": "物种名称"}
    )
    fig_depth.update_layout(showlegend=False)
    fig_depth.write_html("depth_analysis.html")

    # --- 视图 3: 时间序列统计 (行为模式挖掘) ---
    print("生成时间趋势视图...")
    df['year'] = df['date_start'].dt.year
    yearly_counts = df.groupby(['year', 'scientificName']).size().reset_index(name='counts')
    
    fig_time = px.bar(
        yearly_counts, 
        x="year", 
        y="counts", 
        color="scientificName",
        title="<b>年度观测频率趋势</b>",
        barmode="stack",
        template="plotly_white"
    )
    fig_time.write_html("temporal_trends.html")

    print("\n可视化完成！生成了以下文件：")
    print("- map_distribution.html (交互式地图)")
    print("- depth_analysis.html (深度分布分析)")
    print("- temporal_trends.html (时间趋势图)")

if __name__ == "__main__":
    # 确保 github_demo_data.csv 在当前目录下
    run_marine_visualization('github_demo_data.csv')