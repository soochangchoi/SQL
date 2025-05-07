import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
# 데이터 불러오기
file_path_unemployment = "연령_교육정도별_실업률.xlsx"  # 실업률 데이터 파일
file_path_population = "active_non_active_population.xlsx"  # 경제활동 및 비경제활동인구 데이터 파일

# 실업률 데이터 로드
df_unemployment = pd.read_excel(file_path_unemployment, sheet_name="데이터")

# 전체 실업률 데이터 추출 (연령계층별 '계' & 교육정도별 '계' 행 선택)
df_unemployment_total = df_unemployment[(df_unemployment["연령계층별"] == "계") & (df_unemployment["교육정도별"] == "계")]
df_unemployment_total = df_unemployment_total.iloc[:, 2:].apply(pd.to_numeric, errors='coerce')

# 연도별 실업률 데이터 정리
years = df_unemployment_total.columns.astype(int)
unemployment_rate = df_unemployment_total.values.flatten()

df_unemployment_cleaned = pd.DataFrame({
    "년도": years,
    "실업률 (%)": unemployment_rate
})

# 비경제활동 및 경제활동인구 데이터 로드
df_population = pd.read_excel(file_path_population)

# 데이터 전처리 (비경제활동 & 경제활동 인구 데이터)
years_pop = list(map(int, df_population.columns[1:]))
non_economically_active = pd.to_numeric(df_population.iloc[0, 1:].str.replace(',', ''), errors='coerce')
economically_active = pd.to_numeric(df_population.iloc[1, 1:].str.replace(',', ''), errors='coerce')

# 증가율 계산
non_active_growth = non_economically_active.pct_change() * 100  # 비경제활동인구 증가율 (%)
active_growth = economically_active.pct_change() * 100  # 경제활동인구 증가율 (%)

# 경기침체 분석 데이터프레임 생성
analysis_df = pd.DataFrame({
    "년도": years_pop[1:],  # 첫 번째 연도는 증가율 계산 불가
    "비경제활동인구 증가율 (%)": non_active_growth.iloc[1:].values,
    "경제활동인구 증가율 (%)": active_growth.iloc[1:].values
})

# 실업률 데이터 결합
df_combined = analysis_df.merge(df_unemployment_cleaned, on="년도", how="inner")

# 실업률, 비경제활동인구 증가율, 경제활동인구 증가율 비교 그래프
fig, ax1 = plt.subplots(figsize=(12, 6))

# 비경제활동인구 증가율 (막대 그래프)
ax1.bar(df_combined["년도"], df_combined["비경제활동인구 증가율 (%)"], 
        color='red', alpha=0.6, label="비경제활동인구 증가율 (%)")
ax1.set_ylabel("비경제활동인구 증가율 (%)", color='red')
ax1.tick_params(axis='y', labelcolor='red')

# 경제활동인구 증가율 (파란색 선 그래프)
ax2 = ax1.twinx()
ax2.plot(df_combined["년도"], df_combined["경제활동인구 증가율 (%)"], 
         marker='o', color='blue', linestyle='-', label="경제활동인구 증가율 (%)")
ax2.set_ylabel("경제활동인구 증가율 (%)", color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

# 실업률 (초록색 점선 그래프)
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("outward", 60))  # 실업률 축을 추가하여 가독성 확보
ax3.plot(df_combined["년도"], df_combined["실업률 (%)"], 
         marker='s', color='green', linestyle='--', label="실업률 (%)")
ax3.set_ylabel("실업률 (%)", color='green')
ax3.tick_params(axis='y', labelcolor='green')

# 그래프 제목 및 레전드
plt.title("비경제활동인구 증가율 vs 경제활동인구 증가율 vs 실업률 (경기침체 분석)")
fig.tight_layout()
plt.show()
