import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 데이터 불러오기
data = pd.read_excel('active_non_active_population.xlsx')
print(data.info())

## 년도, 비경제활동인구, 경제활동인구 열 선택
years = data.columns[1:]  # 첫 번째 열(년도)
non_economically_active = data.iloc[0, 1:]  # 비경제활동인구
economically_active = data.iloc[1, 1:]  # 경제활동인구

# 그래프 생성
plt.figure(figsize=(12, 6))
plt.plot(years, non_economically_active, marker='o', label='비경제활동인구', color='blue')
plt.plot(years, economically_active, marker='o', label='경제활동인구', color='orange')

# 그래프 제목 및 레이블 설정
plt.title('비경제활동인구와 경제활동인구 변화 추이 (2000-2024)')
plt.xlabel('년도')
plt.ylabel('인구 수')
plt.xticks(rotation=45)
plt.grid()
plt.legend()

# 그래프 출력
plt.tight_layout()
plt.show()
