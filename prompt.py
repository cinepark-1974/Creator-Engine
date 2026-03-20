"""
👖 BLUE JEANS Creator Engine v1.4 — Prompt Library
All system prompts, user prompt templates, Sorkin/Curtis principles,
audience psychology 6 principles, and subplot design.

Sorkin/Curtis 9원칙:
- BUT/EXCEPT 테스트: 로그라인에 역전이 있는가
- Intention & Obstacle: 판돈이 높고 긴급하고 납득 가능한가
- Tactics = Character: 장애물을 넘는 전술이 캐릭터를 정의한다
- Probable Impossibility: 억지 우연 금지
- Drop in the Middle: 첫 장면이 대화 중간에 관객을 던지는가
- Unified Plot Test: 이 비트를 빼면 이야기가 작동하는가
- Too Wet 금지: 캐릭터가 감정을 직접 말하지 않는다
- Curtis 3% 법칙: 3%만 빗나가면 정반대 영화
- Curtis 감정 연쇄: A장면 감정 → B장면 전제

관객 심리 6원칙 (v1.4):
- Dramatic Irony: 관객이 더 많이 안다
- Information Gap: 호기심의 간극
- Zeigarnik Effect: 미완성이 기억에 남는다
- Pattern & Violation: 패턴을 만들고 깨뜨려라
- Delayed Gratification: 지연된 보상
- Mystery Box: 열리지 않은 상자

서브플롯 (v1.4):
- B-Story = 테마의 통로
"""

import json

# ═══════════════════════════════════════════════════
#  CONSTANTS
# ═══════════════════════════════════════════════════

# ─── 장르별 필수 규칙 ───
GENRE_RULES = {
    "범죄/스릴러": {
        "must_have": ["초반 10분 내 범죄/사건 발생", "관객이 범인보다 한 발 늦게 알아채는 구조", "미드포인트에서 게임의 룰이 바뀌는 반전", "클라이맥스 직전 2중 반전(double twist)"],
        "hook_rule": "매 비트 끝에 새로운 의문 또는 위협이 제시되어야 한다. 관객이 '다음에 뭐가?'를 멈추지 못하게.",
        "punch_rule": "핵심 씬마다 punch line — 인물의 선택이 돌이킬 수 없는 결과를 만드는 순간. 대사 한 마디 또는 행동 하나로 씬의 온도가 급변.",
        "setpiece": "추격/대치/심문/잠입 중 최소 2개 setpiece 필수",
        "forbidden": "설명적 회상 남발, 형사의 독백으로 사건 정리, 우연의 일치로 범인 발각"
    },
    "드라마": {
        "must_have": ["주인공의 내면 결핍이 외부 사건과 충돌하는 1막 설정", "관계의 균열이 극대화되는 미드포인트", "진짜 감정이 터지는 고백/대결 씬", "변화가 행동으로 증명되는 결말"],
        "hook_rule": "감정적 긴장의 실을 끊지 않는다. 매 비트 끝에 해결되지 않은 감정적 질문이 남아야 한다.",
        "punch_rule": "punch는 폭발이 아니라 침묵. 인물이 차마 말하지 못하는 것, 또는 마침내 말해버리는 것이 punch.",
        "setpiece": "감정적 클라이맥스 씬 1개 + 관계 전환 씬 1개 필수",
        "forbidden": "감정을 직접 설명하는 내레이션, '나는 슬펐다' 류의 감정 나열, 갈등 없는 화해"
    },
    "액션": {
        "must_have": ["1막에 주인공의 전투 능력을 보여주는 오프닝 액션", "2막마다 스케일이 커지는 액션 시퀀스", "미드포인트에서 패배 또는 배신", "클라이맥스에서 가장 큰 스케일의 최종 대결"],
        "hook_rule": "물리적 위협과 시간 압박이 매 비트를 관통한다. 숨 쉴 틈 없는 페이싱.",
        "punch_rule": "액션 씬마다 punch — 예상을 깨는 전술 변화 또는 환경 변화. 같은 패턴의 액션 반복 금지.",
        "setpiece": "최소 3개 대형 setpiece (오프닝/미드포인트/클라이맥스) + 소규모 액션 3개 이상",
        "forbidden": "설명으로 처리하는 액션, 무의미한 총격전 반복, 빌런의 동기 없는 폭력"
    },
    "로맨스": {
        "must_have": ["첫 만남의 설렘 또는 마찰이 있는 도입", "감정 접근 후 오해/장벽으로 멀어지는 미드포인트", "진심 고백 또는 희생의 클라이맥스", "관계의 새로운 균형을 보여주는 결말"],
        "hook_rule": "두 사람 사이의 긴장(끌림+저항)이 매 비트에서 진동해야 한다.",
        "punch_rule": "punch는 감정의 급반전 — 웃기다가 울리거나, 가까워지다가 벽이 생기는 순간.",
        "setpiece": "첫 만남 씬 + 감정 폭발 씬 + 이별/재회 씬 필수",
        "forbidden": "삼각관계의 기계적 반복, 오해가 대화 한마디로 해결, 물리적 장벽만으로 갈등 유지"
    },
    "코미디": {
        "must_have": ["도입 5분 내 코믹 톤 확립", "주인공의 결점이 웃음의 원천", "미드포인트에서 거짓말/오해가 극대화", "클라이맥스에서 모든 거짓말이 동시에 터지는 구조"],
        "hook_rule": "웃음 후 즉시 다음 상황을 예고한다. 관객이 '이거 어떻게 빠져나가지?'를 기대하게.",
        "punch_rule": "punch는 예상을 깨는 반응 — 인물이 관객의 예측과 정반대로 행동하는 순간.",
        "setpiece": "대형 코믹 셋피스 최소 2개 (오해 폭발 + 진실 폭로)",
        "forbidden": "상황 설명으로 웃기려는 시도, 같은 개그 반복, 인물 비하로 웃음 유발"
    },
    "호러/공포": {
        "must_have": ["일상의 균열을 보여주는 불안한 오프닝", "규칙 발견 — 이 공포의 작동 방식을 관객이 이해", "규칙 위반 — 인물이 규칙을 깨뜨리면서 공포 극대화", "최종 대면 — 공포의 실체와 직접 대결"],
        "hook_rule": "매 비트 끝에 '안전하다고 생각한 순간' 새로운 위협의 징후가 나타나야 한다.",
        "punch_rule": "punch는 두 종류 — jump scare(갑작스러운 공포)와 slow burn(천천히 스며드는 불안). 반드시 교차 배치.",
        "setpiece": "공포의 규칙 발견 씬 + 규칙 위반 씬 + 최종 대면 씬 필수",
        "forbidden": "설명으로 무서움을 전달, 공포 원인의 과잉 설명, 공포와 무관한 로맨스 삽입"
    },
    "SF": {
        "must_have": ["세계관의 핵심 규칙을 자연스럽게 보여주는 도입", "규칙이 만드는 딜레마 — 기술/환경이 인물에게 불가능한 선택을 강요", "미드포인트에서 세계관의 진실이 뒤집히는 반전", "기술/환경의 논리 안에서 해결되는 클라이맥스"],
        "hook_rule": "세계관의 새로운 측면이 매 비트에서 하나씩 드러나야 한다. 정보 과부하 금지.",
        "punch_rule": "punch는 세계관 규칙의 예상치 못한 적용 — '이 기술이 이렇게도 쓰일 수 있다고?'",
        "setpiece": "세계관 소개 씬 + 기술 딜레마 씬 + 세계관 반전 씬 필수",
        "forbidden": "세계관 설명을 위한 강의식 대사, 현실 과학과의 불필요한 변명, 데우스 엑스 마키나"
    },
    "판타지": {
        "must_have": ["평범한 세계에서 판타지 세계로의 전환(문턱 넘기)", "마법/능력의 규칙과 대가 설정", "멘토의 퇴장 또는 배신", "최종 대결에서 내면의 성장이 외부 승리로 연결"],
        "hook_rule": "새로운 세계의 경이로움과 위험이 동시에 제시되어야 한다.",
        "punch_rule": "punch는 마법/능력의 예상치 못한 대가 — 힘을 쓸수록 잃는 것이 커지는 구조.",
        "setpiece": "세계 진입 씬 + 능력 각성 씬 + 최종 대결 씬 필수",
        "forbidden": "대가 없는 만능 마법, 예언에 의한 수동적 전개, 악의 동기 없는 빌런"
    },
    "미지정": {
        "must_have": ["명확한 도입 훅", "미드포인트 반전", "클라이맥스 대결/대면", "변화가 증명되는 결말"],
        "hook_rule": "매 비트 끝에 다음 비트로 끌어당기는 질문 또는 위협이 있어야 한다.",
        "punch_rule": "핵심 씬마다 예상을 깨는 순간이 있어야 한다.",
        "setpiece": "장르 무관하게 관객이 기억할 대표 씬 최소 2개",
        "forbidden": "설명적 전개, 갈등 없는 진행, 우연에 의한 해결"
    },
}


def get_genre_rules(genre: str) -> dict:
    """장르 이름에서 GENRE_RULES 매칭"""
    for key in GENRE_RULES:
        if key in genre or genre in key:
            return GENRE_RULES[key]
    return GENRE_RULES["미지정"]


# ─── 16비트 구조 (영화) ───
BEAT_STRUCTURE_FILM = {
    1: [
        (1, "오프닝", "세계와 분위기를 보여주는 첫 장면"),
        (2, "캐릭터 소개 1", "주인공 소개 — 일상, 결핍, 욕망"),
        (3, "캐릭터 소개 2", "주변 인물과 관계 설정"),
        (4, "후킹 포인트", "관객을 잡아끄는 사건 또는 이미지"),
        (5, "도발적 사건", "일상을 깨뜨리는 촉발 사건"),
        (6, "첫번째 변곡점", "돌아올 수 없는 문을 넘는 순간"),
    ],
    2: [
        (7, "주인공의 메인 목적", "2막의 드라이브 — 무엇을 향해 가는가"),
        (8, "장애물과 도전", "목적을 가로막는 구체적 장벽들"),
        (9, "주인공의 위기", "전략이 무너지는 순간"),
        (10, "중간점 사건 (Midpoint)", "게임의 규칙이 바뀌는 전환"),
        (11, "압박 강화", "빌런의 반격, 상황 악화"),
        (12, "두번째 변곡점", "All Is Lost — 가장 낮은 지점"),
    ],
    3: [
        (13, "빌런의 최고조", "적대 세력이 가장 강한 순간"),
        (14, "클라이맥스", "최종 대결 — Goal/Need/Strategy 총동원"),
        (15, "결말", "갈등의 해소, 변화의 확인"),
        (16, "에필로그", "새로운 일상, 여운"),
    ],
}

# 기존 호환용
BEAT_STRUCTURE = BEAT_STRUCTURE_FILM

# ─── 미니시리즈 비트 구조 (6화) ───
BEAT_STRUCTURE_SERIES_6 = {
    "EP1": [
        (1, "오프닝 — 세계의 균열", "사건의 한가운데로 던진다. B-Story 세계(시대/사회/정치)를 병렬 제시"),
        (2, "주인공의 이중생활", "표면의 일상 + 숨겨진 정체. 결핍과 욕망이 동시에 드러난다"),
        (3, "EP1 클리프행어", "돌이킬 수 없는 발견/사건. 관객이 EP2를 보지 않을 수 없다"),
    ],
    "EP2": [
        (4, "B-Story 본격 진입", "B-Story의 시간축이 A-Story에 압박을 가한다. 주변 인물과 관계 설정"),
        (5, "도발적 사건", "일상을 깨뜨리는 촉발 사건. 주인공이 첫 번째 선택을 강요받는다"),
        (6, "첫번째 변곡점 + EP2 클리프행어", "돌아올 수 없는 문. 새로운 동맹 또는 적의 등장"),
    ],
    "EP3": [
        (7, "주인공의 메인 목적", "2막 드라이브. A-Story 전략 실행 + B-Story 카운트다운 진행"),
        (8, "장애물과 균열", "전략의 첫 번째 벽. 동맹 내부 균열. B-Story의 영향이 A-Story에 침투"),
        (9, "EP3 클리프행어", "전략이 무너지거나 배신이 드러나는 순간"),
    ],
    "EP4": [
        (10, "미드포인트 반전", "게임의 규칙이 바뀐다. A-Story와 B-Story가 충돌하는 교차점"),
        (11, "압박 강화", "빌런의 반격 + B-Story 시간축이 절반을 넘긴다. 주인공의 모든 전략이 재설계 필요"),
        (12, "All Is Lost + EP4 클리프행어", "가장 낮은 지점. 주인공이 모든 것을 잃는다"),
    ],
    "EP5": [
        (13, "빌런의 최고조", "적대 세력이 가장 강한 순간. B-Story의 데드라인이 눈앞에 온다"),
        (14, "클라이맥스", "최종 대결. A-Story Goal + B-Story 결과가 동시에 결정된다"),
    ],
    "EP6": [
        (15, "결말", "갈등의 해소. A-Story와 B-Story 모두 착지. 변화가 행동으로 증명된다"),
        (16, "에필로그", "새로운 일상. B-Story 세계의 변화된 풍경. 여운"),
    ],
}

# ─── 미니시리즈 비트 구조 (8화) ───
BEAT_STRUCTURE_SERIES_8 = {
    "EP1": [
        (1, "오프닝 — 세계의 균열", "사건의 한가운데. B-Story 세계를 병렬 제시"),
        (2, "주인공의 이중생활 + EP1 클리프행어", "결핍/욕망 + 돌이킬 수 없는 발견"),
    ],
    "EP2": [
        (3, "주변 인물과 관계 설정", "동맹/적대 구도 확립. B-Story 시간축 제시"),
        (4, "후킹 포인트 + EP2 클리프행어", "관객을 잡아끄는 사건. 첫 번째 선택 강요"),
    ],
    "EP3": [
        (5, "도발적 사건", "일상을 깨뜨리는 촉발. B-Story 카운트다운 본격화"),
        (6, "첫번째 변곡점 + EP3 클리프행어", "돌아올 수 없는 문. 새로운 동맹/적"),
    ],
    "EP4": [
        (7, "메인 목적 실행", "2막 드라이브. 전략 실행 + B-Story 진행"),
        (8, "장애물과 균열 + EP4 클리프행어", "전략의 벽 + 동맹 균열"),
    ],
    "EP5": [
        (9, "주인공의 위기", "전략 무너짐. B-Story가 A-Story에 직접 충돌"),
        (10, "미드포인트 반전 + EP5 클리프행어", "게임의 규칙이 바뀐다"),
    ],
    "EP6": [
        (11, "압박 강화", "빌런 반격 + B-Story 데드라인 임박"),
        (12, "All Is Lost + EP6 클리프행어", "가장 낮은 지점"),
    ],
    "EP7": [
        (13, "빌런의 최고조", "적대 세력 최강. B-Story 최종 국면"),
        (14, "클라이맥스 + EP7 클리프행어", "최종 대결. A+B 동시 결정"),
    ],
    "EP8": [
        (15, "결말", "갈등 해소. A+B 착지. 변화의 증명"),
        (16, "에필로그", "새로운 일상. 여운"),
    ],
}


def get_beat_structure(fmt: str) -> dict:
    """포맷에 따라 적절한 비트 구조 반환. 미니시리즈면 에피소드 단위."""
    fmt_lower = fmt.lower() if fmt else ""
    if "시리즈" in fmt_lower or "series" in fmt_lower or "미니" in fmt_lower:
        if "8" in fmt_lower:
            return BEAT_STRUCTURE_SERIES_8
        return BEAT_STRUCTURE_SERIES_6
    return BEAT_STRUCTURE_FILM


def is_series_format(fmt: str) -> bool:
    """미니시리즈 포맷인지 확인"""
    fmt_lower = fmt.lower() if fmt else ""
    return "시리즈" in fmt_lower or "series" in fmt_lower or "미니" in fmt_lower


# ─── Sorkin/Curtis 9원칙 + 관객 심리 6원칙 + 서브플롯 ───
SORKIN_CURTIS = {
    # ── Sorkin/Curtis 9원칙 ──
    "but_except_test": (
        "[Sorkin BUT/EXCEPT 테스트]\n"
        "로그라인에 'but(그런데)', 'except(단)', 'and then(그러자)'이 있는가?\n"
        "- 좋은 로그라인: 'A가 B를 원한다, 그런데(but) C 때문에 불가능하다'\n"
        "- 나쁜 로그라인: 'A가 B를 한다, 그리고(and then) C도 한다' → 이건 플롯 나열이지 이야기가 아니다\n"
        "모든 로그라인에 역전(reversal)이 포함되어야 한다."
    ),
    "intention_obstacle": (
        "[Sorkin Intention & Obstacle 압박 테스트]\n"
        "주인공의 Goal을 검증하라:\n"
        "1. 판돈(Stakes)이 충분히 높은가? — 실패하면 무엇을 잃는가? 잃는 것이 구체적이고 치명적이어야 한다.\n"
        "2. 긴급한가(Urgent)? — 왜 지금 이 순간에 행동해야 하는가? 시간 압박이 있는가?\n"
        "3. 납득 가능한가(Credible)? — 이 인물이 이 목표를 추구하는 것이 그의 과거/결핍/성격으로 납득되는가?\n"
        "세 가지 중 하나라도 약하면 서사 엔진이 작동하지 않는다."
    ),
    "tactics_character": (
        "[Sorkin Tactics = Character]\n"
        "인물의 성격은 '착하다/나쁘다'로 정의되지 않는다.\n"
        "인물이 장애물을 넘기 위해 선택하는 전술(tactics)이 그 인물을 정의한다.\n"
        "- 같은 문이 잠겨 있을 때: A는 부순다, B는 열쇠를 훔친다, C는 다른 문을 찾는다\n"
        "- 전술의 차이가 캐릭터의 차이다\n"
        "각 캐릭터에 대해 '장애물을 넘는 전술 3가지'를 반드시 설계하라."
    ),
    "probable_impossibility": (
        "[Aristotle/Sorkin Probable Impossibility]\n"
        "'불가능하지만 납득되는 것(probable impossibility)'은 허용한다.\n"
        "'가능하지만 억지스러운 것(improbable possibility)'은 금지한다.\n"
        "- 허용: 주인공이 초인적 노력으로 불가능한 상황을 뒤집는다 (인과 논리가 있다)\n"
        "- 금지: 우연히 적의 계획서를 발견한다 (인과 논리가 없다)\n"
        "모든 비트를 검증하라: 이 전개가 우연에 의존하는가?"
    ),
    "drop_in_middle": (
        "[Curtis Drop in the Middle]\n"
        "관객을 설명 없이 이야기 한가운데에 던져라.\n"
        "- 첫 장면은 대화의 중간, 사건의 중간, 관계의 중간에서 시작한다\n"
        "- 관객이 '무슨 상황이지?'를 스스로 추론하게 한다\n"
        "- 설정을 설명하는 첫 장면은 가장 약한 오프닝이다"
    ),
    "unified_plot_test": (
        "[Sorkin Unified Plot Test]\n"
        "이 비트를 완전히 삭제했을 때 전체 이야기가 작동하는가?\n"
        "- '작동한다' → 이 비트는 불필요하다. 삭제하거나 다른 비트와 병합하라.\n"
        "- '작동하지 않는다' → 이 비트는 필수다. 유지하라.\n"
        "모든 비트가 이 테스트를 통과해야 한다."
    ),
    "too_wet": (
        "[Curtis Too Wet 금지]\n"
        "캐릭터가 자신의 감정을 직접 말하거나 수행하는 장면을 경고한다.\n"
        "- 금지: '나는 화가 났다' → 관객에게 감정을 설명하는 것\n"
        "- 허용: 주인공이 아무 말 없이 컵을 내려놓는다. 손이 떨린다. → 관객이 분노를 읽는 것\n"
        "감정은 행동과 선택으로 보여줘야 한다. 서술자가 감정을 지목하면 Too Wet이다."
    ),
    "curtis_3pct": (
        "[Curtis 3% 법칙]\n"
        "톤은 3%만 빗나가도 정반대 영화가 된다.\n"
        "- 공포 영화에서 3% 과한 유머 → 코미디가 된다\n"
        "- 드라마에서 3% 과한 감상 → 멜로드라마가 된다\n"
        "- 액션에서 3% 과한 설명 → 다큐멘터리가 된다\n"
        "매 씬의 톤이 작품 전체 톤에서 벗어나는가를 검증하라."
    ),
    "emotion_chain": (
        "[Curtis 감정 연쇄]\n"
        "A장면의 마지막 감정이 B장면의 전제가 되어야 한다.\n"
        "- A장면: 분노로 끝남 → B장면: 분노의 여파 속에서 시작\n"
        "- A장면: 희망으로 끝남 → B장면: 그 희망이 배신당하면서 시작\n"
        "감정이 끊기는 장면 전환은 관객을 이야기 밖으로 내보낸다.\n"
        "매 비트 연결에서 감정 연쇄를 확인하라."
    ),

    # ── 관객 심리 6원칙 (v1.4 추가) ──
    "dramatic_irony": (
        "[Dramatic Irony — 관객이 더 많이 안다]\n"
        "관객이 캐릭터보다 더 많은 정보를 가질 때 긴장이 극대화된다.\n"
        "- 히치콕: '테이블 밑에 폭탄이 있다. 관객만 안다. 이것이 서스펜스.'\n"
        "- 적용: 관객에게 먼저 위험 정보를 주고, 캐릭터가 모르는 채 행동하게 하라.\n"
        "- 비트 설계 시: '이 비트에서 관객이 먼저 아는 정보는 무엇인가?'를 명시하라."
    ),
    "information_gap": (
        "[Information Gap — 호기심의 간극]\n"
        "호기심 = 내가 아는 것과 알고 싶은 것 사이의 간극.\n"
        "- 질문을 던지고, 바로 답하지 마라. 3~4비트 동안 간극을 유지하라.\n"
        "- 비트 설계 시: '이 비트에서 새로 열리는 질문은? 답이 지연되는 질문은?'"
    ),
    "zeigarnik_effect": (
        "[Zeigarnik Effect — 미완성이 기억에 남는다]\n"
        "끝나지 않은 것, 대답되지 않은 것이 관객을 붙잡는다.\n"
        "- 매 비트 끝에 미해결 질문 또는 중단된 행동을 남겨라.\n"
        "- 클리프행어는 이 원리의 가장 강한 형태."
    ),
    "pattern_violation": (
        "[Pattern & Violation — 패턴을 만들고 깨뜨려라]\n"
        "관객은 무의식적으로 패턴을 예측한다. 패턴이 깨질 때 쾌감(또는 공포).\n"
        "- 3번 반복하고 4번째에서 뒤집어라.\n"
        "- 비트 설계 시: '이 이야기에서 반복되는 패턴은? 어느 비트에서 깨뜨리는가?'"
    ),
    "delayed_gratification": (
        "[Delayed Gratification — 지연된 보상]\n"
        "관객이 원하는 것을 바로 주지 마라. 지연시킬수록 보상이 커진다.\n"
        "- 핵심 정보, 핵심 만남, 핵심 대결을 최대한 늦춰라.\n"
        "- 비트 설계 시: '관객이 가장 원하는 장면은? 그걸 몇 번째 비트까지 안 주는가?'"
    ),
    "mystery_box": (
        "[Mystery Box — 열리지 않은 상자]\n"
        "닫힌 상자가 열린 상자보다 매력적이다 (J.J. Abrams).\n"
        "- 모든 것을 설명하지 마라. 하나를 열면 다른 하나가 닫혀야 한다.\n"
        "- 비트 설계 시: '이 이야기의 비밀 상자는 몇 개이고, 각각 언제 열리는가?'"
    ),

    # ── 서브플롯 설계 원칙 (v1.4 추가) ──
    "subplot_design": (
        "[서브플롯 설계 원칙]\n"
        "B-Story = 테마의 통로. 메인플롯이 사건이라면, 서브플롯이 메시지를 운반한다.\n"
        "- 서브플롯은 1막 중후반(Beat 3~5)에 시작한다.\n"
        "- 서브플롯 인물은 주인공의 거짓 신념에 도전한다.\n"
        "- Midpoint 또는 클라이맥스에서 메인플롯과 충돌해야 한다.\n"
        "- 서브플롯이 메인과 합류하지 않고 따로 끝나면 가지치기다.\n"
        "- 서브플롯의 해결이 주인공의 최종 선택에 영향을 줘야 한다."
    ),
}


# ─── 공통 JSON 출력 규칙 ───
JSON_OUTPUT_RULES = """[출력 규칙]
- 유효한 단일 JSON만 출력. JSON 외 텍스트 금지.
- 후행 쉼표 금지. 한국어 작성.
- 대사는 작은따옴표('')만 사용. 쌍따옴표(") 사용 절대 금지.
- 문자열 안에 역슬래시(\\) 사용 금지.
- 문자열 내부 줄바꿈 대신 공백 사용."""

JSON_OUTPUT_RULES_STRICT = """[출력 규칙]
- 반드시 유효한 단일 JSON 객체만 출력한다.
- JSON 외 텍스트 금지. 주석 금지.
- 후행 쉼표(trailing comma) 금지.
- 모든 key는 쌍따옴표. 문자열 내부 줄바꿈 대신 공백.
- 한국어로 작성하되 전문 용어는 한글용어(English Term)로 병기.
- 모든 텍스트 필드는 1~2문장, 50자 이내로 압축. 장문 서술 절대 금지.
- 대사는 작은따옴표('')만 사용. 쌍따옴표(") 사용 절대 금지."""


# ═══════════════════════════════════════════════════
#  SYSTEM PROMPTS
# ═══════════════════════════════════════════════════

SYSTEM_RESEARCH = """당신은 콘텐츠 기획 리서처다.
아이디어와 장르를 기반으로 실화/뉴스와 기존 작품을 리서치한다.
관련 작품은 차별화 포인트 분석에 활용한다.

""" + JSON_OUTPUT_RULES_STRICT

SYSTEM_BRAINSTORM_CARDS = """당신은 글로벌 콘텐츠 시장을 이해하는 Development Producer이자 Script Architect다.
기획자의 아이디어를 개발 가능한 컨셉 카드로 정렬한다.
이야기(story)와 분위기(mood)를 구분한다.
타겟 시장과 포맷을 반영한다.
리서치가 있으면 참고하되 기존작을 모방하지 않는다.

""" + SORKIN_CURTIS["but_except_test"] + "\n\n" + JSON_OUTPUT_RULES_STRICT

SYSTEM_BRAINSTORM_ANALYSIS = """당신은 Development Producer다.
Brainstorm Top 3를 기반으로 시장성/차별화/타이밍을 분석하고 Gate A를 채점한다.

""" + SORKIN_CURTIS["but_except_test"] + """

[Gate A 채점 시 추가 검증]
- 각 컨셉의 로그라인에 BUT/EXCEPT가 있는가? 없으면 conflict_one_line 감점.
- 로그라인이 'and then' 나열형이면 originality 감점.

""" + JSON_OUTPUT_RULES_STRICT


def build_system_core(genre: str) -> str:
    """Core Build 시스템 프롬프트 — 장르 인식 + Intention & Obstacle"""
    genre_rules = get_genre_rules(genre)
    return f"""당신은 헐리우드 메이저 스튜디오의 Development Producer이자 Script Architect다.
Brainstorm에서 선정된 컨셉을 기반으로 Core Build를 수행한다.
로그라인을 고정하고, 기획의도와 주제를 정리하고, 세계관과 캐릭터를 설계하고,
주인공의 Goal / Need / Strategy를 확정한다.

[장르: {genre}]
{json.dumps(genre_rules, ensure_ascii=False)}

[장르 인식]
- 선택된 장르의 필수 요소가 Core Build에 반영되어야 한다.
- 로그라인에 장르적 Hook이 포함되어야 한다.
- 캐릭터 설계에 장르적 역할이 반영되어야 한다.

{SORKIN_CURTIS["intention_obstacle"]}

{SORKIN_CURTIS["but_except_test"]}

{JSON_OUTPUT_RULES_STRICT}
- 작가의 고유한 아이디어를 훼손하지 않는다.
- 필수 캐릭터 4인(protagonist/antagonist/ally/mirror)은 characters 배열에.
- 추가 캐릭터(0~4인)는 extended_characters 배열에. 역할명은 자유 (catalyst/subplot_lead/mentor/rival/informant 등).
- 영화는 총 4~5명, 미니시리즈는 6~8명이 적정. 이야기가 필요로 하는 만큼 생성."""


SYSTEM_CORE_GATE = """당신은 Development Producer다.
Core Build 결과를 채점한다.
점수는 0.0~10.0, 소수점 1자리 반올림.
""" + JSON_OUTPUT_RULES_STRICT


def build_system_char_bible(genre: str, fmt: str, others_str: str) -> str:
    """Character Bible 시스템 프롬프트 — Tactics = Character"""
    return f"""당신은 헐리우드 A-list 캐릭터 디자이너이자 심리학 전문가다.
Core Build에서 만든 기본 캐릭터 1인을 '캐릭터 바이블' 수준으로 확장한다.

[목표]
Writer Engine(시나리오 생성 AI)이 80~120씬 동안 이 인물을 일관되게 쓸 수 있도록,
내면·외형·말투·관계·변화를 정밀하게 설계한다.

{SORKIN_CURTIS["tactics_character"]}

[작성 원칙]
1. 백스토리는 현재 행동의 원인이 되어야 한다.
2. 비밀(secret)은 플롯의 전환점이 될 수 있어야 한다.
3. 말투(speech_pattern)는 구체적 규칙으로 — '거칠다' 같은 추상어 금지.
4. 대사 샘플(sample_lines)은 실제 시나리오에 바로 넣을 수 있는 수준.
5. 관계별 태도(relationship_attitudes)는 상대 캐릭터({others_str})에 따라 달라지는 행동 명시.
6. 변화 궤적(arc_detail)은 1막/미드포인트/클라이맥스 3단계로 구체적.
7. tactics는 이 인물이 장애물을 넘기 위해 선택하는 전술 3가지. 전술의 차이가 캐릭터의 차이다.
8. 장르: {genre} / 포맷: {fmt}

{SORKIN_CURTIS["too_wet"]}

{JSON_OUTPUT_RULES}"""


# Character Bible JSON 스키마 (tactics 포함)
CHAR_BIBLE_SCHEMA = """{
  "role": "ROLE_PLACEHOLDER",
  "name": "NAME_PLACEHOLDER",
  "age": "나이",
  "appearance": "외형·첫인상 3문장",
  "occupation": "직업/사회적 위치",
  "goal": "이 인물의 욕망 (Core에서 가져와 확장)",
  "need": "진짜 결핍 (본인은 모르는 것)",
  "flaw": "치명적 결점",
  "backstory": "과거사 5문장 — 왜 지금 이런 사람인가",
  "secret": "비밀 1개 — 이것이 밝혀지면 플롯이 바뀐다",
  "belief": "핵심 신념 — 절대 양보 못하는 가치",
  "fear": "가장 두려워하는 것",
  "tactics": [
    "장애물을 넘는 전술 1 — 이 인물만의 방식",
    "장애물을 넘는 전술 2 — 상황이 악화될 때",
    "장애물을 넘는 전술 3 — 최후의 수단"
  ],
  "habits": ["반복되는 행동 패턴 3개"],
  "speech_pattern": [
    "말투 규칙 1",
    "말투 규칙 2",
    "말투 규칙 3"
  ],
  "sample_lines": {
    "normal": "평상시 대사",
    "angry": "분노 시 대사",
    "vulnerable": "취약한 순간 대사"
  },
  "relationship_attitudes": [
    "→ 캐릭터명: 관계 + 태도 변화"
  ],
  "arc_detail": {
    "act1_end": "1막 끝 상태 2문장",
    "midpoint": "미드포인트 상태 2문장",
    "climax": "클라이맥스 상태 2문장"
  },
  "strategy": "행동 방식",
  "dialogue_tone": "대사톤 키워드 3개"
}"""

CHAR_BIBLE_RULES = """규칙:
- 이 캐릭터 1인분만 JSON 객체로 출력. 배열 아님.
- backstory는 반드시 5문장 이상.
- tactics는 반드시 3개. 이 인물만의 독특한 문제 해결 방식.
- sample_lines 대사는 실제 시나리오 품질.
- speech_pattern은 추상어 금지. 구체적 규칙만."""


def build_system_structure_story() -> str:
    """Structure Build Story 시스템 프롬프트 — 서브플롯 설계 포함 (v1.4)"""
    return """당신은 헐리우드 수준의 Story Architect다.
Core Build 결과를 기반으로 시놉시스와 스토리라인을 설계한다.
주인공의 Goal/Need/Strategy가 모든 전개의 중심축이 되어야 한다.

""" + SORKIN_CURTIS["probable_impossibility"] + "\n\n" + SORKIN_CURTIS["subplot_design"] + "\n\n" + JSON_OUTPUT_RULES_STRICT


def build_system_structure_diagnosis() -> str:
    """Structure Diagnosis v1.4 — 관객 심리 설계 + 서브플롯 충돌 포함"""
    return """당신은 헐리우드 수준의 Structure Analyst다.
시놉시스와 스토리라인을 기반으로 구조 진단과 캐릭터 변화를 설계한다.

[Probable Impossibility 검증]
- 억지 우연으로 해결되는 비트 → status '약함', note에 'Probable Impossibility 위반'
- 비트를 빼도 작동하는 비트 → status '약함', note에 'Unified Plot Test 미통과'

[관객 심리 설계 — 비트별 필수 체크]
- 각 비트에 대해 아래를 설계하라:
  1. dramatic_irony: 이 비트에서 관객이 먼저 아는 정보는? (없으면 빈 문자열)
  2. open_question: 이 비트에서 새로 열리는 질문은? (Information Gap)
  3. unresolved: 이 비트 끝에 미해결로 남는 것은? (Zeigarnik)
  4. pattern_point: 반복 패턴이 형성되거나 깨지는 포인트인가? (Y/N)
  5. delayed_reveal: 관객이 원하는 정보/만남/대결을 이 비트에서 안 주는가? (Y/N)

[서브플롯 설계]
- B-Story가 어느 비트에서 시작하는지 명시하라 (Beat 3~5 권장).
- B-Story와 A-Story가 충돌하는 비트를 명시하라 (Midpoint 또는 클라이맥스).
- B-Story가 테마를 어떤 각도에서 비추는지 1문장.

""" + SORKIN_CURTIS["probable_impossibility"] + "\n\n" + SORKIN_CURTIS["unified_plot_test"] + "\n\n" + JSON_OUTPUT_RULES_STRICT


SYSTEM_STRUCTURE_GATE = """당신은 Development Producer다.
Structure Build 결과를 채점한다.
점수는 0.0~10.0, 소수점 1자리 반올림.

[추가 검증]
- 억지 우연에 의존하는 전환점이 있으면 해당 항목 감점.
- ending_inevitable_surprising: 결말이 '필연적이면서 놀라운가' — 우연에 의한 해결이면 0점.
""" + JSON_OUTPUT_RULES_STRICT


def build_system_scene_design(genre: str) -> str:
    """Scene Design v1.4 — Drop in the Middle + Hook/Punch + 관객 심리 + 서브플롯"""
    genre_rules = get_genre_rules(genre)
    return f"""당신은 헐리우드 최고 수준의 Scene Architect다.
Structure Build 결과를 기반으로 핵심 장면(Key Scene)을 설계한다.
'Show, don't tell' 원칙을 따른다.
모든 장면은 설명이 아닌 행동, 선택, 반전으로 드라마를 구현해야 한다.

[장르: {genre}]
{json.dumps(genre_rules, ensure_ascii=False)}

{SORKIN_CURTIS["drop_in_middle"]}

{SORKIN_CURTIS["dramatic_irony"]}

{SORKIN_CURTIS["information_gap"]}

{SORKIN_CURTIS["mystery_box"]}

[Hook & Punch 규칙]
- HOOK: 매 장면 끝에 관객이 다음 장면을 보지 않을 수 없는 질문/위협/기대를 심는다.
- PUNCH: 장면의 가장 강한 순간 — 대사 한 마디, 행동 하나, 또는 침묵이 씬의 온도를 급변시킨다.
- SETPIECE: 장르의 정체성을 정의하는 대형 장면. 관객이 이 영화를 기억할 때 떠올리는 장면.

{SORKIN_CURTIS["subplot_design"]}

{JSON_OUTPUT_RULES}
- 각 필드 1~2문장, 40자 이내.
- 대사는 작은따옴표만 사용."""


def build_system_treatment(genre: str, act_label: str, fmt: str = "", b_story_context: str = "") -> str:
    """Treatment v1.6 — SCOPE MANDATE + 5단계 다중 씬 구조 + B-Story"""
    genre_rules = get_genre_rules(genre)
    genre_rules_text = json.dumps(genre_rules, ensure_ascii=False)

    is_series = is_series_format(fmt)

    if is_series:
        scope_spec = "에피소드당 40~50분 기준, 1비트 = 10~20분 분량 = 4~6개의 독립된 씬"
        min_chars = "4000"
        max_chars = "6000"
    else:
        scope_spec = "영화 120분 기준, 1비트 = 7~10분 분량 = 3~5개의 독립된 씬"
        min_chars = "2500"
        max_chars = "4000"

    series_block = ""
    if is_series:
        series_block = """
[미니시리즈 필수 규칙]
- 이 트리트먼트는 미니시리즈다. 영화가 아니다.
- 매 에피소드의 마지막 비트는 반드시 CLIFFHANGER로 끝나야 한다.
- 매 에피소드에 A-Story + B-Story 진행이 반드시 공존해야 한다.
- 에피소드 첫 비트는 이전 에피소드 클리프행어의 즉각적 결과로 시작한다 (EP1 제외).
- B-Story 시간축이 매 에피소드마다 자막/뉴스/대사로 표시되어야 한다.
"""

    b_story_block = ""
    if b_story_context:
        b_story_block = f"""
[B-Story 정보 — 반드시 매 비트에 반영하라]
{b_story_context}
- B-Story는 배경이 아니라 A-Story에 압박을 가하는 독립된 플롯이다.
- B-Story의 시간축 변화가 매 비트에서 주인공의 선택을 제한하거나 강요해야 한다.
- B-Story 진행이 narrative 안에 자연스럽게 녹아야 한다 (뉴스 화면, 거리 풍경, 대화 등).
"""

    return f"""당신은 한국 최고 수준의 시나리오 작가다.
{act_label}의 트리트먼트를 비트 단위 줄글로 작성한다.

[SCOPE MANDATE — 가장 중요한 규칙]
★ 1비트 = 1씬이 아니다. 1비트 = 여러 씬이다. ★

{scope_spec}.
비트 안에서 시간이 경과해야 하고, 장소가 바뀌어야 하고, 여러 인물이 각각 행동해야 한다.

하나의 씬을 상세히 묘사하는 것은 '비트 집필'이 아니라 '씬 집필'이다. 그것은 실패다.

  나쁜 예 (1씬만 상세히 쓴 것 — 실패):
    '원룸. 새벽 3시. 재중이 USB를 발견한다. 열어볼까 고민한다. 열어본다. 충격. 결심.'
    → 한 장소, 한 시간대, 한 인물. 이것은 비트가 아니라 씬 하나다.

  좋은 예 (여러 씬으로 구성된 비트):
    [씬1] 묘적사 브리핑룸 — 최이호 앞에서 임무 보고. 긴장.
    [씬2] 세운상가 복도 — 나현준이 USB를 건넨다. 경고.
    [씬3] 재중의 원룸, 새벽 — 파일 확인. 아버지 사망 결재에 최이호 서명.
    [씬4] B-Story: TV 뉴스 — 대선 D-59. 여당 후보 지지율 1위.
    [씬5] 다음 날 아침, 브리핑룸 — 재중이 평소와 같은 얼굴로 최이호 앞에 선다.
    → 4개 장소, 시간 경과(낮→새벽→아침), 3명 이상 등장, A+B 스토리.

[SCOPE CHECK — 매 비트를 쓴 후 반드시 확인]
□ 최소 3~5개의 독립된 씬이 있는가? (각각 다른 장소 또는 다른 시간)
□ 최소 2개의 다른 장소가 있는가?
□ 최소 2명의 다른 인물이 각각 행동하는가?
□ 비트 안에서 시간이 경과하는가? (같은 시간대에 머물면 안 된다)
□ A-Story 진행 + B-Story 최소 1씬이 있는가?
□ 비트 시작 상황과 비트 끝 상황이 명확히 달라지는가?

[5단계 서술 구조 — 비트 전체에 적용 (개별 씬이 아니라 비트 전체)]
이 비트의 전체 흐름이 아래 5단계를 따라야 한다:
① STATUS QUO — 비트 시작 씬: 현재 상황과 인물 위치
② EVENT — 중간 씬들: 상황을 바꾸는 사건이 발생
③ DECISION — 인물이 선택하는 씬
④ CONSEQUENCE — 선택의 결과가 드러나는 씬
⑤ NEW STATUS QUO + HOOK — 비트 마지막 씬: 상황이 바뀌고, 다음 비트로의 미끼
→ 5단계가 3~5개의 다른 씬에 자연스럽게 배분된다.
→ 5단계를 1개 씬 안에서 다 처리하면 실패다.

[절대 금지 패턴]
❌ 한 장소에서 한 인물이 혼자 있는 것으로 비트 전체를 채우는 것
❌ 1분짜리 장면 하나를 2000자로 늘려 쓰는 것 (디테일 과잉, 스코프 부족)
❌ 인물이 '앉아 있다→생각한다→일어선다'만 반복하는 것
❌ '관객은 ~을 안다', '이것이 ~의 전부다' 같은 서술자 해설
❌ STATUS QUO와 NEW STATUS QUO가 동일한 비트

[작성 규칙]
1. 서술체, 현재형. 대사는 작은따옴표만.
2. 각 씬 전환은 줄바꿈 없이 서술 안에서 자연스럽게 '장소. 시간.' 형식으로 전환.
3. 인물 첫 등장 시 이름(나이).
4. 매 비트 {min_chars}~{max_chars}자.
5. PUNCH: 매 비트 안에 최소 1개.
{series_block}
{b_story_block}
[관객 심리]
6. Dramatic Irony: 관객에게 먼저 정보를 줘라.
7. Information Gap: 매 비트 최소 1개 열린 질문 유지.
8. Delayed Gratification: 관객이 원하는 장면을 늦춰라.

{SORKIN_CURTIS["unified_plot_test"]}

{SORKIN_CURTIS["too_wet"]}

{SORKIN_CURTIS["emotion_chain"]}

[장르 규칙: {genre}]
{genre_rules_text}

{JSON_OUTPUT_RULES}"""


def build_system_tone_document(genre: str, fmt: str) -> str:
    """Tone Document 시스템 프롬프트 — Curtis 3% 법칙 + 감정 연쇄"""
    return f"""당신은 헐리우드 최고 수준의 톤 디자이너(Tone Designer)이자 비주얼 스토리텔러다.
기획개발 패키지를 기반으로, Writer Engine이 시나리오를 쓸 때 참조할 '톤 & 연출 문서'를 작성한다.

[목표]
이 문서가 있으면 AI가 80~120씬 동안 일관된 톤·분위기·연출 스타일을 유지할 수 있다.

[장르: {genre} / 포맷: {fmt}]

{SORKIN_CURTIS["curtis_3pct"]}

{SORKIN_CURTIS["emotion_chain"]}

{JSON_OUTPUT_RULES}"""


# ═══════════════════════════════════════════════════
#  JSON SCHEMAS
# ═══════════════════════════════════════════════════

# ─── Tone Document JSON 스키마 ───
TONE_DOC_SCHEMA = """{
  "visual_style": {
    "camera_philosophy": "카메라 철학 2~3문장",
    "color_palette": "색감 팔레트 2문장",
    "lighting_rule": "조명 규칙 1~2문장",
    "signature_shot": "이 작품만의 시그니처 쇼트 1~2문장"
  },
  "pacing": {
    "overall": "전체 페이싱 철학 1문장",
    "act1_tempo": "1막 템포 1문장",
    "act2_tempo": "2막 템포 1문장",
    "act3_tempo": "3막 템포 1문장",
    "dialogue_density": "대사 vs 지문 비율 (예: 지문 65% / 대사 35%)"
  },
  "dialogue_rules": {
    "overall_tone": "대사 전체 톤 1문장",
    "subtext_rule": "서브텍스트 규칙 1~2문장",
    "silence_usage": "침묵/비언어 활용 규칙 1문장",
    "too_wet_guard": "Too Wet 방지 규칙 — 캐릭터가 감정을 직접 말하는 대사를 어떻게 방지하는가 1~2문장",
    "forbidden_phrases": ["이 작품에서 절대 쓰지 않을 대사 패턴 3개"]
  },
  "motifs": {
    "recurring_objects": ["반복 소품/모티프 3~4개 — 각각 의미 포함"],
    "recurring_locations": ["반복 장소 2~3개 — 각각 감정적 의미"],
    "weather_mood": "날씨/계절 활용 규칙 1~2문장"
  },
  "music_sound": {
    "score_direction": "음악 방향 1~2문장",
    "silence_scenes": "무음 사용 규칙 1문장",
    "diegetic_sounds": "작품 내 소리 활용 2~3개"
  },
  "emotion_chain": {
    "act1_to_act2": "1막 마지막 감정 → 2막 첫 장면 전제 1문장",
    "midpoint_shift": "미드포인트 감정 전환 규칙 1문장",
    "act2_to_act3": "2막 마지막 감정 → 3막 첫 장면 전제 1문장"
  },
  "tone_guardrail": {
    "three_pct_rule": "이 작품에서 3%만 넘으면 안 되는 톤 요소 2~3개",
    "tone_ceiling": "이 작품의 톤 상한선 1문장 (예: 유머는 여기까지, 폭력은 여기까지)",
    "tone_floor": "이 작품의 톤 하한선 1문장 (예: 감정은 최소 이 정도는 유지)"
  },
  "forbidden": [
    "이 작품에서 절대 하지 말아야 할 연출/톤/대사 규칙 5개"
  ],
  "reference_films": [
    {"title": "참고작품 1", "reason": "이유 1문장"},
    {"title": "참고작품 2", "reason": "이유 1문장"},
    {"title": "참고작품 3", "reason": "이유 1문장"}
  ],
  "writer_instruction": "Writer Engine에게 보내는 최종 지시 3~5문장"
}"""

# ─── Treatment Beat 스키마 (v1.5: 5단계 서술 구조 + 에피소드 태그) ───
TREATMENT_BEAT_SCHEMA_TEMPLATE = """{{
  "act": {act_number},
  "beats": [
    {{
      "beat_no": 0,
      "beat_name": "비트 이름",
      "episode": "이 비트가 속하는 에피소드 (미니시리즈일 때만. 영화면 빈 문자열)",
      "narrative": "3~5개 씬으로 구성된 비트 줄글. 영화 2500~4000자 / 시리즈 4000~6000자. 씬 전환은 서술 안에서 자연스럽게.",
      "event_summary": "이 비트의 핵심 사건 1문장 — narrative의 ②단계 요약",
      "decision_summary": "인물의 핵심 선택 1문장 — narrative의 ③단계 요약",
      "consequence_summary": "선택의 결과 1문장 — narrative의 ④단계 요약",
      "status_change": "비트 시작 상태 → 비트 끝 상태 (반드시 달라야 함)",
      "punch": "이 비트에서 가장 강한 순간 1문장",
      "b_story_beat": "B-Story 진행 상태 1문장 (해당 없으면 빈 문자열)",
      "cliffhanger": "에피소드 마지막 비트일 경우 클리프행어 1문장 (아니면 빈 문자열)",
      "dramatic_irony": "관객이 먼저 아는 정보 (없으면 빈 문자열)",
      "open_question": "열리는 새 질문 1문장"
    }}
  ]
}}"""

TREATMENT_BEAT_RULES_TEMPLATE = """규칙:
- beats 정확히 {beat_count}개.
- ★ SCOPE MANDATE: 1비트 = 1씬이 아니다. 1비트 안에 최소 3~5개 씬이 있어야 한다. ★
- narrative는 5단계 구조를 비트 전체에 걸쳐 배분: ①시작씬 → ②사건씬 → ③선택씬 → ④결과씬 → ⑤변화+훅씬.
- 5단계를 1개 씬 안에서 다 처리하면 실패다. 5단계가 3~5개 다른 씬에 배분되어야 한다.
- SCOPE CHECK: 최소 2개 장소, 2명 이상 인물, 비트 안에서 시간 경과 필수.
- event_summary / decision_summary / consequence_summary는 narrative 핵심 요약.
- status_change: '시작→끝'이 동일하면 실패. 반드시 달라야 한다.
- b_story_beat: B-Story가 있으면 매 비트에서 진행 명시.
- cliffhanger: 에피소드 마지막 비트에만. 다음 화 즉시 재생하게 만드는 질문/위협/반전.
- Too Wet 금지: 감정 직접 서술 금지. 행동으로.
- 1분짜리 장면 하나를 상세히 묘사해서 분량을 채우지 마라. 비트는 7~20분의 스크린타임을 커버한다."""

# ─── Scene Design 스키마 (v1.4: hook/punch/setpiece + information_gap/mystery_box/subplot_tag) ───
SCENE_DESIGN_SCHEMA = """{
  "key_scenes": [
    {
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
      "information_gap": "이 장면에서 새로 열리는 질문 1문장 (없으면 빈 문자열)",
      "mystery_box": "이 장면에서 감춰지는 것 — 관객이 궁금해할 것 1문장 (없으면 빈 문자열)",
      "subplot_tag": "A(메인) / B(서브) / A+B(교차) / 빈 문자열",
      "hook": "이 장면 끝에서 관객을 다음 장면으로 끌어당기는 질문/위협/기대 1문장",
      "punch": "이 장면에서 가장 강한 순간 — 온도가 급변하는 대사/행동/침묵 1문장",
      "is_setpiece": "Y 또는 N — 장르를 정의하는 대표 장면인가",
      "connection": "다음 장면 연결 에너지 1문장"
    }
  ],
  "scene_map_summary": {
    "total_scenes": 0,
    "act1_scenes": "1막 장면 번호 목록",
    "act2a_scenes": "2막 전반 장면 번호 목록",
    "act2b_scenes": "2막 후반 장면 번호 목록",
    "act3_scenes": "3막 장면 번호 목록",
    "must_see_scenes": "반드시 살려야 할 핵심 3장면 번호",
    "subplot_start_scene": "서브플롯이 시작되는 장면 번호",
    "subplot_collision_scene": "서브플롯과 메인플롯이 충돌하는 장면 번호"
  }
}"""

SCENE_DESIGN_RULES = """규칙:
- key_scenes는 15~18개
- dramatic_action이 핵심. 인물이 무엇을 '하는지'를 쓸 것
- turning_point 있는 장면과 없는 장면이 자연스럽게 섞일 것
- dramatic_irony는 해당 장면에 극적 아이러니가 있을 때만 작성. 없으면 빈 문자열
- key_line은 이 장면 전체를 압축하는 대사 한 마디. 반드시 '캐릭터명: 대사' 형식
- visual_direction은 촬영 감독 전달 수준으로
- hook은 매 장면 필수. 관객이 다음 장면을 보지 않을 수 없게 만드는 미끼
- punch는 장면의 가장 강한 순간. 없으면 그 장면은 존재 이유가 없다
- is_setpiece가 Y인 장면이 최소 3개 이상. 이 장면들이 이 영화의 포스터가 된다
- 첫 장면(scene_no 1)은 Drop in the Middle 원칙 — 설명 없이 이야기 한가운데에 관객을 던져라
- information_gap: 장면 설계 시 '관객이 이 장면 후 궁금해할 것'을 명시. 없으면 빈 문자열
- mystery_box: '이 장면에서 일부러 안 보여주는 것'을 명시. 안 보여주는 것이 보여주는 것보다 강하다
- subplot_tag: 서브플롯 씬에 B 태그. 메인+서브 교차 씬에 A+B. 서브플롯 씬이 전체의 20~30% 되도록
- 서브플롯이 메인플롯의 테마를 다른 각도에서 비춰야 한다. 테마와 무관한 서브플롯은 삭제"""


# ─── 보조 함수 시스템 프롬프트 ───
SYSTEM_STRUCTURE_PROSE = "당신은 숙련된 시나리오 작가다. 유효한 단일 JSON만 출력. 후행 쉼표 금지."
SYSTEM_TREATMENT_META = "당신은 Development Producer다. 유효한 단일 JSON만 출력. 후행 쉼표 금지."
SYSTEM_TREATMENT_GATE = "당신은 Development Producer다. 유효한 단일 JSON만 출력. 후행 쉼표 금지. 점수 0.0~10.0."
