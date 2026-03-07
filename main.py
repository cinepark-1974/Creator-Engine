"""
👖 BLUE JEANS Creative Development Engine v1.2
아이디어 → 기획개발 패키지
단일 페이지 · 사이드바 없음 · 2단계 Brainstorm
"""

import streamlit as st
import json
import re
from datetime import datetime

ANTHROPIC_MODEL = "claude-sonnet-4-6"

# ─── Page Config ───
st.set_page_config(
    page_title="BLUE JEANS · Creator Engine",
    page_icon="👖",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ───
st.markdown("""
<style>
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

:root {
    --y: #FFCB05;
    --bg: #0E1117;
    --card: #262730;
    --t: #FAFAFA;
    --r: #FF6B6B;
    --g: #51CF66;
    --dim: #8B8B8B;
}

html, body, [class*="css"] {
    font-family: 'Pretendard', sans-serif;
}

/* 사이드바 숨김 */
section[data-testid="stSidebar"] {
    display: none;
}

.header {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--y);
    margin-bottom: 0.1rem;
}

.sub {
    font-size: 0.8rem;
    color: var(--dim);
    margin-bottom: 1.5rem;
}

.callout {
    background: var(--card);
    border-left: 3px solid var(--y);
    padding: 0.8rem 1rem;
    margin: 0.5rem 0;
    border-radius: 0 6px 6px 0;
    font-size: 0.85rem;
}

.cl {
    color: var(--y);
    font-weight: 600;
    font-size: 0.75rem;
    margin-bottom: 0.3rem;
}

.card {
    background: var(--card);
    border: 1px solid #3a3a4a;
    border-radius: 8px;
    padding: 1rem;
    margin-bottom: 0.8rem;
}

.card:hover {
    border-color: var(--y);
}

.ri {
    background: var(--card);
    border-radius: 6px;
    padding: 0.8rem;
    margin-bottom: 0.5rem;
    font-size: 0.85rem;
}

.rl {
    color: var(--y);
    font-weight: 600;
    font-size: 0.7rem;
}

.big {
    font-size: 2.2rem;
    font-weight: 700;
    color: var(--y);
    text-align: center;
}

.sm {
    font-size: 0.7rem;
    color: var(--dim);
    text-align: center;
}

.badge {
    display: inline-block;
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 600;
}

.b-done { background: var(--g); color: #000; }
.b-run  { background: var(--y); color: #000; }
.b-not  { background: #3a3a4a; color: var(--dim); }
.b-fail { background: var(--r); color: #000; }

/* ── Stepper ── */
.stepper {
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 1rem 0 1.5rem 0;
    gap: 0;
}
.step {
    display: flex;
    align-items: center;
    gap: 0;
}
.step-circle {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
}
.step-circle.active {
    background: var(--y);
    color: #000;
}
.step-circle.done {
    background: var(--g);
    color: #000;
}
.step-circle.upcoming {
    background: #3a3a4a;
    color: var(--dim);
}
.step-label {
    font-size: 0.65rem;
    margin-top: 0.2rem;
    text-align: center;
    width: 70px;
}
.step-label.active { color: var(--y); font-weight: 600; }
.step-label.done { color: var(--g); }
.step-label.upcoming { color: var(--dim); }
.step-line {
    width: 40px;
    height: 2px;
    margin: 0 2px;
    flex-shrink: 0;
}
.step-line.done { background: var(--g); }
.step-line.upcoming { background: #3a3a4a; }
.step-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
}
</style>
""", unsafe_allow_html=True)


# ─── Session State ───
defaults = {
    "view": "home",         # home | project | core | structure | treatment | export
    "projects": {},
    "cur": None,
    "last_research_raw": "",
    "last_cards_raw": "",
    "last_analysis_raw": "",
    "last_error": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─── Stepper ───
STEPS = [
    ("project", "아이디어"),
    ("project", "Brainstorm"),
    ("core", "Core"),
    ("structure", "Structure"),
    ("treatment", "Treatment"),
    ("export", "Export"),
]

def render_stepper(current_view, project_data=None):
    """상단 단계 표시 바"""
    # 현재 단계 인덱스 결정
    view_to_step = {
        "project": 1 if project_data and project_data.get("brainstorm_cards") else 0,
        "core": 2,
        "structure": 3,
        "treatment": 4,
        "export": 5,
    }
    current_idx = view_to_step.get(current_view, 0)

    # 완료된 단계 결정
    done_idx = -1
    if project_data:
        if project_data.get("brainstorm_cards"):
            done_idx = 1
        if project_data.get("brainstorm_analysis"):
            ga = project_data["brainstorm_analysis"].get("gate_a_scores", {})
            if ga.get("average", 0) >= 7.0:
                done_idx = 1  # Gate A 통과
        if project_data.get("core"):
            done_idx = 2
        # structure, treatment, export는 Phase 2

    html_parts = []
    for i, (view_key, label) in enumerate(STEPS):
        # 상태 결정
        if i < current_idx and i <= done_idx:
            state = "done"
        elif i == current_idx:
            state = "active"
        else:
            state = "upcoming"

        # 클릭 가능 여부 (done 단계만)
        circle_content = "✓" if state == "done" else str(i + 1)

        html_parts.append(
            f'<div class="step-wrap">'
            f'<div class="step-circle {state}">{circle_content}</div>'
            f'<div class="step-label {state}">{label}</div>'
            f'</div>'
        )

        # 마지막이 아니면 연결선
        if i < len(STEPS) - 1:
            line_state = "done" if i < current_idx and i <= done_idx else "upcoming"
            html_parts.append(f'<div class="step-line {line_state}"></div>')

    stepper_html = '<div class="stepper">' + ''.join(html_parts) + '</div>'
    st.markdown(stepper_html, unsafe_allow_html=True)


# ─── JSON Helpers ───
def extract_json_object(text: str) -> str:
    """응답 텍스트에서 JSON 객체만 추출"""
    text = text.strip()

    # 코드블록 제거
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    # 첫 { 부터 마지막 } 까지 추출
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("JSON 객체 시작/끝을 찾지 못했습니다.")

    return text[start:end + 1]


def safe_json_loads(text: str):
    """JSON 파싱 (trailing comma 자동 제거)"""
    cleaned = extract_json_object(text)
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)
    return json.loads(cleaned)


# ─── API Client ───
def get_client():
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("anthropic 패키지가 설치되지 않았습니다. requirements.txt를 확인하세요.")

    if "ANTHROPIC_API_KEY" not in st.secrets:
        raise RuntimeError("ANTHROPIC_API_KEY가 secrets에 설정되지 않았습니다.")

    return anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])


# ─── API Call: Research ───
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

        txt = "".join(
            block.text for block in response.content if hasattr(block, "text")
        ).strip()
        st.session_state["last_research_raw"] = txt

        return safe_json_loads(txt)

    except Exception as e:
        st.error(f"리서치 실패: {e}")
        raw = st.session_state.get("last_research_raw")
        if raw:
            with st.expander("🔧 Research Raw Response (디버그)"):
                st.text_area("Raw", raw, height=300)
        return None


# ─── API Call: Brainstorm Cards (1단계) ───
def call_brainstorm_cards(idea, genre, market, fmt, research=None):
    """1단계: 아이디어 카드 10개 + Top 3 생성 (토큰 집중)"""
    try:
        client = get_client()

        system_prompt = """당신은 글로벌 콘텐츠 시장을 이해하는 Development Producer이자 Script Architect다.
기획자의 아이디어를 개발 가능한 컨셉 카드로 정렬한다.
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
- 모든 텍스트 필드는 반드시 1문장, 50자 이내로 압축한다.
- 장문 서술 절대 금지. 짧고 선명하게 핵심만 쓴다.
- JSON이 잘리면 안 되므로 간결함이 최우선이다.
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
  "idea_cards": [
    {{
      "id": 1,
      "title": "10자 이내",
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
  ]
}}

규칙:
- idea_cards는 10개 (10개 초과 금지)
- top3는 3개
- total_score는 6개 점수 평균, 소수점 1자리
- scores 각 항목은 0.0~10.0
- idea_type_diagnosis는 1문장
- 각 카드의 logline_seed는 1문장, 50자 이내
- protagonist는 1문장, 30자 이내
- conflict는 1문장, 40자 이내
- hook는 1문장, 30자 이내
- visual_image는 1문장, 40자 이내
- reason은 1문장, 30자 이내
- 절대로 장문 서술하지 말 것. 짧고 강하게.
"""

        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=6000,
            temperature=0.35,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        # 토큰 한계 도달 감지
        if response.stop_reason == "max_tokens":
            st.warning("⚠️ 응답이 토큰 한계에서 잘렸습니다. 재시도합니다...")
            # 재시도: max_tokens 더 올리고 카드 수 줄이기
            retry_prompt = user_prompt.replace("idea_cards는 10개", "idea_cards는 7개")
            response = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=8000,
                temperature=0.35,
                system=system_prompt,
                messages=[{"role": "user", "content": retry_prompt}]
            )

        txt = "".join(
            block.text for block in response.content if hasattr(block, "text")
        ).strip()
        st.session_state["last_cards_raw"] = txt

        return safe_json_loads(txt)

    except Exception as e:
        st.session_state["last_error"] = str(e)
        st.error(f"카드 생성 실패: {e}")
        raw = st.session_state.get("last_cards_raw")
        if raw:
            with st.expander("🔧 Cards Raw Response (디버그)"):
                st.text_area("Raw", raw, height=400)
        return None


# ─── API Call: Brainstorm Analysis (2단계) ───
def call_brainstorm_analysis(idea, genre, market, fmt, top3_cards, research=None):
    """2단계: Top 3 기반 시장분석 + 차별화 + Gate A 채점"""
    try:
        client = get_client()

        system_prompt = """당신은 Development Producer다.
이미 생성된 Top 3 컨셉 카드를 기반으로 시장 분석, 차별화, 개발 방향, Gate A 채점을 수행한다.

중요 규칙:
- 반드시 유효한 단일 JSON 객체만 출력한다.
- JSON 외 텍스트 금지.
- 모든 key는 반드시 쌍따옴표를 사용한다.
- 후행 쉼표(trailing comma) 금지.
- 주석 금지.
- 모든 짧은 설명은 2문장 이내로 제한한다.
"""

        research_block = ""
        if research:
            research_block = f"""
[리서치 참고]
{json.dumps(research, ensure_ascii=False)}
"""

        user_prompt = f"""[입력]
아이디어: {idea}
장르: {genre}
타겟: {market}
포맷: {fmt}

[Top 3 컨셉 카드]
{json.dumps(top3_cards, ensure_ascii=False)}
{research_block}

[JSON 스키마]
{{
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
  "hook_sentence": "",
  "differentiation": ["", "", ""],
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
- gate_a_scores.average = 5개 항목의 평균, 소수점 1자리 반올림
- 모든 점수는 0.0~10.0
- hook_sentence는 1위 컨셉의 핵심을 기반으로 작성
- market_insight, cultural_code, market_risk, format_rationale, structure_note는 각 2문장 이내
- differentiation은 정확히 3개
"""

        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=2000,
            temperature=0.3,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        txt = "".join(
            block.text for block in response.content if hasattr(block, "text")
        ).strip()
        st.session_state["last_analysis_raw"] = txt

        return safe_json_loads(txt)

    except Exception as e:
        st.session_state["last_error"] = str(e)
        st.error(f"분석 실패: {e}")
        raw = st.session_state.get("last_analysis_raw")
        if raw:
            with st.expander("🔧 Analysis Raw Response (디버그)"):
                st.text_area("Raw", raw, height=400)
        return None


# ═══════════════════════════════════════════════════
#  UI 렌더링
# ═══════════════════════════════════════════════════

# ─── 공통 헤더 ───
st.markdown('<div class="header">👖 CREATOR ENGINE</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub">BLUE JEANS Creative Development Engine v1.2</div>',
    unsafe_allow_html=True
)

# ─── 뒤로가기 ───
if st.session_state.view in ("project", "core") and st.session_state.cur:
    if st.session_state.view == "core":
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("← 프로젝트 목록"):
                st.session_state.view = "home"
                st.rerun()
        with col_nav2:
            if st.button("← Brainstorm"):
                st.session_state.view = "project"
                st.rerun()
    else:
        if st.button("← 프로젝트 목록"):
            st.session_state.view = "home"
            st.rerun()


# ═══════════════════════════════════════════════════
#  HOME
# ═══════════════════════════════════════════════════
if st.session_state.view == "home":

    # 새 프로젝트 생성
    with st.expander("➕ 새 프로젝트", expanded=not bool(st.session_state.projects)):
        col1, col2 = st.columns([2, 1])

        with col1:
            title_input = st.text_input(
                "프로젝트 제목",
                placeholder="예: 인도네시아 물귀신 프로젝트"
            )
            idea_input = st.text_area(
                "💡 아이디어",
                height=120,
                placeholder=(
                    "자유롭게 입력\n"
                    "예: 인도네시아용 물귀신 이야기\n"
                    "예: 은퇴한 킬러가 다시 돌아오는 이야기\n"
                    "예: 40대 여형사, 연쇄살인범이 딸의 담임교사"
                )
            )

        with col2:
            genre_input = st.selectbox(
                "🎬 장르",
                ["미지정", "범죄/스릴러", "드라마", "액션", "로맨스", "코미디",
                 "호러/공포", "SF", "판타지", "시대극/사극", "느와르",
                 "미스터리", "전쟁", "뮤지컬", "다큐/논픽션"]
            )

            market_type = st.selectbox(
                "🌏 타겟 시장",
                ["미지정", "한국", "북미/미국", "일본", "중국",
                 "동남아", "유럽", "중동", "글로벌", "직접 입력"]
            )

            market_custom = ""
            if market_type == "직접 입력":
                market_custom = st.text_input(
                    "시장 직접 입력",
                    placeholder="예: 인도네시아+한국 공동제작"
                )

            format_input = st.selectbox(
                "📐 포맷",
                ["미지정", "영화", "시리즈", "미니시리즈(4~8화)",
                 "웹툰", "웹소설", "숏폼", "다큐멘터리", "애니메이션"]
            )

        if st.button("🚀 프로젝트 생성", use_container_width=True, disabled=not idea_input.strip()):
            market_final = market_custom if market_type == "직접 입력" else market_type
            project_id = f"p_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            st.session_state.projects[project_id] = {
                "project_id": project_id,
                "title": title_input or "새 프로젝트",
                "idea_text": idea_input,
                "genre": genre_input,
                "target_market": market_final,
                "format": format_input,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "research": None,
                "brainstorm_cards": None,
                "brainstorm_analysis": None,
            }

            st.session_state.cur = project_id
            st.session_state.view = "project"
            st.rerun()

    # 프로젝트 목록
    if st.session_state.projects:
        st.markdown("---")
        st.markdown("### 📁 프로젝트")

        for project_id, project in sorted(
            st.session_state.projects.items(),
            key=lambda x: x[1]["updated_at"],
            reverse=True
        ):
            col1, col2 = st.columns([5, 1])

            with col1:
                has_cards = "✅" if project.get("brainstorm_cards") else "—"
                has_analysis = "✅" if project.get("brainstorm_analysis") else "—"

                st.markdown(
                    f'<div class="card">'
                    f'<b>{project["title"]}</b><br>'
                    f'<span style="font-size:.75rem;color:var(--dim)">'
                    f'{project["genre"]} · {project["target_market"]} · {project["format"]} · '
                    f'{project["updated_at"]}'
                    f'<br>카드 {has_cards} · 분석 {has_analysis}'
                    f'</span></div>',
                    unsafe_allow_html=True
                )

            with col2:
                if st.button("열기 →", key=f"open_{project_id}"):
                    st.session_state.cur = project_id
                    st.session_state.view = "project"
                    st.rerun()


# ═══════════════════════════════════════════════════
#  PROJECT (단일 페이지 스크롤)
# ═══════════════════════════════════════════════════
elif st.session_state.view == "project" and st.session_state.cur:

    project = st.session_state.projects[st.session_state.cur]

    # ─── 프로젝트 헤더 ───
    st.markdown(f"## {project['title']}")
    st.caption(f"{project['genre']} · {project['target_market']} · {project['format']}")

    # ─── 단계 표시 ───
    render_stepper("project", project)

    st.markdown(
        f'<div class="callout">'
        f'<div class="cl">IDEA</div>'
        f'{project["idea_text"]}'
        f'</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ═══════════════════════════════════════
    # STEP 1: 리서치 (선택)
    # ═══════════════════════════════════════
    st.markdown("### 🔍 리서치")
    st.caption("실화/뉴스 + 기존 작품 정보 검색. 건너뛰어도 됩니다.")

    if st.button("🔍 리서치 실행"):
        with st.spinner("리서치 정리 중..."):
            result = call_research(
                project["idea_text"],
                project["genre"],
                project["target_market"]
            )
            if result:
                project["research"] = result
                project["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.rerun()

    # 리서치 결과 표시
    if project.get("research"):
        research_data = project["research"]
        summary = research_data.get("research_summary", {})

        with st.expander(
            f"📰 리서치 결과 — "
            f"실화 {summary.get('total_real_events', 0)}건 · "
            f"작품 {summary.get('total_existing_works', 0)}건",
            expanded=True
        ):
            # 실화/뉴스
            if research_data.get("real_events"):
                st.markdown("**📰 실화 / 뉴스**")
                for event in research_data["real_events"]:
                    st.markdown(
                        f'<div class="ri">'
                        f'<div class="rl">#{event.get("id", "")} '
                        f'[{event.get("year", "")}] {event.get("source", "")}</div>'
                        f'<b>{event.get("title", "")}</b><br>'
                        f'{event.get("summary", "")}<br>'
                        f'<span style="color:var(--y)">→ {event.get("story_potential", "")}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            # 기존 작품
            if research_data.get("existing_works"):
                st.markdown("**🎬 기존 작품**")
                for work in research_data["existing_works"]:
                    st.markdown(
                        f'<div class="ri">'
                        f'<div class="rl">#{work.get("id", "")} '
                        f'{work.get("type", "")} · {work.get("country", "")} · '
                        f'{work.get("year", "")}</div>'
                        f'<b>{work.get("title", "")}</b><br>'
                        f'유사: {work.get("similarity", "")}<br>'
                        f'<span style="color:var(--y)">→ 차별화: '
                        f'{work.get("difference_opportunity", "")}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            # 핵심 시사점
            if summary.get("key_insight"):
                st.markdown(
                    f'<div class="callout">'
                    f'<div class="cl">💡 핵심 시사점</div>'
                    f'{summary["key_insight"]}'
                    f'</div>',
                    unsafe_allow_html=True
                )

    st.markdown("---")

    # ═══════════════════════════════════════
    # STEP 2: Brainstorm (2단계 분할 호출)
    # ═══════════════════════════════════════
    st.markdown("### 🧠 Brainstorm")

    if st.button("🧠 Brainstorm 실행", type="primary"):

        # ── 1단계: 카드 생성 ──
        with st.spinner("① 컨셉 카드 생성 중... (약 20~30초)"):
            cards_result = call_brainstorm_cards(
                project["idea_text"],
                project["genre"],
                project["target_market"],
                project["format"],
                project.get("research")
            )

        if cards_result:
            project["brainstorm_cards"] = cards_result
            project["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

            # Top 3 카드 추출
            all_cards = cards_result.get("idea_cards", [])
            cards_map = {c["id"]: c for c in all_cards}

            top3_data = []
            for t in cards_result.get("top3", []):
                card = cards_map.get(t["card_id"])
                if card:
                    top3_data.append(card)

            # ── 2단계: 분석 + Gate A ──
            if top3_data:
                with st.spinner("② 시장 분석 + Gate A 채점 중... (약 10~20초)"):
                    analysis_result = call_brainstorm_analysis(
                        project["idea_text"],
                        project["genre"],
                        project["target_market"],
                        project["format"],
                        top3_data,
                        project.get("research")
                    )

                if analysis_result:
                    project["brainstorm_analysis"] = analysis_result
                    project["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            else:
                st.warning("Top 3 카드를 추출하지 못했습니다. 카드만 표시합니다.")

            st.rerun()

    # ═══════════════════════════════════════
    # 결과 표시
    # ═══════════════════════════════════════
    if project.get("brainstorm_cards"):
        bc = project["brainstorm_cards"]
        ba = project.get("brainstorm_analysis", {})

        # ── 아이디어 유형 ──
        st.markdown(
            f'<div class="callout">'
            f'<div class="cl">아이디어 유형: {bc.get("idea_type", "").upper()}</div>'
            f'{bc.get("idea_type_diagnosis", "")}'
            f'</div>',
            unsafe_allow_html=True
        )

        # ── 시장 · 포맷 맥락 (분석 있을 때) ──
        if ba:
            market_ctx = ba.get("market_context", {})
            format_ctx = ba.get("format_context", {})

            col1, col2 = st.columns(2)

            with col1:
                ref_titles = ", ".join(market_ctx.get("reference_titles", []))
                st.markdown(
                    f'<div class="callout">'
                    f'<div class="cl">🌏 시장 — {market_ctx.get("target_market", "")}</div>'
                    f'기회: {market_ctx.get("market_insight", "")}<br>'
                    f'문화코드: {market_ctx.get("cultural_code", "")}<br>'
                    f'리스크: {market_ctx.get("market_risk", "")}<br>'
                    f'참고작: {ref_titles}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    f'<div class="callout">'
                    f'<div class="cl">📐 포맷 — {format_ctx.get("selected_format", "")}</div>'
                    f'적합성: {format_ctx.get("format_rationale", "")}<br>'
                    f'구조: {format_ctx.get("structure_note", "")}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            # ── 훅 문장 ──
            hook = ba.get("hook_sentence", "")
            if hook:
                st.markdown(
                    f'<div style="text-align:center;padding:1.5rem 0">'
                    f'<div style="font-size:.7rem;color:var(--y);font-weight:600">HOOK</div>'
                    f'<div style="font-size:1.15rem;font-weight:600;color:var(--t);line-height:1.5">'
                    f'"{hook}"</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        st.markdown("---")

        # ── Top 3 컨셉 ──
        st.markdown("#### 🏆 Top 3 컨셉")

        cards_map = {c["id"]: c for c in bc.get("idea_cards", [])}

        for top_item in bc.get("top3", []):
            card = cards_map.get(top_item["card_id"], {})
            if card:
                col1, col2 = st.columns([5, 1])

                with col1:
                    st.markdown(
                        f'<div class="card">'
                        f'<span style="color:var(--y);font-weight:700">#{top_item["rank"]}</span> '
                        f'<b>{card.get("title", "")}</b><br>'
                        f'<span style="color:#ccc">{card.get("logline_seed", "")}</span><br>'
                        f'<span style="font-size:.8rem;color:#999">'
                        f'👤 {card.get("protagonist", "")}<br>'
                        f'⚔️ {card.get("conflict", "")}<br>'
                        f'✨ {card.get("hook", "")}<br>'
                        f'🎬 {card.get("visual_image", "")}'
                        f'</span><br>'
                        f'<span style="font-size:.75rem;color:var(--dim)">'
                        f'이유: {top_item.get("reason", "")}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

                with col2:
                    st.markdown(
                        f'<div class="big">{card.get("total_score", 0.0)}</div>'
                        f'<div class="sm">{card.get("genre", "")}</div>',
                        unsafe_allow_html=True
                    )

        # ── 차별화 포인트 (분석 있을 때) ──
        if ba:
            differentiation = ba.get("differentiation", [])
            if differentiation:
                st.markdown("#### 💎 차별화 포인트")
                for idx, item in enumerate(differentiation, 1):
                    st.markdown(f"**{idx}.** {item}")

            # ── 개발 우선순위 ──
            dev_priority = ba.get("development_priority", {})
            if dev_priority:
                st.markdown("#### 🧭 개발 우선순위")
                col1, col2, col3 = st.columns(3)

                col1.markdown(
                    f'<div class="callout">'
                    f'<div class="cl">추천 방향</div>'
                    f'{dev_priority.get("recommended_direction", "")}'
                    f'</div>',
                    unsafe_allow_html=True
                )
                col2.markdown(
                    f'<div class="callout">'
                    f'<div class="cl">Core Build 집중</div>'
                    f'{dev_priority.get("next_step", "")}'
                    f'</div>',
                    unsafe_allow_html=True
                )
                col3.markdown(
                    f'<div class="callout" style="border-left-color:var(--r)">'
                    f'<div class="cl" style="color:var(--r)">리스크</div>'
                    f'{dev_priority.get("risk", "")}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            st.markdown("---")

            # ── Gate A: Concept Gate ──
            gate = ba.get("gate_a_scores", {})
            avg = gate.get("average", 0)
            passed = avg >= 7.0

            st.markdown("#### 🚪 Gate A: Concept Gate")

            col1, col2 = st.columns([1, 2])

            with col1:
                gate_color = "var(--g)" if passed else "var(--r)"
                gate_label = "PASS" if passed else "FAIL"
                st.markdown(
                    f'<div style="text-align:center">'
                    f'<div class="big" style="color:{gate_color}">{avg}</div>'
                    f'<div class="sm" style="color:{gate_color};'
                    f'font-size:1rem;font-weight:700">{gate_label}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            with col2:
                gate_items = [
                    ("주인공", gate.get("protagonist_visible", 0)),
                    ("갈등", gate.get("conflict_one_line", 0)),
                    ("차별점", gate.get("differentiation", 0)),
                    ("포스터", gate.get("poster_image", 0)),
                    ("시장성", gate.get("market_potential", 0)),
                ]
                for name, score in gate_items:
                    bar_pct = score * 10
                    st.markdown(
                        f'<div style="display:flex;align-items:center;'
                        f'margin:.2rem 0;font-size:.8rem">'
                        f'<div style="width:60px;color:var(--dim)">{name}</div>'
                        f'<div style="flex:1;background:#3a3a4a;'
                        f'border-radius:4px;height:8px;margin:0 .5rem">'
                        f'<div style="width:{bar_pct}%;background:var(--y);'
                        f'height:100%;border-radius:4px"></div>'
                        f'</div>'
                        f'<div style="width:30px;text-align:right">{score}</div>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

            if passed:
                st.success("✅ Gate A 통과. Core Build 진행 가능.")
                if st.button("🎯 Core Build 진행 →", type="primary", use_container_width=True):
                    project["stage"] = "core"
                    st.session_state.view = "core"
                    st.rerun()
            else:
                st.warning(
                    f"⚠️ Gate A 미통과 (평균 {avg}). "
                    f"아이디어 보강 또는 재실행 권장."
                )
                col_o1, col_o2 = st.columns(2)
                with col_o1:
                    if st.button("🔓 Override (강제 통과)"):
                        project["stage"] = "core"
                        st.session_state.view = "core"
                        st.rerun()
                with col_o2:
                    if st.button("🔄 Brainstorm 재실행"):
                        project["brainstorm_cards"] = None
                        project["brainstorm_analysis"] = None
                        st.rerun()

        # ── 전체 아이디어 카드 (접이식) ──
        all_cards = bc.get("idea_cards", [])
        if all_cards:
            with st.expander(f"📋 전체 아이디어 카드 ({len(all_cards)}개)"):
                for card in sorted(
                    all_cards,
                    key=lambda x: x.get("total_score", 0),
                    reverse=True
                ):
                    st.markdown(
                        f"**#{card['id']} {card.get('title', '')}** — "
                        f"{card.get('total_score', 0.0)}점 &nbsp; "
                        f"{card.get('logline_seed', '')}"
                    )

    # ─── 푸터 ───
    st.markdown("---")
    st.caption("© 2026 BLUE JEANS PICTURES · Creator Engine v1.2")


# ═══════════════════════════════════════════════════
#  CORE BUILD
# ═══════════════════════════════════════════════════
elif st.session_state.view == "core" and st.session_state.cur:

    project = st.session_state.projects[st.session_state.cur]
    bc = project.get("brainstorm_cards", {})
    ba = project.get("brainstorm_analysis", {})

    st.markdown(f"## {project['title']} — Core Build")
    st.caption(f"{project['genre']} · {project['target_market']} · {project['format']}")

    # ─── 단계 표시 ───
    render_stepper("core", project)

    # Brainstorm에서 인계받은 정보 표시
    if bc:
        cards_map = {c["id"]: c for c in bc.get("idea_cards", [])}
        top3 = bc.get("top3", [])

        if top3:
            top1 = cards_map.get(top3[0].get("card_id"), {})
            if top1:
                st.markdown(
                    f'<div class="callout">'
                    f'<div class="cl">🏆 선정 컨셉: {top1.get("title", "")}</div>'
                    f'{top1.get("logline_seed", "")}'
                    f'</div>',
                    unsafe_allow_html=True
                )

    if ba:
        hook = ba.get("hook_sentence", "")
        dp = ba.get("development_priority", {})
        if dp.get("next_step"):
            st.markdown(
                f'<div class="callout">'
                f'<div class="cl">Core Build 집중 포인트</div>'
                f'{dp["next_step"]}'
                f'</div>',
                unsafe_allow_html=True
            )

    st.markdown("---")

    st.markdown("### 🎯 Core Build 실행")
    st.caption("로그라인 · 기획의도 · 세계관 · 캐릭터 · Goal/Need/Strategy를 고정합니다.")

    if st.button("🎯 Core Build 실행", type="primary"):
        st.info("Core Build Prompt는 다음 단계에서 구현됩니다.")
        # TODO: call_core_build() 구현 후 연결

    # Core Build 결과 표시 영역 (구현 예정)
    if project.get("core"):
        st.markdown("#### Core Build 결과")
        st.json(project["core"])
    else:
        st.markdown(
            '<div style="text-align:center;padding:3rem 0;color:var(--dim)">'
            '🎯 Core Build를 실행하면 여기에 결과가 표시됩니다.<br>'
            'Logline Pack · Project Intent · World Build · Character Build'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.caption("© 2026 BLUE JEANS PICTURES · Creator Engine v1.2")
