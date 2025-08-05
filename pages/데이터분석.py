import streamlit as st
import plotly.express as px
import pandas as pd

# Streamlit 페이지 설정
st.set_page_config(page_title="학생 성적 시각화 대시보드", layout="wide")

# 데이터 준비
data = {
    'name': ['lee', 'park', 'kim'],
    'grade': [2, 2, 2],
    'number': [1, 2, 3],
    'kor': [90, 88, 99],
    'eng': [91, 89, 99],
    'math': [81, 77, 99],
    'info': [100, 100, 100]
}
df = pd.DataFrame(data)

# 웹앱 제목
st.title("학생 성적 시각화 대시보드")

# 데이터프레임 표시
st.header("학생 성적 데이터")
st.dataframe(df, use_container_width=True)

# 사이드바에서 시각화 옵션 선택
st.sidebar.header("시각화 옵션")
chart_type = st.sidebar.selectbox("그래프 유형 선택", ["막대 그래프", "선 그래프", "산점도"])
subject = st.sidebar.multiselect("과목 선택", ["kor", "eng", "math", "info"], default=["kor", "eng", "math"])

# 데이터 필터링
if not subject:
    st.warning("최소 한 개의 과목을 선택해주세요.")
else:
    # 그래프 생성
    if chart_type == "막대 그래프":
        fig = px.bar(
            df,
            x='name',
            y=subject,
            barmode='group',
            title="학생별 과목 성적 (막대 그래프)",
            labels={'name': '학생 이름', 'value': '점수', 'variable': '과목'},
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
    elif chart_type == "선 그래프":
        fig = px.line(
            df,
            x='name',
            y=subject,
            title="학생별 과목 성적 (선 그래프)",
            labels={'name': '학생 이름', 'value': '점수', 'variable': '과목'},
            markers=True,
            color_discrete_sequence=px.colors.qualitative.Plotly
        )
    else:  # 산점도
        # 산점도는 두 과목 비교를 위해 첫 두 과목만 사용
        if len(subject) >= 2:
            fig = px.scatter(
                df,
                x=subject[0],
                y=subject[1],
                color='name',
                size='math' if 'math' in df.columns else None,
                title=f"{subject[0]} vs {subject[1]} 산점도",
                labels={subject[0]: subject[0].upper(), subject[1]: subject[1].upper()},
                color_discrete_sequence=px.colors.qualitative.Plotly
            )
        else:
            st.warning("산점도는 최소 두 과목을 선택해야 합니다.")
            fig = None

    # 그래프 표시
    if fig:
        fig.update_layout(
            xaxis_title="학생 이름" if chart_type != "산점도" else subject[0].upper(),
            yaxis_title="점수" if chart_type != "산점도" else subject[1].upper(),
            template="plotly_white",
            showlegend=True
        )
        st.plotly_chart(fig, use_container_width=True)

# 추가 통계 정보
st.header("성적 통계")
st.write("과목별 평균 점수")
avg_scores = df[subject].mean().reset_index()
avg_scores.columns = ['과목', '평균 점수']
st.dataframe(avg_scores, use_container_width=True)

# 막대 그래프로 평균 점수 시각화
fig_avg = px.bar(
    avg_scores,
    x='과목',
    y='평균 점수',
    title="과목별 평균 점수",
    color='과목',
    color_discrete_sequence=px.colors.qualitative.Plotly
)
fig_avg.update_layout(template="plotly_white")
st.plotly_chart(fig_avg, use_container_width=True)

# 실행 안내
st.markdown("""
### 사용 방법
1. 왼쪽 사이드바에서 원하는 **그래프 유형**을 선택하세요 (막대 그래프, 선 그래프, 산점도).
2. 표시하고 싶은 **과목**을 선택하세요.
3. 그래프와 통계 데이터를 확인하세요!
""")