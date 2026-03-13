# 👖 BLUE JEANS · Creator Engine v1.2

> **아이디어 한 줄 → 헐리우드 수준 기획개발 패키지**
>
> 9단계 AI 파이프라인으로 로그라인, 캐릭터 바이블, 시놉시스, 장면 설계, 트리트먼트, 톤 문서까지 자동 생성

---

## 3-Engine Pipeline

```
[1] Creator Engine  → 아이디어 → 기획개발 패키지 (현재)
[2] Writer Engine   → 기획개발 → 시나리오 초고   (개발 예정)
[3] Rewrite Engine  → 시나리오 → 리라이트 완성   (운영 중)
```

---

## 9단계 파이프라인

```
① 아이디어 입력
② Brainstorm (컨셉 카드 10개 + 시장 분석 + Gate A)
③ Core Build (Logline Pack + 기획의도 + GNS + 세계관 + 캐릭터 + Gate B/C)
④ Character Bible (백스토리 · 비밀 · 말투 규칙 · 대사 샘플 · 관계 태도 · 변화 궤적)
⑤ Structure Build (Synopsis 1P + Storyline 8시퀀스 + 3막 진단 + 15Beat + Gate D)
⑥ Scene Design (핵심 장면 15~18개 · Show/don't tell · 극적 아이러니 · 핵심 대사)
⑦ Treatment Build (16비트 줄글 트리트먼트 · 1막/2막/3막 분할 생성 · 40~50페이지 + Gate E)
⑧ Tone Document (카메라 · 색감 · 페이싱 · 대사 규칙 · 모티프 · 금기 · 참고 작품)
⑨ Export (기획개발보고서 DOCX — 노란 헤더 + 한영 병기 기획서 스타일)
```

### Gate 시스템

| Gate | 위치 | 통과 기준 |
|------|------|---------|
| Gate A | Brainstorm 후 | 평균 7.0 이상 |
| Gate B+C | Core 후 | 평균 7.0 이상 |
| Gate D | Structure 후 | 평균 7.0 이상 |
| Gate E | Treatment 후 | 영화적읽힘 / 씬감정일치 / 비트충실도 / 초고직행 |

---

## 프로젝트 구조

```
bjcde/
├── main.py                    # 메인 앱 (4,200+ 줄)
├── requirements.txt           # Python 의존성
├── .streamlit/
│   ├── config.toml            # 테마 설정 (라이트모드)
│   └── secrets.toml           # API 키 (로컬 전용, .gitignore)
├── README.md
└── MANUAL.md                  # 운영 매뉴얼
```

---

## 시작하기

### 1. 저장소 클론

```bash
git clone https://github.com/cinepark-1974/creator-engine.git
cd creator-engine
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. API 키 설정

`.streamlit/secrets.toml` 파일 생성:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

### 4. 로컬 실행

```bash
streamlit run main.py
```

---

## Streamlit Cloud 배포

1. GitHub 저장소에 push
2. [share.streamlit.io](https://share.streamlit.io) 에서 저장소 연결
3. **Advanced Settings > Secrets** 에 `ANTHROPIC_API_KEY = "sk-ant-..."` 등록
4. Deploy

---

## 기술 스택

| 항목 | 스펙 |
|------|------|
| 프레임워크 | Streamlit 1.55+ |
| AI 엔진 | Claude Sonnet 4.6 (Anthropic API) |
| DOCX 생성 | python-docx 1.2+ |
| 차트 | Plotly 6.0+ |
| 테마 | 라이트모드 · Midnight Blue (#191970) + Stitch Yellow (#FFCB05) |
| 폰트 | Paperlogy (헤더) + Playfair Display (타이틀) + Pretendard (본문) |

---

## API 비용 참고

| 단계 | 호출 수 | 예상 토큰 (입력+출력) |
|------|--------|-------------------|
| Brainstorm | 3회 | ~15,000 |
| Core Build | 2회 | ~12,000 |
| Character Bible | 4회 (캐릭터당 1회) | ~20,000 |
| Structure | 4회 | ~18,000 |
| Scene Design | 1회 | ~10,000 |
| Treatment | 3회 (막별 1회) + 2회 | ~35,000 |
| Tone Document | 1회 | ~6,000 |
| **합계** | **~20회** | **~116,000 토큰** |

---

## Writer Engine 연동 (예정)

Creator Engine 완료 시 생성되는 데이터:

```
project_data
├── core (Logline / GNS / 세계관)
├── char_bible (캐릭터 바이블 — Writer Engine 일관성의 핵심)
├── structure (Synopsis / Storyline / 3막 / 15Beat)
├── scene_design (핵심 장면 15~18개)
├── treatment (16비트 40P 줄글)
└── tone_doc (톤 & 연출 가이드 — Writer Engine 톤 일관성의 핵심)
```

---

## 라이선스

© 2026 BLUE JEANS PICTURES. All rights reserved.

이 소프트웨어는 BLUE JEANS PICTURES의 내부 기획개발 도구입니다.
