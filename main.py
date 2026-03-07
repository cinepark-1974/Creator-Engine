"""
👖 BLUE JEANS Creative Development Engine v1.2
아이디어 → 기획개발 패키지
"""

import streamlit as st
import json
from datetime import datetime
import anthropic

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
:root{--y:#FFCB05;--bg:#0E1117;--card:#262730;--t:#FAFAFA;--r:#FF6B6B;--g:#51CF66;--dim:#8B8B8B}
html,body,[class*="css"]{font-family:'Pretendard',sans-serif}
.mt{font-size:1.6rem;font-weight:700;color:var(--y);margin-bottom:.2rem}
.st{font-size:.85rem;color:var(--dim);margin-bottom:2rem}
.callout{background:var(--card);border-left:3px solid var(--y);padding:.8rem 1rem;margin:.5rem 0;border-radius:0 6px 6px 0;font-size:.85rem}
.ct{color:var(--y);font-weight:600;font-size:.75rem;margin-bottom:.3rem}
.sb{font-size:2.5rem;font-weight:700;color:var(--y);text-align:center}
.sl{font-size:.7rem;color:var(--dim);text-align:center}
.cc{background:var(--card);border:1px solid #3a3a4a;border-radius:8px;padding:1rem;margin-bottom:.8rem}
.cc:hover{border-color:var(--y)}
.ri{background:var(--card);border-radius:6px;padding:.8rem;margin-bottom:.5rem;font-size:.85rem}
.rl{color:var(--y);font-weight:600;font-size:.7rem}
section[data-testid="stSidebar"]{background:#1a1a2e}
.badge{display:inline-block;padding:.15rem .5rem;border-radius:4px;font-size:.7rem;font-weight:600}
.b-done{background:var(--g);color:#000}.b-run{background:var(--y);color:#000}
.b-not{background:#3a3a4a;color:var(--dim)}.b-fail{background:var(--r);color:#000}
</style>
""", unsafe_allow_html=True)

# ─── Session State ───
for k, v in {"page":"home","projects":{},"cur":None,"tab":"brainstorm"}.items():
    if k not in st.session_state:
        st.session_state[k] = v

def badge(s):
    m={"DONE":"b-done","RUNNING":"b-run","NOT_RUN":"b-not","FAILED":"b-fail"}
    return f'<span class="badge {m.get(s,"b-not")}">{s.replace("_"," ")}</span>'

# ─── API Calls ───
def get_client():
    import anthropic
    return anthropic.Anthropic(
        api_key=st.secrets["ANTHROPIC_API_KEY"]
    )

def call_research(idea, genre, market):
    try:
        client = get_client()
        sys = """당신은 콘텐츠 기획 리서처다. 기획자의 아이디어 키워드 기반으로 웹 검색하여 1)실화/뉴스 2)기존 작품을 수집한다. 한국어 작성. 반드시 유효한 JSON만 출력. JSON 외 텍스트 금지."""
        user = f"""[입력] 아이디어: {idea} / 장르: {genre} / 타겟: {market}
[JSON 스키마]
{{"search_keywords":[],"real_events":[{{"id":1,"title":"","summary":"","source":"","year":"","relevance":"","story_potential":""}}],"existing_works":[{{"id":1,"title":"","type":"","country":"","year":"","summary":"","similarity":"","difference_opportunity":""}}],"research_summary":{{"total_real_events":0,"total_existing_works":0,"key_insight":""}}}}
real_events 3~10개, existing_works 3~10개."""
        r = client.messages.create(model="claude-sonnet-latest",max_tokens=3000,temperature=0.3,system=sys,messages=[{"role":"user","content":user}],tools=[{"type":"web_search_20250305","name":"web_search"}])
        txt = "".join(b.text for b in r.content if hasattr(b,"text")).strip()
        if txt.startswith("```"): txt = txt.split("\n",1)[1].rsplit("```",1)[0]
        return json.loads(txt)
    except Exception as e:
        st.error(f"리서치 실패: {e}")
        return None

def call_brainstorm(idea, genre, market, fmt, research=None):
    try:
        client = get_client()
        sys = """당신은 글로벌 콘텐츠 시장을 이해하는 Development Producer이자 Script Architect다.
기획자의 아이디어를 개발 가능한 컨셉으로 정렬한다. 이야기와 분위기를 구분한다.
타겟 시장/포맷 인식하여 반영한다. 리서치가 있으면 참고하되, 기존작 때문에 제한하지 않는다.
반드시 유효한 JSON만 출력. 점수 0.0~10.0. 한국어 작성, 전문용어 한글(English) 병기."""
        rb = ""
        if research:
            rb = f"\n[리서치 참고]\n{json.dumps(research,ensure_ascii=False)}\n실화에서 소재 참고 가능. 기존작은 차별화 참고만."
        user = f"""[입력] 아이디어: {idea} / 장르: {genre} / 타겟: {market} / 포맷: {fmt}{rb}
[JSON 스키마]
{{"idea_type":"story|mood|hybrid","idea_type_diagnosis":"","market_context":{{"target_market":"","market_insight":"","cultural_code":"","market_risk":"","reference_titles":[]}},"format_context":{{"selected_format":"","format_rationale":"","structure_note":""}},"research_applied":{{"real_events_used":[],"inspiration_note":""}},"idea_cards":[{{"id":1,"title":"","logline_seed":"","protagonist":"","conflict":"","hook":"","visual_image":"","genre":"","scores":{{"active_hero":0.0,"conflict_clarity":0.0,"visual_power":0.0,"genre_immediacy":0.0,"originality":0.0,"market_fit":0.0}},"total_score":0.0}}],"top3":[{{"rank":1,"card_id":0,"reason":""}}],"hook_sentence":"","differentiation":[],"development_priority":{{"recommended_direction":"","next_step":"","risk":""}},"gate_a_scores":{{"protagonist_visible":0.0,"conflict_one_line":0.0,"differentiation":0.0,"poster_image":0.0,"market_potential":0.0,"average":0.0}}}}
idea_cards 10~15개. total_score=6축평균. gate_a average=5항목평균. 텍스트 2문장 이내."""
        r = client.messages.create(model="claude-sonnet-latest",max_tokens=4000,temperature=0.7,system=sys,messages=[{"role":"user","content":user}])
        txt = r.content[0].text.strip()
        if txt.startswith("```"): txt = txt.split("\n",1)[1].rsplit("```",1)[0]
        return json.loads(txt)
    except Exception as e:
        st.error(f"Brainstorm 실패: {e}")
        return None

# ─── Sidebar ───
with st.sidebar:
    st.markdown('<div class="mt">👖 CREATOR ENGINE</div>',unsafe_allow_html=True)
    st.markdown('<div class="st">Creative Development Engine v1.2</div>',unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🏠 Home",use_container_width=True):
        st.session_state.page="home"; st.rerun()
    if st.session_state.cur:
        p=st.session_state.projects[st.session_state.cur]
        st.markdown(f"**📁 {p['title']}**")
        for k,lb in [("brainstorm","🧠 Brainstorm"),("core","🎯 Core"),("structure","🏗️ Structure"),("treatment","📝 Treatment"),("export","📦 Export")]:
            if st.button(lb,use_container_width=True,key=f"n_{k}"):
                st.session_state.page="project";st.session_state.tab=k;st.rerun()
        st.markdown("---")
        for s,v in p["stage_status"].items():
            st.markdown(f"{s}: {badge(v)}",unsafe_allow_html=True)
    st.markdown("---")
    st.markdown('<div style="font-size:.65rem;color:#555">© 2026 BLUE JEANS PICTURES</div>',unsafe_allow_html=True)

# ─── HOME ───
def home():
    st.markdown('<div class="mt">👖 BLUE JEANS Creative Development Engine</div>',unsafe_allow_html=True)
    st.markdown('<div class="st">From instinct to industry-standard narrative architecture</div>',unsafe_allow_html=True)
    with st.expander("➕ 새 프로젝트",expanded=not bool(st.session_state.projects)):
        c1,c2=st.columns([2,1])
        with c1:
            ti=st.text_input("프로젝트 제목",placeholder="예: 인도네시아 물귀신 프로젝트")
            idea=st.text_area("💡 아이디어",height=120,placeholder="자유롭게 입력\n예: 인도네시아용 물귀신 이야기\n예: 은퇴한 킬러가 다시 돌아오는 이야기")
        with c2:
            genre=st.selectbox("🎬 장르",["미지정","범죄/스릴러","드라마","액션","로맨스","코미디","호러/공포","SF","판타지","시대극/사극","느와르","미스터리","전쟁","뮤지컬","다큐/논픽션"])
            mt=st.selectbox("🌏 타겟 시장",["미지정","한국","북미/미국","일본","중국","동남아","유럽","중동","글로벌","직접 입력"])
            mc=""
            if mt=="직접 입력": mc=st.text_input("시장 직접 입력",placeholder="예: 인도네시아+한국 공동제작")
            fmt=st.selectbox("📐 포맷",["미지정","영화","시리즈","미니시리즈(4~8화)","웹툰","웹소설","숏폼","다큐멘터리","애니메이션"])
        if st.button("🚀 프로젝트 생성",use_container_width=True,disabled=not idea.strip()):
            mk=mc if mt=="직접 입력" else mt
            pid=f"p_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            st.session_state.projects[pid]={"project_id":pid,"title":ti or "새 프로젝트","idea_text":idea,"genre":genre,"target_market":mk,"format":fmt,"created_at":datetime.now().strftime("%Y-%m-%d %H:%M"),"updated_at":datetime.now().strftime("%Y-%m-%d %H:%M"),"current_stage":"brainstorm","stage_status":{"brainstorm":"NOT_RUN","core":"NOT_RUN","structure":"NOT_RUN","treatment":"NOT_RUN"},"research":None,"brainstorm":None,"core":None,"gate_results":{},"final_score":None}
            st.session_state.cur=pid;st.session_state.page="project";st.session_state.tab="brainstorm";st.rerun()
    if st.session_state.projects:
        st.markdown("### 📁 프로젝트")
        for pid,p in sorted(st.session_state.projects.items(),key=lambda x:x[1]["updated_at"],reverse=True):
            c1,c2=st.columns([4,1])
            with c1:
                st.markdown(f'<div class="cc"><b>{p["title"]}</b><br><span style="font-size:.75rem;color:var(--dim)">{p["genre"]} · {p["target_market"]} · {p["format"]} · {p["updated_at"]}</span></div>',unsafe_allow_html=True)
            with c2:
                if st.button("열기 →",key=f"o_{pid}"):
                    st.session_state.cur=pid;st.session_state.page="project";st.session_state.tab="brainstorm";st.rerun()

# ─── BRAINSTORM ───
def brainstorm():
    p=st.session_state.projects[st.session_state.cur]
    st.markdown("### 🧠 Brainstorm")
    st.markdown(f'<div class="callout"><div class="ct">IDEA</div>{p["idea_text"]}</div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    c1.markdown(f"**장르:** {p['genre']}"); c2.markdown(f"**타겟:** {p['target_market']}"); c3.markdown(f"**포맷:** {p['format']}")
    st.markdown("---")

    # 리서치
    st.markdown("#### 🔍 리서치 (선택)")
    st.caption("실화/뉴스 + 기존 작품 정보 검색. 건너뛰어도 됩니다.")
    if st.button("🔍 리서치 실행"):
        with st.spinner("웹 검색 중..."):
            r=call_research(p["idea_text"],p["genre"],p["target_market"])
            if r: p["research"]=r;p["updated_at"]=datetime.now().strftime("%Y-%m-%d %H:%M");st.rerun()
    if p.get("research"):
        rs=p["research"]
        sm=rs.get("research_summary",{})
        with st.expander(f"📰 리서치 결과 — 실화 {sm.get('total_real_events',0)}건 · 기존작품 {sm.get('total_existing_works',0)}건",expanded=True):
            if rs.get("real_events"):
                st.markdown("**📰 실화 / 뉴스**")
                for ev in rs["real_events"]:
                    st.markdown(f'<div class="ri"><div class="rl">#{ev.get("id","")} [{ev.get("year","")}] {ev.get("source","")}</div><b>{ev.get("title","")}</b><br>{ev.get("summary","")}<br><span style="color:var(--y)">→ {ev.get("story_potential","")}</span></div>',unsafe_allow_html=True)
            if rs.get("existing_works"):
                st.markdown("**🎬 기존 작품**")
                for w in rs["existing_works"]:
                    st.markdown(f'<div class="ri"><div class="rl">#{w.get("id","")} {w.get("type","")} · {w.get("country","")} · {w.get("year","")}</div><b>{w.get("title","")}</b><br>유사: {w.get("similarity","")}<br><span style="color:var(--y)">→ 차별화: {w.get("difference_opportunity","")}</span></div>',unsafe_allow_html=True)
            if sm.get("key_insight"):
                st.markdown(f'<div class="callout"><div class="ct">💡 핵심 시사점</div>{sm["key_insight"]}</div>',unsafe_allow_html=True)
    st.markdown("---")

    # 브레인스톰
    st.markdown("#### 🧠 Brainstorm 실행")
    if st.button("🧠 Brainstorm 실행",type="primary"):
        with st.spinner("컨셉 카드 생성 중... (약 30~60초)"):
            r=call_brainstorm(p["idea_text"],p["genre"],p["target_market"],p["format"],p.get("research"))
            if r: p["brainstorm"]=r;p["stage_status"]["brainstorm"]="DONE";p["updated_at"]=datetime.now().strftime("%Y-%m-%d %H:%M");st.rerun()
    if p.get("brainstorm"):
        bs=p["brainstorm"]
        # 아이디어 유형
        st.markdown(f'<div class="callout"><div class="ct">아이디어 유형: {bs.get("idea_type","").upper()}</div>{bs.get("idea_type_diagnosis","")}</div>',unsafe_allow_html=True)
        # 시장·포맷
        mc=bs.get("market_context",{});fc=bs.get("format_context",{})
        c1,c2=st.columns(2)
        with c1:
            st.markdown(f'<div class="callout"><div class="ct">🌏 시장 — {mc.get("target_market","")}</div>기회: {mc.get("market_insight","")}<br>문화코드: {mc.get("cultural_code","")}<br>리스크: {mc.get("market_risk","")}<br>참고작: {", ".join(mc.get("reference_titles",[]))}</div>',unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="callout"><div class="ct">📐 포맷 — {fc.get("selected_format","")}</div>적합성: {fc.get("format_rationale","")}<br>구조: {fc.get("structure_note","")}</div>',unsafe_allow_html=True)
        # 훅
        st.markdown(f'<div style="text-align:center;padding:1.5rem 0"><div style="font-size:.7rem;color:var(--y);font-weight:600">HOOK</div><div style="font-size:1.2rem;font-weight:600;color:var(--t);line-height:1.5">"{bs.get("hook_sentence","")}"</div></div>',unsafe_allow_html=True)
        # Top3
        st.markdown("#### 🏆 Top 3")
        cards={c["id"]:c for c in bs.get("idea_cards",[])}
        for t in bs.get("top3",[]):
            cd=cards.get(t["card_id"],{})
            if cd:
                c1,c2=st.columns([4,1])
                with c1:
                    st.markdown(f'<div class="cc"><span style="color:var(--y);font-weight:700">#{t["rank"]}</span> <b>{cd.get("title","")}</b><br><span style="color:#ccc">{cd.get("logline_seed","")}</span><br><span style="font-size:.8rem;color:#999">👤 {cd.get("protagonist","")}<br>⚔️ {cd.get("conflict","")}<br>✨ {cd.get("hook","")}<br>🎬 {cd.get("visual_image","")}</span><br><span style="font-size:.75rem;color:var(--dim)">이유: {t.get("reason","")}</span></div>',unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="sb">{cd.get("total_score",0.0)}</div><div class="sl">{cd.get("genre","")}</div>',unsafe_allow_html=True)
        # 차별화
        diff=bs.get("differentiation",[])
        if diff:
            st.markdown("#### 💎 차별화 포인트")
            for i,d in enumerate(diff,1): st.markdown(f"**{i}.** {d}")
        # 개발 우선순위
        dp=bs.get("development_priority",{})
        st.markdown("#### 🧭 개발 우선순위")
        c1,c2,c3=st.columns(3)
        c1.markdown(f'<div class="callout"><div class="ct">추천 방향</div>{dp.get("recommended_direction","")}</div>',unsafe_allow_html=True)
        c2.markdown(f'<div class="callout"><div class="ct">Core Build 집중</div>{dp.get("next_step","")}</div>',unsafe_allow_html=True)
        c3.markdown(f'<div class="callout" style="border-left-color:var(--r)"><div class="ct" style="color:var(--r)">리스크</div>{dp.get("risk","")}</div>',unsafe_allow_html=True)
        st.markdown("---")
        # Gate A
        ga=bs.get("gate_a_scores",{});avg=ga.get("average",0);ok=avg>=7.0
        st.markdown("#### 🚪 Gate A: Concept Gate")
        c1,c2=st.columns([1,2])
        with c1:
            cl="var(--g)" if ok else "var(--r)";lb="PASS" if ok else "FAIL"
            st.markdown(f'<div style="text-align:center"><div class="sb" style="color:{cl}">{avg}</div><div class="sl" style="color:{cl};font-size:1rem;font-weight:700">{lb}</div></div>',unsafe_allow_html=True)
        with c2:
            for nm,sc in [("주인공",ga.get("protagonist_visible",0)),("갈등",ga.get("conflict_one_line",0)),("차별점",ga.get("differentiation",0)),("포스터",ga.get("poster_image",0)),("시장성",ga.get("market_potential",0))]:
                bp=sc*10
                st.markdown(f'<div style="display:flex;align-items:center;margin:.2rem 0;font-size:.8rem"><div style="width:60px;color:var(--dim)">{nm}</div><div style="flex:1;background:#3a3a4a;border-radius:4px;height:8px;margin:0 .5rem"><div style="width:{bp}%;background:var(--y);height:100%;border-radius:4px"></div></div><div style="width:30px;text-align:right">{sc}</div></div>',unsafe_allow_html=True)
        if ok: st.success("✅ Gate A 통과. Core Build 진행 가능.")
        else:
            st.warning(f"⚠️ Gate A 미통과 (평균 {avg}). 아이디어 보강 또는 재실행 권장.")
            if st.button("🔓 Override"): st.info("Override. Core Build 이동.")
        # 전체 카드
        ac=bs.get("idea_cards",[])
        if ac:
            with st.expander(f"📋 전체 아이디어 카드 ({len(ac)}개)"):
                for cd in sorted(ac,key=lambda x:x.get("total_score",0),reverse=True):
                    st.markdown(f"**#{cd['id']} {cd.get('title','')}** — {cd.get('total_score',0.0)}점 &nbsp; {cd.get('logline_seed','')}")

# ─── Placeholder Tabs ───
def core_tab():
    st.markdown("### 🎯 Core Build");st.info("Brainstorm 완료 후 활성화됩니다.")
def structure_tab():
    st.markdown("### 🏗️ Structure Build");st.info("Phase 2에서 구현됩니다.")
def treatment_tab():
    st.markdown("### 📝 Treatment Build");st.info("Phase 2에서 구현됩니다.")
def export_tab():
    st.markdown("### 📦 Export");st.info("Core Build 완료 후 활성화됩니다.")

# ─── Router ───
if st.session_state.page=="home":
    home()
elif st.session_state.page=="project" and st.session_state.cur:
    p=st.session_state.projects[st.session_state.cur]
    c1,c2=st.columns([3,1])
    with c1:
        st.markdown(f'<div class="mt">{p["title"]}</div>',unsafe_allow_html=True)
        st.markdown(f'<div class="st">{p["genre"]} · {p["target_market"]} · {p["format"]}</div>',unsafe_allow_html=True)
    with c2:
        sc=p.get("final_score")
        if sc: st.markdown(f'<div class="sb">{sc}</div><div class="sl">Development Fit Score</div>',unsafe_allow_html=True)
    {"brainstorm":brainstorm,"core":core_tab,"structure":structure_tab,"treatment":treatment_tab,"export":export_tab}.get(st.session_state.tab,brainstorm)()
else:
    home()
