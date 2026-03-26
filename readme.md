# 👖 BLUE JEANS · Creator Engine v1.8

> **아이디어 한 줄 → 헐리우드 수준 기획개발 패키지**
>
> BLUE JEANS PICTURES 고유의 3축 설계 + 9단계 AI 파이프라인

---

## 3-Engine Pipeline

```
[1] Creator Engine  → 아이디어 → 기획개발 패키지   (현재)
[2] Writer Engine   → 기획개발 → 시나리오 초고     (운영 중)
[3] Rewrite Engine  → 시나리오 → 리라이트 완성     (운영 중)
    Series Engine   → 기획개발 → 시리즈 시나리오   (운영 중)
    Novel Engine    → 기획개발 → 소설              (운영 중)
```

Creator Engine의 출력물이 Writer / Series / Rewrite / Novel Engine의 입력이 됩니다.
Creator Engine이 좋아야 모든 하위 엔진의 품질이 올라갑니다.

---

## BLUE JEANS 3축 — 이 엔진의 정체성

다른 AI 스크립팅 도구와 BLUE JEANS Creator Engine이 다른 이유.

### ① 주인공 서사동력 (BJND — Blue Jeans Narrative Drive)
```
욕망(Desire) ← 발생요인(Origin: Loss vs Lack) → 해결전략(Resolution)
```
- **상실(Loss)**: 가졌던 것을 잃었다 → 회복/복수/대체
- **결핍(Lack)**: 처음부터 없었다 → 획득/성장/증명
- 발생요인이 이야기 전체의 구조, 아크, 감정 곡선을 결정합니다
- Core Build 단계에서 진단 → 전 파이프라인에 전파

### ② 빌런 설계 (Villain 4 Questions)
```
① 흥미로운가?  ② 다크 미러인가?  ③ 계획을 뒤엎는가?  ④ 이기고 있는가?
```
- 빌런이 매번 실패하면 클라이맥스에서 아무도 긴장하지 않는다 (Patriot Games 규칙)
- Structure Diagnosis에서 비트별 빌런 승률 추적
- Treatment 매 비트에 `villain_beat` 필드로 적대자 행동 + 승/패 기록

### ③ 장르적 재미 (ATTRACTION + Genre Rule Pack v2)
```
Opening Hook · 배반 규칙 · Water Cooler Moment · 한국 구체성 · 감정 억압→폭발
+ 장르별 12필드 Rule Pack (core/opening/items/hooks/punches/fails...)
```
- 9장르 × 12필드 = Writer Engine과 동일한 장르 언어
- Scene Design, Treatment, Core Build에 자동 주입

---

## 9단계 파이프라인

```
① 아이디어 입력 + LOCKED/OPEN 설정
② Brainstorm (컨셉 카드 10개 + 시장 분석 + Gate A)           [Sonnet]
③ Core Build (Logline Pack + GNS + 서사동력 + 세계관 + 캐릭터 + Gate B/C) [Sonnet]
④ Character Bible (백스토리 · 전술 · 말투 · 대사 · 변화궤적)    [Opus]
⑤ Structure Build (Synopsis + Storyline + 3막 진단 + 빌런 승률 + Gate D) [Sonnet]
⑥ Scene Design (핵심 장면 15~18개 · 서브플롯 태그 · 매력 설계도) [Sonnet]
⑦ Treatment Build (16비트 다중씬 트리트먼트 · 영화/시리즈 분기)   [Opus]
⑧ Tone Document (카메라 · 색감 · 페이싱 · 대사 규칙 · 금기)     [Opus]
⑨ Export (기획개발보고서 DOCX)
```

---

## 핵심 기능

### 이중 모델 (Opus / Sonnet)
| 단계 | 모델 | 이유 |
|------|------|------|
| Brainstorm · Core · Structure · Scene · Gate | Sonnet | 구조 작업 — 비용 효율 |
| Character Bible · Treatment · Tone | **Opus** | 서사 품질 — 대사/묘사/감정 |

Opus 호출 시 JSON 파싱 실패 → 자동 재시도 1회 (temperature 낮춤 + JSON 규칙 강화)

### LOCKED / OPEN 시스템
```
🔒 LOCKED — 파이프라인 전 과정에서 절대 변경 불가
   서재중: 29세, 묘적사 현장 요원
   기획의도: 20대 취업난이 재중의 입사 동기에 반영
   역사적 사건: EP2 시작 — 1947년 여운형 암살

🟢 OPEN — AI가 자유롭게 창작 가능
   캐릭터 외형, 습관, 말투 디테일
   장면별 시각 연출과 감정 변화
```
- 프로젝트 생성 시 입력 + 프로젝트 뷰에서 편집 가능
- 모든 API 호출에 자동 주입

### 영화 / 미니시리즈 자동 분기
| 포맷 | 비트 구조 | 분량 | 특수 기능 |
|------|----------|------|----------|
| 영화 | 16비트 3막 | 2500~4000자/비트 | — |
| 미니시리즈 6화 | EP1~EP6 16비트 | 4000~6000자/비트 | 클리프행어 · B-Story 시간축 |
| 미니시리즈 8화 | EP1~EP8 16비트 | 4000~6000자/비트 | 클리프행어 · B-Story 시간축 |

### 유연한 캐릭터 (4~8인)
- 필수 4인: protagonist / antagonist / ally / mirror
- 확장 0~4인: `extended_characters` — 역할명 자유 (catalyst / subplot_lead / mentor / rival / informant 등)
- 영화 4~5명, 미니시리즈 6~8명 적정

### SCOPE MANDATE (1비트 = 다중 씬)
```
★ 1비트 = 1씬이 아니다. 1비트 = 3~5개 독립 씬이다. ★
최소 2개 장소, 2명 이상 인물, 비트 안에서 시간 경과 필수.
```

---

## 파일 구조

```
creator-engine/
├── main.py              4,714줄  UI + API + JSON 파서 + DOCX 생성
├── prompt.py            1,211줄  프롬프트 라이브러리 (BJND + V4Q + GENRE v2 + LOCKED)
├── requirements.txt              streamlit · anthropic · python-docx · plotly
├── .streamlit/config.toml        라이트 모드 테마
├── README.md                     이 파일
└── BLUE_JEANS_CREATOR_ENGINE_v1_8_제품명세서.md
```

---

## 배포

```bash
# GitHub: cinepark-1974/creator-engine
# Streamlit Cloud 자동 배포

# requirements.txt
streamlit>=1.55.0
anthropic>=0.80.0
python-docx>=1.2.0
plotly>=6.0.0

# secrets (Streamlit Cloud)
ANTHROPIC_API_KEY = "sk-ant-..."
```

---

## 버전 이력

| 버전 | 주요 변경 |
|------|---------|
| v1.0 | 기본 9단계 파이프라인 |
| v1.3 | Sorkin/Curtis 9원칙 · Genre Rules 8장르 · Hook/Punch · prompt.py 분리 |
| v1.4 | 관객 심리 6원칙 · 서브플롯 설계 · Tactics=Character |
| v1.5 | LOCKED 시스템 · 5단계 서술 구조 · 시리즈 비트(6/8화) · B-Story 자동 주입 |
| v1.6 | SCOPE MANDATE(1비트=다중씬) · 영화/시리즈 분량 분기 |
| v1.7 | ATTRACTION 6규칙 · Opus/Sonnet 이중 모델 · 유연 4~8 캐릭터 |
| **v1.8** | **BJND 서사동력(Loss/Lack) · Villain 4Q + 승률 설계 · Genre Rule Pack v2(12필드) · JSON 자동 재시도** |

---

## 라이선스

BLUE JEANS PICTURES · 내부 도구 · 비공개

---

*기획 · 개발: Mr.MOON (BLUE JEANS PICTURES)*
*AI 엔진 설계: Claude (Anthropic)*
