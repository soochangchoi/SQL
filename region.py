import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import koreanize_matplotlib
# 엑셀 파일 불러오기
file_path = "sql_teamproject.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")

# 컬럼명 정리
if 'Unnamed: 0' in df.columns:
    df.rename(columns={'Unnamed: 0': '지역'}, inplace=True)

# 연도별 유효 구인-구직 격차 계산
for year in ["2020년", "2021년", "2022년", "2023년", "2024년"]:
    df[f"{year} 구인-구직 격차"] = df[f"{year} 유효구인인원"] - df[f"{year} 유효구직자수"]

# 연도별로 개별 그래프 생성
for year in ["2020년", "2021년", "2022년", "2023년", "2024년"]:
    df_sorted = df.sort_values(by=f"{year} 구인-구직 격차", ascending=True)
    regions = df_sorted["지역"]
    gap_values = df_sorted[f"{year} 구인-구직 격차"]

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(regions, gap_values, color=["red" if x < 0 else "blue" for x in gap_values])

    # 값 표시
    for bar in bars:
        width = bar.get_width()
        ax.annotate(f'{width:,}', 
                    xy=(width, bar.get_y() + bar.get_height()/2),
                    xytext=(5, 0), 
                    textcoords="offset points",
                    ha='left' if width > 0 else 'right', 
                    va='center')

    # 그래프 설정
    ax.set_xlabel("구인-구직 격차 (유효 구인 - 유효 구직)")
    ax.set_ylabel("지역")
    ax.set_title(f"{year} 지역별 유효 구인·구직 격차 분석")
    ax.axvline(0, color='black', linestyle='--', linewidth=1)  # 0 기준선

    # 그래프 출력
    plt.show()
