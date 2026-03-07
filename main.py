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
    font-size: 0.6rem;
    margin-top: 0.2rem;
    text-align: center;
    width: 55px;
}
.step-label.active { color: var(--y); font-weight: 600; }
.step-label.done { color: var(--g); }
.step-label.upcoming { color: var(--dim); }
.step-line {
    width: 25px;
    height: 2px;
    margin: 0 1px;
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
    "last_core_raw": "",
    "last_gate_raw": "",
    "last_structure_story_raw": "",
    "last_structure_diag_raw": "",
    "last_structure_gate_raw": "",
    "last_scene_design_raw": "",
    "last_treatment_raw": "",
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
    ("scene_design", "Scene"),
    ("treatment", "Treatment"),
    ("export", "Export"),
]

def render_stepper(current_view, project_data=None):
    """상단 단계 표시 바"""
    view_to_step = {
        "project": 1 if project_data and project_data.get("brainstorm_cards") else 0,
        "core": 2,
        "structure": 3,
        "scene_design": 4,
        "treatment": 5,
        "export": 6,
    }
    current_idx = view_to_step.get(current_view, 0)

    done_idx = -1
    if project_data:
        if project_data.get("brainstorm_cards"):
            done_idx = 1
        if project_data.get("brainstorm_analysis"):
            ga = project_data["brainstorm_analysis"].get("gate_a_scores", {})
            if ga.get("average", 0) >= 7.0:
                done_idx = 1
        if project_data.get("core"):
            done_idx = 2
        if project_data.get("structure_story"):
            done_idx = 3
        if project_data.get("scene_design"):
            done_idx = 4
        if project_data.get("treatment"):
            done_idx = 5

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


# ─── API Call: Core Build Main (1단계) ───
def call_core_build_main(idea, genre, market, fmt, selected_concept, research=None):
    """Core Build 1단계: Logline + Intent + World + Character + Goal/Need/Strategy"""
    try:
        client = get_client()

        system_prompt = """당신은 헐리우드 메이저 스튜디오의 Development Producer이자 Script Architect다.
Brainstorm에서 선정된 컨셉을 기반으로 Core Build를 수행한다.
로그라인을 고정하고, 기획의도와 주제를 정리하고, 세계관과 캐릭터를 설계하고,
주인공의 Goal / Need / Strategy를 확정한다.

중요 규칙:
- 반드시 유효한 단일 JSON 객체만 출력한다.
- JSON 외 텍스트 금지.
- 후행 쉼표(trailing comma) 금지.
- 문자열 내부 줄바꿈 대신 공백을 사용한다.
- 한국어로 작성하되 전문 용어는 한글용어(English Term)로 병기한다.
- 작가의 고유한 아이디어를 훼손하지 않는다.
- 모든 텍스트 필드는 1~2문장, 50자 이내로 압축한다.
- 캐릭터는 주인공, 적대자, 조력자, 거울 캐릭터 4인으로 제한한다.
"""

        research_block = ""
        if research:
            research_block = f"\n[리서치 참고]\n{json.dumps(research, ensure_ascii=False)}"

        user_prompt = f"""[입력]
아이디어: {idea}
장르: {genre}
타겟: {market}
포맷: {fmt}

[선정 컨셉]
{json.dumps(selected_concept, ensure_ascii=False)}
{research_block}

[JSON 스키마]
{{
  "logline_pack": {{
    "original": "원본 로그라인 1문장",
    "washed": "서사 불순물 제거한 정제 로그라인 1문장",
    "investor": "투자자용 1문장",
    "director": "감독용 1문장",
    "character_hook": "배우용 캐릭터 훅 1문장"
  }},
  "project_intent": {{
    "subject": "소재 기획의도 — 이 소재가 왜 지금 필요한가, 어떤 현실/감정/사회적 맥락과 연결되는가 (2~3문장)",
    "genre_approach": "장르 기획의도 — 이 장르 접근이 왜 유효한가, 관객에게 어떤 체험을 주는가 (2~3문장)",
    "market_rationale": "시장 기획의도 — 타겟 시장에서 왜 통하는가, 어떤 수요/트렌드/공백에 대응하는가 (2~3문장)",
    "pitch": "엘리베이터 피치 1문장",
    "theme": "주제 1문장",
    "tone_manner": ["톤앤매너 키워드 3~5개"]
  }},
  "goal_need_strategy": {{
    "goal": "주인공의 목적/욕망 1문장",
    "need": "상실/결핍의 근원 1문장",
    "strategy": "해결 전략/방법 1문장",
    "risk": "실패 시 잃는 것 1문장",
    "ending_payoff": "결말에서 G/N/S가 어떻게 회수되는가 1문장"
  }},
  "world_build": {{
    "time": "시간 배경",
    "space": "공간 배경",
    "rules": "세계관 규칙 1문장",
    "taboo": "금기 1문장",
    "power_structure": "권력 구조 1문장",
    "visual_keywords": ["시각 이미지 키워드 3~5개"],
    "conflict_points": ["세계관 충돌 포인트 3개"]
  }},
  "characters": [
    {{
      "role": "protagonist",
      "name": "",
      "description": "인물 소개 1문장",
      "goal": "이 인물의 욕망 1문장",
      "need": "결핍 1문장",
      "strategy": "행동 방식 1문장",
      "flaw": "결점 1문장",
      "arc": "변화 1문장",
      "dialogue_tone": "대사 톤 키워드"
    }},
    {{
      "role": "antagonist",
      "name": "",
      "description": "",
      "goal": "",
      "need": "",
      "strategy": "",
      "flaw": "",
      "arc": "",
      "dialogue_tone": ""
    }},
    {{
      "role": "ally",
      "name": "",
      "description": "",
      "goal": "",
      "flaw": "",
      "dialogue_tone": ""
    }},
    {{
      "role": "mirror",
      "name": "",
      "description": "",
      "goal": "",
      "flaw": "",
      "dialogue_tone": ""
    }}
  ],
  "relationship_map": [
    "주인공↔적대자: 관계 1문장",
    "주인공↔조력자: 관계 1문장",
    "주인공↔거울: 관계 1문장"
  ]
}}

규칙:
- logline_pack 각 버전은 관점만 다르고 같은 이야기를 가리켜야 한다.
- goal_need_strategy는 이 작품의 서사 엔진이다. 가장 정밀하게 작성할 것.
- characters는 정확히 4명. 각 인물의 goal이 서로 달라야 한다.
- world_build의 conflict_points는 세계관이 만들어내는 갈등이어야 한다.
"""

        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=6000,
            temperature=0.3,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        if response.stop_reason == "max_tokens":
            st.warning("⚠️ Core Build 응답 잘림. 재시도...")
            response = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=8000,
                temperature=0.3,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )

        txt = "".join(
            block.text for block in response.content if hasattr(block, "text")
        ).strip()
        st.session_state["last_core_raw"] = txt

        return safe_json_loads(txt)

    except Exception as e:
        st.session_state["last_error"] = str(e)
        st.error(f"Core Build 실패: {e}")
        raw = st.session_state.get("last_core_raw", "")
        if raw:
            with st.expander("🔧 Core Build Raw Response (디버그)"):
                st.text_area("Raw", raw, height=400)
        return None


# ─── API Call: Core Gate (2단계) ───
def call_core_gate(core_data):
    """Core Build 2단계: Gate B (Drive) + Gate C (Character) 채점"""
    try:
        client = get_client()

        system_prompt = """당신은 Development Producer다.
Core Build 결과를 기반으로 Gate B (Drive Gate)와 Gate C (Character Gate)를 채점한다.

중요 규칙:
- 유효한 단일 JSON 객체만 출력. JSON 외 텍스트 금지. 후행 쉼표 금지.
- 모든 점수는 0.0~10.0 소수점 1자리.
- 피드백은 1문장 이내.
"""

        user_prompt = f"""[Core Build 결과]
{json.dumps(core_data, ensure_ascii=False)}

[JSON 스키마]
{{
  "gate_b_drive": {{
    "goal_clarity": 0.0,
    "need_from_loss": 0.0,
    "strategy_creative": 0.0,
    "failure_cost": 0.0,
    "average": 0.0,
    "feedback": "Gate B 종합 피드백 1문장"
  }},
  "gate_c_character": {{
    "protagonist_antagonist_logic": 0.0,
    "supporting_not_functional": 0.0,
    "relationship_produces_conflict": 0.0,
    "average": 0.0,
    "feedback": "Gate C 종합 피드백 1문장"
  }},
  "five_axis_scores": {{
    "goal": 0.0,
    "need": 0.0,
    "strategy": 0.0,
    "structure": 0.0,
    "character_concept": 0.0,
    "final_score": 0.0,
    "verdict": "개발 진행 | 개발 보류 | 구조 재설계"
  }}
}}

규칙:
- gate_b average = 4항목 평균
- gate_c average = 3항목 평균
- five_axis: structure는 아직 Structure Build 전이므로 goal/need/strategy 기반으로 잠정 추정
- final_score = 0.20*goal + 0.20*need + 0.20*strategy + 0.25*structure + 0.15*character_concept
- verdict: 8.0 이상 → 개발 진행, 6.0~7.9 → 개발 보류, 5.9 이하 → 구조 재설계
"""

        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=2000,
            temperature=0.2,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )

        txt = "".join(
            block.text for block in response.content if hasattr(block, "text")
        ).strip()
        st.session_state["last_gate_raw"] = txt

        return safe_json_loads(txt)

    except Exception as e:
        st.session_state["last_error"] = str(e)
        st.error(f"Gate 채점 실패: {e}")
        raw = st.session_state.get("last_gate_raw", "")
        if raw:
            with st.expander("🔧 Gate Raw Response (디버그)"):
                st.text_area("Raw", raw, height=400)
        return None


# ─── API Call: Structure Build Story (1단계) ───
def call_structure_story(core_data, genre, market, fmt):
    """Structure 1단계: Synopsis 1P + Storyline"""
    try:
        client = get_client()
        gns = core_data.get("goal_need_strategy", {})
        lp = core_data.get("logline_pack", {})
        chars = core_data.get("characters", [])

        system_prompt = """당신은 헐리우드 수준의 Story Architect다.
Core Build 결과를 기반으로 시놉시스와 스토리라인을 설계한다.
주인공의 Goal/Need/Strategy가 모든 전개의 중심축이 되어야 한다.

중요 규칙:
- 유효한 단일 JSON만 출력. JSON 외 텍스트 금지.
- 후행 쉼표 금지. 문자열 줄바꿈 대신 공백.
- 한국어 작성. 전문용어 한글(English) 병기.
- 각 필드 2문장 이내.
"""

        user_prompt = f"""[Core Build 요약]
로그라인: {lp.get("washed", lp.get("original", ""))}
장르: {genre} / 타겟: {market} / 포맷: {fmt}
Goal: {gns.get("goal","")}
Need: {gns.get("need","")}
Strategy: {gns.get("strategy","")}
캐릭터: {json.dumps(chars, ensure_ascii=False)}

[JSON 스키마]
{{
  "synopsis_1p": {{
    "opening": "시작 상황",
    "catalyst": "촉발 사건",
    "development": "전개",
    "midpoint": "미드포인트 전환",
    "collapse": "붕괴/위기",
    "climax": "결전",
    "ending": "결말"
  }},
  "storyline": [
    {{
      "seq": 1,
      "label": "시퀀스 라벨 (동사→동사 형식)",
      "pages": "p.1~15",
      "summary": "이 구간 전개 요약",
      "conflict": "이 구간의 갈등",
      "emotion": "감정선 키워드",
      "hook": "다음 구간으로 당기는 힘"
    }}
  ]
}}

규칙:
- synopsis_1p 각 항목 2문장 이내
- storyline은 8개 시퀀스 (영화 기준)
- 시리즈면 시퀀스 대신 에피소드 단위 6~8개
- 각 시퀀스의 summary, conflict, hook 1문장씩
"""

        response = client.messages.create(
            model=ANTHROPIC_MODEL, max_tokens=6000, temperature=0.3,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        if response.stop_reason == "max_tokens":
            response = client.messages.create(
                model=ANTHROPIC_MODEL, max_tokens=8000, temperature=0.3,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
        txt = "".join(b.text for b in response.content if hasattr(b, "text")).strip()
        st.session_state["last_structure_story_raw"] = txt
        return safe_json_loads(txt)
    except Exception as e:
        st.error(f"Story 생성 실패: {e}")
        raw = st.session_state.get("last_structure_story_raw", "")
        if raw:
            with st.expander("🔧 Story Raw (디버그)"):
                st.text_area("Raw", raw, height=400)
        return None


# ─── API Call: Structure Build Diagnosis + Character Arcs (2단계) ───
def call_structure_diagnosis(core_data, story_data, genre, fmt):
    """Structure 2단계: 3막 구조 진단 + 15비트 + 캐릭터 관계 변화표"""
    try:
        client = get_client()
        gns = core_data.get("goal_need_strategy", {})
        chars = core_data.get("characters", [])

        system_prompt = """당신은 헐리우드 수준의 Structure Analyst다.
시놉시스와 스토리라인을 기반으로 구조 진단과 캐릭터 변화를 설계한다.

중요 규칙:
- 유효한 단일 JSON만 출력. JSON 외 텍스트 금지.
- 후행 쉼표 금지. 문자열 줄바꿈 대신 공백.
- 한국어 작성. 모든 필드 1~2문장 이내.
"""

        user_prompt = f"""[입력]
장르: {genre} / 포맷: {fmt}
Goal: {gns.get("goal","")} / Need: {gns.get("need","")} / Strategy: {gns.get("strategy","")}

[캐릭터]
{json.dumps(chars, ensure_ascii=False)}

[시놉시스]
{json.dumps(story_data.get("synopsis_1p", {}), ensure_ascii=False)}

[스토리라인]
{json.dumps(story_data.get("storyline", []), ensure_ascii=False)}

[JSON 스키마]
{{
  "three_act": {{
    "act1_end": "1막 끝 전환점",
    "act2_midpoint": "미드포인트",
    "act2_end": "2막 끝 전환점 (All Is Lost)",
    "act3_climax": "클라이맥스",
    "diagnosis": "3막 구조 종합 진단 1문장"
  }},
  "beat_sheet": [
    {{
      "beat": "Opening Image",
      "status": "있음|약함|없음",
      "note": "근거 1문장"
    }}
  ],
  "character_arcs": [
    {{
      "name": "캐릭터 이름",
      "role": "protagonist|antagonist|ally|mirror",
      "act1_state": "1막에서의 상태/태도 1문장",
      "turning_point": "변화를 촉발하는 사건 1문장",
      "act3_state": "3막에서의 변화된 상태 1문장",
      "arc_type": "성장|몰락|각성|반전|정체"
    }}
  ],
  "relationship_changes": [
    {{
      "pair": "캐릭터A ↔ 캐릭터B",
      "act1": "1막 관계 상태",
      "midpoint": "미드포인트 관계 전환",
      "act3": "3막 관계 도착점"
    }}
  ]
}}

규칙:
- beat_sheet는 15비트 전체 (Opening Image ~ Final Image)
- beat status는 반드시 있음/약함/없음 중 하나
- character_arcs는 Core Build의 4인 캐릭터 전원
- relationship_changes는 핵심 관계 3~4쌍
- 모든 필드 1문장 이내로 압축
"""

        response = client.messages.create(
            model=ANTHROPIC_MODEL, max_tokens=5000, temperature=0.25,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        if response.stop_reason == "max_tokens":
            response = client.messages.create(
                model=ANTHROPIC_MODEL, max_tokens=8000, temperature=0.25,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
        txt = "".join(b.text for b in response.content if hasattr(b, "text")).strip()
        st.session_state["last_structure_diag_raw"] = txt
        return safe_json_loads(txt)
    except Exception as e:
        st.error(f"구조 진단 실패: {e}")
        raw = st.session_state.get("last_structure_diag_raw", "")
        if raw:
            with st.expander("🔧 Diagnosis Raw (디버그)"):
                st.text_area("Raw", raw, height=400)
        return None


# ─── API Call: Structure Gate D (3단계) ───
def call_structure_gate(story_data, diag_data):
    """Structure 3단계: Gate D 채점"""
    try:
        client = get_client()
        system_prompt = """당신은 Development Producer다.
Structure Build 결과를 기반으로 Gate D (Structure Gate)를 채점한다.
유효한 단일 JSON만 출력. JSON 외 텍스트 금지. 후행 쉼표 금지.
모든 점수 0.0~10.0. 피드백 1문장."""

        user_prompt = f"""[시놉시스]
{json.dumps(story_data.get("synopsis_1p",{}), ensure_ascii=False)}

[3막 구조]
{json.dumps(diag_data.get("three_act",{}), ensure_ascii=False)}

[15비트]
{json.dumps(diag_data.get("beat_sheet",[]), ensure_ascii=False)}

[JSON 스키마]
{{
  "gate_d_structure": {{
    "turning_points_valid": 0.0,
    "midpoint_redirects": 0.0,
    "all_is_lost_works": 0.0,
    "ending_inevitable_surprising": 0.0,
    "average": 0.0,
    "feedback": "Gate D 종합 피드백 1문장"
  }}
}}
규칙: average = 4항목 평균."""

        response = client.messages.create(
            model=ANTHROPIC_MODEL, max_tokens=1500, temperature=0.2,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        txt = "".join(b.text for b in response.content if hasattr(b, "text")).strip()
        st.session_state["last_structure_gate_raw"] = txt
        return safe_json_loads(txt)
    except Exception as e:
        st.error(f"Gate D 실패: {e}")
        return None


# ─── API Call: 기승전결 1pg 줄글 ───
def call_structure_prose(core_data, story_data):
    """기승전결 구조의 1페이지 줄글 시놉시스"""
    try:
        client = get_client()
        lp = core_data.get("logline_pack", {})
        gns = core_data.get("goal_need_strategy", {})
        syn = story_data.get("synopsis_1p", {})
        storyline = story_data.get("storyline", [])

        user_prompt = f"""[작품 정보]
로그라인: {lp.get("washed", lp.get("original",""))}
Goal: {gns.get("goal","")} / Need: {gns.get("need","")} / Strategy: {gns.get("strategy","")}

[시놉시스]
{json.dumps(syn, ensure_ascii=False)}

[스토리라인]
{json.dumps(storyline, ensure_ascii=False)}

[요청]
위 정보를 기반으로 기-승-전-결 구조의 1페이지 분량 줄글 시놉시스를 작성하라.

규칙:
- 기(起): 상황 설정과 주인공 소개
- 승(承): 사건 전개와 갈등 심화
- 전(轉): 반전과 위기
- 결(結): 해결과 마무리
- 전체 500~700자 분량
- 줄글로 작성. 번호나 구분 기호 없이 자연스러운 서술체.
- 한국어로 작성.
- JSON 형식: {{"prose": "줄글 텍스트"}}
- JSON만 출력. JSON 외 텍스트 금지."""

        response = client.messages.create(
            model=ANTHROPIC_MODEL, max_tokens=2000, temperature=0.3,
            system="당신은 숙련된 시나리오 작가다. 유효한 단일 JSON만 출력. 후행 쉼표 금지.",
            messages=[{"role": "user", "content": user_prompt}]
        )
        txt = "".join(b.text for b in response.content if hasattr(b, "text")).strip()
        return safe_json_loads(txt)
    except Exception as e:
        st.error(f"줄글 시놉시스 생성 실패: {e}")
        return None


# ─── API Call: Scene Design (장면화) ───
def call_scene_design(core_data, story_data, diag_data, genre, fmt):
    """Scene Design: 핵심 장면 15~18개 설계 (Show, don't tell)"""
    try:
        client = get_client()
        gns = core_data.get("goal_need_strategy", {})
        lp = core_data.get("logline_pack", {})
        chars = core_data.get("characters", [])
        storyline = story_data.get("storyline", [])

        system_prompt = """당신은 헐리우드 최고 수준의 Scene Architect다.
Structure Build 결과를 기반으로 핵심 장면(Key Scene)을 설계한다.
'Show, don't tell' 원칙을 따른다.
모든 장면은 설명이 아닌 행동, 선택, 반전으로 드라마를 구현해야 한다.

중요 규칙:
- 유효한 단일 JSON만 출력. JSON 외 텍스트 금지.
- 후행 쉼표 금지. 문자열 줄바꿈 대신 공백.
- 한국어 작성. 전문용어 한글(English) 병기.
- 각 필드 1~2문장, 40자 이내.
"""

        chars_simple = json.dumps(
            [{"name": c.get("name",""), "role": c.get("role","")} for c in chars],
            ensure_ascii=False
        )
        storyline_json = json.dumps(storyline, ensure_ascii=False)

        user_prompt = f"""[Core]
로그라인: {lp.get("washed","")}
Goal: {gns.get("goal","")} / Need: {gns.get("need","")} / Strategy: {gns.get("strategy","")}
캐릭터: {chars_simple}

[Storyline]
{storyline_json}

[JSON 스키마]
{{
  "key_scenes": [
    {{
      "scene_no": 1,
      "sequence": "소속 시퀀스 라벨",
      "title": "장면 제목 (10자 이내)",
      "location": "장소",
      "characters": "등장 인물",
      "setup": "장면 시작 상황 1문장",
      "dramatic_action": "핵심 행동/선택/대결 1문장 — Show, don't tell",
      "turning_point": "반전 또는 전환 1문장 (없으면 빈 문자열)",
      "emotion_shift": "감정 변화 (시작감정 → 끝감정)",
      "visual_direction": "시각적 연출 방향 1문장",
      "stakes": "판돈 — 실패하면 잃는 것 1문장",
      "dramatic_irony": "관객은 알지만 인물은 모르는 것 1문장 (없으면 빈 문자열)",
      "key_line": "이 장면을 정의하는 핵심 대사 한 마디 (캐릭터명: 대사)",
      "connection": "다음 장면 연결 에너지 1문장"
    }}
  ],
  "scene_map_summary": {{
    "total_scenes": 0,
    "act1_scenes": "1막 장면 번호 목록",
    "act2a_scenes": "2막 전반 장면 번호 목록",
    "act2b_scenes": "2막 후반 장면 번호 목록",
    "act3_scenes": "3막 장면 번호 목록",
    "must_see_scenes": "반드시 살려야 할 핵심 3장면 번호"
  }}
}}

규칙:
- key_scenes는 15~18개
- dramatic_action이 핵심. 인물이 무엇을 '하는지'를 쓸 것
- turning_point 있는 장면과 없는 장면이 자연스럽게 섞일 것
- dramatic_irony는 해당 장면에 극적 아이러니가 있을 때만 작성. 없으면 빈 문자열
- key_line은 이 장면 전체를 압축하는 대사 한 마디. 반드시 '캐릭터명: 대사' 형식
- visual_direction은 촬영 감독 전달 수준으로
"""

        response = client.messages.create(
            model=ANTHROPIC_MODEL, max_tokens=6000, temperature=0.3,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        if response.stop_reason == "max_tokens":
            retry = user_prompt.replace("15~18개", "12~15개")
            response = client.messages.create(
                model=ANTHROPIC_MODEL, max_tokens=8000, temperature=0.3,
                system=system_prompt,
                messages=[{"role": "user", "content": retry}]
            )
        txt = "".join(b.text for b in response.content if hasattr(b, "text")).strip()
        st.session_state["last_scene_design_raw"] = txt
        return safe_json_loads(txt)
    except Exception as e:
        st.error(f"Scene Design 실패: {e}")
        raw = st.session_state.get("last_scene_design_raw", "")
        if raw:
            with st.expander("🔧 Scene Design Raw (디버그)"):
                st.text_area("Raw", raw, height=400)
        return None


# ─── API Call: Treatment Build ───
def call_treatment_build(core_data, story_data, diag_data, genre, fmt):
    """Treatment Build: 시퀀스별 트리트먼트 서술"""
    try:
        client = get_client()
        gns = core_data.get("goal_need_strategy", {})
        lp = core_data.get("logline_pack", {})
        chars = core_data.get("characters", [])
        syn = story_data.get("synopsis_1p", {})
        storyline = story_data.get("storyline", [])

        system_prompt = """당신은 헐리우드 최고 수준의 시나리오 작가이자 Treatment Specialist다.
Structure Build 결과를 기반으로 트리트먼트를 작성한다.
인물의 선택이 사건을 일으켜야 한다.
장면 전환의 에너지가 살아있어야 한다.
읽는 맛이 있어야 한다.

중요 규칙:
- 유효한 단일 JSON만 출력. JSON 외 텍스트 금지.
- 후행 쉼표 금지.
- 한국어 작성. 전문용어 한글(English) 병기.
- 서술체로 작성. 시나리오 형식이 아닌 트리트먼트 형식.
"""

        user_prompt = f"""[Core]
로그라인: {lp.get("washed","")}
Goal: {gns.get("goal","")} / Need: {gns.get("need","")} / Strategy: {gns.get("strategy","")}
캐릭터: {json.dumps([{"name":c.get("name",""),"role":c.get("role","")} for c in chars], ensure_ascii=False)}

[Synopsis]
{json.dumps(syn, ensure_ascii=False)}

[Storyline]
{json.dumps(storyline, ensure_ascii=False)}

[JSON 스키마]
{{
  "treatment_sequences": [
    {{
      "seq": 1,
      "title": "시퀀스 제목",
      "narrative": "이 시퀀스의 트리트먼트 서술 (150~200자)"
    }}
  ],
  "emotion_curve": [
    {{
      "point": "Opening",
      "tension": 3,
      "emotion": "감정 키워드"
    }}
  ],
  "director_notes": ["감독용 포인트 3개"],
  "investor_summary": "투자자용 요약 3문장"
}}

규칙:
- treatment_sequences는 스토리라인 시퀀스 수만큼 (6~8개)
- 각 narrative는 서술체, 현재형, 150~200자
- 인물의 선택 → 사건 → 감정 변화가 드러나야 함
- emotion_curve는 8~10개 포인트, tension은 1~10 정수
- director_notes 정확히 3개, 각 1문장
- investor_summary 3문장
"""

        response = client.messages.create(
            model=ANTHROPIC_MODEL, max_tokens=6000, temperature=0.35,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}]
        )
        if response.stop_reason == "max_tokens":
            response = client.messages.create(
                model=ANTHROPIC_MODEL, max_tokens=8000, temperature=0.35,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}]
            )
        txt = "".join(b.text for b in response.content if hasattr(b, "text")).strip()
        st.session_state["last_treatment_raw"] = txt
        return safe_json_loads(txt)
    except Exception as e:
        st.error(f"Treatment 생성 실패: {e}")
        raw = st.session_state.get("last_treatment_raw", "")
        if raw:
            with st.expander("🔧 Treatment Raw (디버그)"):
                st.text_area("Raw", raw, height=400)
        return None


# ─── API Call: Treatment Gate E ───
def call_treatment_gate(treatment_data):
    """Gate E: Treatment Gate 채점"""
    try:
        client = get_client()
        response = client.messages.create(
            model=ANTHROPIC_MODEL, max_tokens=1500, temperature=0.2,
            system="당신은 Development Producer다. 유효한 단일 JSON만 출력. 후행 쉼표 금지. 점수 0.0~10.0.",
            messages=[{"role": "user", "content": f"""[Treatment]
{json.dumps(treatment_data, ensure_ascii=False)}

[JSON 스키마]
{{
  "gate_e_treatment": {{
    "cinematic_reading": 0.0,
    "scene_emotion_match": 0.0,
    "screenplay_ready": 0.0,
    "average": 0.0,
    "feedback": "Gate E 종합 피드백 1문장"
  }}
}}
규칙: average = 3항목 평균."""}]
        )
        txt = "".join(b.text for b in response.content if hasattr(b, "text")).strip()
        return safe_json_loads(txt)
    except Exception as e:
        st.error(f"Gate E 실패: {e}")
        return None


# ─── DOCX 생성 ───
def generate_docx(project):
    """기획개발보고서 DOCX 생성"""
    from docx import Document
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    import io

    doc = Document()

    # 스타일 설정
    style = doc.styles['Normal']
    style.font.name = 'Pretendard'
    style.font.size = Pt(10)

    # ── Cover ──
    doc.add_paragraph("")
    doc.add_paragraph("")
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title_p.add_run("BLUE JEANS PICTURES")
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(0xFF, 0xCB, 0x05)

    title_p2 = doc.add_paragraph()
    title_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = title_p2.add_run(f"기획개발보고서")
    run2.font.size = Pt(24)
    run2.font.bold = True

    title_p3 = doc.add_paragraph()
    title_p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run3 = title_p3.add_run(project.get("title", ""))
    run3.font.size = Pt(18)
    run3.font.bold = True

    meta_p = doc.add_paragraph()
    meta_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    meta_p.add_run(f"{project.get('genre','')} · {project.get('target_market','')} · {project.get('format','')}")

    doc.add_page_break()

    # Helper
    def add_heading(text, level=1):
        doc.add_heading(text, level=level)

    def add_body(text):
        if text:
            doc.add_paragraph(text)

    def add_labeled(label, text):
        if text:
            p = doc.add_paragraph()
            run_l = p.add_run(f"[{label}] ")
            run_l.bold = True
            p.add_run(text)

    # ── Core Build ──
    core = project.get("core", {})
    if core:
        # Logline
        add_heading("Logline Pack", 1)
        lp = core.get("logline_pack", {})
        for label, key in [("Original","original"),("Washed","washed"),("투자자용","investor"),("감독용","director"),("캐릭터 훅","character_hook")]:
            add_labeled(label, lp.get(key, ""))

        # 기획의도
        add_heading("기획의도", 1)
        pi = core.get("project_intent", {})
        add_labeled("소재", pi.get("subject", ""))
        add_labeled("장르", pi.get("genre_approach", ""))
        add_labeled("시장", pi.get("market_rationale", ""))
        add_labeled("Pitch", pi.get("pitch", ""))
        add_labeled("Theme", pi.get("theme", ""))

        # G/N/S
        add_heading("Goal / Need / Strategy", 1)
        gns = core.get("goal_need_strategy", {})
        add_labeled("Goal", gns.get("goal", ""))
        add_labeled("Need", gns.get("need", ""))
        add_labeled("Strategy", gns.get("strategy", ""))
        add_labeled("Risk", gns.get("risk", ""))
        add_labeled("Ending Payoff", gns.get("ending_payoff", ""))

        # 세계관
        add_heading("세계관", 1)
        wb = core.get("world_build", {})
        for label, key in [("시간","time"),("공간","space"),("규칙","rules"),("금기","taboo"),("권력구조","power_structure")]:
            add_labeled(label, wb.get(key, ""))

        # 캐릭터
        add_heading("캐릭터", 1)
        role_labels = {"protagonist":"주인공","antagonist":"적대자","ally":"조력자","mirror":"거울"}
        for ch in core.get("characters", []):
            role = role_labels.get(ch.get("role",""), ch.get("role",""))
            add_heading(f"{role}: {ch.get('name','')}", 2)
            add_body(ch.get("description", ""))
            add_labeled("욕망", ch.get("goal", ""))
            add_labeled("결핍", ch.get("need", ch.get("flaw", "")))
            add_labeled("대사톤", ch.get("dialogue_tone", ""))

    doc.add_page_break()

    # ── Structure Build ──
    story = project.get("structure_story", {})
    diag = project.get("structure_diag", {})

    if story:
        add_heading("Synopsis 1P", 1)
        syn = story.get("synopsis_1p", {})
        for label, key in [("시작","opening"),("촉발사건","catalyst"),("전개","development"),("미드포인트","midpoint"),("붕괴","collapse"),("결전","climax"),("결말","ending")]:
            add_labeled(label, syn.get(key, ""))

        # 줄글 시놉시스
        prose = project.get("structure_prose", {})
        if prose and prose.get("prose"):
            add_heading("기승전결 시놉시스", 1)
            add_body(prose["prose"])

        add_heading("스토리라인", 1)
        for seq in story.get("storyline", []):
            add_heading(f"SEQ {seq.get('seq','')} · {seq.get('label','')}", 2)
            add_body(seq.get("summary", ""))

    if diag:
        add_heading("3막 구조 진단", 1)
        ta = diag.get("three_act", {})
        for label, key in [("1막 끝","act1_end"),("미드포인트","act2_midpoint"),("All Is Lost","act2_end"),("클라이맥스","act3_climax")]:
            add_labeled(label, ta.get(key, ""))

        add_heading("15-Beat Sheet", 1)
        for bt in diag.get("beat_sheet", []):
            add_labeled(bt.get("beat",""), f"[{bt.get('status','')}] {bt.get('note','')}")

    doc.add_page_break()

    # ── Scene Design ──
    scene_design = project.get("scene_design", {})
    if scene_design:
        add_heading("Scene Design (장면화)", 1)
        sms = scene_design.get("scene_map_summary", {})
        if sms.get("must_see_scenes"):
            add_labeled("Must-See 장면", sms["must_see_scenes"])

        for sc in scene_design.get("key_scenes", []):
            add_heading(f"S#{sc.get('scene_no','')} {sc.get('title','')}", 2)
            add_labeled("장소", sc.get("location", ""))
            add_labeled("인물", sc.get("characters", ""))
            add_labeled("상황", sc.get("setup", ""))
            add_labeled("행동(Show)", sc.get("dramatic_action", ""))
            tp = sc.get("turning_point", "")
            if tp:
                add_labeled("전환", tp)
            di = sc.get("dramatic_irony", "")
            if di:
                add_labeled("극적 아이러니", di)
            add_labeled("감정", sc.get("emotion_shift", ""))
            add_labeled("연출", sc.get("visual_direction", ""))
            add_labeled("판돈", sc.get("stakes", ""))
            kl = sc.get("key_line", "")
            if kl:
                add_labeled("핵심 대사", kl)

    doc.add_page_break()

    # ── Treatment ──
    treatment = project.get("treatment", {})
    if treatment:
        add_heading("Treatment", 1)
        for seq in treatment.get("treatment_sequences", []):
            add_heading(f"SEQ {seq.get('seq','')} · {seq.get('title','')}", 2)
            add_body(seq.get("narrative", ""))

        if treatment.get("investor_summary"):
            add_heading("투자자용 요약", 2)
            add_body(treatment["investor_summary"])

    # ── 점수 ──
    add_heading("Development Fit Score", 1)
    cg = project.get("core_gate", {})
    fa = cg.get("five_axis_scores", {})
    if fa:
        add_labeled("Final Score", str(fa.get("final_score", "")))
        add_labeled("Verdict", fa.get("verdict", ""))

    # Footer
    doc.add_paragraph("")
    footer = doc.add_paragraph()
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_f = footer.add_run("© 2026 BLUE JEANS PICTURES · Creator Engine v1.2")
    run_f.font.size = Pt(8)
    run_f.font.color.rgb = RGBColor(0x88, 0x88, 0x88)

    # Save to buffer
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer


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
if st.session_state.view in ("project", "core", "structure", "scene_design", "treatment") and st.session_state.cur:
    if st.session_state.view == "treatment":
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("← 프로젝트 목록"):
                st.session_state.view = "home"
                st.rerun()
        with col_nav2:
            if st.button("← Scene Design"):
                st.session_state.view = "scene_design"
                st.rerun()
    elif st.session_state.view == "scene_design":
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("← 프로젝트 목록"):
                st.session_state.view = "home"
                st.rerun()
        with col_nav2:
            if st.button("← Structure"):
                st.session_state.view = "structure"
                st.rerun()
    elif st.session_state.view == "structure":
        col_nav1, col_nav2 = st.columns(2)
        with col_nav1:
            if st.button("← 프로젝트 목록"):
                st.session_state.view = "home"
                st.rerun()
        with col_nav2:
            if st.button("← Core Build"):
                st.session_state.view = "core"
                st.rerun()
    elif st.session_state.view == "core":
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
                "core": None,
                "core_gate": None,
                "structure_story": None,
                "structure_diag": None,
                "structure_gate": None,
                "structure_prose": None,
                "scene_design": None,
                "treatment": None,
                "treatment_gate": None,
                "final_score": None,
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

        # ── 분석 없을 때 fallback 네비게이션 ──
        if not ba:
            st.markdown("---")
            st.warning("⚠️ 시장 분석 + Gate A 채점이 아직 완료되지 않았습니다.")

            col_fb1, col_fb2 = st.columns(2)
            with col_fb1:
                if st.button("🔄 분석 재시도", use_container_width=True):
                    # 2단계만 재실행
                    cards_map = {c["id"]: c for c in bc.get("idea_cards", [])}
                    top3_data = [
                        cards_map[t["card_id"]]
                        for t in bc.get("top3", [])
                        if t["card_id"] in cards_map
                    ]
                    if top3_data:
                        with st.spinner("② 시장 분석 + Gate A 채점 중..."):
                            ar = call_brainstorm_analysis(
                                project["idea_text"],
                                project["genre"],
                                project["target_market"],
                                project["format"],
                                top3_data,
                                project.get("research")
                            )
                        if ar:
                            project["brainstorm_analysis"] = ar
                            project["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                            st.rerun()
            with col_fb2:
                if st.button("🎯 분석 건너뛰고 Core Build →", use_container_width=True):
                    project["stage"] = "core"
                    st.session_state.view = "core"
                    st.rerun()

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

    st.markdown(f"## {project['title']}")
    st.caption(f"{project['genre']} · {project['target_market']} · {project['format']}")

    # ─── 단계 표시 ───
    render_stepper("core", project)

    # Brainstorm에서 인계받은 정보 표시
    selected_concept = None
    if bc:
        cards_map = {c["id"]: c for c in bc.get("idea_cards", [])}
        top3 = bc.get("top3", [])
        if top3:
            selected_concept = cards_map.get(top3[0].get("card_id"), {})
            if selected_concept:
                st.markdown(
                    f'<div class="callout">'
                    f'<div class="cl">🏆 선정 컨셉: {selected_concept.get("title", "")}</div>'
                    f'{selected_concept.get("logline_seed", "")}'
                    f'</div>',
                    unsafe_allow_html=True
                )

    if ba:
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
        if not selected_concept:
            st.error("선정된 컨셉이 없습니다. Brainstorm을 먼저 실행해주세요.")
        else:
            with st.spinner("① Core Build 생성 중... (약 30~40초)"):
                core_result = call_core_build_main(
                    project["idea_text"], project["genre"],
                    project["target_market"], project["format"],
                    selected_concept, project.get("research")
                )
            if core_result:
                project["core"] = core_result
                project["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                with st.spinner("② Gate B + Gate C 채점 중... (약 10~20초)"):
                    gate_result = call_core_gate(core_result)
                if gate_result:
                    project["core_gate"] = gate_result
                    project["final_score"] = gate_result.get("five_axis_scores", {}).get("final_score")
                    project["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.rerun()

    # ── Core Build 결과 표시 ──
    if project.get("core"):
        core = project["core"]

        # Logline Pack
        st.markdown("#### 📝 Logline Pack")
        lp = core.get("logline_pack", {})
        for label, key in [("Original", "original"), ("Washed", "washed"),
                           ("투자자용", "investor"), ("감독용", "director"),
                           ("캐릭터 훅", "character_hook")]:
            val = lp.get(key, "")
            if val:
                st.markdown(f'<div class="callout"><div class="cl">{label}</div>{val}</div>', unsafe_allow_html=True)

        # Goal / Need / Strategy
        st.markdown("#### 🎯 Goal / Need / Strategy")
        gns = core.get("goal_need_strategy", {})
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="callout"><div class="cl">GOAL</div>{gns.get("goal","")}</div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="callout"><div class="cl">NEED</div>{gns.get("need","")}</div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="callout"><div class="cl">STRATEGY</div>{gns.get("strategy","")}</div>', unsafe_allow_html=True)
        cr, ce = st.columns(2)
        cr.markdown(f'<div class="callout" style="border-left-color:var(--r)"><div class="cl" style="color:var(--r)">RISK</div>{gns.get("risk","")}</div>', unsafe_allow_html=True)
        ce.markdown(f'<div class="callout" style="border-left-color:var(--g)"><div class="cl" style="color:var(--g)">ENDING PAYOFF</div>{gns.get("ending_payoff","")}</div>', unsafe_allow_html=True)

        # Project Intent (소재 · 장르 · 시장분석)
        st.markdown("#### 📋 기획의도 — 왜 이 작품을 기획하는가")
        pi = core.get("project_intent", {})

        if pi.get("subject"):
            st.markdown(f'<div class="callout"><div class="cl">소재 — 왜 이 소재인가</div>{pi["subject"]}</div>', unsafe_allow_html=True)

        if pi.get("genre_approach"):
            st.markdown(f'<div class="callout"><div class="cl">장르 — 왜 이 장르인가</div>{pi["genre_approach"]}</div>', unsafe_allow_html=True)

        if pi.get("market_rationale"):
            st.markdown(f'<div class="callout"><div class="cl">시장 — 왜 지금 이 시장인가</div>{pi["market_rationale"]}</div>', unsafe_allow_html=True)

        cp1, cp2 = st.columns(2)
        if pi.get("pitch"):
            cp1.markdown(f'<div class="callout"><div class="cl">Elevator Pitch</div>{pi["pitch"]}</div>', unsafe_allow_html=True)
        if pi.get("theme"):
            cp2.markdown(f'<div class="callout"><div class="cl">Theme</div>{pi["theme"]}</div>', unsafe_allow_html=True)
        if pi.get("tone_manner"):
            st.markdown(f"**Tone & Manner:** {', '.join(pi['tone_manner'])}")

        # World Build
        st.markdown("#### 🌍 세계관")
        wb = core.get("world_build", {})
        cw1, cw2 = st.columns(2)
        with cw1:
            for label, key in [("시간","time"),("공간","space"),("규칙","rules"),("금기","taboo"),("권력구조","power_structure")]:
                val = wb.get(key, "")
                if val:
                    st.markdown(f"**{label}:** {val}")
        with cw2:
            if wb.get("visual_keywords"):
                st.markdown(f"**시각 키워드:** {', '.join(wb['visual_keywords'])}")
            if wb.get("conflict_points"):
                st.markdown("**충돌 포인트:**")
                for cp in wb["conflict_points"]:
                    st.markdown(f"- {cp}")

        # Characters
        st.markdown("#### 🎭 캐릭터")
        role_labels = {"protagonist":"주인공","antagonist":"적대자","ally":"조력자","mirror":"거울 캐릭터"}
        for ch in core.get("characters", []):
            role = role_labels.get(ch.get("role",""), ch.get("role",""))
            st.markdown(
                f'<div class="card"><div class="cl">{role}: {ch.get("name","")}</div>'
                f'{ch.get("description","")}<br>'
                f'<span style="font-size:.8rem;color:#999">'
                f'🎯 {ch.get("goal","")}<br>💔 {ch.get("need",ch.get("flaw",""))}<br>'
                f'⚡ {ch.get("strategy","")}<br>🗣️ {ch.get("dialogue_tone","")}</span></div>',
                unsafe_allow_html=True
            )

        # Relationship
        rel = core.get("relationship_map", [])
        if rel:
            st.markdown("#### 🔗 관계도")
            for r in rel:
                st.markdown(f"- {r}")

        st.markdown("---")

        # Gate B + C
        if project.get("core_gate"):
            cg = project["core_gate"]
            gb = cg.get("gate_b_drive", {})
            gc = cg.get("gate_c_character", {})
            fa = cg.get("five_axis_scores", {})

            st.markdown("#### 🚪 Gate B: Drive Gate")
            c1, c2 = st.columns([1, 2])
            with c1:
                gb_avg = gb.get("average", 0)
                cl = "var(--g)" if gb_avg >= 7.0 else "var(--r)"
                lb = "PASS" if gb_avg >= 7.0 else "FAIL"
                st.markdown(f'<div style="text-align:center"><div class="big" style="color:{cl}">{gb_avg}</div><div class="sm" style="color:{cl};font-size:1rem;font-weight:700">{lb}</div></div>', unsafe_allow_html=True)
            with c2:
                for nm, sc in [("Goal 선명도",gb.get("goal_clarity",0)),("Need 자연스러움",gb.get("need_from_loss",0)),("Strategy 창의성",gb.get("strategy_creative",0)),("실패 대가",gb.get("failure_cost",0))]:
                    st.markdown(f'<div style="display:flex;align-items:center;margin:.2rem 0;font-size:.8rem"><div style="width:110px;color:var(--dim)">{nm}</div><div style="flex:1;background:#3a3a4a;border-radius:4px;height:8px;margin:0 .5rem"><div style="width:{sc*10}%;background:var(--y);height:100%;border-radius:4px"></div></div><div style="width:30px;text-align:right">{sc}</div></div>', unsafe_allow_html=True)
            if gb.get("feedback"):
                st.caption(gb["feedback"])

            st.markdown("#### 🚪 Gate C: Character Gate")
            c1, c2 = st.columns([1, 2])
            with c1:
                gc_avg = gc.get("average", 0)
                cl = "var(--g)" if gc_avg >= 7.0 else "var(--r)"
                lb = "PASS" if gc_avg >= 7.0 else "FAIL"
                st.markdown(f'<div style="text-align:center"><div class="big" style="color:{cl}">{gc_avg}</div><div class="sm" style="color:{cl};font-size:1rem;font-weight:700">{lb}</div></div>', unsafe_allow_html=True)
            with c2:
                for nm, sc in [("주인공/적대자 논리",gc.get("protagonist_antagonist_logic",0)),("조연 입체성",gc.get("supporting_not_functional",0)),("관계축 갈등",gc.get("relationship_produces_conflict",0))]:
                    st.markdown(f'<div style="display:flex;align-items:center;margin:.2rem 0;font-size:.8rem"><div style="width:110px;color:var(--dim)">{nm}</div><div style="flex:1;background:#3a3a4a;border-radius:4px;height:8px;margin:0 .5rem"><div style="width:{sc*10}%;background:var(--y);height:100%;border-radius:4px"></div></div><div style="width:30px;text-align:right">{sc}</div></div>', unsafe_allow_html=True)
            if gc.get("feedback"):
                st.caption(gc["feedback"])

            # 5축 스코어
            st.markdown("---")
            st.markdown("#### 📊 Development Fit Score")
            final = fa.get("final_score", 0)
            verdict = fa.get("verdict", "")
            vc = {"개발 진행":"var(--g)","개발 보류":"var(--y)","구조 재설계":"var(--r)"}.get(verdict,"var(--dim)")
            c1, c2 = st.columns([1, 2])
            with c1:
                st.markdown(f'<div style="text-align:center"><div class="big">{final}</div><div class="sm" style="color:{vc};font-size:1rem;font-weight:700">{verdict}</div></div>', unsafe_allow_html=True)
            with c2:
                for nm, sc in [("Goal",fa.get("goal",0)),("Need",fa.get("need",0)),("Strategy",fa.get("strategy",0)),("Structure",fa.get("structure",0)),("Character/Concept",fa.get("character_concept",0))]:
                    st.markdown(f'<div style="display:flex;align-items:center;margin:.2rem 0;font-size:.8rem"><div style="width:110px;color:var(--dim)">{nm}</div><div style="flex:1;background:#3a3a4a;border-radius:4px;height:8px;margin:0 .5rem"><div style="width:{sc*10}%;background:var(--y);height:100%;border-radius:4px"></div></div><div style="width:30px;text-align:right">{sc}</div></div>', unsafe_allow_html=True)

            if verdict == "개발 진행":
                st.success(f"✅ {verdict}. Structure Build로 진행할 수 있습니다.")
                if st.button("🏗️ Structure Build 진행 →", type="primary", use_container_width=True):
                    st.session_state.view = "structure"
                    st.rerun()
            elif verdict == "개발 보류":
                st.warning(f"⚠️ {verdict}. Core Build 보강 필요.")
                col_cv1, col_cv2 = st.columns(2)
                with col_cv1:
                    if st.button("🔓 Override → Structure Build"):
                        st.session_state.view = "structure"
                        st.rerun()
                with col_cv2:
                    if st.button("🔄 Core Build 재실행"):
                        project["core"] = None
                        project["core_gate"] = None
                        st.rerun()
            else:
                st.error(f"🔴 {verdict}. Brainstorm 재검토 필요.")

        else:
            st.warning("⚠️ Gate B + C 채점이 완료되지 않았습니다.")
            if st.button("🔄 Gate 재시도"):
                with st.spinner("Gate B + C 채점 중..."):
                    gate_result = call_core_gate(core)
                if gate_result:
                    project["core_gate"] = gate_result
                    project["final_score"] = gate_result.get("five_axis_scores", {}).get("final_score")
                    st.rerun()

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


# ═══════════════════════════════════════════════════
#  STRUCTURE BUILD
# ═══════════════════════════════════════════════════
elif st.session_state.view == "structure" and st.session_state.cur:

    project = st.session_state.projects[st.session_state.cur]
    core = project.get("core", {})

    st.markdown(f"## {project['title']}")
    st.caption(f"{project['genre']} · {project['target_market']} · {project['format']}")
    render_stepper("structure", project)

    gns = core.get("goal_need_strategy", {})
    lp = core.get("logline_pack", {})
    if lp.get("washed"):
        st.markdown(f'<div class="callout"><div class="cl">Logline</div>{lp["washed"]}</div>', unsafe_allow_html=True)
    if gns:
        c1, c2, c3 = st.columns(3)
        c1.markdown(f'<div class="callout"><div class="cl">GOAL</div>{gns.get("goal","")}</div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="callout"><div class="cl">NEED</div>{gns.get("need","")}</div>', unsafe_allow_html=True)
        c3.markdown(f'<div class="callout"><div class="cl">STRATEGY</div>{gns.get("strategy","")}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏗️ Structure Build 실행")
    st.caption("시놉시스 · 스토리라인 · 3막 구조 · 15비트 · 캐릭터 변화표를 설계합니다.")

    if st.button("🏗️ Structure Build 실행", type="primary"):
        if not core:
            st.error("Core Build가 없습니다.")
        else:
            with st.spinner("① 시놉시스 + 스토리라인... (20~30초)"):
                story = call_structure_story(core, project["genre"], project["target_market"], project["format"])
            if story:
                project["structure_story"] = story
                with st.spinner("② 구조 진단 + 캐릭터 변화표... (20~30초)"):
                    diag = call_structure_diagnosis(core, story, project["genre"], project["format"])
                if diag:
                    project["structure_diag"] = diag
                    with st.spinner("③ Gate D 채점... (10초)"):
                        gate_d = call_structure_gate(story, diag)
                    if gate_d:
                        project["structure_gate"] = gate_d
                with st.spinner("④ 기승전결 줄글 시놉시스... (10~15초)"):
                    prose = call_structure_prose(core, story)
                if prose:
                    project["structure_prose"] = prose
                project["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.rerun()

    if project.get("structure_story"):
        story = project["structure_story"]
        st.markdown("#### 📖 Synopsis 1P")
        syn = story.get("synopsis_1p", {})
        for label, key in [("시작","opening"),("촉발사건","catalyst"),("전개","development"),("미드포인트","midpoint"),("붕괴","collapse"),("결전","climax"),("결말","ending")]:
            val = syn.get(key, "")
            if val:
                st.markdown(f'<div class="callout"><div class="cl">{label}</div>{val}</div>', unsafe_allow_html=True)

        st.markdown("#### 📊 스토리라인 (시퀀스 방향)")
        for seq in story.get("storyline", []):
            st.markdown(f'<div class="card"><div class="cl">SEQ {seq.get("seq","")} · {seq.get("label","")} ({seq.get("pages","")})</div>{seq.get("summary","")}<br><span style="font-size:.8rem;color:#999">⚔️ {seq.get("conflict","")} · 💭 {seq.get("emotion","")} · → {seq.get("hook","")}</span></div>', unsafe_allow_html=True)

    if project.get("structure_diag"):
        diag = project["structure_diag"]
        st.markdown("#### 🎬 3막 구조 진단")
        ta = diag.get("three_act", {})
        for label, key in [("1막 끝","act1_end"),("미드포인트","act2_midpoint"),("All Is Lost","act2_end"),("클라이맥스","act3_climax")]:
            val = ta.get(key, "")
            if val:
                st.markdown(f'<div class="callout"><div class="cl">{label}</div>{val}</div>', unsafe_allow_html=True)
        if ta.get("diagnosis"):
            st.caption(f"진단: {ta['diagnosis']}")

        st.markdown("#### 🥁 15-Beat Sheet")
        for bt in diag.get("beat_sheet", []):
            status = bt.get("status", "")
            color = {"있음":"var(--g)","약함":"var(--y)","없음":"var(--r)"}.get(status, "var(--dim)")
            st.markdown(
                f'<div style="margin:.3rem 0;font-size:.85rem">'
                f'<span style="color:{color};font-weight:700">[{status}]</span> '
                f'<b>{bt.get("beat","")}</b> — '
                f'<span style="color:#bbb">{bt.get("note","")}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

        # 캐릭터 변화표
        arcs = diag.get("character_arcs", [])
        if arcs:
            st.markdown("#### 🎭 캐릭터 변화표")
            role_labels = {"protagonist":"주인공","antagonist":"적대자","ally":"조력자","mirror":"거울"}
            for arc in arcs:
                role = role_labels.get(arc.get("role",""), arc.get("role",""))
                arc_type = arc.get("arc_type", "")
                st.markdown(
                    f'<div class="card">'
                    f'<div class="cl">{role}: {arc.get("name","")} [{arc_type}]</div>'
                    f'<span style="font-size:.8rem;color:#999">'
                    f'1막: {arc.get("act1_state","")}<br>'
                    f'전환: {arc.get("turning_point","")}<br>'
                    f'3막: {arc.get("act3_state","")}'
                    f'</span></div>',
                    unsafe_allow_html=True
                )

        # 관계 변화표
        rels = diag.get("relationship_changes", [])
        if rels:
            st.markdown("#### 🔗 관계 변화표")
            for rel in rels:
                st.markdown(
                    f'<div class="card">'
                    f'<div class="cl">{rel.get("pair","")}</div>'
                    f'<span style="font-size:.8rem;color:#999">'
                    f'1막: {rel.get("act1","")} → '
                    f'미드: {rel.get("midpoint","")} → '
                    f'3막: {rel.get("act3","")}'
                    f'</span></div>',
                    unsafe_allow_html=True
                )

    # 기승전결 줄글 시놉시스
    if project.get("structure_prose"):
        prose_data = project["structure_prose"]
        if prose_data.get("prose"):
            st.markdown("#### 📝 기승전결 시놉시스 (1P 줄글)")
            st.markdown(f'<div class="callout" style="line-height:1.8;font-size:.9rem">{prose_data["prose"]}</div>', unsafe_allow_html=True)

    if project.get("structure_gate"):
        sg = project["structure_gate"]
        gd = sg.get("gate_d_structure", {})
        gd_avg = gd.get("average", 0)
        gd_ok = gd_avg >= 7.0
        st.markdown("---")
        st.markdown("#### 🚪 Gate D: Structure Gate")
        c1, c2 = st.columns([1, 2])
        with c1:
            cl = "var(--g)" if gd_ok else "var(--r)"
            st.markdown(f'<div style="text-align:center"><div class="big" style="color:{cl}">{gd_avg}</div><div class="sm" style="color:{cl};font-size:1rem;font-weight:700">{"PASS" if gd_ok else "FAIL"}</div></div>', unsafe_allow_html=True)
        with c2:
            for nm, sc in [("전환점",gd.get("turning_points_valid",0)),("Midpoint",gd.get("midpoint_redirects",0)),("All Is Lost",gd.get("all_is_lost_works",0)),("결말",gd.get("ending_inevitable_surprising",0))]:
                st.markdown(f'<div style="display:flex;align-items:center;margin:.2rem 0;font-size:.8rem"><div style="width:80px;color:var(--dim)">{nm}</div><div style="flex:1;background:#3a3a4a;border-radius:4px;height:8px;margin:0 .5rem"><div style="width:{sc*10}%;background:var(--y);height:100%;border-radius:4px"></div></div><div style="width:30px;text-align:right">{sc}</div></div>', unsafe_allow_html=True)
        if gd.get("feedback"):
            st.caption(gd["feedback"])

        if gd_ok:
            st.success("✅ Gate D 통과. Scene Design 진행 가능.")
            if st.button("🎬 Scene Design 진행 →", type="primary", use_container_width=True):
                st.session_state.view = "scene_design"
                st.rerun()
        else:
            st.warning(f"⚠️ Gate D 미통과 (평균 {gd_avg}).")
            col_sd1, col_sd2 = st.columns(2)
            with col_sd1:
                if st.button("🔓 Override → Scene Design"):
                    st.session_state.view = "scene_design"
                    st.rerun()
            with col_sd2:
                if st.button("🔄 Structure 재실행"):
                    for k in ["structure_story","structure_diag","structure_gate","structure_prose"]:
                        project[k] = None
                    st.rerun()

        # DOCX 다운로드 (Structure 완료 시점부터 가능)
        st.markdown("---")
        st.markdown("#### 📥 기획개발보고서 다운로드")
        st.caption("현재까지 완성된 내용으로 DOCX 보고서를 생성합니다.")
        title_safe = project.get("title", "프로젝트").replace(" ", "_")
        docx_buffer = generate_docx(project)
        st.download_button(
            label="📥 기획개발보고서 다운로드 (.docx)",
            data=docx_buffer,
            file_name=f"기획개발보고서_{title_safe}_Blue.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    elif not project.get("structure_story"):
        st.markdown('<div style="text-align:center;padding:3rem 0;color:var(--dim)">🏗️ Structure Build를 실행하면 여기에 결과가 표시됩니다.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("© 2026 BLUE JEANS PICTURES · Creator Engine v1.2")


# ═══════════════════════════════════════════════════
#  SCENE DESIGN (장면화)
# ═══════════════════════════════════════════════════
elif st.session_state.view == "scene_design" and st.session_state.cur:

    project = st.session_state.projects[st.session_state.cur]
    core = project.get("core", {})
    story = project.get("structure_story", {})
    diag = project.get("structure_diag", {})

    st.markdown(f"## {project['title']}")
    st.caption(f"{project['genre']} · {project['target_market']} · {project['format']}")
    render_stepper("scene_design", project)

    gns = core.get("goal_need_strategy", {})
    lp = core.get("logline_pack", {})
    if lp.get("washed"):
        st.markdown(f'<div class="callout"><div class="cl">Logline</div>{lp["washed"]}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🎬 Scene Design (장면화)")
    st.caption("Show, don't tell — 핵심 장면의 극적 행동 · 반전 · 시각 연출을 설계합니다.")

    if st.button("🎬 Scene Design 실행", type="primary"):
        if not story:
            st.error("Structure Build가 없습니다.")
        else:
            with st.spinner("핵심 장면 설계 중... (약 30~40초)"):
                sd = call_scene_design(core, story, diag, project["genre"], project["format"])
            if sd:
                project["scene_design"] = sd
                project["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.rerun()

    # ── Scene Design 결과 표시 ──
    if project.get("scene_design"):
        sd = project["scene_design"]
        scenes = sd.get("key_scenes", [])
        sms = sd.get("scene_map_summary", {})

        # 장면 맵 요약
        if sms:
            st.markdown("#### 🗺️ Scene Map")
            c1, c2, c3, c4 = st.columns(4)
            c1.markdown(f'<div class="callout"><div class="cl">1막</div>{sms.get("act1_scenes","")}</div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="callout"><div class="cl">2막 전반</div>{sms.get("act2a_scenes","")}</div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="callout"><div class="cl">2막 후반</div>{sms.get("act2b_scenes","")}</div>', unsafe_allow_html=True)
            c4.markdown(f'<div class="callout"><div class="cl">3막</div>{sms.get("act3_scenes","")}</div>', unsafe_allow_html=True)

            if sms.get("must_see_scenes"):
                st.markdown(f'<div class="callout" style="border-left-color:var(--y)"><div class="cl">⭐ Must-See 장면</div>{sms["must_see_scenes"]}</div>', unsafe_allow_html=True)

        # 핵심 장면 카드
        st.markdown(f"#### 🎬 핵심 장면 ({len(scenes)}개)")
        for sc in scenes:
            tp = sc.get("turning_point", "")
            tp_html = f'<br>🔄 <b>전환:</b> {tp}' if tp else ""
            di = sc.get("dramatic_irony", "")
            di_html = f'<br>👁️ <b>아이러니:</b> <i>{di}</i>' if di else ""
            kl = sc.get("key_line", "")
            kl_html = f'<br><span style="color:var(--y);font-weight:600">💬 "{kl}"</span>' if kl else ""
            st.markdown(
                f'<div class="card">'
                f'<div class="cl">S#{sc.get("scene_no","")} · {sc.get("sequence","")} · {sc.get("location","")}</div>'
                f'<b>{sc.get("title","")}</b> — {sc.get("characters","")}<br>'
                f'<span style="font-size:.85rem">'
                f'📍 {sc.get("setup","")}<br>'
                f'🎭 <b>행동:</b> {sc.get("dramatic_action","")}'
                f'{tp_html}'
                f'{di_html}<br>'
                f'💭 {sc.get("emotion_shift","")}<br>'
                f'🎥 {sc.get("visual_direction","")}<br>'
                f'⚡ 판돈: {sc.get("stakes","")}'
                f'{kl_html}<br>'
                f'→ {sc.get("connection","")}'
                f'</span></div>',
                unsafe_allow_html=True
            )

        st.markdown("---")

        # Treatment 진행
        st.success("✅ Scene Design 완료. Treatment Build 진행 가능.")
        if st.button("📝 Treatment Build 진행 →", type="primary", use_container_width=True):
            st.session_state.view = "treatment"
            st.rerun()

        # DOCX 다운로드
        st.markdown("---")
        st.markdown("#### 📥 기획개발보고서 다운로드")
        title_safe = project.get("title", "프로젝트").replace(" ", "_")
        docx_buffer = generate_docx(project)
        st.download_button(
            label="📥 기획개발보고서 다운로드 (.docx)",
            data=docx_buffer,
            file_name=f"기획개발보고서_{title_safe}_Blue.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    else:
        st.markdown(
            '<div style="text-align:center;padding:3rem 0;color:var(--dim)">'
            '🎬 Scene Design을 실행하면 여기에 핵심 장면이 표시됩니다.<br>'
            'Show, don\'t tell — 행동 · 반전 · 시각 연출'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.caption("© 2026 BLUE JEANS PICTURES · Creator Engine v1.2")


# ═══════════════════════════════════════════════════
#  TREATMENT BUILD
# ═══════════════════════════════════════════════════
elif st.session_state.view == "treatment" and st.session_state.cur:

    project = st.session_state.projects[st.session_state.cur]
    core = project.get("core", {})
    story = project.get("structure_story", {})
    diag = project.get("structure_diag", {})

    st.markdown(f"## {project['title']}")
    st.caption(f"{project['genre']} · {project['target_market']} · {project['format']}")
    render_stepper("treatment", project)

    # 요약 정보
    gns = core.get("goal_need_strategy", {})
    lp = core.get("logline_pack", {})
    if lp.get("washed"):
        st.markdown(f'<div class="callout"><div class="cl">Logline</div>{lp["washed"]}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📝 Treatment Build 실행")
    st.caption("시퀀스별 트리트먼트 서술 · 감정 곡선 · 감독용 포인트 · 투자자 요약")

    if st.button("📝 Treatment Build 실행", type="primary"):
        if not story:
            st.error("Structure Build가 없습니다.")
        else:
            with st.spinner("① Treatment 생성 중... (약 30~40초)"):
                treat = call_treatment_build(core, story, diag, project["genre"], project["format"])
            if treat:
                project["treatment"] = treat
                project["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                with st.spinner("② Gate E 채점 중... (약 10초)"):
                    gate_e = call_treatment_gate(treat)
                if gate_e:
                    project["treatment_gate"] = gate_e
                    project["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")
                st.rerun()

    # ── Treatment 결과 표시 ──
    if project.get("treatment"):
        treat = project["treatment"]

        # 시퀀스별 트리트먼트
        st.markdown("#### 📖 Treatment")
        for seq in treat.get("treatment_sequences", []):
            st.markdown(
                f'<div class="card">'
                f'<div class="cl">SEQ {seq.get("seq","")} · {seq.get("title","")}</div>'
                f'<div style="line-height:1.7;font-size:.9rem">{seq.get("narrative","")}</div>'
                f'</div>',
                unsafe_allow_html=True
            )

        # 감정 곡선
        ec = treat.get("emotion_curve", [])
        if ec:
            st.markdown("#### 📈 감정 곡선")
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[p.get("point","") for p in ec],
                y=[p.get("tension",0) for p in ec],
                mode='lines+markers',
                line=dict(color='#FFCB05', width=3),
                marker=dict(size=8),
                text=[p.get("emotion","") for p in ec],
                hovertemplate='%{x}<br>텐션: %{y}<br>감정: %{text}<extra></extra>'
            ))
            fig.update_layout(
                plot_bgcolor='#0E1117', paper_bgcolor='#0E1117',
                font_color='#FAFAFA', yaxis_range=[0,10],
                yaxis_title="Tension", height=300,
                margin=dict(l=40,r=20,t=20,b=40)
            )
            st.plotly_chart(fig, use_container_width=True)

        # 감독용 포인트
        notes = treat.get("director_notes", [])
        if notes:
            st.markdown("#### 🎬 감독용 포인트")
            for i, n in enumerate(notes, 1):
                st.markdown(f"**{i}.** {n}")

        # 투자자 요약
        inv = treat.get("investor_summary", "")
        if inv:
            st.markdown(f'<div class="callout"><div class="cl">💰 투자자용 요약</div>{inv}</div>', unsafe_allow_html=True)

        st.markdown("---")

        # Gate E
        if project.get("treatment_gate"):
            tg = project["treatment_gate"]
            ge = tg.get("gate_e_treatment", {})
            ge_avg = ge.get("average", 0)
            ge_ok = ge_avg >= 7.0

            st.markdown("#### 🚪 Gate E: Treatment Gate")
            c1, c2 = st.columns([1, 2])
            with c1:
                cl = "var(--g)" if ge_ok else "var(--r)"
                st.markdown(f'<div style="text-align:center"><div class="big" style="color:{cl}">{ge_avg}</div><div class="sm" style="color:{cl};font-size:1rem;font-weight:700">{"PASS" if ge_ok else "FAIL"}</div></div>', unsafe_allow_html=True)
            with c2:
                for nm, sc in [("영화적 읽힘",ge.get("cinematic_reading",0)),("씬-감정 일치",ge.get("scene_emotion_match",0)),("초고 직행 가능",ge.get("screenplay_ready",0))]:
                    st.markdown(f'<div style="display:flex;align-items:center;margin:.2rem 0;font-size:.8rem"><div style="width:100px;color:var(--dim)">{nm}</div><div style="flex:1;background:#3a3a4a;border-radius:4px;height:8px;margin:0 .5rem"><div style="width:{sc*10}%;background:var(--y);height:100%;border-radius:4px"></div></div><div style="width:30px;text-align:right">{sc}</div></div>', unsafe_allow_html=True)
            if ge.get("feedback"):
                st.caption(ge["feedback"])

            if ge_ok:
                st.success("✅ Gate E 통과. 기획개발 완료. Screenplay Writer Engine 연동 준비 완료.")
            else:
                st.warning(f"⚠️ Gate E 미통과 (평균 {ge_avg}). Treatment 보강 필요.")
                if st.button("🔄 Treatment 재실행"):
                    project["treatment"] = None
                    project["treatment_gate"] = None
                    st.rerun()

        # DOCX 다운로드 (전체 결과 포함)
        st.markdown("---")
        st.markdown("#### 📥 기획개발보고서 최종 다운로드")
        title_safe = project.get("title", "프로젝트").replace(" ", "_")
        docx_buffer = generate_docx(project)
        st.download_button(
            label="📥 기획개발보고서_최종 다운로드 (.docx)",
            data=docx_buffer,
            file_name=f"기획개발보고서_{title_safe}_Blue.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

    else:
        st.markdown(
            '<div style="text-align:center;padding:3rem 0;color:var(--dim)">'
            '📝 Treatment Build를 실행하면 여기에 결과가 표시됩니다.'
            '</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.caption("© 2026 BLUE JEANS PICTURES · Creator Engine v1.2")
