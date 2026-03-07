"""
👖 BLUE JEANS Creative Development Engine v1.2
아이디어 → 기획개발 패키지
"""

import streamlit as st
import json
import re
from datetime import datetime

ANTHROPIC_MODEL = "claude-sonnet-4-6"

# ─── Page Config ───
st.set_page_config(
    page_title="BLUE JEANS · Creative Development Engine",
    page_icon="👖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS ───
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root{
    --y:#FFCB05;
    --bg:#0E1117;
    --card:#262730;
    --t:#FAFAFA;
    --r:#FF6B6B;
    --g:#51CF66;
    --dim:#8B8B8B
}

html, body, [class*="css"]{
    font-family:'Pretendard',sans-serif
}

.mt{
    font-size:1.6rem;
    font-weight:700;
    color:var(--y);
    margin-bottom:.2rem
}

.st{
    font-size:.85rem;
    color:var(--dim);
    margin-bottom:2rem
}

.callout{
    background:var(--card);
    border-left:3px solid var(--y);
    padding:.8rem 1rem;
    margin:.5rem 0;
    border-radius:0 6px 6px 0;
    font-size:.85rem
}

.ct{
    color:var(--y);
    font-weight:600;
    font-size:.75rem;
    margin-bottom:.3rem
}

.sb{
    font-size:2.5rem;
    font-weight:700;
    color:var(--y);
    text-align:center
}

.sl{
    font-size:.7rem;
    color:var(--dim);
    text-align:center
}

.cc{
    background:var(--card);
    border:1px solid #3a3a4a;
    border-radius:8px;
    padding:1rem;
    margin-bottom:.8rem
}

.cc:hover{
    border-color:var(--y)
}

.ri{
    background:var(--card);
    border-radius:6px;
    padding:.8rem;
    margin-bottom:.5rem;
    font-size:.85rem
}

.rl{
    color:var(--y);
    font-weight:600;
    font-size:.7rem
}

section[data-testid="stSidebar"]{
    background:#1a1a2e
}

.badge{
    display:inline-block;
    padding:.15rem .5rem;
    border-radius:4px;
    font-size:.7rem;
    font-weight:600
}

.b-done{
    background:var(--g);
    color:#000
}

.b-run{
    background:var(--y);
    color:#000
}

.b-not{
    background:#3a3a4a;
    color:var(--dim)
}

.b-fail{
    background:var(--r);
    color:#000
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ───
defaults = {
    "page": "home",
    "projects": {},
    "cur": None,
    "tab": "brainstorm",
    "last_research_raw": "",
    "last_brainstorm_raw": "",
    "last_brainstorm_error": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def badge(status: str) -> str:
    mapping = {
        "DONE": "b-done",
        "RUNNING": "b-run",
        "NOT_RUN": "b-not",
        "FAILED": "b-fail"
    }
    css_class = mapping.get(status, "b-not")
    return f'<span class="badge {css_class}">{status.replace("_", " ")}</span>'


# ─── JSON Helpers ───
def extract_json_object(text: str) -> str:
    text = text.strip()

    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("JSON 객체 시작/끝을 찾지 못했습니다.")

    return text[start:end + 1]


def safe_json_loads(text: str):
    cleaned = extract_json_object(text)

    # trailing comma 제거
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)

    return json.loads(cleaned)


# ─── API Calls ───
def get_client():
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("anthropic 패키지가 설치되지 않았습니다. requirements.txt를 확인하세요.")

    if "ANTHROPIC_API_KEY" not in st.secrets:
        raise RuntimeError("ANTHROPIC_API_KEY가 secrets에 설정되지 않았습니다.")

    return anthropic.Anthropic(
        api_key=st.secrets["ANTHROPIC_API_KEY"]
    )


def call_research(idea, genre, market):
    try:
        client = get_client()

        system_prompt = """당신은 콘텐츠 기획 리서처다.
기획자의 아이디어 키워드를 바탕으로 참고 가능한 1) 실화/뉴스 2) 기존 작품을 정리한다.
한국어로 작성한다.
반드시 유효한 단일 JSON 객체만 출력한다.
JSON 외 텍스트 금지.
모든 key는 반드시 쌍따옴표를 사용한다.
후행 쉼표(trailing comma) 금지.
문자열 내부 줄바꿈은 최소화한다."""

        user_prompt = f"""[입력]
아이디어: {idea}
장르: {genre}
타겟: {market}

[JSON 스키마]
{{
  "search_keywords": [],
  "real_events": [
    {{
      "id": 1,
      "title": "",
      "summary": "",
      "source": "",
      "year": "",
      "relevance": "",
      "story_potential": ""
    }}
  ],
  "existing_works": [
    {{
      "id": 1,
      "title": "",
      "type": "",
      "country": "",
      "year": "",
      "summary": "",
      "similarity": "",
      "difference_opportunity": ""
    }}
  ],
  "research_summary": {{
    "total_real_events": 0,
    "total_existing_works": 0,
    "key_insight": ""
  }}
}}

규칙:
- real_events 3~7개
- existing_works 3~7개
- source는 가능한 한 짧게
- key_insight는 2문장 이내
"""

        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=3000,
            temperature=0.2,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        txt = "".join(block.text for block in response.content if hasattr(block, "text")).strip()
        st.session_state["last_research_raw"] = txt

        return safe_json_loads(txt)

    except Exception as e:
        st.error(f"리서치 실패: {e}")
        raw = st.session_state.get("last_research_raw")
        if raw:
            st.text_area("Research Raw Response", raw, height=300)
        return None


def call_brainstorm(idea, genre, market, fmt, research=None):
    try:
        client = get_client()

        system_prompt = """당신은 글로벌 콘텐츠 시장을 이해하는 Development Producer이자 Script Architect다.
기획자의 아이디어를 개발 가능한 컨셉으로 정렬한다.
이야기(story)와 분위기(mood)를 구분한다.
타겟 시장과 포맷을 반영한다.
리서치가 있으면 참고하되 기존작을 모방하지 않는다.

중요 규칙:
- 반드시 유효한 단일 JSON 객체만 출력한다.
- JSON 외 텍스트 금지.
- 모든 key는 반드시 쌍따옴표를 사용한다.
- 후행 쉼표(trailing comma) 금지.
- 주석 금지.
- 설명 문장 금지.
- 문자열 내부 줄바꿈 대신 공백을 사용한다.
- 모든 짧은 설명은 2문장 이내로 제한한다.
"""

        research_block = ""
        if research:
            research_block = f"""
[리서치 참고]
{json.dumps(research, ensure_ascii=False)}

규칙:
- 실화/뉴스는 소재 참고용
- 기존작은 차별화 포인트 참고용
- 동일 구조/설정 반복 금지
"""

        user_prompt = f"""[입력]
아이디어: {idea}
장르: {genre}
타겟: {market}
포맷: {fmt}
{research_block}

[JSON 스키마]
{{
  "idea_type": "story|mood|hybrid",
  "idea_type_diagnosis": "",
  "market_context": {{
    "target_market": "",
    "market_insight": "",
    "cultural_code": "",
    "market_risk": "",
    "reference_titles": []
  }},
  "format_context": {{
    "selected_format": "",
    "format_rationale": "",
    "structure_note": ""
  }},
  "research_applied": {{
    "real_events_used": [],
    "inspiration_note": ""
  }},
  "idea_cards": [
    {{
      "id": 1,
      "title": "",
      "logline_seed": "",
      "protagonist": "",
      "conflict": "",
      "hook": "",
      "visual_image": "",
      "genre": "",
      "scores": {{
        "active_hero": 0.0,
        "conflict_clarity": 0.0,
        "visual_power": 0.0,
        "genre_immediacy": 0.0,
        "originality": 0.0,
        "market_fit": 0.0
      }},
      "total_score": 0.0
    }}
  ],
  "top3": [
    {{
      "rank": 1,
      "card_id": 0,
      "reason": ""
    }}
  ],
  "hook_sentence": "",
  "differentiation": [],
  "development_priority": {{
    "recommended_direction": "",
    "next_step": "",
    "risk": ""
  }},
  "gate_a_scores": {{
    "protagonist_visible": 0.0,
    "conflict_one_line": 0.0,
    "differentiation": 0.0,
    "poster_image": 0.0,
    "market_potential": 0.0,
    "average": 0.0
  }}
}}

규칙:
- idea_cards는 10~12개
- top3는 3개
- total_score는 6개 점수 평균
- gate_a_scores.average는 5개 점수 평균
- scores와 gate 점수는 0.0~10.0
- idea_type_diagnosis, market_insight, format_rationale, structure_note, reason, risk는 2문장 이내
- 훅은 과장보다 선명함 우선
"""

        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=4000,
            temperature=0.35,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        txt = "".join(block.text for block in response.content if hasattr(block, "text")).strip()
        st.session_state["last_brainstorm_raw"] = txt

        return safe_json_loads(txt)

    except Exception as e:
        st.session_state["last_brainstorm_error"] = str(e)
        st.error(f"Brainstorm 실패: {e}")

        raw = st.session_state.get("last_brainstorm_raw")
        if raw:
            st.text_area("Brainstorm Raw Response", raw, height=400)

        return None


# ─── Sidebar ───
with st.sidebar:
    st.markdown('<div class="mt">👖 CREATOR ENGINE</div>', unsafe_allow_html=True)
    st.markdown('<div class="st">Creative Development Engine v1.2</div>', unsafe_allow_html=True)
    st.markdown("---")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state.page = "home"
        st.rerun()

    if st.session_state.cur:
        project = st.session_state.projects[st.session_state.cur]
        st.markdown(f"**📁 {project['title']}**")

        for key, label in [
            ("brainstorm", "🧠 Brainstorm"),
            ("core", "🎯 Core"),
            ("structure", "🏗️ Structure"),
            ("treatment", "📝 Treatment"),
            ("export", "📦 Export"),
        ]:
            if st.button(label, use_container_width=True, key=f"n_{key}"):
                st.session_state.page = "project"
                st.session_state.tab = key
                st.rerun()

        st.markdown("---")
        for stage_name, stage_value in project["stage_status"].items():
            st.markdown(f"{stage_name}: {badge(stage_value)}", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        '<div style="font-size:.65rem;color:#555">© 2026 BLUE JEANS PICTURES</div>',
        unsafe_allow_html=True
    )


# ─── HOME ───
def home():
    st.markdown('<div class="mt">👖 BLUE JEANS Creative Development Engine</div>', unsafe_allow_html=True)
    st.markdown('<div class="st">From instinct to industry-standard narrative architecture</div>', unsafe_allow_html=True)

    with st.expander("➕ 새 프로젝트", expanded=not bool(st.session_state.projects)):
        col1, col2 = st.columns([2, 1])

        with col1:
            title_input = st.text_input("프로젝트 제목", placeholder="예: 인도네시아 물귀신 프로젝트")
            idea_input = st.text_area(
                "💡 아이디어",
                height=120,
                placeholder="자유롭게 입력\n예: 인도네시아용 물귀신 이야기\n예: 은퇴한 킬러가 다시 돌아오는 이야기"
            )

        with col2:
            genre = st.selectbox(
                "🎬 장르",
                ["미지정", "범죄/스릴러", "드라마", "액션", "로맨스", "코미디", "호러/공포",
                 "SF", "판타지", "시대극/사극", "느와르", "미스터리", "전쟁", "뮤지컬", "다큐/논픽션"]
            )
            market_type = st.selectbox(
                "🌏 타겟 시장",
                ["미지정", "한국", "북미/미국", "일본", "중국", "동남아", "유럽", "중동", "글로벌", "직접 입력"]
            )

            market_custom = ""
            if market_type == "직접 입력":
                market_custom = st.text_input("시장 직접 입력", placeholder="예: 인도네시아+한국 공동제작")

            fmt = st.selectbox(
                "📐 포맷",
                ["미지정", "영화", "시리즈", "미니시리즈(4~8화)", "웹툰", "웹소설", "숏폼", "다큐멘터리", "애니메이션"]
            )

        if st.button("🚀 프로젝트 생성", use_container_width=True, disabled=not idea_input.strip()):
            market_final = market_custom if market_type == "직접 입력" else market_type
            project_id = f"p_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            st.session_state.projects[project_id] = {
                "project_id": project_id,
                "title": title_input or "새 프로젝트",
                "idea_text": idea_input,
                "genre": genre,
                "target_market": market_final,
                "format": fmt,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "current_stage": "brainstorm",
                "stage_status": {
                    "brainstorm": "NOT_RUN",
                    "core": "NOT_RUN",
                    "structure": "NOT_RUN",
                    "treatment": "NOT_RUN"
                },
                "research": None,
                "brainstorm": None,
                "core": None,
                "gate_results": {},
                "final_score": None
            }

            st.session_state.cur = project_id
            st.session_state.page = "project"
            st.session_state.tab = "brainstorm"
            st.rerun()

    if st.session_state.projects:
        st.markdown("### 📁 프로젝트")

        for project_id, project in sorted(
            st.session_state.projects.items(),
            key=lambda x: x[1]["updated_at"],
            reverse=True
        ):
            c1, c2 = st.columns([4, 1])

            with c1:
                st.markdown(
                    f'<div class="cc"><b>{project["title"]}</b><br>'
                    f'<span style="font-size:.75rem;color:var(--dim)">'
                    f'{project["genre"]} · {project["target_market"]} · {project["format"]} · {project["updated_at"]}'
                    f'</span></div>',
                    unsafe_allow_html=True
                )

            with c2:
                if st.button("열기 →", key=f"o_{project_id}"):
                    st.session_state.cur = project_id
                    st.session_state.page = "project"
                    st.session_state.tab = "brainstorm"
                    st.rerun()


# ─── BRAINSTORM ───
def brainstorm():
    project = st.session_state.projects[st.session_state.cur]

    st.markdown("### 🧠 Brainstorm")
    st.markdown(
        f'<div class="callout"><div class="ct">IDEA</div>{project["idea_text"]}</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)
    c1.markdown(f"**장르:** {project['genre']}")
    c2.markdown(f"**타겟:** {project['target_market']}")
    c3.markdown(f"**포맷:** {project['format']}")

    st.markdown("---")

    # 리서치
    st.markdown("#### 🔍 리서치 (선택)")
    st.caption("실화/뉴스 + 기존 작품 정보 검색. 건너뛰어도 됩니다.")

    if st.button("🔍 리서치 실행"):
        with st.spinner("리서치 정리 중..."):
            result = call_research(project["idea_text"], project["genre"], project["target_market"])
            if result:
                project["research"] = result
                project["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.rerun()

    if project.get("research"):
        research_data = project["research"]
        summary = research_data.get("research_summary", {})

        with st.expander(
            f"📰 리서치 결과 — 실화 {summary.get('total_real_events', 0)}건 · 기존작품 {summary.get('total_existing_works', 0)}건",
            expanded=True
        ):
            if research_data.get("real_events"):
                st.markdown("**📰 실화 / 뉴스**")
                for event in research_data["real_events"]:
                    st.markdown(
                        f'<div class="ri">'
                        f'<div class="rl">#{event.get("id","")} [{event.get("year","")}] {event.get("source","")}</div>'
                        f'<b>{event.get("title","")}</b><br>'
                        f'{event.get("summary","")}<br>'
                        f'<span style="color:var(--y)">→ {event.get("story_potential","")}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            if research_data.get("existing_works"):
                st.markdown("**🎬 기존 작품**")
                for work in research_data["existing_works"]:
                    st.markdown(
                        f'<div class="ri">'
                        f'<div class="rl">#{work.get("id","")} {work.get("type","")} · {work.get("country","")} · {work.get("year","")}</div>'
                        f'<b>{work.get("title","")}</b><br>'
                        f'유사: {work.get("similarity","")}<br>'
                        f'<span style="color:var(--y)">→ 차별화: {work.get("difference_opportunity","")}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            if summary.get("key_insight"):
                st.markdown(
                    f'<div class="callout"><div class="ct">💡 핵심 시사점</div>{summary["key_insight"]}</div>',
                    unsafe_allow_html=True
                )

    st.markdown("---")

    # 브레인스톰
    st.markdown("#### 🧠 Brainstorm 실행")

    if st.button("🧠 Brainstorm 실행", type="primary"):
        with st.spinner("컨셉 카드 생성 중... (약 20~40초)"):
            result = call_brainstorm(
                project["idea_text"],
                project["genre"],
                project["target_market"],
                project["format"],
                project.get("research")
            )
            if result:
                project["brainstorm"] = result
                project["stage_status"]["brainstorm"] = "DONE"
                project["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.rerun()

    if project.get("brainstorm"):
        data = project["brainstorm"]

        st.markdown(
            f'<div class="callout"><div class="ct">아이디어 유형: {data.get("idea_type", "").upper()}</div>{data.get("idea_type_diagnosis", "")}</div>',
            unsafe_allow_html=True
        )

        market_context = data.get("market_context", {})
        format_context = data.get("format_context", {})

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f'<div class="callout"><div class="ct">🌏 시장 — {market_context.get("target_market","")}</div>'
                f'기회: {market_context.get("market_insight","")}<br>'
                f'문화코드: {market_context.get("cultural_code","")}<br>'
                f'리스크: {market_context.get("market_risk","")}<br>'
                f'참고작: {", ".join(market_context.get("reference_titles", []))}'
                f'</div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f'<div class="callout"><div class="ct">📐 포맷 — {format_context.get("selected_format","")}</div>'
                f'적합성: {format_context.get("format_rationale","")}<br>'
                f'구조: {format_context.get("structure_note","")}</div>',
                unsafe_allow_html=True
            )

        st.markdown(
            f'<div style="text-align:center;padding:1.5rem 0">'
            f'<div style="font-size:.7rem;color:var(--y);font-weight:600">HOOK</div>'
            f'<div style="font-size:1.2rem;font-weight:600;color:var(--t);line-height:1.5">"{data.get("hook_sentence","")}"</div>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown("#### 🏆 Top 3")

        cards = {card["id"]: card for card in data.get("idea_cards", [])}

        for top_item in data.get("top3", []):
            card = cards.get(top_item["card_id"], {})
            if card:
                c1, c2 = st.columns([4, 1])

                with c1:
                    st.markdown(
                        f'<div class="cc">'
                        f'<span style="color:var(--y);font-weight:700">#{top_item["rank"]}</span> '
                        f'<b>{card.get("title","")}</b><br>'
                        f'<span style="color:#ccc">{card.get("logline_seed","")}</span><br>'
                        f'<span style="font-size:.8rem;color:#999">'
                        f'👤 {card.get("protagonist","")}<br>'
                        f'⚔️ {card.get("conflict","")}<br>'
                        f'✨ {card.get("hook","")}<br>'
                        f'🎬 {card.get("visual_image","")}'
                        f'</span><br>'
                        f'<span style="font-size:.75rem;color:var(--dim)">이유: {top_item.get("reason","")}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                with c2:
                    st.markdown(
                        f'<div class="sb">{card.get("total_score", 0.0)}</div>'
                        f'<div class="sl">{card.get("genre","")}</div>',
                        unsafe_allow_html=True
                    )

        differentiation = data.get("differentiation", [])
        if differentiation:
            st.markdown("#### 💎 차별화 포인트")
            for idx, item in enumerate(differentiation, 1):
                st.markdown(f"**{idx}.** {item}")

        development_priority = data.get("development_priority", {})
        st.markdown("#### 🧭 개발 우선순위")

        c1, c2, c3 = st.columns(3)
        c1.markdown(
            f'<div class="callout"><div class="ct">추천 방향</div>{development_priority.get("recommended_direction","")}</div>',
            unsafe_allow_html=True
        )
        c2.markdown(
            f'<div class="callout"><div class="ct">Core Build 집중</div>{development_priority.get("next_step","")}</div>',
            unsafe_allow_html=True
        )
        c3.markdown(
            f'<div class="callout" style="border-left-color:var(--r)"><div class="ct" style="color:var(--r)">리스크</div>{development_priority.get("risk","")}</div>',
            unsafe_allow_html=True
        )

        st.markdown("---")

        gate = data.get("gate_a_scores", {})
        avg = gate.get("average", 0)
        ok = avg >= 7.0

        st.markdown("#### 🚪 Gate A: Concept Gate")

        c1, c2 = st.columns([1, 2])

        with c1:
            color = "var(--g)" if ok else "var(--r)"
            label = "PASS" if ok else "FAIL"
            st.markdown(
                f'<div style="text-align:center">'
                f'<div class="sb" style="color:{color}">{avg}</div>'
                f'<div class="sl" style="color:{color};font-size:1rem;font-weight:700">{label}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        with c2:
            for name, score in [
                ("주인공", gate.get("protagonist_visible", 0)),
                ("갈등", gate.get("conflict_one_line", 0)),
                ("차별점", gate.get("differentiation", 0)),
                ("포스터", gate.get("poster_image", 0)),
                ("시장성", gate.get("market_potential", 0)),
            ]:
                bar_percent = score * 10
                st.markdown(
                    f'<div style="display:flex;align-items:center;margin:.2rem 0;font-size:.8rem">'
                    f'<div style="width:60px;color:var(--dim)">{name}</div>'
                    f'<div style="flex:1;background:#3a3a4a;border-radius:4px;height:8px;margin:0 .5rem">'
                    f'<div style="width:{bar_percent}%;background:var(--y);height:100%;border-radius:4px"></div>'
                    f'</div>'
                    f'<div style="width:30px;text-align:right">{score}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        if ok:
            st.success("✅ Gate A 통과. Core Build 진행 가능.")
        else:
            st.warning(f"⚠️ Gate A 미통과 (평균 {avg}). 아이디어 보강 또는 재실행 권장.")
            if st.button("🔓 Override"):
                st.info("Override. Core Build 이동.")

        all_cards = data.get("idea_cards", [])
        if all_cards:
            with st.expander(f"📋 전체 아이디어 카드 ({len(all_cards)}개)"):
                for card in sorted(all_cards, key=lambda x: x.get("total_score", 0), reverse=True):
                    st.markdown(
                        f"**#{card['id']} {card.get('title','')}** — {card.get('total_score', 0.0)}점 &nbsp; {card.get('logline_seed','')}"
                    )


# ─── Placeholder Tabs ───
def core_tab():
    st.markdown("### 🎯 Core Build")
    st.info("Brainstorm 완료 후 활성화됩니다.")


def structure_tab():
    st.markdown("### 🏗️ Structure Build")
    st.info("Phase 2에서 구현됩니다.")


def treatment_tab():
    st.markdown("### 📝 Treatment Build")
    st.info("Phase 2에서 구현됩니다.")


def export_tab():
    st.markdown("### 📦 Export")
    st.info("Core Build 완료 후 활성화됩니다.")


# ─── Router ───
if st.session_state.page == "home":
    home()
elif st.session_state.page == "project" and st.session_state.cur:
    project = st.session_state.projects[st.session_state.cur]

    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f'<div class="mt">{project["title"]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="st">{project["genre"]} · {project["target_market"]} · {project["format"]}</div>',
            unsafe_allow_html=True
        )
    with c2:
        score = project.get("final_score")
        if score:
            st.markdown(
                f'<div class="sb">{score}</div><div class="sl">Development Fit Score</div>',
                unsafe_allow_html=True
            )

    router = {
        "brainstorm": brainstorm,
        "core": core_tab,
        "structure": structure_tab,
        "treatment": treatment_tab,
        "export": export_tab,
    }
    router.get(st.session_state.tab, brainstorm)()
else:
    home()
