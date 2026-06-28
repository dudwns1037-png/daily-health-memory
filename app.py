import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar

# ------------------------------------------------------------
# 페이지 기본 설정
# ------------------------------------------------------------

st.set_page_config(
    page_title="Daily Health Memory",
    page_icon="💪",
    layout="centered"
)

# ------------------------------------------------------------
# Health Memory 저장 공간 만들기
# ------------------------------------------------------------

if "records" not in st.session_state:
    st.session_state.records = []

if "selected_memory_date" not in st.session_state:
    st.session_state.selected_memory_date = None

# ------------------------------------------------------------
# 앱 제목
# ------------------------------------------------------------

st.title("💪 Daily Health Memory")

# ------------------------------------------------------------
# 페이지 상단 memory read
# ------------------------------------------------------------

st.markdown("### memory read")

st.info(
    f"현재 Health Memory에 저장된 기록: {len(st.session_state.records)}개"
)

if len(st.session_state.records) == 0:
    st.write("아직 Health Memory에 저장된 기록이 없습니다. 오늘의 건강 습관을 분석하면 memory가 저장됩니다.")

else:
    records_df_top = pd.DataFrame(st.session_state.records)
    records_df_top["날짜"] = pd.to_datetime(records_df_top["날짜"])
    records_df_top = records_df_top.sort_values(by="날짜").reset_index(drop=True)

    max_date_top = records_df_top["날짜"].max()

    selected_month_top = st.date_input(
        "확인할 월을 선택하세요.",
        value=max_date_top,
        key="top_memory_month"
    )

    year_top = selected_month_top.year
    month_top = selected_month_top.month

    st.write(f"#### {year_top}년 {month_top}월 Health Memory")

    saved_dates_top = records_df_top["날짜"].dt.strftime("%Y-%m-%d").tolist()

    cal = calendar.Calendar(firstweekday=6)
    month_days = cal.monthdayscalendar(year_top, month_top)

    week_cols = st.columns(7)
    week_names = ["일", "월", "화", "수", "목", "금", "토"]

    for col, name in zip(week_cols, week_names):
        col.markdown(f"**{name}**")

    for week in month_days:
        cols = st.columns(7)

        for i, day in enumerate(week):
            if day == 0:
                cols[i].write("")
            else:
                date_str = f"{year_top}-{month_top:02d}-{day:02d}"

                if date_str in saved_dates_top:
                    if cols[i].button(f"📌 {day}", key=f"top_memory_{date_str}"):
                        st.session_state.selected_memory_date = date_str
                else:
                    cols[i].write(f"{day}")

    st.markdown("#### Selected Memory Read")

    if st.session_state.selected_memory_date is None:
        st.info("달력에서 📌 표시가 있는 날짜를 선택하면 해당 날짜의 점수와 일기를 읽어옵니다.")
    else:
        selected_date_top = st.session_state.selected_memory_date

        selected_rows_top = records_df_top[
            records_df_top["날짜"].dt.strftime("%Y-%m-%d") == selected_date_top
        ]

        selected_row_top = selected_rows_top.iloc[-1]

        st.write(f"##### {selected_date_top} Memory")

        st.metric(
            "건강 루틴 점수",
            f"{selected_row_top['건강루틴점수']} / 100"
        )

        if selected_row_top["짧은일기"]:
            st.info(selected_row_top["짧은일기"])
        else:
            st.info("이 날짜에는 저장된 일기가 없습니다.")

# ------------------------------------------------------------
# 앱 소개
# ------------------------------------------------------------

st.write(
    "수면시간, 운동시간, 근무시간, 휴식시간, 식사 횟수, 간식 횟수, 짧은 일기를 바탕으로 "
    "하루 건강 습관을 점검하고, 저장된 memory를 통해 건강 루틴의 변화를 확인하는 AI Agent입니다."
)

st.info(
    "이 Agent는 개인의 생활 기록을 정리하고 건강한 습관 형성을 돕기 위한 도구입니다. "
    "의학적 진단이나 치료 목적의 서비스는 아닙니다."
)

# ------------------------------------------------------------
# 기준값 설정
# ------------------------------------------------------------

st.sidebar.header("기준값 설정")

recommended_sleep_min = st.sidebar.number_input(
    "최소 권장 수면시간",
    min_value=0.0,
    max_value=24.0,
    value=7.0,
    step=0.5
)

recommended_sleep_max = st.sidebar.number_input(
    "최대 권장 수면시간",
    min_value=0.0,
    max_value=24.0,
    value=9.0,
    step=0.5
)

target_exercise = st.sidebar.number_input(
    "하루 목표 운동시간",
    min_value=0.0,
    max_value=24.0,
    value=0.5,
    step=0.5
)

target_rest = st.sidebar.number_input(
    "하루 목표 휴식시간",
    min_value=0.0,
    max_value=24.0,
    value=1.0,
    step=0.5
)

excessive_rest_limit = st.sidebar.number_input(
    "과잉 휴식 기준 시간",
    min_value=0.0,
    max_value=24.0,
    value=3.0,
    step=0.5
)

target_meals = st.sidebar.number_input(
    "하루 목표 식사 횟수",
    min_value=0,
    max_value=10,
    value=3,
    step=1
)

max_snacks = st.sidebar.number_input(
    "하루 권장 간식 횟수 상한",
    min_value=0,
    max_value=10,
    value=2,
    step=1
)

# ------------------------------------------------------------
# 1. 오늘의 건강 기록 입력
# ------------------------------------------------------------

st.subheader("1. Health Data Write")

date = st.date_input("날짜")

sleep_hours = st.number_input(
    "수면시간",
    min_value=0.0,
    max_value=24.0,
    value=7.0,
    step=0.5
)

exercise_hours = st.number_input(
    "운동시간",
    min_value=0.0,
    max_value=24.0,
    value=0.5,
    step=0.5
)

work_hours = st.number_input(
    "근무시간",
    min_value=0.0,
    max_value=24.0,
    value=8.0,
    step=0.5
)

rest_hours = st.number_input(
    "휴식시간",
    min_value=0.0,
    max_value=24.0,
    value=1.0,
    step=0.5
)

meal_count = st.number_input(
    "하루 식사 횟수",
    min_value=0,
    max_value=10,
    value=3,
    step=1
)

snack_count = st.number_input(
    "간식 횟수",
    min_value=0,
    max_value=10,
    value=1,
    step=1
)

diary = st.text_area(
    "오늘의 짧은 일기",
    placeholder="오늘 하루 기억에 남는 일을 한 줄로 표현해보세요.",
    height=100
)

# ------------------------------------------------------------
# 분석 버튼
# ------------------------------------------------------------

if st.button("오늘의 건강 습관 분석하기"):

    score = 0
    feedback = []

    # 수면시간 판단
    if recommended_sleep_min <= sleep_hours <= recommended_sleep_max:
        score += 25
        sleep_status = "권장 범위 내"
        feedback.append("수면시간이 설정한 권장 범위 안에 있습니다.")
    elif sleep_hours < recommended_sleep_min:
        sleep_status = "권장 범위보다 부족"
        feedback.append(
            f"수면시간이 권장 최소 기준보다 {recommended_sleep_min - sleep_hours:.1f}시간 부족합니다."
        )
    else:
        sleep_status = "권장 범위보다 많음"
        feedback.append(
            f"수면시간이 권장 최대 기준보다 {sleep_hours - recommended_sleep_max:.1f}시간 많습니다."
        )

    # 운동시간 판단
    if exercise_hours >= target_exercise:
        score += 25
        exercise_status = "목표 달성"
        feedback.append("운동시간 목표를 달성했습니다.")
    else:
        exercise_status = "목표보다 부족"
        feedback.append(
            f"운동시간이 목표보다 {target_exercise - exercise_hours:.1f}시간 부족합니다."
        )

    # 식사 횟수 판단
    if meal_count >= target_meals:
        score += 20
        meal_status = "목표 달성"
        feedback.append("식사 횟수가 설정한 목표에 도달했습니다.")
    elif meal_count == 0:
        meal_status = "식사 기록 없음"
        feedback.append("오늘은 식사 기록이 없습니다. 규칙적인 식사 루틴을 챙겨보세요.")
    else:
        meal_status = "목표보다 부족"
        feedback.append(
            f"식사 횟수가 목표보다 {target_meals - meal_count}회 부족합니다."
        )

    # 간식 횟수 판단
    if snack_count <= max_snacks:
        score += 15
        snack_status = "권장 범위 내"
        feedback.append("간식 횟수가 설정한 기준 안에 있습니다.")
    else:
        snack_status = "기준보다 많음"
        feedback.append(
            f"간식 횟수가 설정 기준보다 {snack_count - max_snacks}회 많습니다. "
            "내일은 간식 횟수를 조금 줄여보는 것도 좋습니다."
        )

    # 휴식시간 판단
    if rest_hours >= excessive_rest_limit:
        rest_status = "과잉 휴식"
        feedback.append(
            f"휴식시간이 {rest_hours:.1f}시간으로 다소 긴 편입니다. "
            "충분히 쉰 것은 좋지만, 일부 시간을 자기개발이나 가벼운 활동에 투자해보는 것도 좋습니다."
        )
    elif rest_hours >= target_rest:
        score += 15
        rest_status = "목표 달성"
        feedback.append("휴식시간을 적절히 확보했습니다.")
    else:
        rest_status = "목표보다 부족"
        feedback.append(
            f"휴식시간이 목표보다 {target_rest - rest_hours:.1f}시간 부족합니다."
        )

    # 근무시간 피드백
    if work_hours == 0:
        feedback.append(
            "오늘은 근무가 없는 날입니다. 휴식과 건강 루틴을 챙기며 하루를 알차게 보내보세요."
        )
    else:
        feedback.append(
            f"오늘은 {work_hours:.1f}시간 근무했습니다. 오늘 하루도 수고했습니다."
        )

    # --------------------------------------------------------
    # 분석 결과 출력
    # --------------------------------------------------------

    st.subheader("2. Health Data Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("건강 루틴 점수", f"{score} / 100")

    with col2:
        st.metric("수면 상태", sleep_status)

    result_df = pd.DataFrame({
        "항목": [
            "수면시간",
            "운동시간",
            "근무시간",
            "휴식시간",
            "식사 횟수",
            "간식 횟수"
        ],
        "입력값": [
            sleep_hours,
            exercise_hours,
            work_hours,
            rest_hours,
            meal_count,
            snack_count
        ],
        "상태": [
            sleep_status,
            exercise_status,
            "기록용",
            rest_status,
            meal_status,
            snack_status
        ],
        "기준": [
            f"{recommended_sleep_min}~{recommended_sleep_max}시간",
            f"{target_exercise}시간 이상",
            "기록용",
            f"{target_rest}시간 이상, {excessive_rest_limit}시간 이상은 과잉 휴식",
            f"{target_meals}회 이상",
            f"{max_snacks}회 이하"
        ]
    })

    st.dataframe(result_df, use_container_width=True)

    st.subheader("3. Agent Feedback")

    for item in feedback:
        st.write("- " + item)

    st.subheader("4. Health Routine Suggestion")

    if rest_status == "과잉 휴식":
        st.warning(
            "오늘은 휴식시간이 긴 편입니다. 회복은 충분히 되었을 가능성이 있으니, "
            "내일은 짧은 자기개발이나 산책처럼 부담이 낮은 활동을 하나 추가해보는 것을 추천합니다."
        )
    elif score >= 80:
        st.success(
            "오늘은 수면, 운동, 식사, 간식, 휴식의 균형이 좋은 편입니다. "
            "현재 건강 루틴을 유지해도 좋습니다."
        )
    elif score >= 60:
        st.warning(
            "일부 건강 습관이 목표에 미치지 못했습니다. "
            "내일은 부족한 항목 하나를 우선 개선해보는 것이 좋습니다."
        )
    else:
        st.error(
            "오늘은 건강 루틴의 균형이 다소 낮게 나타났습니다. "
            "내일은 수면, 식사, 휴식처럼 기본 회복 루틴부터 챙기는 것을 추천합니다."
        )

    st.subheader("5. Today's Time Distribution")

    time_graph_df = pd.DataFrame({
        "category": ["Sleep", "Exercise", "Work", "Rest"],
        "hours": [sleep_hours, exercise_hours, work_hours, rest_hours]
    })

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(time_graph_df["category"], time_graph_df["hours"])
    ax.set_ylabel("Hours")
    ax.set_title("Today's Time Distribution")
    st.pyplot(fig)

    # --------------------------------------------------------
    # memory write
    # --------------------------------------------------------

    new_record = {
        "날짜": date,
        "수면시간": sleep_hours,
        "운동시간": exercise_hours,
        "근무시간": work_hours,
        "휴식시간": rest_hours,
        "식사횟수": meal_count,
        "간식횟수": snack_count,
        "건강루틴점수": score,
        "수면상태": sleep_status,
        "운동상태": exercise_status,
        "식사상태": meal_status,
        "간식상태": snack_status,
        "휴식상태": rest_status,
        "짧은일기": diary
    }

    st.session_state.records.append(new_record)

    st.success("memory write 완료: 오늘의 건강 기록이 Health Memory에 저장되었습니다.")

# ------------------------------------------------------------
# 하단 memory summary
# ------------------------------------------------------------

if len(st.session_state.records) > 0:

    records_df = pd.DataFrame(st.session_state.records)
    records_df["날짜"] = pd.to_datetime(records_df["날짜"])
    records_df = records_df.sort_values(by="날짜").reset_index(drop=True)

    st.subheader("6. Memory Summary")

    avg_score = records_df["건강루틴점수"].mean()
    avg_sleep = records_df["수면시간"].mean()
    avg_exercise = records_df["운동시간"].mean()
    avg_rest = records_df["휴식시간"].mean()
    avg_meal = records_df["식사횟수"].mean()
    avg_snack = records_df["간식횟수"].mean()

    summary_df = pd.DataFrame({
        "항목": [
            "평균 건강 루틴 점수",
            "평균 수면시간",
            "평균 운동시간",
            "평균 휴식시간",
            "평균 식사 횟수",
            "평균 간식 횟수"
        ],
        "값": [
            round(avg_score, 1),
            round(avg_sleep, 1),
            round(avg_exercise, 1),
            round(avg_rest, 1),
            round(avg_meal, 1),
            round(avg_snack, 1)
        ]
    })

    st.dataframe(summary_df, use_container_width=True)

    st.subheader("7. Health Routine Score Trend")

    fig2, ax2 = plt.subplots(figsize=(8, 4))

    ax2.plot(
        records_df["날짜"],
        records_df["건강루틴점수"],
        marker="o",
        label="Health Routine Score"
    )

    if len(records_df) >= 3:
        records_df["점수_이동평균"] = records_df["건강루틴점수"].rolling(
            window=3,
            min_periods=1
        ).mean()

        ax2.plot(
            records_df["날짜"],
            records_df["점수_이동평균"],
            marker="s",
            label="3-Day Moving Average"
        )

    ax2.set_ylim(0, 100)
    ax2.set_ylabel("Score")
    ax2.set_title("Health Routine Score Trend")
    ax2.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig2)

    st.subheader("8. Agent Memory Insight")

    record_count = len(records_df)

    st.write(f"총 {record_count}일의 Health Memory가 저장되어 있습니다.")

    if record_count == 1:
        st.write(
            "아직 저장된 memory가 1개뿐이라 트렌드를 판단하기는 어렵습니다. "
            "며칠 더 기록하면 건강 루틴의 변화 흐름을 확인할 수 있습니다."
        )

    else:
        first_score = records_df["건강루틴점수"].iloc[0]
        last_score = records_df["건강루틴점수"].iloc[-1]
        score_change = last_score - first_score

        if score_change > 0:
            st.success(
                f"첫 memory 대비 최근 건강 루틴 점수가 {score_change:.1f}점 상승했습니다. "
                "전반적으로 건강 습관이 개선되는 흐름입니다."
            )
        elif score_change < 0:
            st.warning(
                f"첫 memory 대비 최근 건강 루틴 점수가 {abs(score_change):.1f}점 낮아졌습니다. "
                "최근 수면, 식사, 휴식 중 부족한 항목을 확인해보는 것이 좋습니다."
            )
        else:
            st.info(
                "첫 memory와 최근 건강 루틴 점수가 동일합니다. "
                "현재 루틴을 유지하면서 부족한 항목을 조금씩 개선해보세요."
            )

        recent_df = records_df.tail(3)

        recent_avg_sleep = recent_df["수면시간"].mean()
        recent_avg_exercise = recent_df["운동시간"].mean()
        recent_avg_rest = recent_df["휴식시간"].mean()
        recent_avg_meal = recent_df["식사횟수"].mean()
        recent_avg_snack = recent_df["간식횟수"].mean()

        st.write("최근 memory 기준으로 보면:")

        if recent_avg_sleep < recommended_sleep_min:
            st.write(
                f"- 최근 평균 수면시간은 {recent_avg_sleep:.1f}시간으로, 설정한 최소 권장 수면시간보다 낮습니다."
            )
        else:
            st.write(
                f"- 최근 평균 수면시간은 {recent_avg_sleep:.1f}시간으로, 설정한 기준에 가까운 편입니다."
            )

        if recent_avg_exercise < target_exercise:
            st.write(
                f"- 최근 평균 운동시간은 {recent_avg_exercise:.1f}시간으로, 목표 운동시간보다 부족합니다."
            )
        else:
            st.write(
                f"- 최근 평균 운동시간은 {recent_avg_exercise:.1f}시간으로, 목표를 충족하고 있습니다."
            )

        if recent_avg_rest >= excessive_rest_limit:
            st.write(
                f"- 최근 평균 휴식시간은 {recent_avg_rest:.1f}시간으로, 다소 긴 편입니다. "
                "일부 시간을 자기개발이나 가벼운 활동에 활용해볼 수 있습니다."
            )
        elif recent_avg_rest < target_rest:
            st.write(
                f"- 최근 평균 휴식시간은 {recent_avg_rest:.1f}시간으로, 목표 휴식시간보다 부족합니다."
            )
        else:
            st.write(
                f"- 최근 평균 휴식시간은 {recent_avg_rest:.1f}시간으로, 적절한 범위에 있습니다."
            )

        if recent_avg_meal < target_meals:
            st.write(
                f"- 최근 평균 식사 횟수는 {recent_avg_meal:.1f}회로, 목표 식사 횟수보다 부족합니다."
            )
        else:
            st.write(
                f"- 최근 평균 식사 횟수는 {recent_avg_meal:.1f}회로, 규칙적인 식사 루틴에 가까운 편입니다."
            )

        if recent_avg_snack > max_snacks:
            st.write(
                f"- 최근 평균 간식 횟수는 {recent_avg_snack:.1f}회로, 설정한 기준보다 높습니다."
            )
        else:
            st.write(
                f"- 최근 평균 간식 횟수는 {recent_avg_snack:.1f}회로, 설정한 기준 안에 있습니다."
            )

    csv_data = records_df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label="Health Memory CSV 다운로드",
        data=csv_data,
        file_name="daily_health_memory.csv",
        mime="text/csv"
    )

    if st.button("Health Memory 초기화"):
        st.session_state.records = []
        st.session_state.selected_memory_date = None
        st.rerun()