import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
# 데이터 불러오기
file_path = "active_non_active_population.xlsx"  
data = pd.read_excel(file_path)

# 년도 및 데이터 변환
years = list(map(int, data.columns[1:]))  # 첫 번째 열 이후의 컬럼(년도) 변환
non_economically_active = pd.to_numeric(data.iloc[0, 1:].str.replace(',', ''), errors='coerce')
economically_active = pd.to_numeric(data.iloc[1, 1:].str.replace(',', ''), errors='coerce')

# 증가폭(차분) 계산
non_active_diff = non_economically_active.diff().fillna(0)  # 비경제활동인구 증가폭
active_diff = economically_active.diff().fillna(0)  # 경제활동인구 증가폭

# 비경제활동인구 대비 경제활동인구 증가폭 차이
ratio_diff = non_active_diff - active_diff

# 데이터프레임 생성
diff_df = pd.DataFrame({
    '년도': years,
    '비경제활동인구': non_economically_active,
    '경제활동인구': economically_active,
    '비경제활동인구 증가폭': non_active_diff,
    '경제활동인구 증가폭': active_diff,
    '비경제활동인구 대비 증가 차이': ratio_diff
})

# 데이터 확인
print(diff_df)

# 그래프 생성 (년도 기준)
plt.figure(figsize=(12, 6))
plt.bar(years, ratio_diff, color='#32a852', label='비경제활동인구 - 경제활동인구 증가폭 차이')
plt.plot(years, ratio_diff, marker='o', color='red', linestyle='-', label='변화 추이')  # 라인 그래프 추가
plt.title('비경제활동인구 대비 경제활동인구 증가폭 차이 (2000-2024)')
plt.xlabel('년도')
plt.ylabel('증가폭 차이 (천 명)')
plt.xticks(years, rotation=45)  # x축 년도 표시 회전
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.legend()
plt.tight_layout()
plt.show()
