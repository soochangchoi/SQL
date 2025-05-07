import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
# 엑셀 파일 불러오기
file_path = "sql_teamproject.xlsx"
df = pd.read_excel(file_path, engine="openpyxl")


# 연도별 유효 구인-구직 격차 계산
for year in ["2020년", "2021년", "2022년", "2023년", "2024년"]:
    df[f"{year} 구인-구직 격차"] = df[f"{year} 유효구인인원"] - df[f"{year} 유효구직자수"]

# 그래프 그리기
fig, axes = plt.subplots(nrows=5, figsize=(12, 20))

# 연도별 구인-구직 격차 막대 그래프 생성
for i, year in enumerate(["2020년", "2021년", "2022년", "2023년", "2024년"]):
    df_sorted = df.sort_values(by=f"{year} 구인-구직 격차", ascending=True)
    regions = df_sorted["지역"]
    gap_values = df_sorted[f"{year} 구인-구직 격차"]

    ax = axes[i]
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

plt.tight_layout()
plt.show()