# 📖 Creator Engine v1.2 — 운영 매뉴얼

> BLUE JEANS PICTURES · Creative Development Engine
>
> 최종 업데이트: 2026-03-08

---

## 목차

1. 개요
2. 9단계 파이프라인 상세
3. 각 단계별 사용법
4. DOCX 기획개발보고서
5. 에러 대응
6. Writer Engine 연동 가이드
7. 커스터마이징

---

## 1. 개요

Creator Engine은 영화/시리즈 아이디어를 입력하면 헐리우드 수준의 기획개발 패키지를 자동 생성하는 AI 도구입니다. 9단계 파이프라인과 5개의 Gate 시스템을 통해 품질을 보장하며, 최종 산출물은 투자자용 DOCX 기획개발보고서와 Writer Engine 연동용 데이터입니다.

### 핵심 원칙

- 모든 콘텐츠 생성에 Claude Sonnet 4.6 사용 (max_tokens=16000)
- Gate 통과 기준: 평균 7.0 이상 (10점 만점)
- Gate 미통과 시 Override 또는 재실행 선택 가능
- 캐릭터 바이블은 캐릭터당 개별 호출 (품질 보장)
- 트리트먼트는 막별 분할 생성 (1막/2막/3막)

---

## 2. 9단계 파이프라인

```
┌─────────────────────────────────────────────────────┐
│  ① 아이디어   제목 + 자유 텍스트 + 장르 + 시장 + 포맷  │
│      ↓                                               │
│  ② Brainstorm  컨셉 카드 10개 + 시장 분석 + Gate A    │
│      ↓                                               │
│  ③ Core Build  Logline Pack(5종) + 기획의도 + GNS     │
│                + 세계관 + 캐릭터(4인) + Gate B/C       │
│      ↓                                               │
│  ④ Char Bible  캐릭터별 분할 생성 (4회 호출)           │
│                백스토리·비밀·말투·대사·관계·변화궤적      │
│      ↓                                               │
│  ⑤ Structure   Synopsis 1P + Storyline 8시퀀스        │
│                + 3막 진단 + 15Beat + 줄글 시놉시스      │
│                + Gate D                               │
│      ↓                                               │
│  ⑥ Scene Design  핵심 장면 15~18개                    │
│                   Show/don't tell + 극적 아이러니       │
│      ↓                                               │
│  ⑦ Treatment   16비트 줄글 (1막→2막→3막 분할)          │
│                + 감정곡선 + 감독포인트 + 투자자요약       │
│                + Gate E                               │
│      ↓                                               │
│  ⑧ Tone Doc   카메라·색감·페이싱·대사규칙·모티프·금기   │
│      ↓                                               │
│  ⑨ Export      기획개발보고서 DOCX 다운로드             │
└─────────────────────────────────────────────────────┘
```

---

## 3. 각 단계별 사용법

### ① 아이디어 입력

홈 화면에서 "➕ 새 프로젝트" 클릭 후 입력합니다.

- **제목**: 작업 제목 (가제). 최종 제목은 Writer Engine 마지막에서 결정
- **아이디어**: 자유 텍스트. 한 줄이든 한 문단이든 OK
  - 예: "인도네시아용 물귀신 이야기"
  - 예: "40대 여형사, 연쇄살인범이 딸의 담임교사"
- **장르**: 선택 또는 미지정
- **타겟 시장**: 한국, 글로벌, 직접 입력 가능
- **포맷**: 영화, 시리즈, 미니시리즈, 웹툰 등

### ② Brainstorm

"🔍 리서치" 버튼(선택)으로 실화/뉴스 + 기존 작품을 검색한 후, "🧠 Brainstorm 실행"으로 컨셉 카드 10개를 생성합니다.

- **컨셉 카드**: 제목, 로그라인, 장르 어프로치, 차별점, 리스크 포함
- **Top 3 선택**: AI가 추천하는 상위 3개 컨셉
- **Gate A**: 독창성/시장성/캐릭터 잠재력/구조 가능성/장르 적합성 자동 채점

Gate A 통과(평균 7.0+) 시 → Core Build로 진행

### ③ Core Build

선택한 컨셉을 기반으로 핵심 기획 요소를 생성합니다.

- **Logline Pack** (5종): Original, Washed, 투자자용, 감독용, 캐릭터 훅
- **기획의도**: 소재/장르/시장/Pitch/Theme
- **Goal / Need / Strategy**: 서사 엔진의 핵심
- **세계관**: 시간/공간/규칙/금기/권력구조
- **캐릭터** (4인): 주인공/적대자/조력자/거울
- **Gate B+C**: 서사 엔진 + 캐릭터 채점
- **Development Fit Score**: 5축 종합 점수

### ④ Character Bible (신규)

Core Build의 기본 캐릭터를 헐리우드 수준으로 확장합니다. 캐릭터당 개별 API 호출로 품질 보장합니다.

각 캐릭터에 대해 생성되는 항목:

| 항목 | 설명 |
|------|------|
| 외형·첫인상 | 시각적 디테일 3문장 |
| 백스토리 | 과거사 5문장 — 현재 행동의 원인 |
| 비밀 | 밝혀지면 플롯이 바뀌는 것 1개 |
| 신념 | 절대 양보 못하는 가치 |
| 두려움 | 가장 무서워하는 것 |
| 반복 습관 | 행동 패턴 3개 |
| 말투 규칙 | 구체적 규칙 3줄 (추상어 금지) |
| 대사 샘플 | 평상시/분노/취약 — 시나리오 품질 |
| 관계별 태도 | 다른 캐릭터에 대한 태도 변화 |
| 변화 궤적 | 1막 끝 → 미드포인트 → 클라이맥스 |

소요 시간: 캐릭터당 약 30초 × 4명 = 약 2분

### ⑤ Structure Build

스토리 구조를 설계합니다.

- **Synopsis 1P**: 시작/촉발사건/전개/미드포인트/붕괴/결전/결말
- **Storyline**: 8시퀀스 방향 서술
- **3막 구조 진단**: 1막 끝/미드포인트/All Is Lost/클라이맥스
- **15-Beat Sheet**: 있음/약함/없음 상태 표시
- **캐릭터 변화표 + 관계 변화표**
- **기승전결 줄글 시놉시스**: 1페이지 분량
- **Gate D**
- **1차 DOCX 다운로드** (Core + Structure)

### ⑥ Scene Design

핵심 장면 15~18개를 설계합니다.

각 장면: 장소, 인물, 상황, 행동(Show!), 전환점, 극적 아이러니, 감정 변화, 시각 연출, 판돈, 핵심 대사

**Scene Map**: 1막/2막전반/2막후반/3막별 씬 배치 + Must-See 장면

### ⑦ Treatment Build

16비트 줄글 트리트먼트를 막별로 분할 생성합니다.

- **1막** (Beat 1~6): 오프닝 → 도발적 사건 → 첫번째 변곡점
- **2막** (Beat 7~12): 메인 목적 → 미드포인트 → All Is Lost
- **3막** (Beat 13~16): 빌런 최고조 → 클라이맥스 → 에필로그

비트당 1500~2500자, 서술체 현재형, 대사 직접 삽입. 총 40~50페이지 목표.

추가 생성: 감정곡선(16포인트) + 감독 포인트(3개) + 투자자용 요약

- **Gate E**: 영화적 읽힘/씬-감정 일치/비트 충실도/초고 직행 가능
- **최종 DOCX 다운로드** (전체 포함)

### ⑧ Tone Document (신규)

Writer Engine이 시나리오를 쓸 때 참조할 톤 가이드입니다.

| 섹션 | 내용 |
|------|------|
| 비주얼 스타일 | 카메라 철학 / 색감 팔레트 / 조명 규칙 / 시그니처 쇼트 |
| 페이싱 | 전체 철학 / 막별 템포 / 대사 비율 |
| 대사 규칙 | 전체 톤 / 서브텍스트 / 침묵 활용 / 금지 대사 패턴 |
| 모티프 | 반복 소품 / 반복 장소 / 날씨·계절 |
| 사운드 | 음악 방향 / 무음 사용 / 작품 내 소리 |
| 금기 | 절대 하지 말아야 할 연출/톤/대사 규칙 |
| 참고 작품 | 톤 참고 영화 3편 + 이유 |
| Writer 지시 | Writer Engine에게 보내는 최종 지시 |

### ⑨ Export

- 기획개발보고서 DOCX 다운로드
- 노란 하이라이트 섹션 헤더 + 한글/ENGLISH 병기
- 커버 페이지 + 전체 9단계 내용 포함
- Tone Document 섹션 포함

---

## 4. DOCX 기획개발보고서 구조

```
Cover (작품 기획안 + 제목 + 장르 + 로그라인 + BLUE JEANS PICTURES)
  ↓
로그라인 LOGLINE (5종)
  ↓
기획의도 KEY POINTS
  ↓
드라마 구조 GOAL / NEED / STRATEGY
  ↓
세계관 WORLD BUILDING
  ↓
캐릭터 CHARACTER (기본)
  ↓
캐릭터 바이블 CHARACTER BIBLE (확장 — 백스토리/말투/대사/관계/변화)
  ↓
시놉시스 SYNOPSIS
  ↓
스토리라인 STORYLINE
  ↓
3막 구조 진단 THREE-ACT STRUCTURE + 15-Beat Sheet
  ↓
장면 설계 SCENE DESIGN
  ↓
트리트먼트 TREATMENT (네이비 배경 막 헤더 + 16비트 줄글)
  ↓
투자자용 요약 INVESTOR SUMMARY
  ↓
개발 적합도 DEVELOPMENT FIT SCORE (5축 + 점수 테이블)
  ↓
톤 & 연출 문서 TONE DOCUMENT
  ↓
Footer (© BLUE JEANS PICTURES · Creator Engine v1.2)
```

DOCX 다운로드 시점:
- **1차**: Structure 완료 후 — `기획개발보고서_{제목}_1차_Blue.docx`
- **최종**: Treatment 완료 후 — `기획개발보고서_{제목}_최종_Blue.docx`

---

## 5. 에러 대응

### JSON 파싱 에러

AI 응답에서 대사 안 쌍따옴표가 JSON을 깨뜨리는 경우가 있습니다. `safe_json_loads`가 4단계 자동 복구를 수행합니다.

1차: 그대로 파싱
2차: 문자별 추적 + 스마트 종료 판단
3차: 에러 위치 역추적 반복 수정 (30회)
4차: 모든 값 내부 쌍따옴표 강제 치환

에러 발생 시 디버그 expander에서 Raw 응답을 확인할 수 있습니다.

### Gate 미통과

- Override 버튼으로 강제 진행 가능
- 또는 해당 단계를 재실행

### API 타임아웃

- Character Bible: 캐릭터당 개별 호출이므로 실패한 캐릭터만 건너뜀
- Treatment: 막별 분할이므로 실패한 막만 재시도

---

## 6. Writer Engine 연동 가이드 (예정)

Creator Engine 완료 후 Writer Engine에 넘길 데이터:

```
project_data (JSON)
├── core
│   ├── logline_pack (5종)
│   ├── goal_need_strategy
│   └── world_build
├── char_bible ← 캐릭터 일관성의 핵심
│   └── characters[] (백스토리/말투규칙/대사샘플/관계태도/변화궤적)
├── structure
│   ├── synopsis_1p
│   ├── storyline (8시퀀스)
│   └── beat_sheet (15비트)
├── scene_design
│   └── key_scenes[] (15~18개)
├── treatment
│   ├── act1/act2/act3 (16비트 줄글)
│   └── meta (감정곡선/감독포인트/투자자요약)
└── tone_doc ← 톤 일관성의 핵심
    ├── visual_style
    ├── pacing
    ├── dialogue_rules
    ├── motifs
    └── writer_instruction
```

Writer Engine 처리 흐름:

1. 기획서 + 트리트먼트 로드 (외부 트릿 업로드도 가능)
2. 40P 트릿 → 20P 자동 요약 (Writer Engine 입력 최적화)
3. Character Bible + Tone Document 확인/편집
4. 시나리오 분할 생성: 오프닝~1막 → 2막 전반 → 2막 후반 → 3막~엔딩
5. 연속성 검증
6. 제목 추천 (마지막)
7. 시나리오 DOCX 출력

---

## 7. 커스터마이징

### 모델 변경

`main.py` 상단의 `ANTHROPIC_MODEL` 수정:

```python
ANTHROPIC_MODEL = "claude-sonnet-4-6"  # 현재
```

### 디자인 변경

- **CSS**: `main.py` 상단 `<style>` 블록
- **테마**: `.streamlit/config.toml`
- **폰트**: CSS `@import` + CSS 변수 (`--heading`, `--body`, `--display`)

### Gate 기준 조정

각 Gate 함수에서 `average >= 7.0` 부분 수정

---

© 2026 BLUE JEANS PICTURES · Creator Engine v1.2
