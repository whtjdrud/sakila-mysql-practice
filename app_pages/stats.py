from collections import Counter
from datetime import date, datetime, timedelta

import pandas as pd
import streamlit as st

from app_state import load_history, problems
from sakila_bank import CATEGORIES, LEVELS

st.title("학습 통계")

items = problems()
hist = load_history()
solved = set(hist["solved"])
revealed = set(hist["revealed"])
attempts = pd.DataFrame(hist["attempts"], columns=["pid", "ts", "status"])

if attempts.empty and not solved:
    st.info("아직 제출 기록이 없습니다. 문제를 풀고 제출하면 여기에 통계가 쌓입니다.", icon=":material/insights:")
    st.stop()

attempts["ts"] = pd.to_datetime(attempts["ts"])
attempts["day"] = attempts["ts"].dt.date
meta = pd.DataFrame([{"pid": p["id"], "category": p["category"], "level": p["level"]} for p in items])
attempted = set(attempts["pid"]) | solved

# 첫 제출에 바로 맞힌 문제 비율
first = attempts.sort_values("ts").groupby("pid").first()
first_try = (first["status"] == "success").sum()

# 연속 학습일: 오늘(또는 어제)부터 거꾸로 제출이 있는 날을 센다
days = set(attempts["day"])
streak, d = 0, date.today()
if d not in days:
    d -= timedelta(days=1)
while d in days:
    streak += 1
    d -= timedelta(days=1)

week_ago = datetime.now() - timedelta(days=7)
solved_at = attempts[attempts["status"] == "success"].groupby("pid")["ts"].min()
solved_week = int((solved_at >= week_ago).sum())

with st.container(horizontal=True):
    st.metric("해결", f"{len(solved)} / {len(items)}", f"{len(solved) / len(items):.1%}", border=True,
              delta_color="off")
    st.metric("최근 7일 해결", solved_week, border=True)
    st.metric("총 제출", len(attempts), border=True)
    st.metric("첫 제출 정답률", f"{first_try / max(len(first), 1):.0%}",
              f"{first_try} / {len(first)}문제", border=True, delta_color="off",
              help="처음 제출한 답이 바로 정답이었던 문제의 비율")
    st.metric("연속 학습일", f"{streak}일", border=True)
    st.metric("해설 보고 푼 문제", len(revealed & solved), border=True,
              help="정답·해설을 먼저 열어 본 뒤 해결한 문제 수")

st.subheader("유형 × 난이도 해결률")
rows = []
for code, _, name, _ in CATEGORIES:
    cat = meta[meta["category"] == code]
    if cat.empty:
        continue
    row = {"유형": name, "해결": f"{cat['pid'].isin(solved).sum()} / {len(cat)}",
           "전체": cat["pid"].isin(solved).mean()}
    for lv in LEVELS:
        sub = cat[cat["level"] == lv]
        row[LEVELS[lv]] = sub["pid"].isin(solved).mean() if len(sub) else None
    rows.append(row)
progress_cfg = {c: st.column_config.ProgressColumn(c, min_value=0, max_value=1, format="percent")
                for c in ["전체", *LEVELS.values()]}
st.dataframe(pd.DataFrame(rows), hide_index=True, column_config=progress_cfg)
st.caption("빈 칸은 그 유형에 해당 난이도 문제가 없다는 뜻입니다.")

st.subheader("일별 활동")
daily = (attempts.groupby("day")
         .agg(제출=("pid", "size"))
         .join(solved_at.dt.date.value_counts().rename("해결"))
         .fillna(0).astype(int))
full_days = pd.date_range(min(daily.index), max(max(daily.index), date.today()), freq="D").date
daily = daily.reindex(full_days, fill_value=0)
daily.index = pd.to_datetime(daily.index)
daily.index.name = "날짜"
left, right = st.columns(2)
with left:
    st.markdown("**하루에 해결한 문제 수**")
    st.bar_chart(daily["해결"], color="#2563eb", x_label="날짜", y_label="해결")
with right:
    st.markdown("**하루 제출 수**")
    st.bar_chart(daily["제출"], color="#2563eb", x_label="날짜", y_label="제출")

st.subheader("막힌 문제")
by_id = {p["id"]: p for p in items}
stuck = Counter(attempts.loc[~attempts["pid"].isin(solved), "pid"])
if stuck:
    st.dataframe(pd.DataFrame([{
        "ID": pid, "제목": by_id[pid]["title"], "유형": by_id[pid]["category_name"],
        "난이도": "★" * by_id[pid]["level"], "제출 횟수": n, "링크": f"/solve?pid={pid}",
    } for pid, n in stuck.most_common(10)]), hide_index=True,
        column_config={"링크": st.column_config.LinkColumn("풀기", display_text="열기")})
else:
    st.caption("제출했지만 아직 못 푼 문제가 없습니다.")

st.subheader("다음 추천 문제")
# 안 푼 문제 중 가장 쉬운 것. 같은 난이도면 이미 시작한 유형 → 커리큘럼 순서
order = {c[0]: i for i, c in enumerate(CATEGORIES)}
started = set(meta.loc[meta["pid"].isin(attempted), "category"])
candidates = sorted((p for p in items if p["id"] not in solved),
                    key=lambda p: (p["level"], p["category"] not in started, order[p["category"]], p["id"]))
if candidates:
    nxt = candidates[0]
    st.markdown(f"**{nxt['id']}. {nxt['title']}** — {nxt['category_name']} · {'★' * nxt['level']}")
    # 시작한 유형 중 해결률이 가장 낮은 유형을 약점으로 알려 준다
    weak = sorted((meta[meta["category"] == c]["pid"].isin(solved).mean(), order[c], c) for c in started)
    if weak and weak[0][0] < 1:
        name = CATEGORIES[weak[0][1]][2]
        st.caption(f"시작한 유형 중 해결률이 가장 낮은 유형: **{name}** ({weak[0][0]:.0%})")
    if st.button("이 문제 풀기", icon=":material/arrow_forward:", type="primary"):
        st.session_state["pid"] = nxt["id"]
        st.switch_page("app_pages/solve.py", query_params={"pid": nxt["id"]})
else:
    st.success("모든 문제를 해결했습니다!", icon=":material/emoji_events:")
