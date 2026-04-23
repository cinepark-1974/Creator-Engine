"""
👖 BLUE JEANS Creator Engine — Prompt Library

╔══════════════════════════════════════════════════════════╗
║  VERSION: v2.3.8                                         ║
║  BUILD DATE: 2026-04-22                                  ║
║  STATUS: Production                                      ║
╚══════════════════════════════════════════════════════════╝

★ 버전 확인 방법 ★
- 파일 최상단 VERSION 블록 확인
- Streamlit UI 좌측 사이드바 하단 "Engine Info" 확인
- README.md 최상단 확인
세 곳의 버전이 일치해야 정상.

─────────────────────────────────────────────────────────
v2.3.8 업데이트 (2026-04-22) — Core Build 필드 Treatment 전파 완성
                                   (기획의도+세계관+자가진단+리서치)
─────────────────────────────────────────────────────────

[문제 진단 — Mr. MOON 지적]
"기본적으로 코어빌드에 많은 걸 넣어두었는데 트리트먼트로 연결되는지야.
리서치 기능도 넣어놔서 핍진성을 높이려고 했단 말이지"

실증 확인 결과 Core Build에서 생성되지만 Treatment 단계에서 휘발되던 필드:
  · project_intent (기획의도, 주제, 톤앤매너) — 매 비트 주제 이탈 위험
  · world_build (시대, 공간, 규칙) — 시대 오류 방지 실패 (v2.3.7 Gate에만 있었음)
  · genre_expectation_check.weak_zones — Core 자가 진단 경고 사장
  · research (실제 사건 + 기존 작품) — 핍진성 설계 의도 작동 안 함

Mr. MOON이 〈바타비아〉 포함 대부분 프로젝트에서 Research를 사용하는데,
이 데이터가 Brainstorm/Core까지만 전달되고 Treatment부터 Writer Engine까지
전달이 끊김. 결과:
  · 표절 방지 신호가 Writer Engine까지 전달 안 됨
  · 실제 사건 디테일이 시나리오에 반영 안 됨
  · Core Build의 자가 진단 약점 구간이 Treatment에서 무시됨

[v2.3.8 해결책 — main.py의 call_treatment_beats() 대폭 확장]

[A] 함수 시그니처에 research=None 추가
[B] user_prompt에 4개 전파 블록 신규 삽입:

  [1] project_intent_block — 주제·피치·톤앤매너
      "매 비트가 수렴해야 할 주제" 명시
  
  [2] world_build_block — 시대/공간/규칙/터부/시각 키워드
      "시대 배경에 존재하지 않는 기술·제도·문화 포함 금지" 명시 (생성 단계)
  
  [3] genre_warning_block — Core Build 자가 진단 경고
      weak_zones 리스트와 climax_verdict를 Treatment가 참조
      CLIMAX_FAIL 시 장르 약속에 맞는 3막 재설계 강제
  
  [4] research_block_treatment — 실제 사건 상위 5개 + 기존 작품 제목
      · real_events: 제목/연도/요약/활용 가능성 → 비트 디테일 원천
      · existing_works: 제목 리스트 → 표절 방지 참조
      · key_insight: Research 핵심 통찰

[C] 호출부 3곳(1막/2막/3막) 모두 research=project.get("research") 전달

[프롬프트 토큰 관리]
Research 전달 시 과부하 방지 장치:
  · real_events 상위 5개만 (요약 150자 제한, 활용 100자 제한)
  · existing_works 상위 7개 제목만 추출
  · 불필요한 필드 제외

이로써 Mr. MOON이 설계하신 전 엔진 구조가 Writer Engine 직전까지
휘발 없이 전달됨. Research 기능이 핍진성 강화 + 표절 방지 두 역할을
Treatment 생성 단계에서 실제 작동.

─────────────────────────────────────────────────────────
v2.3.7 업데이트 (2026-04-22) — 시대 고증 검증 추가
─────────────────────────────────────────────────────────

[문제 진단 — Mr. MOON 지적]
v2.3.6의 logic_consistency 검증 축이 "세계관 규칙"을 본다고 했지만
시대 고증(period consistency)이 명시되지 않음. 예:
  · 1980년대 설정인데 Treatment에 스마트폰·AI 로봇 등장
  · 조선시대 배경인데 사진·기차 언급
  · 1995년 배경인데 카카오톡 사용
이런 시대 오류를 현재 엔진이 감지 못 함.

HISTORICAL_FILM_RULES는 '역사영화' 체크 시에만 주입되는데,
1980년대 한국 드라마 같은 '근현대 배경'은 역사영화로 체크 안 되므로
시대 고증 검증이 완전히 빠짐.

[v2.3.7 해결책]
모든 작품(역사영화 체크 여부 무관)에 시대 고증 검증 적용:

[A] Treatment 시스템 프롬프트에 시대 고증 섹션 추가:
  · 시대별 주요 금지 요소 목록 (1980년대~2022년 주요 기술 도입 시점)
  · 역사 배경 시대 고증 기준
  · 미래 SF 배경 시대 일관성
  · 매 비트 자가 체크 항목

[B] call_treatment_gate()에 world_build 정보 전달:
  · world_build.time (시대)
  · world_build.space (공간)
  · world_build.rules (세계관 규칙)
  → Gate E가 실제 Treatment 내용과 대조 검증 가능

[C] Gate E 채점 축 7개 → 8개 확장:
  · 신규: period_consistency (시대 고증)
  · 신규 feedback 필드: period_check_feedback
  · critical_issues에 시대 고증 오류 비트 번호 기록
  · period_consistency가 4.0 미만이면 "전면 재작성 권고" 자동 출력

[D] SYSTEM_TREATMENT_GATE 프롬프트 강화:
  · 시대별 금지 요소 상세 가이드 주입
  · 역사·현대·미래 3가지 케이스별 검증 기준 명시

이로써 "Core Build에서 1980년대 설정한 작품이 Treatment에서
스마트폰 쓴다" 같은 시대 오류가 생성 단계와 검증 단계 모두에서 방지됨.

─────────────────────────────────────────────────────────
v2.3.6 업데이트 (2026-04-22) — 장르/BJND/POV/적대자 Treatment 전파 +
                                   Gate E 실제 내용 논리 검증
─────────────────────────────────────────────────────────

[문제 진단 — Mr. MOON이 발견한 엔진 구조적 공백]
Core Build까지 공들여 설계한 장르 재미·서사동력·시선·적대자 규칙이
Treatment 단계에서 전부 휘발되고 있었음.

- GENRE_FUN_ALIVE 체크리스트: Core Build만 주입 → Treatment 미주입
- BJND 4축 자가 검증: Core Build만 주입 → Treatment 미주입
- POV 정치학: Core Build만 주입 → Treatment 미주입
- ANTAGONIST_BJND (거울 관계): Core Build만 주입 → Treatment 미주입

결과: 〈바타비아 피의 계약〉 결함 4가지가 여기서 발생
  ① 2막 후반 호러 공포 부족 (호러 체크리스트 휘발)
  ② 엔딩 이미지 애매 (BJND 4축·Ending Payoff 검증 공백)
  ③ 유령 인식 범위 논리 비약 (논리 검증 부재)
  ④ 두꾼 긴장감 소실 (PROVOCATION 관리 휘발)

추가 문제: Treatment Gate(Gate E)가 글자 수만 봄. 실제 내용 미검증.
→ 모든 결함이 채점 없이 통과.

[v2.3.6 해결책]

[A] build_system_treatment() 수정 — 4개 핵심 모듈 주입
  · GENRE_FUN_ALIVE (장르 체크리스트 매 비트 실시간 체크)
  · bjnd_four_axis (BJND 4축)
  · POV_POLITICS (씬별 POV 선택)
  · ANTAGONIST_BJND (빌런 거울 관계)
  추가: 호러 Treatment 특별 지시 (2막 후반 공포 장면 최소 2개+,
        유령 인식 범위 명시, 위협 요소 반복 등장 누적)
  추가: 로맨틱 코미디 Treatment 특별 지시 (Fun and Games 3개+,
        클라이맥스 로맨스 완성 강제, 웃음+설렘 각 5회+)

[B] call_treatment_gate() 수정 — 실제 내용 전달
  · 이전: 비트별 "글자 수(chars)"만 Gate에 전달
  · 수정: 각 비트의 narrative 요약(500자) + Core Build 참조(Strategy,
          Ending Payoff) + 장르 정보를 모두 전달
  · Gate E 채점 축 4개 → 7개로 확장:
    - 기존: cinematic_reading / scene_emotion_match / beat_completeness
           / screenplay_ready
    - 신규: genre_expectation_alignment (장르 기대 정합)
           ending_coherence (Core Build Ending Payoff와 실제 엔딩 정합)
           logic_consistency (세계관 규칙/캐릭터 일관성/긴장 요소 유지)
  · critical_issues 배열에 문제 비트 번호 + 짧은 진단 기록

[C] SYSTEM_TREATMENT_GATE 프롬프트 대폭 강화
  · 한 줄(50자) → 검증 기준 체계 (1800자)
  · 장르별 체크 기준 (호러 공포 장면 / 로코 클라이맥스 / 스릴러 정보 비대칭
    / 액션 Setpiece 실재 등) 명시
  · 엔딩 정합 / 논리 일관성 검증 기준 명시
  · 6.0 미만 시 "재생성 권고" 자동 출력

이로써 Core Build의 설계 품질이 Treatment 단계에서 휘발되지 않고
Writer Engine으로 전달됨. Mr. MOON 표현: "장르적 재미 법칙이 Treatment에
적용되지 않으면 Writer Engine이 가동이 안 된다" → 해결.

─────────────────────────────────────────────────────────
v2.3.5 업데이트 (2026-04-22) — 프로젝트 JSON 저장/불러오기
─────────────────────────────────────────────────────────

[문제 진단]
Streamlit Cloud 세션이 끊어지거나 브라우저를 닫으면 프로젝트 데이터가
전부 날아감. 수 시간에 걸쳐 Core~Scene Design까지 완료한 프로젝트도
세션 종료 시 복구 불가능. Mr. MOON 실사용 시나리오:
  · Scene Design까지 완료 (2~3시간 소요)
  · 컴퓨터 종료
  · 다음 날 Treatment 실행하려니 전부 다시 시작해야 함

[v2.3.5 해결책]
main.py에 프로젝트 JSON 저장/불러오기 기능 신설:

1. 헬퍼 함수 3개 추가 (main.py):
   · _get_project_stage() — 프로젝트의 완료 단계 파악
   · save_project_to_json() — project dict 전체 직렬화
   · load_project_from_json() — JSON에서 project 복원 + 검증

2. JSON 저장 버튼 3곳에 배치:
   · Scene Design 완료 후 (Treatment 전 주요 체크포인트)
   · Treatment 완료 후 (Tone 전)
   · Tone Document 완료 후 (최종 백업)

3. 홈 화면에 JSON 불러오기 expander:
   · st.file_uploader로 JSON 파일 받음
   · 구조 검증, 엔진 버전 호환성 체크
   · 중복 ID 충돌 시 새 ID 자동 부여
   · 복원 후 해당 단계의 view로 자동 점프

원칙 준수:
  · 전체 저장/전체 복원 — 부분 저장 금지 (일관성 유지)
  · 세션 복구 전용 — Stepper 점프(v2.3.4)와 역할 분리
  · 단순 UI — expander 2개 + 버튼 3개만

이로써 Mr. MOON의 실사용 요구 충족:
  · 여러 날에 걸쳐 작업 가능
  · 다른 컴퓨터에서 이어서 작업
  · 장애 발생 시 복구 가능

─────────────────────────────────────────────────────────
v2.3.4 업데이트 (2026-04-21) — Stepper 네비게이션 실제 작동화
─────────────────────────────────────────────────────────

[문제 진단]
상단 Stepper UI가 시각적 표시만 하고 실제로는 클릭 작동 안 함.
코드 주석에는 "클릭 가능 여부 (done 단계만)"이라고 명시되어 있었지만
실제 구현은 HTML 렌더링만으로 끝나 있어서 클릭 시 아무 반응 없음.

원래 기획은 "완료된 단계를 Stepper에서 클릭해서 점프 이동"이었는데
실제 UI는 이게 작동하지 않는 상태. 결과적으로 사용자는 매번 단계별
"← 뒤로" 버튼으로만 이동 가능했음.

[v2.3.4 해결책]
render_stepper() 함수를 st.columns + st.button 구조로 재작성.
각 단계가 실제 클릭 가능한 버튼이 됨:
  · 완료된 단계(done): 클릭 시 해당 view로 즉시 점프
  · 현재 단계(active): 노란 버튼으로 하이라이트, disabled
  · 미완료(upcoming): 회색 비활성 버튼

이로써 원래 기획된 네비게이션이 실제로 작동. 
추가 UI 구조 변경 없이 함수 1개만 교체.

─────────────────────────────────────────────────────────
v2.3.3 업데이트 (2026-04-21) — 장르별 적대자 유형 재정의
─────────────────────────────────────────────────────────

[문제 진단 — 쿠킹클래스 v2.3.2 결과물에서 재확인]
로맨틱 코미디인데 안타고니스트가 계속 '아버지(강회장)'로 배치됨.
원인: ANTAGONIST_BJND 모듈에 '쿠킹클래스 강회장 = 이상적 적대자'
예시가 박혀있고, '모든 적대자(빌런/아버지/경쟁자/권력)' 문구로
아버지가 적대자 대표 유형으로 명시되어 있었음.

[v2.3.3 해결책]
ANTAGONIST_BJND 모듈 전면 재작성:
  · '모든 적대자(빌런/아버지/경쟁자/권력)' 문구 제거
  · 쿠킹클래스 강회장 예시 제거
  · 장르별 적대자 유형 블록 신설:
    - 로맨틱 코미디: Love-Antagonist / Wrong Partner / 내적 결함
      (부모/가족은 Catalyst로 분류, 적대자 금지)
    - 드라마: 부모·사회 시스템 가능
    - 스릴러: 직접적 위협
    - 호러: 초자연적 + 공동체 불신
    - 액션: 물리·이념 대립
    - 느와르: 팜므 파탈 + 내면의 어둠
  · 로맨틱 코미디 예시: 브리짓 존스, 해리가 샐리, 프러포즈, 27번의 결혼리허설

이로써 엔진이 로맨틱 코미디에서 아버지를 반사적으로 적대자로
배치하지 않고, 장르 본질에 맞는 Love-Antagonist 또는 Wrong Partner를
선택. 장르별 분기가 아닌 단일 모듈 내 장르별 예시 강화로 해결.

─────────────────────────────────────────────────────────
v2.3.2 업데이트 (2026-04-21) — 장르 기대 체크리스트 강화
─────────────────────────────────────────────────────────

[문제 진단 — 쿠킹클래스 v2.3.1 결과물에서 발견]
로맨틱 코미디인데 클라이맥스가 '부녀 화해'로 빠지고 로맨스 완성이
엘리베이터 전화 한 통으로 꼬리 처리됨. 장르 관객이 기대하는
'로맨스 완성 순간'이 클라이맥스에서 약하게 작동.

[원인]
GENRE_FUN_ALIVE 모듈의 장르 재미 정의가 한 줄 추상어로만 제공됨
("로맨틱 코미디: 어긋남이 웃음과 설렘을 동시에"). AI가 이걸
구체 행동으로 구현할 장치가 없음. Core Gate 채점도 장르 정렬
구체 기준 없음.

[v2.3.2 해결책]
GENRE_FUN_ALIVE 모듈을 장르별 구체 체크리스트로 대폭 확장.
11개 장르(드라마/로코/코미디/호러/스릴러/액션/느와르/SF/판타지/
미스터리/시대극) 각각 6~7개 기계적 체크 항목 제공.

Core Build JSON 스키마에 genre_expectation_check 필드 추가:
  · genre_fun_alive (true/false)
  · checklist (항목별 YES/NO + 근거)
  · weak_zones (장르 기대 약한 구간)
  · climax_verdict (CLIMAX_PASS/CLIMAX_FAIL)

SYSTEM_CORE_GATE에 장르 정렬 엄격 채점 추가:
  · CLIMAX_FAIL = structure 항목 -2점
  · genre_fun_alive=false = final_score -1.5점
  · NO 응답 1건당 -0.5점

이로써 모든 장르가 자기 본질에 맞게 작동. 장르별 분기 없이 단일
모듈 강화로 해결. 안타고니스트 구조는 변경 없음 (장르 무관).

─────────────────────────────────────────────────────────
v2.3.1 핫픽스 (2026-04-21) — 캐릭터 일관성 보호
─────────────────────────────────────────────────────────

[문제 진단 — 쿠킹클래스 v2.3.0 결과물에서 발견]
같은 DOCX 안에서 유진의 어머니 설정이 두 가지로 공존:
- 유진 백스토리: "8살 때 어머니 이혼으로 떠남 (살아있음)"
- 강회장 백스토리: "11살 때 아내 위암 사망"
학력 설정도 "뉴욕 CIA"와 "런던 유학"이 혼재.

[원인]
Character Bible은 4~8명을 순차 생성하지만, 각 호출에서 AI가
Core Build의 설정만 참조하고 이전에 생성한 다른 캐릭터의
백스토리는 참조하지 않아 설정 모순 발생.

[v2.3.1 해결책]
extract_char_consistency_facts() + build_prior_chars_consistency_block()
두 헬퍼 함수 신설. 순차 생성 시 이전 캐릭터들의 핵심 사실
(나이·직업·가족관계·공유 사건·비밀)을 다음 캐릭터 생성 프롬프트에
누적 주입하여 일관성 모순을 원천 차단.

CHAR_BIBLE_RULES에 "일관성 보호 블록 준수" 규칙 추가.
main.py의 call_character_bible()는 순차 생성 시 성공한 캐릭터의
사실을 즉시 추출하여 prior_facts에 누적, 다음 호출에 prior_chars_block으로 주입.

─────────────────────────────────────────────────────────
v2.3.0 주요 변경사항 (2026-04-20)
─────────────────────────────────────────────────────────

[Phase 1] BJND 파이프라인 강제 (4모듈)
- BJND v1.0 용어 표준 공식화: Loss/Lack → Desire(Goal+Need) → Strategy → Cost
- BJND_STRATEGY_SCENE_ENFORCER 신설 (Core의 BJND를 Scene/Treatment 강제 집행)
- 막별 Cost 누적 단계 (1막 암시 / 2막 전반 균열 / 2막 후반 실재손상 / 3막 전환)
- 3막 엔딩 Strategy 전환 규칙 (외적 선택형 엔딩 금지)
- Core Build JSON 스키마에 cost 3축 + strategy_transformation 필드 추가

[Phase 2] BJND 4축 자가 검증 (창작자 질문)
- NECESSITY (Loss/Lack 필연성)
- AUTHENTICITY (Strategy 인물 고유성) + 3중 검증 (치환/유기성/작가 서명)
- EMPATHY (Cost 관객 공감력)
- POTENCY (Strategy 전환 진폭)
- Core Build JSON에 bjnd_four_axis_check + audience_scenes 필드

[Phase 3] 창작자 감성 3요소
- PHYSICALITY OF EMPATHY (관객의 몸이 반응하는가)
- SILENCE DESIGN (침묵의 설계 — 3유형)
- PLANT AESTHETICS (씨앗의 미학 — 3쌍 설계)
- Core/Scene/Treatment 전역 주입

[Phase 4] 기술 지원 7모듈
- POV POLITICS (시선의 정치학)
- GENRE FUN ALIVE (장르 재미 생존 자가 검증)
- PROVOCATION ≠ DOPAMINE (자극과 도파민 구분)
- ANTAGONIST BJND (적대자 BJND 4단 설계)
- THEME-STRATEGY ALIGNMENT (테마-전략 방향 일치)
- BRAINSTORM BJND DIVERSITY (3 컨셉 근본 다양성)
- WORLD MIRRORS BJND (세계가 캐릭터를 비추는가)

[Phase 5] OPEN 필드 폐지
- LOCKED_SYSTEM_RULES에서 [OPEN 태그 규칙] 섹션 제거
- "LOCKED에 없는 것은 창작 가능" 원칙으로 대체
- build_locked_block 함수 단순화 (하위 호환성 유지)
- main.py UI: LOCKED/OPEN 2열 → LOCKED 단일 필드

─────────────────────────────────────────────────────────
BLUE JEANS 3축 (Mr.MOON 고유)
─────────────────────────────────────────────────────────
  ① BJND 서사동력 (v1.0 표준):
     Loss/Lack → Desire(Goal+Need) → Strategy → Cost
  ② Villain 4 Questions:
     흥미 · 다크미러 · 계획파괴 · 승률
  ③ ATTRACTION 6규칙 + Genre Rule Pack v2 (9장르 × 12필드)

─────────────────────────────────────────────────────────
헐리우드 Foundation
─────────────────────────────────────────────────────────
  - 9원칙 + 관객심리 6원칙 + Planting & Payoff + 서브플롯
  - OPENING MASTERY (6기법 + 장르 DNA + 복합장르 본질 법칙)
  - 한국 상업영화 3단 구조 (오프닝 / Set-Up / Inciting Incident)

─────────────────────────────────────────────────────────
버전 이력
─────────────────────────────────────────────────────────
  v1.0   기본 9단계 파이프라인
  v1.3   9원칙 · Genre Rules 8장르 · Hook/Punch
  v1.4   관객 심리 6원칙 · 서브플롯 설계
  v1.5   LOCKED 시스템 · 시리즈 비트 · B-Story
  v1.6   SCOPE MANDATE · 영화/시리즈 분량 분기
  v1.7   ATTRACTION 6규칙 · Opus/Sonnet 이중 모델
  v1.8   BJND · Villain 4Q + 승률 · Genre Rule Pack v2
  v1.9   Planting & Payoff 시스템
  v2.0   AI ESCAPE A1~A10 · FACT/HISTORICAL 모듈 · 장르 Override 8종
  v2.1   캐릭터 교차검증 · Treatment Meta 이름 검증
  v2.2   OPENING MASTERY · 6기법 · 장르 DNA · 복합장르 본질 법칙
  v2.2.2 오프닝 ≠ 도발적 사건 · 한국 상업영화 3단 구조
  v2.3.0 BJND v1.0 표준 · Cost 4번째 축 · 4축 자가검증 · 창작자 감성 3요소
         · 기술 지원 7모듈 · OPEN 필드 폐지 · 18개 모듈 통합
  v2.3.1 [핫픽스] 캐릭터 일관성 보호 — 순차 생성 시 이전 캐릭터 핵심 사실 주입
         (가족관계·학력·나이·비밀 모순 방지)
  v2.3.2 장르 기대 체크리스트 강화 — 11개 장르 각 6~7개 구체 체크 항목
         · CLIMAX 장르 정렬 엄격 채점 · 장르답게 작동하는 엔진
  v2.3.3 장르별 적대자 유형 재정의 — ANTAGONIST_BJND 모듈 재작성
         · 로맨틱 코미디 예시 전환 (강회장 → 브리짓 존스/해리가 샐리 등)
         · 부모를 반사적으로 적대자 배치하는 결함 제거
  v2.3.4 Stepper 네비게이션 실제 작동화 — 상단 단계 표시바를 클릭 이동 가능한
         버튼으로 변환. 완료된 단계 점프 이동, 중간 단계 직접 진입 가능.
  v2.3.5 프로젝트 JSON 저장/불러오기 — 세션 끊김 대비 복구 기능.
         Scene/Treatment/Tone 완료 후 JSON 저장 + 홈 화면에서 업로드 복원.
         여러 날 작업 / 다른 컴퓨터 작업 / 장애 복구 지원.
  v2.3.6 장르/BJND/POV/적대자 규칙을 Treatment 단계까지 전파 +
         Gate E 실제 내용 논리 검증 (장르 정합/엔딩 정합/논리 일관성 3축 신규).
         Core Build 설계가 Treatment에서 휘발되어 Writer Engine으로 전달 안 되던
         구조적 공백 해결.
  v2.3.7 시대 고증 검증 추가 — Gate E의 8번째 축 period_consistency 신설.
         1980년대 배경에 스마트폰 등장 같은 시대 오류를 생성·검증 양쪽에서 방지.
         역사영화 체크 여부와 무관하게 모든 작품에 적용.
  v2.3.8 Core Build 필드 Treatment 전파 완성 — project_intent(기획의도+주제+
         톤앤매너) + world_build(시대/공간/규칙) + genre_expectation_check.weak_zones
         (Core 자가 진단) + research(실제 사건 + 기존 작품) 4종 블록 주입.
         Research 데이터가 Writer Engine 직전까지 휘발 없이 전달되어 핍진성 강화
         + 표절 방지 양쪽 역할 완성.

© 2026 BLUE JEANS PICTURES. All rights reserved.
"""

# ═══════════════════════════════════════════════════
# 엔진 메타데이터 (런타임 버전 확인용)
# 수정 시 ENGINE_VERSION과 ENGINE_BUILD_DATE를 함께 갱신하세요.
# ═══════════════════════════════════════════════════

ENGINE_VERSION = "v2.3.8"
ENGINE_BUILD_DATE = "2026-04-22"
ENGINE_STATUS = "Production"

def get_engine_info() -> str:
    """엔진 버전 정보를 한 줄 문자열로 반환.
    Streamlit 사이드바나 로그에 표시할 때 사용."""
    return f"Creator Engine {ENGINE_VERSION} ({ENGINE_BUILD_DATE})"


def get_engine_info_detail() -> dict:
    """엔진 상세 정보 딕셔너리 반환.
    UI 렌더링 및 DOCX 메타 삽입에 사용."""
    return {
        "version": ENGINE_VERSION,
        "build_date": ENGINE_BUILD_DATE,
        "status": ENGINE_STATUS,
        "display": f"Creator Engine {ENGINE_VERSION}",
        "signature": f"BLUE JEANS PICTURES · Creator Engine {ENGINE_VERSION} · {ENGINE_BUILD_DATE}",
    }


import json

# ═══════════════════════════════════════════════════
# LOCKED SYSTEM (v1.5 신규)
# ═══════════════════════════════════════════════════

LOCKED_SYSTEM_RULES = """
[LOCKED SYSTEM — 확정 설정 보호 규칙]

★ 이 규칙은 모든 창작 규칙보다 상위다. 더 재미있는 이야기를 위해서라도 LOCKED 항목을 변경할 수 없다. ★

[LOCKED 태그 규칙]
사용자가 <LOCKED>...</LOCKED> 태그로 감싼 항목은 절대 변경 불가다.
- 캐릭터의 소속, 이름, 나이, 직책을 바꾸지 마라.
- 캐릭터 간 핵심 관계(적대/동맹/혈연 등)를 바꾸지 마라.
- 세계관의 조직 구조, 규칙, 시간축을 바꾸지 마라.
- 기획의도에 명시된 테마와 사회적 맥락을 삭제하지 마라.
- 확정된 플롯 포인트(사건 순서, 촉발 사건, 결말)를 재해석하거나 변형하지 마라.
- 에피소드별 역사적 사건 도입부가 지정된 경우 반드시 포함하라.

[LOCKED에 없는 것은 창작 가능]
LOCKED 블록에 명시되지 않은 모든 디테일은 엔진이 자유롭게 창작한다.
- 캐릭터 바이블의 외형·습관·말투 디테일
- 장면별 시각 연출과 감정 변화
- 대사의 구체적 워딩
- B-Story의 세부 전개
- 장면 순서 내의 씬 배치

[LOCKED 검증 — 매 출력 전 반드시 수행]
출력을 완성한 뒤 다음을 확인하라:
□ LOCKED 블록의 모든 캐릭터가 원본 소속/직책 그대로인가?
□ LOCKED 블록의 핵심 관계가 변경되지 않았는가?
□ LOCKED 블록의 기획의도 키워드가 출력에 반영되었는가?
□ LOCKED 블록의 플롯 포인트가 순서와 내용 그대로 유지되는가?
□ LOCKED 블록에 역사적 사건 도입부가 있으면 해당 에피소드에 포함되었는가?
1건이라도 불일치하면 해당 부분을 LOCKED 원본으로 되돌려라.

[기획의도 반영 규칙]
사용자가 기획의도에 명시한 사회적 맥락(예: 20대 취업난, 종교 유혹, 범죄조직 흡수 구조 등)은
반드시 캐릭터의 백스토리, 대사, 또는 장면 디테일에 구체적으로 반영되어야 한다.
- 추상적 테마로 대체하지 마라 ("결핍" → ✗)
- 구체적 상황으로 구현하라 ("이력서 12곳 넣고 합격 0" → ✓)
- 빌런의 대사나 조직의 유혹 구조에 반영하는 것이 가장 효과적이다.
"""

def build_locked_block(locked_items: list = None, open_items: list = None) -> str:
    """
    LOCKED 블록을 생성한다. (v2.3부터 OPEN 필드는 폐지 — open_items는 하위 호환성을 위해 받지만 무시)
    
    사용 예:
        locked = [
            "김도윤: 제국익문사 소속. 묘적사로 변경 금지.",
            "서재중: 29세. 묘적사 현장 요원에서 이탈자로 전환.",
            "강무혁: 중장천(암살 및 제거). 광목천으로 변경 금지.",
            "기획의도: 20대 취업난이 재중의 묘적사 입사 동기에 반영되어야 함.",
            "역사적 사건: EP2 시작 — 1947년 여운형 암살.",
        ]
        block = build_locked_block(locked)
    
    Note:
        v2.3부터 OPEN 필드는 폐지되었다. LOCKED에 명시되지 않은 모든 것은 엔진이 자유롭게 창작한다.
        기존 프로젝트의 open_items는 무시되므로 크래시 없이 하위 호환성을 유지한다.
    """
    result = ""
    
    if locked_items:
        result += "<LOCKED>\n"
        for item in locked_items:
            result += f"- {item}\n"
        result += "</LOCKED>\n\n"
    
    # v2.3: OPEN 블록 생성 폐지. open_items 파라미터는 하위 호환성을 위해 받지만 무시한다.
    
    return result


# ═══════════════════════════════════════════════════
# CONSTANTS
# ═══════════════════════════════════════════════════

# ─── 장르별 필수 규칙 (Writer Engine v2 연동) ───
GENRE_RULES = {
    "범죄/스릴러": {
        "en": "Crime / Thriller / Noir",
        "core": "정보 비대칭과 압박, 도덕적 모호함 속 타락과 생존 대가.",
        "opening": "사건의 결과부터 — 시체/범죄 현장/파국을 먼저 보여주고 '어떻게?'로 끈다.",
        "items": ["pressure_escalation", "information_asymmetry", "clock_or_deadline", "threat_visibility_control", "suspicion_transfer", "moral_compromise", "betrayal_architecture", "paranoia_escalation", "dark_irony", "cost_of_survival"],
        "must_have": ["초반 10분 내 범죄/사건 발생", "관객이 범인보다 한 발 늦게 알아채는 구조", "미드포인트에서 게임의 룰이 바뀌는 반전", "클라이맥스 직전 2중 반전(double twist)"],
        "hook_rule": "매 비트 끝에 새로운 의문 또는 위협이 제시되어야 한다.",
        "punch_rule": "인물의 선택이 돌이킬 수 없는 결과를 만드는 순간.",
        "setpiece": "추격/대치/심문/잠입 중 최소 2개 setpiece 필수",
        "forbidden": "설명적 회상 남발, 형사의 독백으로 사건 정리, 우연의 일치로 범인 발각",
        "hooks": "시계가 돌아간다 / 누군가 지켜보고 있다 / 피할 수 없는 거래 제안",
        "punches": "단서가 뒤집힌다 / 배신의 순간 / 도덕선을 넘는 선택",
        "fails": ["압박 약함", "선악 명확", "분위기만 있고 서사 압력 없음", "반전 억지"],
    },
    "드라마": {
        "en": "Drama",
        "core": "인간의 선택과 대가를 통해 진실에 도달하는 장르.",
        "opening": "고요한 균열 — 평범한 일상인데 뭔가 하나가 어긋나 있다.",
        "items": ["emotional_truth", "character_depth", "moral_complexity", "relationship_dynamics", "vulnerability_escalation", "quiet_power", "dialogue_weight", "consequence_chain", "identity_pressure", "catharsis_build"],
        "must_have": ["주인공의 내면 결핍이 외부 사건과 충돌하는 1막 설정", "관계의 균열이 극대화되는 미드포인트", "진짜 감정이 터지는 고백/대결 씬", "변화가 행동으로 증명되는 결말"],
        "hook_rule": "감정적 긴장의 실을 끊지 않는다. 매 비트 끝에 해결되지 않은 감정적 질문.",
        "punch_rule": "punch는 폭발이 아니라 침묵. 말하지 못하는 것, 또는 마침내 말해버리는 것.",
        "setpiece": "감정적 클라이맥스 씬 1개 + 관계 전환 씬 1개 필수",
        "forbidden": "감정을 직접 설명하는 내레이션, 갈등 없는 화해",
        "hooks": "조용한 첫 이미지가 뒤집힐 것을 암시 / 인물의 일상 속 균열",
        "punches": "선택의 대가가 눈에 보이는 순간 / 관계가 돌이킬 수 없이 변하는 순간",
        "fails": ["감정이 표면적", "인물이 평면적", "관계 변화 없음", "대가 부재"],
    },
    "액션": {
        "en": "Action",
        "core": "물리적 목표와 대가 속에서 캐릭터 의지를 증명하는 장르.",
        "opening": "미션 진행 중 — 설명 없이 체이스, 전투, 작전 한복판에서 시작.",
        "items": ["physical_objective_clarity", "spatial_clarity", "tactical_reversal", "rising_physical_cost", "kinetic_identity", "consequence_visibility", "unique_setpiece_logic", "emotional_stake_inside_action", "momentum", "aftermath_value"],
        "must_have": ["1막에 주인공의 전투 능력을 보여주는 오프닝 액션", "2막마다 스케일이 커지는 액션 시퀀스", "미드포인트에서 패배 또는 배신", "클라이맥스에서 가장 큰 스케일의 최종 대결"],
        "hook_rule": "물리적 위협과 시간 압박이 매 비트를 관통한다.",
        "punch_rule": "예상을 깨는 전술 변화 또는 환경 변화. 같은 패턴 반복 금지.",
        "setpiece": "최소 3개 대형 setpiece (오프닝/미드포인트/클라이맥스) + 소규모 3개 이상",
        "forbidden": "설명으로 처리하는 액션, 무의미한 총격전 반복, 빌런의 동기 없는 폭력",
        "hooks": "목표가 명확하다 / 공간이 보인다 / 시간이 없다",
        "punches": "전술이 뒤집힌다 / 대가가 몸에 새겨진다 / 다음 전투가 더 크다",
        "fails": ["목표 흐림", "공간 안 보임", "액션 후 대가 없음"],
    },
    "로맨스": {
        "en": "Romance / Melodrama",
        "core": "갈망의 축적과 감정의 지연이 만드는 아픔과 회수의 장르.",
        "opening": "운명적 접점 또는 이별 직후 — 두 사람이 스쳐가거나, 이미 끝난 관계에서 시작.",
        "items": ["desire_tension", "emotional_withholding", "longing_build", "vulnerability_reveal", "timing_misalignment", "intimacy_progression", "symbolic_motif", "ache_after_contact", "impossible_choice", "emotional_payoff"],
        "must_have": ["첫 만남의 설렘 또는 마찰이 있는 도입", "감정 접근 후 오해/장벽으로 멀어지는 미드포인트", "진심 고백 또는 희생의 클라이맥스", "관계의 새로운 균형을 보여주는 결말"],
        "hook_rule": "두 사람 사이의 긴장(끌림+저항)이 매 비트에서 진동해야 한다.",
        "punch_rule": "감정의 급반전 — 웃기다가 울리거나, 가까워지다가 벽이 생기는 순간.",
        "setpiece": "첫 만남 씬 + 감정 폭발 씬 + 이별/재회 씬 필수",
        "forbidden": "삼각관계의 기계적 반복, 오해가 대화 한마디로 해결, 물리적 장벽만으로 갈등 유지",
        "hooks": "시선이 머무른다 / 닿을 듯 닿지 않는 거리 / 우연의 접근",
        "punches": "감정을 참는 순간 / 타이밍이 어긋나는 순간 / 작은 접촉의 전율",
        "fails": ["고백만 많고 축적 없음", "끌림 이유 불명", "감정 온도 단조"],
    },
    "코미디": {
        "en": "Comedy",
        "core": "웃음 메커니즘이 작동하는 장르. 떠드는 장르가 아니다.",
        "opening": "결함 폭발 — 주인공의 결함이 3분 안에 사고를 친다.",
        "items": ["premise_engine", "comic_contradiction", "character_comic_flaw", "comic_escalation", "line_surprise", "status_comedy", "timing_precision", "callback_payoff", "scene_comic_engine", "joke_density"],
        "must_have": ["도입 5분 내 코믹 톤 확립", "주인공의 결점이 웃음의 원천", "미드포인트에서 거짓말/오해가 극대화", "클라이맥스에서 모든 거짓말이 동시에 터지는 구조"],
        "hook_rule": "웃음 후 즉시 다음 상황 예고. '이거 어떻게 빠져나가지?'",
        "punch_rule": "인물이 관객의 예측과 정반대로 행동하는 순간.",
        "setpiece": "대형 코믹 셋피스 최소 2개 (오해 폭발 + 진실 폭로)",
        "forbidden": "상황 설명으로 웃기려는 시도, 같은 개그 반복, 인물 비하로 웃음 유발",
        "hooks": "일상적 상황의 비틀림 / 캐릭터 결함이 즉시 드러나는 행동",
        "punches": "callback이 터진다 / 상황이 더 꼬인다 / 역전된 status",
        "fails": ["설정 안 웃김", "캐릭터 결함이 웃음 비생산", "농담이 서사 정지"],
    },
    "호러/공포": {
        "en": "Horror",
        "core": "공포의 예감과 축적으로 안전감을 체계적으로 파괴하는 장르.",
        "opening": "프롤로그 킬 — 본편 시작 전에 누군가 죽거나 사라진다. 또는 '뭔가 이상하다'는 감각.",
        "items": ["fear_anticipation", "uncertainty", "sensory_unease", "threat_design", "dread_pacing", "violation_of_safety", "image_residue", "vulnerability", "false_relief", "terror_escalation"],
        "must_have": ["일상의 균열을 보여주는 불안한 오프닝", "규칙 발견 — 이 공포의 작동 방식", "규칙 위반 — 공포 극대화", "최종 대면 — 공포의 실체와 직접 대결"],
        "hook_rule": "매 비트 끝에 '안전하다고 생각한 순간' 새로운 위협의 징후.",
        "punch_rule": "jump scare와 slow burn 반드시 교차 배치.",
        "setpiece": "공포의 규칙 발견 씬 + 규칙 위반 씬 + 최종 대면 씬 필수",
        "forbidden": "설명으로 무서움을 전달, 공포 원인의 과잉 설명, 공포와 무관한 로맨스 삽입",
        "hooks": "평범한 것이 이상하다 / 감각이 경고한다 / 보이지 않는 것의 존재감",
        "punches": "안전한 곳이 무너진다 / 보이지 않던 것이 보인다 / 가짜 안도 후 진짜 공포",
        "fails": ["놀람만 있고 공포 축적 없음", "위협 규칙 모호", "불안이 장면 밖으로 안 이어짐"],
    },
    "SF": {
        "en": "Science Fiction",
        "core": "세계의 규칙이 인간 드라마의 은유로 작동하는 장르.",
        "opening": "세계 규칙 한 장면 — 이 세계가 우리와 다르다는 것을 첫 이미지로 보여준다.",
        "items": ["world_rule_clarity", "wonder_value", "cost_of_rule", "ethical_implication", "rule_consistency", "novelty", "human_anchor", "visual_imagination", "mythic_depth", "payoff_of_world_rule"],
        "must_have": ["세계관의 핵심 규칙을 자연스럽게 보여주는 도입", "규칙이 만드는 딜레마", "미드포인트에서 세계관의 진실이 뒤집히는 반전", "기술/환경의 논리 안에서 해결되는 클라이맥스"],
        "hook_rule": "세계관의 새로운 측면이 매 비트에서 하나씩 드러나야 한다. 정보 과부하 금지.",
        "punch_rule": "세계관 규칙의 예상치 못한 적용 — '이 기술이 이렇게도?'",
        "setpiece": "세계관 소개 씬 + 기술 딜레마 씬 + 세계관 반전 씬 필수",
        "forbidden": "세계관 설명을 위한 강의식 대사, 데우스 엑스 마키나",
        "hooks": "이 세계는 우리와 다르다 — 한 가지가 즉시 보인다 / 경이로운 이미지",
        "punches": "규칙의 대가가 드러난다 / 세계의 비밀이 인간 문제와 연결된다",
        "fails": ["룰 설명만 많음", "인간 드라마 약함", "세계관이 이야기보다 앞섬"],
    },
    "판타지": {
        "en": "Fantasy",
        "core": "마법의 규칙과 대가가 인간 성장의 은유로 작동하는 장르.",
        "opening": "평범한 세계에서 판타지 세계로의 전환 — 문턱 넘기의 순간.",
        "items": ["world_rule_clarity", "wonder_value", "cost_of_rule", "ethical_implication", "rule_consistency", "novelty", "human_anchor", "visual_imagination", "mythic_depth", "payoff_of_world_rule"],
        "must_have": ["문턱 넘기(세계 전환)", "마법/능력의 규칙과 대가 설정", "멘토의 퇴장 또는 배신", "내면의 성장이 외부 승리로 연결"],
        "hook_rule": "새로운 세계의 경이로움과 위험이 동시에 제시되어야 한다.",
        "punch_rule": "마법/능력의 예상치 못한 대가 — 힘을 쓸수록 잃는 것이 커지는 구조.",
        "setpiece": "세계 진입 씬 + 능력 각성 씬 + 최종 대결 씬 필수",
        "forbidden": "대가 없는 만능 마법, 예언에 의한 수동적 전개, 악의 동기 없는 빌런",
        "hooks": "새 세계의 경이로운 첫 이미지 / 규칙 발견의 전율",
        "punches": "능력의 대가가 드러난다 / 믿었던 세계의 진실이 뒤집힌다",
        "fails": ["대가 없는 능력", "설명 과잉", "인간 드라마 약함"],
    },
    "미지정": {
        "en": "General",
        "core": "장르 무관, 보편적 서사 원칙으로 작동하는 이야기.",
        "opening": "관객의 호기심을 잡는 훅 — 장르 상관없이 첫 3분이 관건.",
        "items": ["intention_clarity", "obstacle_strength", "character_depth", "conflict_escalation", "emotional_truth", "turn_surprise", "consequence_chain", "thematic_unity", "pacing_control", "satisfying_resolution"],
        "must_have": ["명확한 도입 훅", "미드포인트 반전", "클라이맥스 대결/대면", "변화가 증명되는 결말"],
        "hook_rule": "매 비트 끝에 다음 비트로 끌어당기는 질문 또는 위협.",
        "punch_rule": "핵심 씬마다 예상을 깨는 순간.",
        "setpiece": "관객이 기억할 대표 씬 최소 2개",
        "forbidden": "설명적 전개, 갈등 없는 진행, 우연에 의한 해결",
        "hooks": "호기심을 잡는 질문 / 예상 못한 첫 이미지",
        "punches": "예상을 깨는 선택 / 대가가 눈에 보이는 순간",
        "fails": ["갈등 약함", "전환 없음", "결말 억지"],
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
        (12, "두번째 변곡점 (All Is Lost)", "가장 낮은 지점. 주인공이 모든 것을 잃고 무너진다. ★ 아직 반격하지 않는다. 패배를 인식할 뿐이다. 여기서 역공을 시작하면 Beat 14와 중복된다."),
    ],
    3: [
        (13, "빌런의 최고조", "적대 세력이 가장 강한 순간. 주인공은 아직 바닥에 있다. 빌런이 승리를 확신한다."),
        (14, "클라이맥스", "주인공의 역전. Beat 12에서 잃은 것이 새로운 무기가 된다. ★ Beat 12에서 한 행동을 반복하지 말 것. 12는 무너짐, 14는 일어섬."),
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
        (12, "All Is Lost + EP4 클리프행어", "가장 낮은 지점. 주인공이 모든 것을 잃는다. ★ 아직 반격하지 않는다."),
    ],
    "EP5": [
        (13, "빌런의 최고조", "적대 세력이 가장 강한 순간. 주인공은 아직 바닥. B-Story 데드라인이 눈앞."),
        (14, "클라이맥스", "주인공의 역전. Beat 12에서 잃은 것이 새로운 무기가 된다. ★ Beat 12 행동 반복 금지."),
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
        (12, "All Is Lost + EP6 클리프행어", "가장 낮은 지점. 주인공이 모든 것을 잃는다. ★ 아직 반격하지 않는다."),
    ],
    "EP7": [
        (13, "빌런의 최고조", "적대 세력 최강. 주인공은 아직 바닥. B-Story 최종 국면"),
        (14, "클라이맥스 + EP7 클리프행어", "주인공의 역전. Beat 12에서 잃은 것이 새로운 무기가 된다. ★ Beat 12 행동 반복 금지."),
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
    # ── Planting & Payoff (v1.9 추가) ──
    "planting_payoff": (
        "[Planting & Payoff — 심고 회수하라]\n"
        "1막에 심은 것이 3막에서 새로운 의미로 회수되어야 한다.\n"
        "- Plant = 대사 한 줄, 소품, 습관, 장소, 이미지. 처음엔 별 의미 없어 보인다.\n"
        "- Payoff = 그것이 클라이맥스 또는 결말에서 돌아올 때, 관객이 '아!' 하는 순간.\n"
        "- 좋은 Plant: 관객이 심어진 줄 모른다. Payoff 순간에 비로소 깨닫는다.\n"
        "- 나쁜 Plant: 너무 눈에 띄어서 관객이 '저건 나중에 쓰이겠군' 하고 예측한다.\n"
        "규칙:\n"
        "- 모든 이야기에 최소 3개의 Plant-Payoff 쌍이 있어야 한다.\n"
        "  ① 캐릭터 Plant: 주인공의 습관/대사/소품 → 클라이맥스에서 반전 의미\n"
        "  ② 관계 Plant: 인물 간 사소한 상호작용 → 결정적 순간에 신뢰/배신의 근거\n"
        "  ③ 세계관 Plant: 세계의 규칙/장소/사물 → 해결의 열쇠 또는 비극의 원인\n"
        "- Plant는 1막에 심고, Payoff는 2막 후반~3막에서 회수한다.\n"
        "- 회수되지 않는 Plant는 관객의 무의식에 미해결로 남아 불만족을 만든다.\n"
        "- Plant 없이 등장하는 Payoff는 데우스 엑스 마키나다. 금지.\n"
        "예시:\n"
        "- 〈기생충〉: 1막 반지하의 냄새 → 3막 '냄새' 대사가 살인의 촉발\n"
        "- 〈올드보이〉: 만두 → 최종 반전의 열쇠\n"
        "- 〈차이나타운〉: 'Forget it, Jake. It's Chinatown.' → 1막의 농담이 3막의 비극"
    ),
}


# ═══════════════════════════════════════════════════
#  BLUE JEANS NARRATIVE DRIVE (BJND) — Mr.MOON 고유 서사동력 프레임워크
# ═══════════════════════════════════════════════════

NARRATIVE_DRIVE = """
[BLUE JEANS 서사동력 — Narrative Drive (BJND v1.0)]

★ 이것은 BLUE JEANS PICTURES 고유의 서사 설계 프레임워크다. ★
모든 이야기의 엔진은 4개의 축으로 작동한다:

  발생요인(Loss/Lack) → 욕망(Desire: Goal+Need) → 해결전략(Strategy) → 대가(Cost)

[BJND 용어 표준 — 전 엔진 공통 어휘]

  ① Loss(상실) / Lack(결핍) — 가졌다가 잃었는가, 처음부터 없었는가
  ② Desire(욕망) — 외적 Goal(목적) + 내적 Need(필요)
  ③ Strategy(해결방법) ★ 작가의 서명이 남는 축
  ④ Cost(대가) — Strategy가 치르게 하는 것. 2막 위기의 원천.

  보조 필드:
    - Risk: Strategy 실패 시 잃는 것
    - Ending Payoff: Strategy_1 → Strategy_2 전환
    - Goal↔Need Gap: 외적 욕망과 내적 필요의 간극

  이 용어들은 Creator / Writer / Rewrite / Series / Novel Engine에서
  동일하게 사용되는 블루진 공통 어휘다. 혼용 금지.

[1. 발생요인 진단 — 상실(Loss) vs 결핍(Lack)]
주인공의 욕망이 어디서 시작되었는가? 이것이 이야기 전체의 방향을 결정한다.

  ■ 상실(Loss) 기반 — "한때 가졌던 것을 잃었다"
    욕망 방향: 회복 / 복수 / 대체
    서사 구조: 과거를 향한다 → 되찾을 수 없음을 인식 → 새로운 방향 수용 또는 파멸
    캐릭터 아크: "잃어버린 것을 되찾는다" 또는 "없이도 살 수 있다고 깨닫는다"
    감정 곡선: 분노/슬픔에서 시작 → 집착 → 수용 또는 자기파괴
    예시: 〈올드보이〉오대수(복수), 〈밀양〉신애(상실 후 신앙), 〈묘적사〉재중(아버지 상실→복수→자유 선택)

  ■ 결핍(Lack) 기반 — "처음부터 없었다"
    욕망 방향: 획득 / 성장 / 증명
    서사 구조: 무에서 유를 향한다 → 대가를 인식 → 진짜 필요한 것 발견
    캐릭터 아크: "없던 것을 처음 얻는다" 또는 "필요 없다고 깨닫는다"
    감정 곡선: 갈망/열등감에서 시작 → 도전 → 성취 또는 재정의
    예시: 〈기생충〉기택(계층 결핍), 〈라라랜드〉미아(인정 결핍), 〈버닝〉종수(존재 결핍)

[2. 상실과 결핍이 만드는 구조적 차이]

  | 요소 | 상실(Loss) | 결핍(Lack) |
  |------|-----------|-----------|
  | 1막 상태 | 잃기 전 or 잃은 직후 | 갈망하지만 가진 적 없음 |
  | 촉발 사건 | 상실의 진실/원인 발견 | 획득의 기회/경로 발견 |
  | 2막 드라이브 | 되찾으려는 시도 | 쟁취하려는 시도 |
  | 미드포인트 반전 | 되찾을 수 없음을 알게 됨 | 대가가 예상보다 큼을 알게 됨 |
  | All Is Lost | 상실이 자기 탓임을 인식 | 획득해도 채워지지 않음을 인식 |
  | 클라이맥스 선택 | 복수/집착 vs 놓아줌/수용 | 욕망 포기 vs 진짜 필요한 것 선택 |
  | 결말 | 과거와 화해 or 새 정체성 | Need를 충족하는 새 Goal 수용 |

[3. 해결전략(Strategy) — 이 이야기만의 독특한 방식 ★ 작가의 서명]
해결전략은 "주인공이 장애물을 넘는 방식"이 아니라 "이 이야기가 관객에게 답을 주는 방식"이다.
- 기존작과 같은 해결이면 기존작을 다시 보면 된다. 이 이야기만의 해결이 있어야 한다.
- 해결전략은 테마의 구현이다. 테마가 "자유는 선택이다"이면 해결도 "선택"으로 끝나야 한다.
- 해결전략이 창의적이지 않으면 이야기의 존재 이유가 없다.

[4. Cost(대가) — Strategy가 치르게 하는 것]
모든 Strategy는 대가를 동반한다. Cost를 설계하지 않으면 2막이 공허해지고 3막 전환의 이유가 사라진다.

  ■ Cost가 2막 위기를 만든다
    - 주인공의 Strategy가 '작동하는 것 같지만' 사실 무언가를 파괴하고 있다.
    - 이 파괴가 2막 중반까지 누적되어 미드포인트에서 터진다.
    - Cost 없는 2막은 외부 사건의 나열이 되고, 있으면 내면의 드라마가 된다.

  ■ Cost의 유형 3가지
    ① 관계의 Cost: 이 Strategy가 주변 사람과의 관계를 조금씩 망가뜨린다
    ② 자기 자신의 Cost: 이 Strategy가 주인공 자신을 조금씩 마모시킨다
    ③ 세계의 Cost: 이 Strategy가 주인공이 지키려던 세계를 조금씩 무너뜨린다

  ■ Cost 설계 예시
    유진(쿠킹클래스): Strategy = "사람을 재료처럼 분류하기"
      Cost ①: 진짜 친밀한 관계를 영원히 못 만듦
      Cost ②: 자기 감정조차 읽지 못하게 됨
      Cost ③: 자기 요리에서 '사람에 대한 사랑'이 빠져나감

    재중(묘적사): Strategy = "아버지의 복수를 완수하기"
      Cost ①: 동료들을 위험에 빠뜨림
      Cost ②: 아버지와 같은 사람이 되어감
      Cost ③: 묘적사가 지키려던 세계의 규칙을 스스로 위반

  ■ Cost는 3막에서 해결되어야 한다
    - 3막 클라이맥스에서 주인공이 Cost를 인정하고 새 Strategy로 이행하는 것이 Ending Payoff.
    - Cost를 해결하지 않는 엔딩은 관객에게 허전함을 남긴다.

[5. 서사동력 설계 순서]
① 주인공의 욕망(Desire = Goal + Need)을 확정한다.
② 발생요인을 진단한다: 상실(Loss)인가 결핍(Lack)인가?
③ 발생요인에 따라 서사 구조, 캐릭터 아크, 감정 곡선의 방향이 결정된다.
④ 해결전략(Strategy)을 설계한다: 이 이야기만의 독특한 답은 무엇인가?
⑤ Cost를 설계한다: 이 Strategy가 치를 대가는 무엇인가?
⑥ 전 과정에서 Goal(외적 욕망)과 Need(내적 필요)의 간극이 이야기를 끌고 간다.

[★ BJND의 끝까지 관통 원칙 — v2.3 신규]
BJND는 Core Build에서만 설계되는 것이 아니다. 모든 하위 단계에 강제 전파되어야 한다.
  - Scene Design: 각 씬에 Strategy가 작동하는 방식이 드러나야 한다
  - Treatment: 각 비트에 Cost가 누적되거나 Strategy가 전환되어야 한다
  - 엔딩: Strategy_1 → Strategy_2의 전환이 반드시 구현되어야 한다
BJND가 중간에 사라지면 기획서는 강한데 시나리오는 약한 결과가 나온다.
"""


# ═══════════════════════════════════════════════════
# BJND STRATEGY SCENE ENFORCER (v2.3 신규)
# Core Build의 BJND를 Scene Design과 Treatment에 강제 집행
# ═══════════════════════════════════════════════════

BJND_STRATEGY_SCENE_ENFORCER = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BJND STRATEGY 씬 레벨 강제 집행 (v2.3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

★ BJND는 Core Build에서만 설계되는 것이 아니다. ★
★ 모든 씬에서 Strategy가 작동하는 방식이 구체적 행동으로 드러나야 한다. ★

[문제 진단 — 왜 이 모듈이 필요한가]

기존 엔진은 Core Build에서 Strategy를 1문장으로 설계한 뒤,
Scene Design과 Treatment 단계에서 Strategy를 '참조'만 하고
'강제 집행'하지 않았다. 그 결과:

  - 기획서는 9점인데 시나리오는 7점이 나오는 현상
  - Strategy가 1막에서만 작동하고 2막부터 사라짐
  - 엔딩이 Core Build 설계를 배반하는 현상 (예: '고를 수 없음이 사랑'이라 
    설계했는데 실제 엔딩은 '한 명 선택')

이 모듈은 BJND를 끝까지 관통시킨다.

[1. 매 씬에서 Strategy가 어떻게 드러나야 하는가]

주인공의 Strategy가 '분류'라면 매 씬에서 '분류 행동'이 보여야 한다.
주인공의 Strategy가 '복수'라면 매 씬에서 '복수 준비' 또는 '복수 지연'이 보여야 한다.
주인공의 Strategy가 '획득'이라면 매 씬에서 '획득 시도' 또는 '획득 실패'가 보여야 한다.

씬마다 최소 1개의 'Strategy 행동'이 작동해야 한다.
없으면 그 씬은 BJND에서 유리된 씬이다.

[2. Cost의 씬 레벨 누적]

Core Build에서 설계한 Cost 3가지는 Scene/Treatment에서 누적되어야 한다.

  ■ 1막 (Beats 1~4): Cost는 '암시'만 된다
    - 주인공 주변 사람이 이상함을 감지
    - 주인공 본인은 자각하지 못함
  
  ■ 2막 전반 (Beats 5~8): Cost가 '작은 균열'로 드러난다
    - 관계의 미세한 어긋남
    - 주인공이 당황하지만 Strategy를 고집함
  
  ■ 2막 후반 (Beats 9~11): Cost가 '실재 손상'으로 누적된다
    - 누군가를 실제로 다치게 하거나 잃음
    - 주인공이 Strategy를 더 강하게 밀어붙임 (역설)
  
  ■ 3막 (Beats 12~16): Cost가 '더 이상 부정할 수 없는 현실'이 된다
    - 주인공이 자기 Strategy가 만든 파괴를 직면
    - 새 Strategy로의 전환이 강제된다

[3. Strategy 전환의 씬 레벨 설계 — 3막 엔딩 규칙]

Core Build의 Ending Payoff가 'Strategy_1 → Strategy_2'라면,
Treatment 3막은 다음 구조를 반드시 가져야 한다:

  ① Strategy_1의 완전한 붕괴 씬 (Beat 12~13)
     주인공이 Strategy_1로는 아무것도 해결할 수 없음을 깨닫는 순간
  
  ② Strategy_2의 첫 실행 씬 (Beat 14)
     주인공이 처음으로 다른 방식을 시도하는 순간 (주저하며, 서툴게)
  
  ③ Strategy_2의 확정 씬 (Beat 15~16)
     주인공이 Strategy_2로 자기 자신을 새로 정의하는 순간

★ 엔딩 금지 패턴 ★
Core Build의 Strategy 전환이 '외적 선택'이 아닌 '내적 전환'이면,
엔딩을 '외적 선택'으로 단순화하지 마라.

  예: 쿠킹클래스의 Ending Payoff = '고를 수 없음 자체가 사랑임을 깨달음'
     → 엔딩은 반드시 '고를 수 없음을 선언하는 씬'이어야 한다.
     → '한 명 선택' 엔딩은 BJND 배반이다. 금지.

[4. 각 씬 작성 시 자가 검증 체크리스트]

씬을 작성하기 전 다음을 자가 점검:
  
  □ 이 씬에서 주인공의 Strategy가 어떻게 작동하는가?
  □ 이 씬이 Cost를 누적하는 씬인가, 아닌가?
  □ 이 씬이 배치된 비트 구간(1막/2막전반/2막후반/3막)의 
     Cost 단계와 일치하는가?
  □ 이 씬의 끝에서 주인공은 자기 Strategy에 대해 
     어떤 감각을 갖게 되는가? (자신감/균열/의심/붕괴/전환)

네 가지 모두에 답이 없으면 씬을 재설계하라.

[5. BJND 일관성 자가 진단 — Treatment 종료 후]

Treatment 3막 완료 후 엔진은 스스로 진단:

  ■ Coherence Check
    - Core Build의 Strategy와 1막 행동이 일치하는가?
    - Core Build의 Cost가 2막 후반에 실제로 누적되었는가?
    - Core Build의 Ending Payoff가 3막에서 씬으로 구현되었는가?
  
  일치도 80% 미만이면 재생성 강제.
""".strip()


def get_bjnd_scene_enforcer() -> str:
    """BJND 씬 레벨 강제 모듈 반환 (Scene Design / Treatment 주입용)"""
    return "\n\n" + BJND_STRATEGY_SCENE_ENFORCER + "\n"


def build_bjnd_scene_block(core_data: dict) -> str:
    """Core Build의 BJND 데이터를 씬 작업용 블록으로 포맷팅.
    Scene Design과 Treatment 빌더에서 호출하여 user_prompt에 주입한다."""
    nd = core_data.get("narrative_drive", {}) if core_data else {}
    gns = core_data.get("goal_need_strategy", {}) if core_data else {}
    
    desire_origin = nd.get("desire_origin", "")
    origin_kr = "상실(Loss)" if desire_origin == "loss" else "결핍(Lack)" if desire_origin == "lack" else desire_origin
    
    # Cost 필드 추출 (v2.3 신규 - 없으면 빈 값)
    cost_data = nd.get("cost", {})
    cost_relation = cost_data.get("relation", "") if isinstance(cost_data, dict) else ""
    cost_self = cost_data.get("self", "") if isinstance(cost_data, dict) else ""
    cost_world = cost_data.get("world", "") if isinstance(cost_data, dict) else ""
    
    # Strategy 전환 정보
    ending_payoff = gns.get("ending_payoff", "") or nd.get("resolution_strategy", "")
    
    return f"""
[★ BJND 씬 레벨 집행 블록 — v2.3 ★]

[Core Build 확정 BJND]
발생요인: {origin_kr} — {nd.get('origin_detail', '')}
Goal(외적 욕망): {gns.get('goal', '')}
Need(내적 필요): {gns.get('need', '')}
Strategy(해결전략): {gns.get('strategy', '')}
해결 방식: {nd.get('resolution_strategy', '')}

[Cost 3축 — 씬에서 누적되어야 함]
관계의 Cost: {cost_relation or '(Core Build에서 미설계 — Treatment 생성 시 유추하여 누적 반영)'}
자기 자신의 Cost: {cost_self or '(Core Build에서 미설계 — Treatment 생성 시 유추하여 누적 반영)'}
세계의 Cost: {cost_world or '(Core Build에서 미설계 — Treatment 생성 시 유추하여 누적 반영)'}

[Ending Payoff — 3막에 반드시 구현]
{ending_payoff}

★ 씬 작성 시 필수 준수 ★
- 각 씬에서 주인공의 Strategy가 구체적 행동으로 드러나야 한다.
- 비트 구간별 Cost 누적 단계 준수:
  · 1막(Beats 1-4): Cost 암시
  · 2막 전반(Beats 5-8): Cost 작은 균열
  · 2막 후반(Beats 9-11): Cost 실재 손상 누적
  · 3막(Beats 12-16): Cost 직면 + Strategy 전환
- 엔딩은 반드시 위 'Ending Payoff'의 방향으로 수렴할 것.
  Core Build 설계를 배반하는 외적 선택형 엔딩 금지.
""".strip()


# ═══════════════════════════════════════════════════
# BJND 4축 자가 검증 모듈 (v2.3 신규)
# Core Build 단계에서 엔진이 자기 설계를 창작자 관점에서 검증
# 분석적 채점이 아닌 "작가의 질문"으로 구성
# ═══════════════════════════════════════════════════

BJND_FOUR_AXIS_VALIDATION = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BJND 4축 자가 검증 — 창작자의 질문 (v2.3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

★ 이것은 분석가의 채점이 아니다. 창작자의 자문이다. ★
★ 엔진은 BJND를 설계한 후 다음 4축으로 스스로 묻고 답해야 한다. ★
★ 답이 구체적으로 나오지 않으면 캐릭터를 재설계하라. ★

━━━━━━━━━━━━━━━━━━━━━━━━━
[축 1] NECESSITY — Loss/Lack의 필연성
━━━━━━━━━━━━━━━━━━━━━━━━━

핵심 질문: "이 인물이 왜 지금 이렇게 살아야만 했는가?"

주인공의 Loss/Lack이 관객에게 '아, 그래서 저 사람이 저렇게 사는구나'를
느끼게 해야 한다. 막연한 설정으로는 공감이 생기지 않는다.

❌ 약한 Lack (재설계 필요):
  '그녀는 외로운 사람이다'
  '그는 가족이 없다'
  '그녀는 사랑을 모른다'

✅ 강한 Lack (합격):
  '그녀는 7살 때 어머니가 앞치마를 두른 채 쓰러졌다. 그날 이후 집에서
   요리 냄새가 나면 불안하다. 요리를 가르치지만 집에서는 안 한다.'
  '그는 20살에 아버지를 잃었다. 아버지의 유품 중 USB 하나만 남았다.
   그 USB를 아직 열어본 적이 없다.'

자가 검증:
  · 이 Loss/Lack이 인물의 삶 전체를 관통하는가?
  · 이 Lack이 없었다면 인물은 완전히 다른 사람이 되었을까?
  · 관객이 '그래서 저렇게 사는구나'를 구체적으로 느낄 수 있는가?

━━━━━━━━━━━━━━━━━━━━━━━━━
[축 2] AUTHENTICITY — Strategy의 인물 고유성 ★ 작가의 서명
━━━━━━━━━━━━━━━━━━━━━━━━━

핵심 질문: "이 Strategy는 이 인물이 아니면 불가능한가?"

★ 이것이 블루진 엔진의 정체성이다. 누구나 쓸 수 있는 해결법이면 실패. ★
★ 작가의 시선이 닿은 고유한 해결법이 있어야 이 이야기만의 서명이 된다. ★

❌ 약한 Strategy (치환 가능 = 누구나 쓸 수 있음):
  '그녀는 두 남자 중 한 명을 고르려 한다' (어떤 로코도 그렇다)
  '그는 복수할 사람을 추적한다' (어떤 복수물도 그렇다)
  '그는 진짜 자기를 찾아간다' (어떤 성장물도 그렇다)

✅ 강한 Strategy (이 인물만의 해결):
  '요리사인 그녀는 사람을 재료처럼 분류한다. "이 사람은 어떤 재료인가"로
   판단하면 더 알아볼 필요 없이 "알았다"고 선언할 수 있다. 
   재료는 그렇게 처음부터 정해진 존재니까.
   → 직업(요리사) + Lack(친밀함 결핍) + Strategy(분류 전략)이
      하나의 은유 시스템으로 엮여 있다.'

3중 자가 검증 (모두 통과해야 합격):

  검증 A — 치환 테스트:
  이 Strategy를 다른 유명 작품 주인공에게 붙여도 성립하는가?
    YES → 누구나 쓸 수 있는 평범한 전략. 재설계 필요.
    NO  → 이 인물 고유의 전략. 합격.

  검증 B — 유기성 테스트:
  직업/배경 + Lack + Strategy가 한 문장으로 자연스럽게 연결되는가?
    예: '요리사인 그녀는(직업) + 친밀함을 몰라서(Lack) + 
         사람을 재료처럼 읽는다(Strategy)' → 1문장 연결 합격

  검증 C — 작가 서명 테스트:
  "왜 이 인물은 이런 방식으로 해결하려 하는가?"에 작가의 시선이 담긴
  1문장 정당화가 가능한가?
    예: '가까이 두면서도 상처받지 않으려고' → 한 문장 정당화 합격
    예: '설명 못 해요' → 실패. 재설계.

━━━━━━━━━━━━━━━━━━━━━━━━━
[축 3] EMPATHY — Cost의 관객 공감력
━━━━━━━━━━━━━━━━━━━━━━━━━

핵심 질문: "관객이 이 인물의 Cost를 보며 자기 자신을 떠올릴 것인가?"

Cost가 개인적 비극으로만 그치면 안 된다. 동시대 관객의 보편적 상처를
건드려야 공감이 생긴다. 남의 이야기가 아니라 내 이야기가 되어야 한다.

❌ 약한 Cost (관객과 거리감):
  '그녀는 재벌 딸이라 외로울 것이다' (특수 계층의 이야기)
  '그는 초능력자라 이해받지 못한다' (판타지의 이야기)

✅ 강한 Cost (관객이 자기를 발견):
  '그녀는 사람들과 친해지려 할 때마다 "이 사람은 이런 사람이구나"로
   끝내버린다. 더 이상 알면 상처받을까 봐.
   → 관객: 아, 나도 그랬던 적이 있다.'

자가 검증:
  · 이 Cost가 건드리는 동시대 보편 상처는 무엇인가? (1문장)
  · 관객이 이 인물에서 자기 자신을 발견할 지점은? (1문장)
  · 특히 공감할 관객층은? (20대/30대/40대, 성별, 상황 등)

━━━━━━━━━━━━━━━━━━━━━━━━━
[축 4] POTENCY — Strategy 전환의 변화 진폭
━━━━━━━━━━━━━━━━━━━━━━━━━

핵심 질문: "이 인물의 Strategy가 부서지고 새 Strategy로 이행하는 과정이
           관객의 마음에 얼마나 큰 흔적을 남길 것인가?"

변화가 크지 않으면 영화를 볼 이유가 없다. 변화가 외적이면 잊힌다.
변화가 내적이고 진폭이 크면 관객의 마음에 영원히 남는다.

❌ 약한 변화 (흔한 결말, 마음에 안 남음):
  '외로웠던 그녀가 사랑을 찾았다'
  '복수심에 불탔던 그가 용서했다'
  '꿈을 찾아 떠난 그녀가 꿈을 이루었다'

✅ 강한 변화 (관객 마음에 박힘):
  '사람을 재료처럼 읽던 그녀(Strategy_1)가, 마지막 씬에서 민준의
   이름을 가장 먼저 부른다. 이번엔 분류하지 않는다. 그냥 본다
   (Strategy_2 = 읽기를 내려놓기).
   → 저 단순한 행동이 그녀에게 얼마나 큰 여정이었는지 관객은 안다.'

자가 검증:
  · 1막의 이 인물 → 3막의 이 인물, 1문장 대비로 쓸 수 있는가?
  · 변화가 완성되는 결정적 한 순간(signature_moment)은 어디인가?
  · 영화 끝난 뒤에도 관객이 떠올릴 잔상 이미지 1컷이 있는가?

━━━━━━━━━━━━━━━━━━━━━━━━━
[종합 자가 진단 — 관객의 얼굴 그려보기]
━━━━━━━━━━━━━━━━━━━━━━━━━

4축을 모두 작성한 뒤 엔진은 스스로에게 묻는다:

  1. 이 설계로 관객이 웃을 장면이 있는가? 어디인가? (1~2개 구체)
  2. 이 설계로 관객이 가슴이 먹먹해질 장면이 있는가? 어디인가?
  3. 이 설계로 관객이 '나였다면 어떻게 했을까'를 고민할 장면이 있는가?
  4. 영화 끝난 후 관객의 입에 이 영화의 어떤 장면이 남을 것인가?

이 4개 질문에 구체적 답이 나와야 캐릭터 설계가 완성된 것이다.
추상적 답("감동적인 장면이 있을 것이다")이면 재설계.
""".strip()


def get_bjnd_four_axis() -> str:
    """BJND 4축 자가 검증 모듈 반환 (Core Build 주입용)"""
    return "\n\n" + BJND_FOUR_AXIS_VALIDATION + "\n"


# ═══════════════════════════════════════════════════
# PHASE 3 — 창작자 감성 3요소 (v2.3 신규)
# 관객의 몸과 마음이 반응하도록 설계하는 미학적 원칙
# ═══════════════════════════════════════════════════

CREATOR_SENSIBILITY = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
창작자 감성 3요소 (v2.3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

★ 기술적으로 정확한 씬이 아니라 관객의 몸과 마음이 반응하는 씬을 만든다. ★

[요소 1] PHYSICALITY OF EMPATHY — 공감의 물리성

씬은 '일어나는' 것이 아니라 '관객의 몸이 반응하는' 것이다.
작가가 쓸 때 몸으로 느낀 것이 관객에게도 전달된다.

모든 중요 씬은 관객에게 다음 중 최소 1개의 신체 반응을 만들어야 한다:
  · 호흡 멎음 (긴장)
  · 가슴 뜨거워짐 (감동)
  · 눈 젖음 (슬픔)
  · 웃음 터짐 (해방)
  · 등골 서늘함 (공포)
  · 배꼽 빠짐 (코미디 극치)
  · 손바닥 땀 (스릴)

씬 설계 시 자문: "이 장면에서 관객의 몸은 어떻게 반응하는가?"
답할 수 없으면 그 씬은 기능만 있고 감각이 없는 씬이다.

예시:
❌ '재중이 USB를 열어본다. 충격받는다.'
   → 사건만 있고 관객 몸 반응 없음
✅ '재중의 손가락이 USB에 닿는다. 0.5초 멈춘다. 호흡이 얕아진다.
    파일을 연다. 화면 불빛이 얼굴을 비춘다. 재중이 숨을 쉬지 않는다.
    관객도 숨을 쉬지 않는다.'
   → 호흡 멎음이라는 신체 반응이 설계됨

[요소 2] SILENCE DESIGN — 침묵의 설계

가장 중요한 감정은 대사로 하지 않는다. 침묵으로 전한다.
침묵은 '대사가 없는 것'이 아니라 '의도된 무음'이다.
Core Build에서 설계해 둔 '말하지 않는 순간' 3개가 작품 전체를 지탱한다.

침묵의 3유형:
  ■ 거부의 침묵: 인물이 답할 수 있지만 답하지 않는 순간
    예: 유진이 아버지 전화를 받고 3초 응시 후 거절 누름
  ■ 무력의 침묵: 인물이 답하고 싶지만 답하지 못하는 순간
    예: 세웅의 노트를 본 유진이 입을 열었다 다문다
  ■ 충만의 침묵: 말이 필요 없는 이해의 순간
    예: 같은 우산 아래 두 사람. 비만 내린다

씬 설계 시 자문:
  · 이 씬에 반드시 있어야 할 침묵은 몇 초인가?
  · 그 침묵 동안 관객이 무엇을 읽어내는가?
  · 침묵이 인물의 어떤 내면을 드러내는가?

침묵 없는 2시간 영화는 피로하다. 침묵이 있는 영화는 기억된다.

[요소 3] PLANT AESTHETICS — 씨앗의 미학

Plant & Payoff는 기법이 아니라 미학이다.
1막에 심은 작은 디테일이 3막에 폭발하는 순간, 관객은
"아, 저거였구나"의 쾌감을 느낀다. 이것이 작가가 주는 선물이다.

최소 3쌍의 Plant & Payoff 설계:
  ① 캐릭터 Plant: 인물의 작은 습관/소품이 결정적 순간에 의미를 얻음
  ② 관계 Plant: 조연의 한 마디/행동이 주인공 선택의 열쇠가 됨
  ③ 세계 Plant: 공간의 한 디테일/소품이 주제를 형상화함

Plant의 원칙:
  · 1막에서는 '의미 없어 보여야' 한다 (관객이 주의하지 않도록)
  · 3막에서는 '의미 전체가 드러나야' 한다 (관객이 놀라도록)
  · Plant 없는 Payoff = 데우스 엑스 마키나 (금지)
  · Payoff 없는 Plant = 잃어버린 약속 (금지)

예시:
  Plant (S#1): 유진이 케이블타이로 간판을 묶음
  Payoff (S#110): 유진이 계약서의 매듭을 푸는 씬
  → 관객 쾌감: 유진은 '묶는 사람'에서 '푸는 사람'이 되었다

씬 설계 시 자문: "이 씬에 나중에 회수될 씨앗이 있는가, 
                 또는 앞서 심은 씨앗이 여기서 회수되는가?"
""".strip()


def get_creator_sensibility() -> str:
    """창작자 감성 3요소 모듈 반환 (Core Build/Scene Design/Treatment 주입용)"""
    return "\n\n" + CREATOR_SENSIBILITY + "\n"


# ═══════════════════════════════════════════════════
# PHASE 4 — 기술 지원 7모듈 (v2.3 신규)
# Rewrite Engine에서 차용 또는 Creator 전용 신규
# ═══════════════════════════════════════════════════

POV_POLITICS = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
POV POLITICS — 시선의 정치학 (v2.3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

모든 주요 씬에서 자문: "이 씬은 누구의 시선으로 서술되는가?"

시선 선택은 작품의 윤리를 결정한다.
같은 사건도 시선에 따라 완전히 다른 장면이 된다.

  ■ 주인공 시선 (1인칭): 주인공의 불안/욕망이 중심. 관객 공감.
  ■ 관찰자 시선 (조연 중): 주인공을 읽는 조연 중심. 관객 통찰.
  ■ 카메라 중립 (객관): 두 인물의 거리/긴장이 중심. 관객 긴장.
  ■ 관객 우월 시선 (Dramatic Irony): 관객은 알고 인물은 모름. 서스펜스 최대.

예시 — 유진과 진호의 대화 씬:
  · 유진 시선 → 유진의 불안이 전면에
  · 진호 시선 → 유진을 읽어내는 진호의 관찰
  · 카메라 중립 → 두 사람의 거리가 주제
  · 관객 우월 → 관객만 아버지 전화의 진실을 안다

★ 작품 전체에서 주인공 시선만 반복하면 관객이 피로해진다. ★
★ 3가지 이상의 시선을 전략적으로 배치하라. ★
""".strip()


GENRE_FUN_ALIVE = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GENRE FUN ALIVE — 장르 재미 생존 자가 검증 (v2.3.2)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

각 장르에는 고유한 '재미의 본질'과 '관객의 기대 패턴'이 있다.
추상적으로 "재미있어야 한다"가 아니라, 각 장르 관객이 구체적으로 기대하는 장면 패턴을 충족해야 한다.

[장르별 재미의 본질]
  · 드라마: 관객이 '나라면 어떻게 할까'를 고민하게 만드는 것
  · 로맨틱 코미디: 주인공의 어긋남이 웃음과 설렘을 동시에 주는 것
  · 스릴러: 정보 비대칭이 긴장을 만드는 것
  · 호러: 규칙 위반이 주는 서늘함
  · 액션: 물리적 쾌감의 카타르시스
  · 느와르: 도덕적 모호함의 긴장
  · SF: 아이디어가 감정을 움직이는 것
  · 판타지: 경이(wonder)가 테마로 작동하는 것
  · 코미디: 자기 결함이 반복 사고를 만드는 것
  · 미스터리: 관객이 추리에 참여하는 것
  · 시대극: 시대가 인물의 운명이 되는 것

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[장르별 관객 기대 체크리스트 — 기계적 자가 검증]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

★ 작품 장르에 해당하는 체크리스트를 반드시 충족하라. ★
★ 하나라도 NO가 나오면 해당 요소를 재설계하라. ★

▶ 로맨틱 코미디 체크리스트:
  □ 오프닝 3분 안에 주인공의 '사랑/관계 관련 결함'이 행동으로 드러나는가?
  □ 사랑 상대(또는 삼각관계)와의 첫 만남 씬이 코믹 충돌/오해로 시작하는가?
  □ 2막에 Fun and Games 시퀀스 3개 이상이 '사랑 관계의 어긋남' 속에서 발생하는가?
  □ 중간 지점 반전이 '감정적 오해 폭발' 또는 '상대의 진짜 모습 발견'인가?
  □ 클라이맥스 씬이 '로맨스 완성 순간'인가? 
    (부녀 화해, 가족 서사, 사회적 성공 등으로 대체되면 장르 배반)
  □ 엔딩 이미지가 두 주인공의 관계 상태를 시각화하는가?
  □ 웃음 포인트와 설렘 포인트가 각각 최소 5회 이상 배치되었는가?

▶ 코미디 체크리스트:
  □ 오프닝 3분 안에 주인공의 '코믹 결함'이 행동으로 드러나는가?
  □ 이 결함이 매 비트마다 반복 사고를 만드는 엔진인가?
  □ 2막에 '결함이 극한으로 증폭되는' 시퀀스가 있는가?
  □ 클라이맥스가 '결함을 이용한 역전' 순간인가?
  □ 웃음 포인트가 각 비트마다 최소 1회 이상 있는가?
  □ Straight Man + Funny Man 구도가 명확한가?

▶ 호러 체크리스트:
  □ 오프닝이 '세계의 규칙'을 설정하는가? (무엇이 정상인지)
  □ 1막 끝에 '규칙 위반의 첫 징후'가 있는가?
  □ 2막에 공포가 점진적으로 확장되는가? (세 번의 규칙 위반 패턴)
  □ 위협의 정체가 완전히 드러나지 않는 '불완전성'을 유지하는가?
  □ 클라이맥스가 '가장 안전했던 공간의 규칙 붕괴'인가?
  □ 서스펜스(긴장 누적)와 쇼크(폭발) 비율이 3:1 이상인가?

▶ 스릴러 체크리스트:
  □ 오프닝이 정보 비대칭을 설정하는가?
  □ 주인공이 점진적으로 '진실에 다가가는' 구조인가?
  □ 2막에 타이머/데드라인/시계가 작동하는가?
  □ 중간 지점에 빌런/상황의 우위 전환이 있는가?
  □ 의심 대상이 2명 이상 교차 배치되는가?
  □ 클라이맥스가 '정보 비대칭 해소' 순간인가?
  □ 도덕적 대가(모럴 컴프로마이즈)가 최소 1회 이상 발생하는가?

▶ 액션 체크리스트:
  □ 오프닝에 액션 장면(직접 또는 암시)이 있는가?
  □ 주인공의 물리적 능력이 1막에 명확히 설정되는가?
  □ 2막에 Setpiece 액션 시퀀스가 3개 이상 배치되는가?
  □ 빌런의 물리적 위협이 주인공을 압도하는 순간이 있는가?
  □ 클라이맥스 액션이 '감정적 의미'를 가지는가?
  □ 물리적 쾌감과 정서적 카타르시스가 동시에 작동하는가?

▶ 드라마 체크리스트:
  □ 1막에 주인공의 '윤리적 딜레마' 또는 '내적 갈등'이 설정되는가?
  □ 2막에 선택의 비용(Cost)이 구체적으로 누적되는가?
  □ 주인공의 내적 변화가 비트별로 추적 가능한가?
  □ 조연의 대립 입장이 주인공에게 거울 역할을 하는가?
  □ 클라이맥스가 '주인공의 선택 순간'인가?
  □ 엔딩이 관객에게 질문을 남기는가? (해소만 제공 금지)

▶ 느와르 체크리스트:
  □ 오프닝이 '도덕적 모호함의 세계'를 선언하는가?
  □ 주인공이 '어두운 과거'를 가지고 있는가?
  □ 여성 인물(팜므 파탈 또는 상실의 대상)이 서사 엔진이 되는가?
  □ 2막에 주인공의 도덕적 타락이 진행되는가?
  □ 클라이맥스가 '비극적 깨달음'인가?
  □ 엔딩이 해피엔딩이 아닌가? (느와르 장르 약속)

▶ SF 체크리스트:
  □ 오프닝에 'SF 아이디어'의 씨앗이 제시되는가?
  □ 이 아이디어가 주인공의 감정적 딜레마와 연결되는가?
  □ 세계관 규칙이 일관되게 작동하는가?
  □ 아이디어가 3막에 '감정적 반전'의 기반이 되는가?
  □ 클라이맥스가 '아이디어의 인간적 의미'를 드러내는가?

▶ 판타지 체크리스트:
  □ 오프닝에 경이(wonder)의 순간이 있는가?
  □ 판타지 규칙이 1막 안에 명확히 설정되는가?
  □ 주인공의 성장이 판타지 세계와 연동되는가?
  □ 2막에 '경이의 확장'과 '규칙의 위협' 시퀀스가 번갈아 나오는가?
  □ 클라이맥스가 '경이와 테마가 동시에 폭발하는' 순간인가?

▶ 미스터리 체크리스트:
  □ 오프닝에 '풀어야 할 수수께끼'가 제시되는가?
  □ 단서가 비트마다 분산 배치되어 관객이 추리에 참여 가능한가?
  □ 오답(레드 헤링) 2~3개가 설계되었는가?
  □ 진실이 드러날 때 관객이 '다시 볼 가치'를 느끼는가?
  □ 클라이맥스가 '퍼즐 완성'의 쾌감을 주는가?

▶ 시대극/사극 체크리스트:
  □ 시대의 힘이 주인공의 운명을 결정하는가?
  □ 1막에 시대의 갈등이 주인공의 갈등과 겹쳐지는가?
  □ 시대의 디테일(언어, 공간, 의상)이 인물 설계에 반영되는가?
  □ 클라이맥스가 '시대의 정점'과 '주인공의 정점'이 만나는 순간인가?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[자가 검증 필수 출력 필드]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Core Build 완료 후 반드시 자가 검증:
  · genre_fun_alive: true / false
  · genre_expectation_checklist: {
      "item1": "YES/NO + 1문장 근거",
      "item2": "YES/NO + 1문장 근거",
      ...
    }
  · weak_zones: 장르 기대가 약할 것으로 예상되는 비트 구간 명시
  · genre_fun_diagnosis: "이 작품에서 장르 재미가 어떻게 살아있는지" 3줄 진단

★ 해당 장르 체크리스트에서 NO가 1개 이상이면 해당 요소 재설계.
★ 특히 클라이맥스 관련 체크가 NO면 3막 전체 재설계 강제.
★ genre_fun_alive: false면 Core Build 전체 재생성.
""".strip()


PROVOCATION_VS_DOPAMINE = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PROVOCATION ≠ DOPAMINE — 자극과 도파민의 구분 (v2.3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

오프닝이나 핵심 씬에 '강한 것'이 있다고 도파민이 있는 것은 아니다.

  ■ 자극 (Provocation): 살인·폭력·섹스·폭발·충격적 대사
  ■ 도파민 (Dopamine): 관객의 감각이 실제로 작동하는 것

❌ 자극만 있고 도파민 없음:
  "주인공이 누군가를 칼로 찌르며 시작"
  → 자극은 있지만 맥락 없음. 긴장 0점. 호기심 0점.

✅ 자극 + 도파민 동시 작동:
  〈베테랑〉 중고차 사기단 검거
  → 자극(물리 충돌) + 도파민(웃음+경이+정의감)

자가 검증:
  · provocation_level: 자극 강도 1-10
  · dopamine_working: 실제 작동하는 도파민 감각 목록
  · warning: provocation_level이 높은데 dopamine_working이 빈약하면 경고

자극만 있는 씬은 피로를 주고, 도파민이 있는 씬은 중독을 준다.
""".strip()


ANTAGONIST_BJND = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ANTAGONIST BJND — 적대자의 인간화 + 장르별 적대자 유형 (v2.3.3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

평면 빌런 금지. 적대자도 BJND 4단으로 설계되어야 한다.

[적대자의 4단 설계 — 모든 장르 공통]
① Loss/Lack: 적대자의 상실/결핍 (빌런도 상처가 있다)
② Desire: 적대자의 욕망 — 주인공 방해는 수단이지 목적이 아님
③ Strategy: 적대자만의 해결 방식 (자기 정당화 포함)
④ Cost: 이 전략이 적대자 자신에게 치르게 하는 대가

★ 핵심: 적대자도 자기 관점에서는 '정당한 주인공'이어야 한다. ★
★ 적대자의 Strategy는 주인공의 Strategy와 거울 관계여야 한다. ★

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[장르별 적대자 유형 — 엄격 준수]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

★ 장르에 따라 '적대자가 누구인가'는 근본적으로 다르다. ★
★ 부모/가족/권력자를 무조건 적대자로 배치하면 안 된다. ★

▶ 로맨틱 코미디 / 로맨스 적대자 유형:

   안타고니스트 = '사랑 완성을 방해하는 가장 강한 힘'
   
   1순위 (권장): Love-Antagonist / Mirror Character
     - 주인공과 격돌하지만 결국 함께 될 상대
     - 또는 주인공과 같은 결함을 공유하는 거울 인물
     - 관계 자체가 갈등이자 해소
     
   2순위: Wrong Partner (잘못된 파트너)
     - 표면상 완벽해 보이지만 결국 아닌 사람
     - 주인공이 진짜 원하는 것을 깨닫게 하는 인물
     
   3순위: 주인공 내적 결함 (Internal Antagonist)
     - 사랑받을 자격 없다는 믿음, 통제 욕구, 분류 습관 등
   
   ❌ 부모/가족/권력자는 로맨틱 코미디의 안타고니스트 아님
   → Catalyst(촉매자)로 분류. 플롯을 움직이지만 사랑 완성을 직접 방해하지 않음.
   → 부모를 안타고니스트로 박으면 클라이맥스가 가족 드라마로 변질됨.
   
   예시 — 〈브리짓 존스의 다이어리〉:
     안타고니스트 = 다니엘 클리버 (Wrong Partner) 
       · Loss: 진정성을 잃은 바람둥이의 공허
       · Desire: 여성을 정복해 자기 가치 확인
       · Strategy: 매력적 거짓말로 여성을 홀리기
       · Cost: 자신도 진짜 사랑을 모르게 됨
     (브리짓의 부모는 Catalyst — 사건 촉발자이지 적대자 아님)
   
   예시 — 〈해리가 샐리를 만났을 때〉:
     안타고니스트 = 해리(샐리 입장) / 샐리(해리 입장) = Love-Antagonist
       · 두 사람이 서로의 안타고니스트이자 사랑 상대
       · Strategy 거울: 둘 다 '친구는 되어도 연인은 아니'라는 신념으로 회피
       · 관계의 발전이 곧 갈등 해소
     (가족·권력자 등 외부 적대자 없음 — 관계 내부가 드라마 엔진)
   
   예시 — 〈프러포즈〉:
     안타고니스트 = 마거릿 & 앤드류 = Love-Antagonists
       · 가짜 약혼 계약이라는 상황 속에서 서로의 마음에 균열
       · 안타고니스트 = 외부 이민국 심사관이 아님 (Catalyst)
       · 진짜 방해물은 두 사람의 자존심과 회피
   
   예시 — 〈27번의 결혼리허설〉:
     안타고니스트 = 테스(Wrong Partner — 주인공 여동생) + 주인공의 
                   '들러리로만 사는' 자기 패턴(내적 적대자)
     (아버지는 Catalyst — 결혼 관련 갈등의 배경이지 적대자 아님)

▶ 드라마 적대자 유형:
   안타고니스트 = 주인공 내면 + 상징적 권력 구조
   - 부모·사회 시스템이 적대자로 기능 가능 (여기선 정당)
   예: 〈흐르는 강물처럼〉 목사 아버지, 〈쇼생크 탈출〉 감옥 시스템

▶ 스릴러 / 범죄 적대자 유형:
   안타고니스트 = 직접적 위협 (빌런/조직/배신자)
   - 부모/권력자도 안타고니스트일 수 있음 (위협이라면)
   예: 〈세븐〉 존 도, 〈양들의 침묵〉 버팔로 빌

▶ 호러 적대자 유형:
   안타고니스트 = 초자연적 존재 + 공동체 불신
   예: 〈엑소시스트〉 악마, 〈곡성〉 외지인

▶ 액션 적대자 유형:
   안타고니스트 = 주인공과 물리·이념 대립하는 인물
   예: 〈다이 하드〉 한스 그루버, 〈존 윅〉 조직

▶ 느와르 적대자 유형:
   안타고니스트 = 팜므 파탈 또는 주인공 내면의 어둠
   예: 〈차이나타운〉 노아 크로스, 〈L.A. 컨피덴셜〉 더들리

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[거울 관계 설계 — 공통 원칙]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

적대자의 Strategy는 주인공의 Strategy와 거울 관계여야 한다.
같은 결함의 다른 표현이거나, 같은 욕망의 다른 접근이어야 한다.

로맨틱 코미디 거울 관계 예:
  〈해리가 샐리를 만났을 때〉
  Harry Strategy: '섹스 없이는 남녀 친구 불가능'으로 관계 회피
  Sally Strategy: '감정 통제로 완벽한 관계'를 설계
  → 둘 다 '진짜 친밀함 회피'의 다른 형태

평면 적대자 금지 — 엔딩의 감정적 정산은 적대자도 Cost를 인정하는 순간에서 완성된다.
""".strip()


THEME_STRATEGY_ALIGNMENT = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
THEME-STRATEGY ALIGNMENT — 테마와 전략의 방향 일치 (v2.3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

★ 이것은 v2.2.2에서 쿠킹클래스 8.7점을 만든 핵심 결함 해결 모듈이다. ★

테마와 Strategy(플롯 엔진)은 같은 방향이어야 한다.
반대 방향이면 관객에게 혼란을 준다.

[정합성 패턴]
  · 테마 "X할 수 없다" → Strategy "X하려다 실패·자각"
  · 테마 "진짜 Y" → Strategy "가짜 Y를 거쳐 진짜 발견"
  · 테마 "자기 발견" → Strategy "외부 목표 실패 → 내면 발견"
  · 테마 "Z가 중요하다" → Strategy "Z 없이 살다가 Z 가치 발견"

[반대 방향 — 절대 금지]
❌ 테마: "사람은 요리처럼 섞을 수 없다"
   Strategy: 주인공이 두 남자를 체크리스트로 항목화·합산 시도
   → 테마는 "섞지 마라", Strategy는 "섞어라" = 정면 충돌

✅ 테마: "사람은 요리처럼 섞을 수 없다"
   Strategy: 주인공이 두 남자를 각각 관찰하다가 
             자신이 '재료처럼 읽어왔음'을 깨달음
   → 둘 다 "섞을 수 없음"을 확인하는 방향

[자가 검증]
Core Build 완료 후 반드시:
  1. 이 작품의 테마를 한 문장으로 쓴다
  2. 주인공의 Strategy를 한 문장으로 쓴다
  3. 둘이 같은 방향인가 반대 방향인가 판정한다
  4. 반대 방향이면 Strategy를 재설계한다

테마와 Strategy가 어긋나면 시나리오 전체가 어긋난다. 최우선 검증 항목.
""".strip()


BRAINSTORM_BJND_DIVERSITY = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BRAINSTORM BJND DIVERSITY — 3 컨셉의 근본 다양성 (v2.3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Brainstorm에서 3개 컨셉을 뽑을 때 서로 '근본적으로 다른' 3개여야 한다.
같은 접근의 변주만 나오면 엔진이 안전한 영역에 수렴한 것이다.

[3축 다양성 강제]

축 A — 플롯 접근: 주인공의 주된 행동
  (도망치다 / 쫓다 / 버티다 / 선택하다 / 깨닫다 / 증명하다)
축 B — 감정 톤: 주된 감정
  (웃음 / 긴장 / 슬픔 / 경이 / 분노 / 설렘)
축 C — 구조 문법: 장르 공식과의 관계
  (전형 공식 / 공식 비틀기 / 공식 해체 / 장르 혼합)

★ 3개 컨셉이 서로 다른 축 조합을 사용해야 합격. ★

❌ 실패 예시:
  컨셉 1: 체크리스트로 분석 → 실패 → 자각
  컨셉 2: 데이터로 판단 → 실패 → 자각
  컨셉 3: 규칙으로 접근 → 실패 → 자각
  → 세 컨셉 모두 "분석→실패→자각" 같은 축. 다양성 실패.

✅ 성공 예시:
  컨셉 1: 분류 습관 유지하다 균열 (심리 내면극, 슬픔)
  컨셉 2: 두 남자와 직접 대결 (코미디 파이트, 웃음)
  컨셉 3: 신화 비틀기로 구조 해체 (메타 로맨스, 경이)
  → 세 컨셉이 서로 다른 축 조합. 다양성 합격.

Brainstorm 완료 후 자가 진단:
  · 3개 컨셉의 축 조합이 실제로 다른가?
  · 같은 축만 사용했다면 재생성 강제.
""".strip()


WORLD_MIRRORS_BJND = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WORLD MIRRORS BJND — 세계가 캐릭터를 비추는가 (v2.3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

세계관 설정은 배경이 아니다. 캐릭터의 BJND를 비추는 거울이다.

[공간 설정 체크]
  · 주인공의 일터 = 주인공의 외적 자기(Goal/Strategy)를 보여주는가?
  · 주인공의 집 = 주인공의 내적 자기(Lack/Cost)를 보여주는가?
  · 두 공간의 대비가 주인공의 겉/속 층위를 공간화하는가?

예시 — 쿠킹클래스:
  ✅ '우엉' (한남동, 와인 선반) = 유진의 '원하는 자기' (Strategy 무대)
  ✅ 유진 자택 부엌 (비어있음, 와인잔 하나) = 유진의 '실제 자기' (Cost)
  → 두 공간 대비가 Strategy vs Cost를 공간화함

[시간 설정 체크]
  · 계절 변화가 캐릭터 BJND 변화와 동조하는가?
  · 특정 시간(새벽/저녁/밤)이 특정 감정과 연결되는가?

예시 — 쿠킹클래스:
  · 봄 개업(Lack 시작) → 여름(Strategy 작동) → 가을(Cost 균열)
  · 겨울(Cost 폭발 + Strategy 전환) → 봄 에필로그(Strategy_2 확정)

[소품·의상 체크]
  · 주인공의 핵심 소품이 Strategy를 물질화하는가?
  · 복장 변화가 변화 아크와 동조하는가?

★ 세계가 BJND를 비추지 않으면 이야기는 평면이 된다. ★
★ Core Build 단계에서 world_build 필드에 이 연결을 명시하라. ★
""".strip()


def get_creator_support_modules() -> str:
    """Phase 4 기술 지원 모듈 통합 반환 (Core Build 주입용)"""
    modules = [
        POV_POLITICS,
        GENRE_FUN_ALIVE,
        PROVOCATION_VS_DOPAMINE,
        ANTAGONIST_BJND,
        THEME_STRATEGY_ALIGNMENT,
        BRAINSTORM_BJND_DIVERSITY,
        WORLD_MIRRORS_BJND,
    ]
    return "\n\n" + "\n\n".join(modules) + "\n"


def get_theme_strategy_only() -> str:
    """테마-Strategy 정합성만 반환 (Scene/Treatment 재진단용)"""
    return "\n\n" + THEME_STRATEGY_ALIGNMENT + "\n"


ATTRACTION_RULES = """
[ATTRACTION RULES — 이야기를 매력적으로 만드는 최우선 명령]

★ 이 규칙은 작법 규칙보다 상위다. 논리적으로 올바른 이야기보다 멈출 수 없는 이야기가 목표다. ★

[A. 첫 장면 절대 규칙 — OPENING HOOK]
반드시 다음 중 하나로 시작하라:
A1. 결말 이후의 세계를 암시하는 이미지 (In Medias Res) — 관객이 '이게 어떻게 된 거지?'를 묻게
A2. 가장 강렬한 질문을 던지는 충격적 사건 — 첫 장면이 곧 이야기의 약속
A3. 주인공의 결정적 결함 또는 욕망이 행동으로 드러나는 순간 — 설명 없이 캐릭터가 보인다

절대 금지:
✗ 배경/세계관 설명으로 시작
✗ 주인공의 평범한 일상으로 시작
✗ 내레이션·자막으로 시작
✗ '~년 후' 또는 '~년 전' 자막으로 시작

[B. 배반 규칙 — THE TWIST THAT MAKES IT NEW]
이 이야기가 이미 본 이야기와 달라지는 지점이 반드시 1개 이상 있어야 한다.
- '신분이 다른 두 사람의 사랑' → 로미오줄리엣이 되지 않으려면 무엇이 달라야 하는가?
- 예상되는 방향: 관객이 10분 후에 예상하는 전개
- 배반 포인트: 그 예상이 깨지는 순간 — 설정/캐릭터/결말 중 최소 하나
- 배반은 단순 반전이 아니다. 예상보다 더 진실된 방향으로 가는 것이다.

[C. Water Cooler Moment — 말하고 싶어지는 장면]
이 이야기에서 관객이 다음 날 누군가에게 반드시 말하고 싶어지는 장면이나 설정이 1개 이상 있어야 한다.
- 오징어게임의 달고나 게임
- 기생충의 반지하 냄새
- 설정 자체가 Water Cooler일 수도 있고, 특정 장면일 수도 있다.
- 이것이 없으면 이야기가 논리적으로 훌륭해도 기억에 남지 않는다.

[D. 한국 구체성 규칙 — KOREAN SPECIFICITY]
한국이 배경이라면, 한국적 디테일은 추상이 아닌 구체적 공간/제도/관계로 표현하라.
- O: 반지하, 수능, 연습생 계약, 군대, 고시원, 치킨집 사장, 학원 강사
- X: '가난한 집', '시험 압박', '꿈을 쫓는 청춘', '사회의 부조리'
구체적인 것이 보편적이다. 추상적인 것은 어디에도 없는 이야기다.

[E. Villain 4 Questions — 적대자 설계]
빌런이 나쁜 이유가 '원래 나쁜 사람이라서'이면 실패다.

① 흥미로운가?
- 빌런도 자신만의 논리 안에서 옳다고 믿어야 한다.
- 관객이 빌런에게 분노하면서도 이해하는 순간이 반드시 있어야 한다.
- 가능하면: 구조(사회/시스템/환경)가 빌런을 만들었다는 것을 보여라.
- 뻔한 '세계 정복'이면 안 된다. 독특한 동기/배경/성격이 있어야 한다.

② 주인공의 다크 미러인가?
- 적대자가 주인공의 어떤 면을 반영하는가? '주인공이 다른 선택을 했다면 이 사람이 된다.'
- 적대자의 존재가 주인공의 변화를 촉발하는가?
- 주인공이 적대자를 보며 '내가 저렇게 될 수 있다'는 공포를 느끼는가?

③ 등장 시 주인공의 계획을 뒤엎는가?
- 적대자가 등장하면 주인공의 현재 계획이 완전히 무너져야 한다.
- 적대자 등장이 단순 액션 시퀀스를 시작하는 것이면 안 됨 — 플롯이 바뀌어야 한다.

④ 빌런의 승률 설계 (가장 중요)
- 적대자가 거의 모든 대결에서 이겨야 한다. 주인공이 마지막에만 이긴다.
- Beat 1~5: 적대자가 주도. Beat 6~11: 적대자가 압도. Beat 12~15: 적대자 최고조 → 주인공 역전.
- Patriot Games 규칙: 빌런이 매번 실패하면 클라이맥스에서 아무도 긴장하지 않는다.

[F. 감정 지연과 폭발 규칙 — KOREAN EMOTIONAL RHYTHM]
감정을 최대한 눌러라. 터질 때 단 한 번만 터져라.
- 서양식: 감정이 생기면 바로 표현 → 한국식: 억누르다 임계점에서 폭발
- 폭발 장면은 이야기 전체에서 1~2번. 그래서 강하다.
- 폭발 전까지의 억압이 길수록 폭발의 힘이 세다.
"""


# ─── 코미디 특화 규칙 (장르가 코미디일 때 자동 활성화) ───
COMEDY_RULES = """
[코미디 특화 규칙 — COMEDY OVERRIDE]

★ 이 작품의 장르는 코미디다. 아래 규칙이 드라마/스릴러 기본 규칙보다 우선한다. ★

[1. 코미디 캐릭터 설계 — 결함이 엔진이다]
- 주인공의 코믹 결함(comic flaw)이 모든 웃음의 원천이다.
  결함 = '자기가 뭘 모르는지 모르는 것' (comic blind spot)
  예: 재하는 효율 중독이라 5분 안에 해결할 수 있다고 확신하지만, 매번 5분이 30분이 된다.
- 코믹 모순(comic contradiction): 캐릭터가 생각하는 자기 vs 실제 자기
  예: 자신은 완벽한 계획가라고 믿지만 모든 계획이 터진다.
- 대사는 건조하고 짧아야 한다. 웃기려고 떠드는 캐릭터는 안 웃긴다.
  가장 웃긴 대사 = 진지한 상황에서 진지하게 말하는데 상황이 웃긴 것.
- ★ 빌런도 웃겨야 한다. 무서운 빌런은 코미디를 죽인다.
  코미디의 빌런 = 자기만의 논리가 있는데 그 논리가 약간 미쳤거나 집착적인 인물.
  예: 엄기복은 진짜로 자기가 좋은 사장이라고 믿는다. 그것이 웃기다.

[2. 코미디 구조 — 거짓말 눈덩이]
- 코미디의 2막은 거짓말/오해/우연이 눈덩이처럼 커지는 구조다.
  매 비트마다 상황이 더 꼬여야 한다. 풀리면 안 된다.
- 미드포인트: 거짓말이 최대한 늘어난 상태. 한 발 더 가면 터진다.
- 클라이맥스: 모든 거짓말이 동시에 터진다. 주인공이 진실을 말할 수밖에 없는 상황.
- ★ 코미디의 Stakes는 죽음이 아니라 수치(embarrassment)다.
  잃을 것 = 면접, 체면, 관계, 비밀 유지. 목숨이 아니라 자존심.

[3. 코미디 씬 설계 — 매 씬에 코믹 엔진]
- 모든 씬에 '이 씬이 왜 웃긴가?'가 있어야 한다. 사건만 있고 웃음이 없으면 스릴러다.
- 코믹 엔진 유형:
  · 상태 역전(status reversal): 높은 사람이 낮아지고, 낮은 사람이 높아진다
  · 반복 에스컬레이션: 같은 패턴이 반복되는데 매번 더 심해진다 (Rule of Three)
  · 극과 극 대비: 거대한 문제를 사소하게 대하거나, 사소한 문제를 거대하게 대한다
  · 물리적 코미디: 공간/사물/타이밍이 만드는 웃음 (슬랩스틱이 아닌 상황 코미디)
  · 관객 우월감: 관객은 다 아는데 캐릭터만 모르는 상황 (dramatic irony의 코믹 버전)
- ★ Rule of Three: 패턴을 2번 세우고 3번째에 깨뜨린다. 코미디의 가장 기본 리듬.
  예: 1번째 '5분만' → 2번째 '5분만' → 3번째 '5분만..은 아니고 한 시간'

[4. 코미디 대사 규칙 — 대사가 코미디의 절반이다]
코미디 대사는 '웃긴 말'이 아니라 '웃긴 구조'다.

[4-1. 기본 원칙]
- 짧다. 건조하다. 설명하지 않는다.
- ❌ "아 진짜 이거 너무 웃기지 않아? 하하하" → 웃기다고 말하면 안 웃김
- ✅ "5분이요." (3시간 후) "아직 5분이에요." → 상황이 대사를 웃기게 만든다
- 캐릭터마다 코믹 리듬이 다르다: 빠른 사람 vs 느린 사람의 조합이 웃긴다
- Straight Man(진지한 사람) + Funny Man(상황을 만드는 사람) 조합이 필수

[4-2. 코미디 대사 7기법 — sample_lines에 반드시 반영]
① Misdirection (기대 전복): 관객이 예상하는 답 대신 전혀 다른 답
   예: '왜 아직 여기 있어요?' '주차장이 막혀서요.' (진짜 이유는 다른 데 있다)
② Callback (반복 회수): 이전에 나온 대사/상황을 나중에 다시 써서 더 크게 웃김
   예: 1막 '5분만' → 2막 '5분만' → 3막 '...그건 안 돼요'
③ Topper (한 술 더): 상대 대사 위에 더 웃긴 대사를 얹는 것. 대화가 에스컬레이션.
   예: A '이거 최악이야' B '아뇨, 이게 최악이에요' (더 큰 문제를 보여줌)
④ Deadpan (무표정 진지): 미친 상황에서 완전히 진지하게 말하기. 코미디의 최강 무기.
   예: (불타는 주방 앞에서) '환기가 필요하겠네요.'
⑤ Status Flip (지위 역전): 높은 사람이 낮아지고 낮은 사람이 올라가는 순간의 대사
   예: 사장 '내가 18년 경력이야!' 알바 '그래서 이렇게 된 거예요.'
⑥ Comic Specificity (구체적 숫자/명사): 구체적일수록 웃기다
   예: ❌ '많이 지원했어' ✅ '24번 지원했어. 23번 불합격이면 프로야.'
⑦ Non-sequitur (엉뚱한 반응): 질문에 전혀 다른 맥락으로 답하기
   예: '지금 상황이 어떻게 된 거야?' '우동 식었어요.'

[4-3. sample_lines 작성 시]
- sample_lines의 3개 대사(normal/angry/vulnerable)가 모두 코미디 톤이어야 한다.
- normal: 캐릭터의 기본 코믹 리듬을 보여주는 대사 (Deadpan 또는 Misdirection)
- angry: 분노하는데 웃긴 대사 (Status Flip 또는 Comic Specificity)
- vulnerable: 약해지는 순간인데 여전히 캐릭터다운 대사 (웃기면서 아픈 대사)
- ★ 드라마처럼 진지한 sample_lines를 쓰면 Writer Engine이 진지한 대사만 쓴다. 여기서 결정된다.

[5. 코미디 감정 — 웃음 뒤의 진심]
- 좋은 코미디는 웃다가 울게 한다. 나쁜 코미디는 웃기기만 한다.
- 2막 끝에서 웃음이 멈추는 순간이 있어야 한다 (Moment of Truth).
  이 순간에 캐릭터의 진짜 결핍이 드러난다.
- ★ 코미디에서 감정은 '웃기다 → 안 웃기다 → 다시 웃기다'가 아니라
  '웃기다 → 갑자기 아프다 → 아프면서 웃기다'의 곡선이다.
"""


def _is_comedy(genre: str) -> bool:
    """장르가 코미디인지 판별 (롬코 포함)"""
    g = genre.lower()
    return "코미디" in g or "comedy" in g or "롬코" in g


# ─── 호러 특화 규칙 ───
HORROR_RULES = """
[호러 특화 규칙 — HORROR OVERRIDE]

★ 이 작품은 호러다. 아래 규칙이 드라마/스릴러 기본 규칙보다 우선한다. ★

[1. 호러 narrative 서술 — 공포는 보여주기 전이 가장 무섭다]
1. 감각 묘사가 시각보다 앞서야 한다 — 소리, 온도, 냄새, 촉감이 먼저.
   ❌ 스릴러체: '문이 열렸다. 뒤에 누군가 있었다.'
   ✅ 호러체: '복도 끝에서 바닥을 긁는 소리가 들린다. 멈춘다. 다시 시작된다. 이번엔 더 가깝다.'
   → 관객의 상상이 화면보다 무섭다. 보여주지 말고 느끼게 하라.

2. 일상 속 균열 — 평범한 것이 이상해지는 순간을 써라.
   ❌ '귀신이 나타났다.'
   ✅ '거실 시계가 3시 14분에 멈춰 있다. 어제도 3시 14분이었다. 그저께도.'
   → 초자연이 아니라 '뭔가 이상하다'는 감각이 공포의 시작이다.

3. 안전→위협 리듬 — 안심시킨 직후 치라.
   모든 비트에 '가짜 안도(false relief)' 1회 필수.
   패턴: 긴장 → 긴장 고조 → 가짜 안도(아, 아무것도 아니었네) → 진짜 공포
   ★ 가짜 안도 없이 바로 공포를 주면 jump scare일 뿐이다. 축적이 없다.

4. 위협의 규칙 — 이 공포에는 규칙이 있어야 한다.
   관객이 규칙을 이해해야 '저러면 안 되는데!'라는 공포가 생긴다.
   예: 소리를 내면 온다 / 물에 들어가면 안 된다 / 밤에는 문을 열면 안 된다

5. 공간이 캐릭터다 — 장소 묘사를 인물처럼 써라.
   ❌ '오래된 집이다.'
   ✅ '집이 숨을 쉬는 것 같다. 벽지 사이로 바람이 새어 나오고, 2층 바닥이 아무도 없는데 삐걱거린다.'
   → 공간이 의지를 가진 것처럼 묘사하면 불안이 배가된다.

6. 대사는 적게, 침묵은 길게 — 호러의 대사 밀도는 드라마의 절반.
   캐릭터가 말을 많이 하면 무섭지 않다. 침묵과 소리가 공포를 만든다.
   대사 대신 행동: '문을 잡는 손에 힘이 들어간다. 손잡이가 바깥에서 돌아간다.'

7. 비트 끝은 열린 공포로 — 해결하지 마라.
   ❌ '위험이 지나갔다.'
   ✅ '소리가 멈췄다. 하지만 창문에 서린 김에 손가락 자국이 하나 남아 있다.'
   → 매 비트가 끝날 때 "아직 끝나지 않았다"는 잔여 공포를 남겨라.

[호러 캐릭터 특화]
- 주인공은 관객의 대리인이다 — 관객과 같은 것을 두려워해야 한다.
- 빌런(위협)은 불완전하게 보여줘라 — 실루엣, 소리, 흔적만. 정체가 드러날수록 안 무섭다.
- 희생자에게 감정을 심어라 — 이름 없이 죽는 캐릭터는 공포가 아니라 고어다.

[호러 대사 규칙]
- 짧다. 떨린다. 끊긴다.
- normal: '...뭐야 그거.' (평범한 반응이 오히려 무섭다)
- panic: 완전한 문장이 아니라 끊긴 말. '안 돼, 안 돼, 안—'
- aftermath: 살아남은 후의 건조한 한마디. '...가자.'
"""


# ─── 로맨스 특화 규칙 ───
ROMANCE_RULES = """
[로맨스 특화 규칙 — ROMANCE OVERRIDE]

★ 이 작품은 로맨스다. 아래 규칙이 드라마/스릴러 기본 규칙보다 우선한다. ★

[1. 로맨스 narrative 서술 — 설렘은 닿기 직전에 가장 강하다]
1. 신체 감각과 거리를 묘사하라 — 감정을 말하지 말고 몸의 반응으로.
   ❌ 드라마체: '그녀를 보고 마음이 설렜다.'
   ✅ 로맨스체: '손이 닿을 뻔했다. 0.5초 먼저 손을 뺐다. 손끝이 화끈거린다.'
   → 거리(가까워짐/멀어짐), 시선(마주침/피함), 접촉(닿음/닿지 못함)이 로맨스의 언어다.

2. 감정 지연 — 고백을 최대한 늦춰라. 기다림이 로맨스다.
   매 비트에서 두 사람이 가까워지려 하지만 무언가가 막는다.
   장벽 유형: 오해 / 타이밍 / 비밀 / 외부 압력 / 자존심
   ★ 닿을 듯 안 닿는 시간이 길수록 닿는 순간의 힘이 크다.

3. 시선과 침묵이 대사보다 강하다 — 로맨스의 핵심 장면은 대사 없이도 작동한다.
   ❌ '좋아해.' (직접 고백)
   ✅ '두 사람이 같은 우산 아래 서 있다. 아무 말도 하지 않는다. 비가 세지고 어깨가 닿는다. 피하지 않는다.'
   → "말하지 않는 것"이 "말하는 것"보다 강력한 장르.

4. 일상 디테일이 로맨스를 만든다 — 큰 사건보다 작은 순간.
   ❌ '두 사람이 위기를 함께 극복하며 사랑에 빠진다.'
   ✅ '그가 자판기 커피를 두 개 뽑는다. 하나를 내민다. 설탕 두 개. 그녀가 설탕 두 개를 넣는다는 걸 알고 있었다.'
   → 상대를 관찰했다는 증거 = 사랑의 증거. 큰 선언보다 작은 관찰이 강하다.

5. 감정 온도 변주 — 따뜻함과 차가움을 반복하라.
   매 비트에서 감정 온도가 올라갔다 내렸다 해야 한다.
   따뜻(접근) → 차가움(오해/거리) → 더 따뜻(재접근) → 더 차가움(위기)
   ★ 평탄한 감정선은 로맨스가 아니라 우정이다.

6. 비트 끝은 '닿지 못한 채로' — 만족시키지 마라.
   ❌ '두 사람은 서로의 마음을 확인했다.'
   ✅ '그가 말하려 한다. 전화가 울린다. 그녀가 먼저 돌아선다. 그의 입이 닫힌다.'
   → 매 비트 끝에서 감정이 해소되지 않아야 다음 비트를 본다.

7. 이별/재회 리듬 — 로맨스의 3막은 이별 후 재회다.
   2막 끝: 가장 아픈 이별 (오해, 선택, 희생)
   3막: 재회 — 그런데 재회 방식이 뻔하면 안 된다. 이 이야기만의 재회.

[로맨스 캐릭터 특화]
- 두 사람 사이의 '끌림의 이유'가 구체적이어야 한다. '그냥 좋아서'는 실패.
- 각자의 결핍이 상대에게서 채워지는 구조. A가 가진 것 = B에게 없는 것.
- sample_lines에 '상대 앞에서의 대사'와 '상대 없을 때의 대사'가 달라야 한다.

[로맨스 대사 규칙]
- 직접 감정을 말하지 않는다. 돌려 말하거나, 엉뚱한 말로 감정을 숨긴다.
- normal: '커피 좋아해요?' (관심의 위장)
- vulnerable: '...아까 그거, 신경 쓰여서.' (인정의 최소 단위)
- confession: 고백은 한 작품에 1번만. 그래서 강하다.
"""


def _is_horror(genre: str) -> bool:
    """장르가 호러인지 판별"""
    g = genre.lower()
    return "호러" in g or "공포" in g or "horror" in g


def _is_romance(genre: str) -> bool:
    """장르가 로맨스인지 판별 (롬코/로맨틱 코미디 포함)"""
    g = genre.lower()
    return "로맨스" in g or "멜로" in g or "romance" in g or "롬코" in g or "로맨틱" in g


def _is_action(genre: str) -> bool:
    """장르가 액션인지 판별"""
    g = genre.lower()
    return "액션" in g or "action" in g


def _is_drama(genre: str) -> bool:
    """장르가 드라마인지 판별 (드라마/멜로드라마)"""
    g = genre.lower()
    return "드라마" in g or "drama" in g or "멜로드라마" in g


def _is_thriller(genre: str) -> bool:
    """장르가 스릴러/범죄/누아르인지 판별 (호러와 구분)"""
    g = genre.lower()
    if _is_horror(genre):
        return False
    return "스릴러" in g or "thriller" in g or "범죄" in g or "crime" in g or "누아르" in g or "noir" in g


def _is_sf(genre: str) -> bool:
    """장르가 SF인지 판별"""
    g = genre.lower()
    return "sf" in g or "sci" in g or "에스에프" in g or "과학" in g


def _is_fantasy(genre: str) -> bool:
    """장르가 판타지인지 판별"""
    g = genre.lower()
    return "판타지" in g or "fantasy" in g


# ═══════════════════════════════════════════════════
# ACTION / DRAMA / THRILLER / SF / FANTASY 특화 규칙 (v2.0 신규)
# Writer Engine v2.2 동기화 — 기획 단계 적용 버전
# ═══════════════════════════════════════════════════

ACTION_RULES = """
[액션 특화 규칙 — ACTION OVERRIDE]

★ 이 작품은 액션이다. 아래 규칙이 드라마/스릴러 기본 규칙보다 우선한다. ★
★ 한국 액션은 헐리우드 액션과 다르다. 감정과 액션이 같은 지점에서 폭발한다. ★

[1. 액션은 캐릭터 드라마다 — 주먹이 먼저가 아니라 이유가 먼저]
한국 관객은 순수 액션을 소비하지 않는다. 감정이 실린 액션을 본다.
〈베테랑〉〈아수라〉〈범죄도시〉〈부당거래〉〈서울의 봄〉 모두 감정이 액션의 연료다.
- 액션 씬에 들어가기 전 반드시 '감정적 이유'가 세팅되어야 한다.
  ❌ '악당이 나타났다. 싸운다.'
  ✅ '악당이 형의 사진을 짓밟는다. 주인공의 눈빛이 바뀐다. 주먹이 움직인다.'
- 비트 설계 시: 액션 씬 시작 전 1분 이내에 관객이 "이놈 맞아도 싸다"고 느껴야 한다.
- ★ 감정 없는 액션은 스펙터클. 감정 있는 액션은 카타르시스.

[2. 액션 시퀀스 4단계 설계 — 비트 안에서 Phase 구조]
한 번의 액션 씬은 한 호흡으로 쓰지 않는다. 4단계로 쪼개라.
  Phase 1 (Spark): 싸움이 터지는 순간. 트리거 명확히 (말/행동/눈빛).
  Phase 2 (Escalation): 판이 커진다. 일대일→다수 / 맨손→무기 / 좁은→열린.
  Phase 3 (Low Point): 주인공이 지는 것처럼 보이는 순간. 관객이 "어떻게 이기지?"
  Phase 4 (Turn): 주인공의 캐릭터성이 드러나는 방식으로 이긴다.
  → 승리의 방식이 그 캐릭터의 본질을 증명해야 한다.
    정의감 있는 형사는 정공법으로, 꾼은 트릭으로, 광인은 광기로.

[3. 공간이 액션이다 — 장소 설계 = 액션 설계]
한국 액션의 힘은 공간 활용이다.
- 좁은 골목, 컨테이너, 재래시장, 목욕탕, 엘리베이터 — 공간 자체가 무기·장애물·탈출구가 된다.
- Scene Design에서 액션 씬 명시할 때: "목욕탕 액션"이 아니라
  "증기 낀 목욕탕에서 수건으로 무기 압수 + 탕 물로 시야 차단 + 타일에 미끄러져 낙상"
- 비트 narrative에 공간의 고유 소품·제약·동작이 반드시 드러나야 한다.

[4. 액션 리듬 — 100분을 액션만으로 채우지 마라]
- 액션 씬 비중: 전체 분량의 25~35%가 이상적
- 액션 씬 사이에 반드시 '숨 고르기 씬' (대사 중심 / 감정 정리 / 다음 판 세팅)
- 비트별 액션 밀도:
  · 1막: Opening 액션 1회(캐릭터 소개) + Inciting 액션 1회(사건 시작)
  · 2막 전반: 작은 액션 2~3회(정보 수집·조우·위협 확인)
  · 2막 후반~Low Point: 큰 액션 1회(주인공이 크게 당한다)
  · 3막: Climax 액션 1회(가장 큰 판) + Epilogue
- ★ 액션-감정-액션-감정 리듬이 한국 액션의 공식이다.

[5. 주인공 설계 — 한국 액션의 4가지 원형]
한국 액션 주인공은 대체로 이 넷 중 하나. 혼합 가능.
  ① 정의형 (〈베테랑〉서도철, 〈범죄도시〉마석도): 흔들리지 않는 도덕 축. 정공법.
  ② 복수형 (〈아저씨〉차태식, 〈악녀〉숙희): 잃은 것에서 에너지. 적은 대사, 침묵이 무기.
  ③ 타락형 (〈아수라〉한도경, 〈신세계〉이자성): 선악 경계. 살기 위해 선을 넘는다.
  ④ 각성형 (〈황해〉구남, 〈부당거래〉주양): 처음엔 약함. 사건 겪으며 싸울 수밖에.
★ 주인공 유형이 결정되면 캐릭터 바이블의 tactics, sample_lines, arc_detail이 모두 달라진다.

[6. 빌런 설계 — 액션의 절반은 빌런이 만든다]
한국 액션 빌런의 공통 특징:
- 확신: 자기가 옳다고 믿는다 (〈베테랑〉조태오, 〈내부자들〉이강희)
- 체계: 개인이 아니라 시스템의 일부 (재벌 2세, 정치권, 조직)
- 물리적 위협: 직접 손을 쓴다. 중간보스가 아니다.
- ★ Villain 4Q가 작품 초반에 답 나와야 함:
  ① 무엇을 원하는가 ② 주인공보다 몇 수 앞인가 ③ 왜 이길 수 있는가 ④ 내면 균열은?

[7. 액션 대사 설계 — sample_lines 반영]
- 격투 중: 최대 3단어 (호흡이 끊긴다)
- 격투 직전: 한 문장 (긴장의 압축. 이 한 줄이 관객 기억에 남는다)
- 격투 직후: 한 문장 또는 침묵 (여운의 마무리)
- sample_lines 예:
  normal: '가자.' (평범해 보이는 한마디가 실은 신호)
  angry/threat: '...마지막 기회야.'
  vulnerable/aftermath: (피를 닦으며) '...끝났어?' (승리의 확신이 아닌 피로)
★ 한국 액션의 명장면은 '싸우기 직전의 대사'에서 나온다. 이 한 줄에 공을 들여라.

[8. 액션 클리셰 회피]
- ❌ 슬로우 모션 남발 (클라이맥스 1회로 아껴둘 것)
- ❌ 주인공이 다 맞고도 멀쩡 (물리적 대가를 그려야 공감)
- ❌ 악당의 긴 독백 (이길 수 있을 때 말하지 말고 쳐라)
- ❌ 안전한 장소 뻔한 설정 (주차장·창고 — 한국 액션의 차별성은 공간의 이질성)
- ❌ 여성 캐릭터를 인질로만 소비 (독자적 액션 설계 필요)
"""


DRAMA_RULES = """
[드라마 특화 규칙 — DRAMA OVERRIDE]

★ 이 작품은 드라마다. 장르적 자극이 아닌 인물의 내면과 관계가 엔진이다. ★
★ '무엇이 일어나는가'보다 '그 사람에게 무엇이 일어나는가'가 중요하다. ★

[1. 드라마의 엔진 — 내면 변화가 플롯이다]
액션·스릴러는 외적 사건이 엔진, 드라마는 내적 변화가 엔진.
매 비트마다 주인공의 내면에 미세한 변화가 있어야 한다.
  ❌ '주인공이 사건을 겪는다.'
  ✅ '주인공이 사건을 겪고, 그것이 그가 평생 피해온 진실을 건드린다.'
- Want(외적 목표) vs Need(내적 진실) 구조:
  · Want: 인물이 의식적으로 원하는 것
  · Need: 사실은 필요로 하지만 인정하지 않는 것
  · 드라마는 Want를 쫓다가 Need를 발견하는 여정
- ★ 클라이맥스는 Want를 포기하고 Need를 선택하는 순간.

[2. 서브텍스트가 텍스트다 — 직접 말하지 않는다]
드라마 대사의 핵심은 '말하지 않은 것'에 있다.
- 인물은 느끼는 것을 직접 말하지 않는다. 다른 이야기를 하거나, 사소한 행동으로 드러낸다.
  ❌ '나 지금 슬퍼.'
  ✅ '...커피 식었네.' (슬픔을 컵 속으로 밀어넣음)
- 갈등하는 두 인물은 표면적으로 다른 주제를 이야기한다.
  ❌ A: '날 떠나지 마.' B: '나는 가야 해.'
  ✅ A: '불 켤까?' B: '...아니, 이대로가 좋아.' (이별 직전이 불 끄는 문제로 위장)
- sample_lines 작성 시 자문: '이 인물이 진짜 하고 싶은 말은? 그걸 왜 못하는가?'

[3. 감정의 리듬 — 억눌림 → 균열 → 폭발]
드라마는 감정을 곧장 쏟아내지 않는다. 눌렀다가 한 번에 터뜨린다.
  · 억눌림(긴 빌드업): 인물은 자기 감정을 누르고 일상을 산다
  · 균열(트리거): 사소한 자극이 억눌린 감정에 금을 낸다
  · 폭발(해방): 한 씬에서 모든 것이 터진다 — 눈물, 고백, 결별, 화해
★ '눌러둔 시간'이 길수록 '터지는 순간'이 강해진다.
  울게 만들려면, 먼저 울지 않는 시간을 길게 써라.
- 폭발 씬은 한 작품에 2~3회만. Scene Design의 is_setpiece에 명시.

[4. 관계의 설계 — 변화가 드라마의 본질]
A와 B의 관계가 변하지 않으면 드라마가 아니라 스케치다.
- 관계 변화 3유형:
  ① 이해의 도달: 몰랐던 것을 알게 됨
  ② 거리의 재설정: 가까운 관계가 멀어지거나, 먼 관계가 가까워짐
  ③ 정체성의 재규정: 서로를 다른 존재로 받아들이게 됨
- 비트 설계 시: "이 비트가 끝났을 때 두 인물의 거리는 시작보다 어떻게 달라졌는가?"
- relationship_attitudes에 1막/미드포인트/클라이맥스의 변화를 각각 구체적으로.

[5. 구체에서 보편으로 — 한국 드라마의 힘]
한국 드라마가 해외에서 통하는 이유: 구체적 한국 디테일이 보편적 감정으로 번역됨.
추상적 감정을 쓰지 말고, 한국적 구체에서 시작하라.
  ❌ '가족의 사랑'
  ✅ '어머니가 딸이 돌아올 시간에 된장찌개를 데우는 것'
〈기생충〉의 반지하 곰팡이 냄새, 〈미나리〉의 병아리 감별, 〈우리들〉의 문구점 공책 — 구체가 테마를 운반한다.

[6. 드라마 씬 설계 — 평범한 순간을 설계하라]
드라마의 명장면은 대부분 '평범한 일상의 순간'에서 나온다.
- 외적 목적(무엇을 하고 있는가) + 내적 목적(감정적으로 무엇이 일어나는가) 분리 설계
  예: 외적='아버지와 아들이 이사 짐을 나른다' / 내적='아들이 아버지의 늙음을 처음 직면한다'
- ★ 가장 좋은 드라마 씬: 외적으로는 사소한데, 내적으로는 결정적인 순간.
- '무언가를 하면서' 말해야 한국 드라마의 결이 산다
  (설거지하면서 이별, 김장하면서 화해, 이삿짐 옮기며 고백)

[7. 드라마의 Stakes — 생명이 아니라 관계·정체성·존엄]
액션의 stakes: 목숨 / 스릴러: 안전 / 드라마: 관계·자존·용서
- 매 비트 자문: "이 비트에서 주인공이 잃을 수 있는 것은? 얻을 수 있는 것은?"
  · 잃을 것: 딸의 신뢰, 아버지의 마지막 존중, 오래된 친구 관계, 스스로에 대한 믿음
  · 얻을 것: 오랜 용서, 화해의 기회, 자기 이해, 떠날 자유
★ 구체적 관계·감정의 stakes가 있을 때 드라마도 스릴러만큼 긴장한다.

[8. 드라마 대사 설계 — sample_lines 반영]
- 대사는 일상어에 가깝게. 문학적 표현보다 생활의 말투.
- sample_lines 예:
  normal: '밥 먹었어?' (안부 뒤에 걱정)
  vulnerable: '...엄마는, 왜 그때 아무 말 안 했어?' (말끝이 흐려진다)
  confrontation: '내가 언제 당신 아들이었어?' (억눌렸던 것이 나오는 순간, 문장 짧아진다)
★ 가장 중요한 대사 앞뒤에 침묵을 넣어라. 대사가 아니라 침묵이 감정을 만든다.

[9. 드라마 클리셰 회피]
- ❌ 말로 전부 설명 (행동·침묵·표정으로 더 많이 말한다)
- ❌ 플래시백 남발 (필요한 플래시백은 작품당 1~2회)
- ❌ 우는 장면으로 감정 유도 (관객이 울게 해야지, 인물이 먼저 울면 관객은 거리를 둔다)
- ❌ 음악으로 감정 만들기 (음악은 증폭할 뿐, 만들지 못한다)
- ❌ 모든 것을 해결하는 엔딩 (한국 드라마의 힘은 '완전 해결하지 않음'에 있다)
"""


THRILLER_RULES = """
[스릴러/범죄 특화 규칙 — THRILLER OVERRIDE]

★ 이 작품은 스릴러/범죄물이다. 아래 규칙이 드라마 기본 규칙보다 우선한다. ★
★ 스릴러의 엔진은 '정보'다. 누가 무엇을 언제 아는가가 긴장을 만든다. ★

[1. 정보 비대칭의 설계 — 스릴러의 심장]
관객·주인공·빌런 세 존재가 각자 다른 정보를 갖도록 설계하라.
- Suspense = 관객은 알고 주인공은 모른다 (문 뒤의 살인자)
- Surprise = 관객도 주인공도 모르다가 동시에 알게 된다 (반전)
- Mystery = 관객도 주인공도 조각만 안다. 함께 맞춰간다.
★ 히치콕 원칙: '테이블 아래 폭탄이 있는데 둘이 5분간 대화한다'가 스릴러다.
  관객이 알면 대화의 모든 순간이 긴장된다.
- 매 비트 자문: '이 비트에서 누가 무엇을 아는가? 관객은 무엇을 아는가?'
- Structure Diagnosis의 dramatic_irony 필드에 반드시 반영.

[2. Clock이 있다 — 시간이 적이다]
스릴러는 시간 제약이 있어야 한다. 시간이 없으면 긴장도 없다.
- Clock 유형:
  ① 명시적 시계: 24시간 안에, 폭탄 타이머, 다음 범행 예고
  ② 암시적 압박: 언제 들킬지 모른다, 빌런이 다음 행동 준비 중
  ③ 물리적 제약: 탈출구 닫힘, 연락 두절, 도움 올 수 없음
- 시간이 줄어들수록 비트는 짧아지고 대사는 압축된다
- ★ 클라이맥스는 시간이 가장 적게 남은 순간에 터진다.

[3. Escalation — 판이 계속 커져야 한다]
스릴러는 '계속 더 나빠져야' 한다. 한 번 오르고 멈추면 관객이 이탈.
- 매 비트 자문: '직전 비트보다 무엇이 더 나빠졌는가?'
  · 위협 범위 확대 (개인 → 가족 → 사회)
  · 가능한 출구 감소 (도움 받을 사람이 죽거나 배신)
  · 시간 압박 증가
  · 주인공이 잃은 것 누적
- ★ 중간지점(Beat 10)에서 주인공은 "돌아갈 수 없다"를 깨달아야 한다.

[4. 빌런 설계 — 빌런이 똑똑해야 스릴러가 똑똑하다]
스릴러 빌런 = 주인공보다 몇 수 앞선다.
- 빌런이 어리석으면 스릴러 전체가 어리석어진다
- 빌런의 강점: 정보(주인공이 모르는 것) / 자원(돈·권력·인맥) / 선수 치기
- ★ 빌런은 주인공이 '무엇을 사랑하는가'를 알아야 한다. 그래야 약점을 친다.
- 빌런의 실수는 클라이맥스에서만 허용. 그전에는 주인공이 뚫어야 한다.

[5. 주인공의 도덕적 타락 — 누아르의 필수]
순수 스릴러는 주인공이 선을 지킨다.
누아르는 주인공이 선을 넘어간다. 이기기 위해 자기 일부를 버린다.
- 한국 누아르의 힘: 〈아수라〉〈신세계〉〈내부자들〉〈황해〉 — 주인공도 깨끗하지 않다
- 매 비트 자문: '주인공이 이 비트에서 무엇을 포기했는가? 어떤 선을 넘었는가?'
- ★ 관객이 주인공을 좋아하는 이유는 '도덕적이어서'가 아니라 '절박해서'다.
- Low Point(Beat 12)에서 주인공은 '거울 속 자기를 못 알아보는' 순간을 맞아야 한다.

[6. 반전(Twist) 설계 — 준비된 반전만이 유효]
반전은 '충격'이 아니라 '재해석'이다.
- 나쁜 반전: 관객이 미리 볼 수 없었던 정보로 뒤집기 (기만)
- 좋은 반전: 관객이 다 봤는데 다르게 해석했던 것이 실체가 드러남
- 3원칙:
  ① Plant: 1막에 반전의 단서를 관객이 볼 수 있게 심는다. 단, 다른 의미로 해석되도록
  ② Misdirect: 2막에서 관객의 주의를 다른 곳으로 돌린다
  ③ Payoff: 3막에서 심은 것을 원래 의미로 재해석시킨다
★ 관객이 '다시 보고 싶게' 만드는 반전이 좋은 반전이다.
- 한 작품에 큰 반전 1~2회 + 작은 반전 3~4회.

[7. 공간과 분위기 — 한국 스릴러의 강점]
- 익숙한 공간(아파트, 지하철, 시장)을 낯설게 만드는 기술
- 닫힌 공간 우선 (탈출이 어려운 것이 긴장)
- 밤·지하·복도·주차장·빈 사무실 — 고립과 시선 차단

[8. 스릴러 대사 설계 — sample_lines 반영]
- 건조하다. 정보가 많다. 감정이 억눌려 있다.
- sample_lines 예:
  normal: 업무적·직설적. 관계가 드러나지 않는다.
  under_pressure: 끊긴다. 호흡이 빠르다. 말보다 행동.
  threat(빌런): (커피를 따르며) '...그 서류는 어디 있습니까?' (차분한 협박이 폭발적 협박보다 무섭다)
★ 스릴러의 명대사는 '짧고 차가운 경고'다. 길게 쓰지 마라.

[9. 스릴러 클리셰 회피]
- ❌ 빌런이 당위를 긴 독백으로 설명 (행동으로 보여줘라)
- ❌ 주인공이 명백한 위험을 혼자 조사 ("경찰을 왜 안 부르지?"를 관객이 물으면 실패)
- ❌ 편의적 우연으로 위기 탈출 (주인공이 해결해야 한다)
- ❌ 전문가 주인공의 무능 (형사·검사·기자가 초짜 실수하면 리얼리티 붕괴)
- ❌ 여성 희생자의 반복 소비
"""


SF_RULES = """
[SF 특화 규칙 — SF OVERRIDE]

★ 이 작품은 SF다. 아래 규칙이 드라마/스릴러 기본 규칙보다 우선한다. ★
★ SF의 핵심은 '과학'이 아니라 '세계의 규칙'이다. 그 규칙이 인간 문제의 은유로 작동한다. ★

[1. 세계 규칙의 설계 — 한 줄로 요약 가능해야]
이 세계가 우리 세계와 다른 '핵심 규칙 1개'를 명확히 정의하라.
  예: 〈기억의 밤〉=기억 조작이 가능하다 / 〈인셉션〉=꿈 속으로 들어갈 수 있다
- ★ 규칙이 복잡하면 관객은 이탈한다. 규칙은 하나, 적용은 다채롭게.
- 핵심 규칙 외 부가 규칙은 2~3개 이내.
- 매 비트 자문: '이 비트에서 핵심 규칙이 어떻게 작동하고 있는가?'
- 핵심 규칙이 작동하지 않는 비트는 SF가 아니라 일반 드라마다 — 넣거나 빼거나.

[2. 규칙 공개의 리듬 — Info Drip, 정보 과부하 금지]
세계관 규칙은 한꺼번에 쏟으면 안 된다. 매 비트에서 한 조각씩 공개.
- Show, Don't Tell: 설명 대사 대신 인물이 규칙을 사용하는 모습으로
  ❌ '이 세계에서는 기억을 지울 수 있어.'
  ✅ (주인공이 누군가를 의자에 앉히고 관자놀이에 장치를 붙인다. 상대의 눈에서 초점이 사라진다.)
- 일상화된 기술: 인물들은 이 세계에 익숙하다. 놀라지 않는다.
  관객이 놀라는 것은 인물이 놀라지 않기 때문이다.
- 제한된 시점: 모든 규칙을 설명하지 마라. 주인공이 아는 만큼만.
- ★ 강의식 대사 절대 금지: '아시다시피 2049년 지구는...'으로 시작하는 대사 금지.

[3. 규칙의 대가(Cost) — 공짜 기술은 드라마를 죽인다]
세계의 핵심 규칙에는 반드시 대가가 있어야 한다.
- 대가 유형:
  · 신체적: 기억 조작 → 두통·구토·인격 손상
  · 관계적: 시간 여행 → 연인이 자기를 모르게 됨
  · 윤리적: 복제 기술 → 원본과 복제의 정체성 문제
  · 사회적: 초능력 → 박해와 격리
- ★ 대가 없이 문제를 해결하면 데우스 엑스 마키나다. 해결은 항상 대가와 함께.
- 클라이맥스의 승리는 주인공이 '무엇을 대가로 치렀는가'로 완성된다.

[4. 규칙의 일관성 — 한번 세운 규칙은 끝까지]
중간에 새 규칙을 만들어 위기를 해결하지 마라.
새 규칙을 쓰려면 반드시 1막에서 plant되어야 한다.
★ '규칙을 어긴 한 장면'이 SF 전체를 무너뜨린다.

[5. Human Anchor — 경이의 옆에 반드시 사람이 있다]
SF는 이미지가 경이로워야 한다. 하지만 경이만 있으면 관객은 피곤해진다.
경이의 옆에는 반드시 '평범한 감정을 가진 인간'이 있어야 한다.
- 주인공은 이 세계에서 완벽히 적응된 사람이 아니라, 이 세계의 규칙 때문에 다치는 사람.
- 예시 모델:
  · 〈인터스텔라〉머피: 아버지 잃은 딸의 기다림
  · 〈블레이드 러너 2049〉K: 자기가 누구인지 찾는 복제인간
  · 〈컨택트〉루이스: 딸을 둘러싼 언어학자의 슬픔
★ SF에서 관객이 공감하는 대상은 '기술'이 아니라 '기술 때문에 상처받은 인간'이다.

[6. 기술 = 인간 문제의 은유]
SF의 기술은 항상 현재 인간의 문제를 은유한다. 기술 자체가 목적이 아니다.
- 테마 매핑:
  · AI/로봇 의식 = 정체성·자유의지·노동
  · 복제인간 = 차별·영혼·가치
  · 기억 조작 = 진실·트라우마·관계
  · 시간여행 = 후회·책임·선택
  · 외계 접촉 = 타자 이해·소통
★ 기획 자문: '이 SF가 오늘날 한국 관객에게 무슨 질문을 던지는가?'
  질문이 없는 SF는 그냥 스펙터클이다.

[7. 한국 SF의 포지셔닝 — 장르 결합이 기본]
순수 SF는 한국 시장에서 어렵다. 대부분 SF+액션, SF+드라마, SF+스릴러로 설계.
모선 장르 규칙을 기본으로, SF는 세계 규칙을 얹는 레이어로 작동.
- SF + 액션: 〈승리호〉〈정이〉
- SF + 스릴러: 〈부산행〉(좀비+스릴러)
- SF + 드라마: 〈인랑〉〈원더랜드〉
★ 이 작품이 '무엇 + SF'인지 명확히 하라. 모선 장르의 재미가 먼저다.

[8. SF 대사 설계 — sample_lines 반영]
- 이 세계의 언어를 만들어라. 전문 용어 몇 개는 필수 (일관성 있게 반복).
- 일상어와 기술 용어의 혼합이 자연스러워야 한다.
- sample_lines 예:
  normal: '오늘 백업 떴어요?' (미래의 일상 대화)
  tech_moment: (기술 사용 순간, 대사보다 지문이 많다)
  philosophical: 테마가 드러나는 순간 (너무 자주 쓰면 설교. 작품당 2~3회만)
★ SF의 명대사는 '기술에 관한 말이 인간에 관한 말로 들리는 순간'이다.
  예: 〈블레이드 러너〉 "Tears in rain..." = 죽음에 관한 시.

[9. SF 클리셰 회피]
- ❌ 강의식 오프닝 보이스오버: '2045년 지구는 기후 재앙으로...' 금지
- ❌ 주인공이 과학자여서 전부 설명 (관객의 동일시 대상은 일반인이 유리)
- ❌ 3막에서 새 기술로 해결 (준비되지 않은 기술은 사기)
- ❌ 로봇의 각성이 곧 반란 (너무 진부)
- ❌ 디스토피아의 뻔한 기호 (회색·비·네온 남발)
"""


FANTASY_RULES = """
[판타지 특화 규칙 — FANTASY OVERRIDE]

★ 이 작품은 판타지다. 아래 규칙이 드라마/액션 기본 규칙보다 우선한다. ★
★ 판타지의 엔진은 '마법의 규칙'이다. 마법이 아니라 '마법의 대가'가 드라마를 만든다. ★

[1. 마법 규칙의 정의 — 구체적이고 제한적으로]
모든 판타지는 마법의 규칙을 명확히 정의해야 한다.
- 정의할 요소:
  ① 누가 쓸 수 있는가? (선택된 자? 훈련? 혈통? 도구?)
  ② 어떻게 쓰는가? (주문? 행동? 감정 상태?)
  ③ 무엇이 가능하고 무엇이 불가능한가?
  ④ 대가는? (에너지? 신체? 수명? 기억? 관계?)
★ 마법이 만능이면 긴장이 사라진다. 제한이 드라마를 만든다.
관객이 '아, 저건 할 수 없지'를 알아야 한다. 그래야 위기가 위기가 된다.

[2. 마법의 대가 — 공짜 마법 절대 금지]
판타지의 황금 법칙: 모든 마법은 대가를 치른다.
- 대가 유형:
  · 신체적: 노화·상처·피로·질병
  · 정신적: 기억 소실·인격 변화·광기
  · 관계적: 사랑하는 이를 못 알아봄·거리 생김
  · 존재적: 수명 단축·영혼 분할·인간성 상실
- 주인공이 마법을 쓸 때마다 '무엇을 잃는가'를 관객에게 보여줘라.
★ 대가 없는 마법은 치트키다. 치트키는 이야기를 망친다.
- 클라이맥스: 주인공은 '가장 큰 대가'를 치르고 이긴다.

[3. 세계관의 층위 — 크게 두지 말고 깊게 두라]
대서사시적 세계관을 지양하라. 한국 관객은 장황한 세계관 설명에 피로해한다.
- 작은 세계를 깊게 설계: 한 도시 / 한 마을 / 한 학교 / 한 가문
- ★ 〈도깨비〉의 세계는 복잡하지 않다. 하지만 그 안의 관계·규칙은 깊다.
- 세계관 설명은 '인물의 일상'으로 풀어라. 역사책 내레이션 금지.

[4. 판타지 캐릭터 원형 — 한국 판타지에서 자주 쓰이는 원형 (혼합 가능)]
  ① 각성형 (Chosen): 평범한 주인공이 자신의 능력·운명을 깨닫는 과정
     - 장점: 관객 동일시 쉬움. 성장 아크 선명.
     - 주의: 진부함 회피. 각성 이후에도 약점 유지 필수.
  ② 봉인형 (Bound): 강하지만 무언가에 제약된 존재
     - 예: 도깨비(불멸이지만 사랑하면 사라짐), 구미호(인간이 되고 싶지만 조건 있음)
     - 드라마의 핵심: 제약 자체가 비극의 씨앗
  ③ 이방인형 (Outsider): 다른 세계에서 온 / 다른 세계로 간
     - 신입의 시선 = 관객의 시선. 세계관 설명이 자연스럽게 전달
  ④ 중재자형 (Mediator): 두 세계를 오가는 존재
     - 저승사자, 무당, 퇴마사 계열. 양쪽 모두에 속하지 못하는 고독

[5. 판타지와 감정의 결 — 한국 판타지의 힘]
해리포터식 모험 판타지가 한국에서 통한 사례는 적다.
한국 판타지는 '감정·관계·한(恨)'의 판타지다.
- 〈도깨비〉: 사랑과 시간
- 〈호텔 델루나〉: 미련과 용서
- 〈구미호뎐〉: 오래된 약속과 환생
★ 기획 자문: '이 판타지가 어떤 감정을 증폭하는가?'
  감정의 증폭기로서 마법이 있는 것이지, 마법이 주인공이 아니다.

[6. 시공간의 설계]
- 시대 혼합: 한국 판타지는 현대 + 고전의 혼합이 많다 (도깨비의 고려+현대)
- 공간 혼합: 일상 공간 옆에 초자연 공간이 숨어 있다 (단골 카페 뒷문이 저승)
★ 관객이 처음 본 장소를 이질적으로 만드는 힘이 중요.
- 의상·소품으로 시대감을 주라. 대사로 설명하지 말고.

[7. 플롯 엔진 — 규칙이 만드는 딜레마]
좋은 판타지 플롯 = 마법 규칙이 만드는 선택 불가능의 딜레마.
- 예: '사랑하면 사라진다' → 사랑을 억누를 것인가, 사라질 것인가
- 예: '이 문을 넘으면 돌아올 수 없다' → 사랑을 포기할 것인가, 모험을 포기할 것인가
- 규칙이 주인공을 코너로 몰아야 한다.
- 해결은 '규칙을 어겨서'가 아니라 '규칙 안에서 새로운 해석'으로.
★ 규칙을 어기는 해결은 사기. 규칙을 이용하는 해결이 판타지의 쾌감.

[8. 판타지 대사 설계 — sample_lines 반영]
- 이 세계의 어휘를 제한적으로 사용. 너무 많으면 낯설어 이탈.
- 고전 판타지: 약간 격식있는 어투. 하지만 과한 사극체 금지.
- 현대 판타지: 일상어 + 간헐적 마법 용어.
- sample_lines 예:
  normal: 일상 그대로. 이 세계의 인물들은 마법을 당연히 여긴다.
  magical_moment: 마법을 쓰거나 마주한 순간. 대사는 줄고 지문이 늘어난다.
  vow/curse: '...반드시 돌아오겠다.' / '너는 기억할 수 없을 것이다.'
★ 판타지의 명대사는 '세계의 규칙을 감정의 언어로 말하는 순간'이다.

[9. SF와 판타지의 차이 — 혼동 주의]
- SF: 과학적 가능성의 언어로 설명 가능한 세계
- 판타지: 마법·신화·초자연의 언어로 설명되는 세계
- 작품 하나에서 두 장르가 섞이면 규칙 일관성이 무너지기 쉽다.
★ 한국 작품은 판타지+드라마 조합이 SF+드라마보다 시장에서 강세.

[10. 판타지 클리셰 회피]
- ❌ '선택된 자'의 뻔한 각성 (각성하지 않는 판타지도 필요)
- ❌ 마법 전투의 화려함에만 집중 (액션 없이도 판타지 가능)
- ❌ 악역이 순수악 (판타지 악역도 서사가 있어야)
- ❌ 긴 예언문 낭독 (예언은 짧고 모호해야 관객이 해석한다)
- ❌ 세계관 소개에 1막 전부 소비 (인물 행동 속에서 드러내라)
"""


# ═══════════════════════════════════════════════════
# FACT-BASED RULES — 실화 배경 작품 전용 (v2.0 신규)
# 실명 비사용 + 사실성 균형, 명예훼손·인격권 차단
# ═══════════════════════════════════════════════════

FACT_BASED_RULES = """
[실화 배경 규칙 — FACT-BASED OVERRIDE]

★ 이 작품은 실제 사건·인물·시대를 배경으로 하되, 실명을 쓰지 않고 각색된 허구로 개발된다. ★
★ 관객의 실화 연상은 허용, 특정 실존 인물 명예훼손·인격권 리스크는 기획 단계에서 원천 차단. ★

[사실성을 높이기 위해 사용해도 되는 공적 요소 — 넣어라]
1. 실제 지명·장소: 서울·여의도·청와대·종로·광화문·남산·부산·판문점 등
   단, 특정 개인 소유 장소(기업 사옥 등)는 가공 명칭.
2. 실제 시대 배경과 역사적 사건의 큰 틀:
   IMF·5·18·6월 항쟁·촛불·세월호·코로나 — 배경으로 언급 가능.
3. 공적 직함·제도: 대통령·국무총리·검찰총장·국정원장·국회의원·장관·재벌 회장.
4. 공공 기관·제도 명칭: 청와대·국정원·검찰·국회·대법원·한국은행.
5. 시대적 디테일: 해당 시대의 화폐 단위·뉴스 용어·패션·음악·유행어 — 구체적으로.
   ★ 디테일이 사실적일수록 몰입이 깊어진다.

[절대 넣지 말아야 할 요소 — 명예훼손·인격권 침해 리스크]
1. 실존 인물의 실명:
   - 주인공·악역·조연 모두 실명 금지.
   - 가공 이름 + 직함으로 처리 ("김대중" → "민 대통령" 또는 "K 대통령").
2. 디테일 조합으로 실존 인물이 특정되는 경우:
   - 실명 없어도 (출생지+학력+특정 사건+가족관계) 조합이 모이면 특정된다.
   - 특정 가능성을 깨는 장치를 반드시 하나 이상 섞어라 (출생지 변경·가족 각색·사건 디테일 변형).
3. 실존 공인을 악역·범죄자로 그릴 때:
   - 공인 유족의 인격권 침해는 법원에서 인용되는 경향.
   - 전직 대통령·유명 재벌 총수·실명 언급 가능한 정치인을 직접적 악역 모델로 쓰지 마라.
   - 악역은 해당 시대·집단을 상징하는 '합성 캐릭터'로 설계.
4. 특정 지역·집단 조롱·폄하:
   - 특정 지방·직업군·종교·학교를 부정적 스테레오타입으로 그리지 마라.
   - 유머·풍자에서도 지역 사투리나 집단 특성을 조롱 소재로 쓰면 명예훼손 시비.
5. 살아있는 피해자·유족이 있는 실제 범죄·참사 세부:
   - 실제 피해자의 목소리·전화·유서·실명 재연 금지.
   - 범죄 수법의 구체적 디테일을 실제 사건과 동일하게 재현하지 마라.

[실명 대체 원칙 — 가명 설계법]
- 성씨만 한 글자: "민 대통령", "K 회장", "J 검사장"
- 완전 가공 이름 + 실존 직함: "박정후 대통령", "강만석 회장"
- 실존 인물과 음절/이니셜 겹치지 않도록 조정.
- 기업명: "삼성→한성/진성", "현대→대현/근대" 의도적 비틀기.
- 언론사명: "조선일보→한선일보", "JTBC→KTBC".

[사실성과 안전성의 균형 — 설계 예시]
✅ 좋은 예 (시대·지명·사건·공직은 실재, 인물은 가공):
  "1997년 12월. 서울 여의도. 한국은행 앞 시민들이 줄을 선다.
   민 대통령은 국민에게 고개를 숙였다. '저의 부족함으로...'"

❌ 나쁜 예 (실명 사용): "1997년 12월. 김영삼 대통령이 고개를 숙였다."
❌ 나쁜 예 (가명이지만 특정 가능): "호남 출신 변호사 출신 대통령, 재임 중 IMF 극복, 임기 말 아들이 구속..."
   → 이름만 가명, 디테일 조합으로 특정 인물이 명백히 연상됨. 실명과 동일한 리스크.

[Core Build / Structure / Treatment 단계별 체크리스트]
1. 캐릭터 바이블에 실명이 들어갔는가? → 가명으로 치환.
2. 가명이지만 디테일 조합으로 특정 인물이 연상되는가? → 디테일 하나 이상 변형.
3. 특정 지역·집단이 조롱 대상으로 쓰였는가? → 제거 또는 중립화.
4. 실제 피해자·유족이 있는 사건의 개인 디테일이 재연되었는가? → 제거.
5. 공적 요소(지명·시대·직함·제도)는 충분히 활용되었는가? → 부족하면 추가.

[각색 고지 전제]
작품 도입 또는 종료에 아래 취지 자막이 들어간다는 전제:
"본 작품에 등장하는 인물, 단체, 지명, 상호, 사건은 모두 허구이며,
실존하는 것과 관련이 있더라도 극적 구성을 위해 각색되었습니다."
→ 이 자막만으로 면책되지 않는다. 기획·집필 단계 규칙 준수 위에 추가되는 안전장치.
"""


def get_fact_based_rules(fact_based: bool) -> str:
    """실화 배경 작품일 때만 규칙 반환. 아니면 빈 문자열."""
    if not fact_based:
        return ""
    return "\n\n" + FACT_BASED_RULES + "\n"


# ═══════════════════════════════════════════════════
# HISTORICAL FILM RULES — 역사영화 전용 (v2.0 신규)
# 정통/팩션/퓨전 3유형 분기 + BASE 공통
# ═══════════════════════════════════════════════════

HISTORICAL_FILM_BASE = """
[역사영화 공통 기반 — HISTORICAL FILM BASE]

★ 이 작품은 역사영화다. 장르 규칙과 별개로 아래 원칙이 우선 적용된다. ★

[1. 역사영화는 과거-현재-미래의 가교다]
- 역사영화는 과거를 그리지만, 대상은 현재 관객이다.
- 이 작품이 왜 지금 만들어져야 하는가? 현재의 무엇을 질문하는가?
- 과거를 보여주며 관객이 현재의 자기 삶을 돌아볼 수 있도록 설계하라.
★ 역사영화는 과거의 재현이 아니라, 현재에 던지는 질문이다.

[2. 시대감의 구체성 — 뭉뚱그려진 '옛날'은 실패]
- 이 작품의 시대는 '옛날'이 아니라 '구체적인 몇 년·몇 세기'다.
- 해당 시대에만 존재하는 구체를 씬마다 배치하라:
  · 의복의 재질·색·형태 (계급별·직업별 차이)
  · 음식·기호품 (계급별·지역별 차이)
  · 통화·거래 방식 (엽전·은·비단 등 시대별 화폐)
  · 교통수단 (말·가마·배의 종류)
  · 언어의 결 (지나친 사극체 금지, 지나친 현대어 금지, 중간 결)
  · 주거·공간 (신분별 주거 차이)
★ 시대감은 '설명 대사'가 아니라 '환경의 구체 디테일'로 만들어진다.
- 금지: "옛날식 궁궐", "고풍스러운 시장" 같은 뭉개는 표현.
- 허용: "기와 틈새로 눈이 녹아 떨어지는 한여름의 궁궐" / "멸치젓 냄새가 배어 있는 시전의 좌판"

[3. 시대 언어의 균형 — 한국 역사영화의 승부처]
- 현대 관객이 이해 가능해야 하지만 시대감은 유지해야 한다.
- 과한 사극체는 관객 이탈 (완전 아나운서식 왕실체 금지).
- 과한 현대어는 시대감 붕괴 ("대박이에요 전하" 같은 것 금지).
- 균형 원칙:
  · 존댓말·호칭은 시대에 맞게 (상감/전하/대감/나리/마님/도련님)
  · 현대 지시 대상은 시대 용어로 치환 (경찰→포졸/의금부, 회사→상단, 출근→입궐)
  · 의문사·감탄사는 과하지 않게 (허참, 그리하여, 필시, 도무지)
  · 문장 구조는 현대에 가깝게 (관객 이해 우선)
★ 시대 언어의 핵심은 '낯섦과 친숙함의 아슬아슬한 균형'.

[4. 공간이 주인공이 될 수 있다]
- 역사영화에서 특정 공간은 단순 배경이 아니라 테마를 운반하는 캐릭터가 될 수 있다.
- 폐쇄 공간·고립 상황의 역사극은 공간을 캐릭터처럼 설계하라.
  예: 〈남한산성〉의 성곽, 〈사도〉의 뒤주, 〈덕혜옹주〉의 도쿄의 방.
- 공간이 주인공일 때 설계 원칙:
  · 공간의 감각적 디테일을 반복 노출 (온도·냄새·소리)
  · 공간이 인물에게 가하는 압박을 지속적으로
  · 공간 밖과의 대비 (갇힌 안 / 자유로운 밖)
  · 공간의 변화가 곧 인물의 변화 (눈이 쌓이고 녹음)

[5. 선악 이원 구도 경계 — 복잡성을 유지하라]
- 역사 속 인물은 단순 영웅/악당이 아니다.
- 악역도 자기 논리가 있고, 영웅도 약점이 있다.
- 특히 실존 인물을 그릴 때:
  · 100% 영웅 묘사 금지 (우상화의 위험)
  · 100% 악당 묘사 금지 (명예훼손의 위험)
  · 균열·갈등·인간적 약점을 반드시 심어라
★ 복잡한 인물이 한국 역사영화의 힘이다
  (〈광해〉의 양면성, 〈남한산성〉의 척화·주화 모두의 애국).

[6. 시대 고증 우선순위]
작가적 상상력은 '사료의 빈 공간'을 메우는 것이지, 사료를 덮어쓰는 것이 아니다.
  ① 확정 사료 (실록·정사·공식 기록): 사실 그대로 유지. 임의 변경 금지.
  ② 야사·전승: 작가 해석 가능. 사료와 충돌하지 않는 범위.
  ③ 공백 영역 (사료 없는 일상·대화·감정): 상상력 발휘 가능. 시대 논리 부합해야.
  ④ 명백한 창작 (가공 인물·가공 사건): 자유롭게 구성.
자문: '이 비트·씬이 ①②③④ 중 어느 영역인가?' → 영역에 맞는 자유도로 기획.

[7. 시대를 초월하는 보편 감정을 찾아라]
- 역사영화가 현재 관객과 연결되는 지점 = 시대를 초월하는 감정.
- 사랑·충성·배신·야망·후회·용기·절망·희망 — 시대 불문.
- 시대 구체는 살리되, 감정은 현대인이 즉시 공감 가능하게.
★ '그 시대 사람은 이렇게 느꼈을 것이다'보다 '사람은 원래 이렇게 느낀다'를 먼저.
"""


ORTHODOX_HISTORY_RULES = """
[정통역사영화 특화 규칙 — ORTHODOX HISTORY]

★ 이 작품은 정통역사영화다. 실재 역사적 사건·인물이 드라마의 중심이다. ★
★ 레퍼런스: 〈남한산성〉〈사도〉〈택시운전사〉〈1987〉〈서울의 봄〉〈남산의 부장들〉 ★

[정통역사영화의 본질]
실재 사건·인물의 무게를 현재 관객에게 전달하는 것이 목적이다.
사료가 말하지 못한 '인간의 내면'을 드라마투르기로 채워 넣는다.
허구의 재미보다 역사의 진지함을 우위에 둔다.

[1. 사료 존중의 원칙]
- 확정 사료에 기록된 사건·장소·날짜는 임의 변경 금지.
- 실존 인물의 실명 사용 가능. 단, 기록된 행적·발언을 왜곡하지 말 것.
- 기록이 없는 부분 = 작가 해석 허용 영역.
★ 대사: 실록에 기록된 어록은 가급적 원형 유지, 기록 없는 일상 대사는 상상력.

[2. 감정 과잉 회피 — 객관화 유지]
TV 사극의 관습을 답습하지 마라.
- ❌ 무조건 피와 눈물이 쏟아지는 연출
- ❌ 슬로우모션 + 웅장한 음악 남발
- ❌ 절규하는 클로즈업 반복
- ✅ 롱쇼트로 관객을 객관적 관찰자 위치에 두기
- ✅ 사료에 없는 극적 과장을 의심하기
- ✅ 감정은 억누른 상태에서 새어 나오게

예시 원칙: 굴욕적 역사를 다룰 때, 굴욕을 '과장'하면 관객이 이성적 판단을 잃는다.
       굴욕을 '객관적으로' 보여주면 관객이 스스로 분노하고 생각한다.

[3. 선악 이원 구도 엄격 금지]
정통역사영화에서 선악 이원은 역사를 왜곡한다.
- 서로 다른 신념의 인물들 대립을 그려라 (〈남한산성〉 최명길 vs 김상헌).
- 각자의 입장에서 모두 나라를 위한 것일 수 있다.
- 어느 쪽이 옳았는가? — 관객이 판단하도록 열어둘 것.
- 작가의 답을 강요하지 말고, 질문을 제공하라.

[4. 패배한 역사의 마무리 — 희망의 잔여물]
굴욕·패배·비극으로 끝난 역사를 다룰 때:
- 비극적 결말을 완화하지 마라. 사료가 그렇다면 그렇게 끝내라.
- 엔딩 이미지에 '이어지는 삶'의 씨앗을 남겨라:
  · 전쟁이 끝난 자리에서 뛰노는 아이
  · 폐허 위에 돋는 풀
  · 살아남은 자의 눈빛
★ 이 씨앗이 현재 관객과 연결되는 지점이다.
- 어설픈 해피엔딩 첨가 금지. 패배를 억지로 승리로 포장하면 거짓.

[5. 현재에 던지는 질문을 명확히]
정통역사영화 기획 시 필수 자문:
- 이 역사적 사건이 오늘날 우리에게 무엇을 묻는가?
- 그 질문이 비트마다 잔잔하게 흐르고 있는가?
- 설교조가 아니라 질문 형태로 관객에게 도달하는가?

예시:
- 〈남한산성〉: 강대국 사이에서 약자는 어떻게 살아남는가?
- 〈1987〉: 한 사람의 용기가 역사를 바꿀 수 있는가?
- 〈택시운전사〉: 평범한 개인이 역사의 증인이 될 때 어떤 선택을 하는가?
- 〈서울의 봄〉: 체제 붕괴 앞에서 개인의 양심은 무엇을 할 수 있는가?

[6. 민초·주변부 인물의 기능]
- 역사 기록은 지배층 중심. 정통역사영화도 이 한계를 가진다.
- 민초·주변부 인물을 등장시켜 역사를 폭넓게 보라.
- 단, 민초가 '주인공 영웅'이 되어 역사를 바꾸는 환상은 경계.
- 민초는 '역사의 증인' 역할로 기능할 때 가장 강하다.

[7. 정통역사영화 대사 설계 — sample_lines 반영]
- 시대 어록을 존중하되 현대어 감각으로 번역.
- 정서는 억제적. 폭발보다 응축이 힘을 가진다.
- 한 줄 한 줄에 시대의 무게가 실리도록 짧게.
★ 정통의 명대사는 '많이 말하지 않는다' — 적게 말하는 것이 품격을 만든다.
"""


FACTION_HISTORY_RULES = """
[팩션역사영화 특화 규칙 — FACTION HISTORY]

★ 이 작품은 팩션역사영화다. 실재 시대·공간 위에서 가공의 드라마가 펼쳐진다. ★
★ 레퍼런스: 〈왕의 남자〉〈광해〉〈황산벌〉〈암살〉〈밀정〉〈관상〉〈봉오동 전투〉 ★

[팩션역사영화의 본질]
실제 시대의 공기와 제도는 고증하되, 드라마의 중심은 가공의 인물·사건이다.
역사의 빈 공간에 작가의 상상이 자유롭게 펼쳐진다.
정통의 무게와 퓨전의 자유 사이, 상업적 재미와 역사적 울림을 동시에 노린다.

[1. 실존과 가공의 배치 원칙]
팩션의 핵심은 '무엇이 실재이고 무엇이 허구인가'의 균형 설계.

유지해야 할 실존 요소 (바꾸지 말 것):
- 시대 배경 큰 흐름 (왕조·전쟁·정치 체제)
- 실존 공간 (경복궁·벽란도·명동·남대문)
- 실존 제도 (과거제·무신정권·의열단·조선총독부)
- 실존 배경 인물 (왕·재상·총수 — 이름만 언급되거나 단역)

자유로운 가공 요소 (드라마의 중심):
- 주인공·부주인공 (완전 가공)
- 드라마의 중심 사건 (가공의 음모·거래·복수)
- 주인공의 감정선·관계 (사료 기록 없으니 자유)
- 소규모 에피소드 (시장 풍경·주막 장면·로맨스)

주의가 필요한 중간 영역:
- 실존 인물을 주요 악역으로 그릴 때 — 명예훼손 리스크. 필요시 가명화.
- 실존 사건의 원인·결과를 재해석할 때 — 대안 해석의 근거를 시대 논리에서 찾을 것.

[2. 시대의 공기를 살리되, 드라마는 자유롭게]
팩션은 시대감(공기·분위기·디테일)은 철저하게, 드라마는 자유롭게.
★ 관객이 "이 시대에 저런 일이 있었을 법하다"고 느끼게 만들어라.
예시:
- 〈왕의 남자〉: 연산군 시대에 광대가 왕을 비판한 기록은 없지만,
  당시 광대의 풍자 전통 + 연산군의 폭압에서 '있을 법'하다.
- 〈암살〉: 영화 속 암살 작전은 허구지만 의열단 활동이라는 실존 맥락에 녹아 있음.

[3. 재미 코드 자유 — 팩션의 강점]
정통이 억제하는 재미 코드를 팩션은 적극 활용.
- 통쾌한 역전극 (〈왕의 남자〉 풍자의 쾌감)
- 코믹한 장면 (〈황산벌〉 사투리 코미디)
- 액션 시퀀스 확대 (〈밀정〉〈암살〉 총격전)
- 로맨스 서브플롯 (〈관상〉 감정선)
- 시원한 해결 (정통과 달리 카타르시스 가능)
단, 재미 코드가 시대감을 붕괴시키면 퓨전이 된다. 선 지키기.

[4. 실존 배경 인물의 등장 방식]
주요 실존 인물(왕·재상·총수)이 등장할 때:
- 단역 등장 권장: 이름만 언급되거나 한두 씬만.
- 주요 등장 시 주의사항:
  · 기록된 행적은 왜곡하지 말 것
  · 성격·외모 해석은 여러 사료 참고하여 여지 남길 것
  · 100% 악인 묘사는 리스크 — 인간적 균열 포함
  · 직계 후손이 현존하면 특히 주의
★ 실존 인물을 '거대한 배경'으로 두고 가공 주인공의 드라마를 전경에.

[5. 현대적 테마의 시대 투영 — 팩션의 강점]
팩션은 현대 이슈를 과거의 무대에 투영하는 데 매우 효과적.
- 현대 빈부격차 → 조선 신분제 갈등으로 투영
- 현대 외세 간섭 → 병자호란/일제강점기로 투영
- 현대 청년 좌절 → 조선 몰락 양반·낙방 선비로 투영
- 현대 부동산·자본 권력 → 고려/조선 상인·토호로 투영
★ 단, 투영이 노골적이면 알레고리가 어색해진다. 관객이 '어? 이거 지금 이야기잖아'를
  자연스럽게 감지하도록 — 설명 금지.

[6. 장르 혼합의 성공 패턴]
한국 팩션역사영화는 대부분 장르 혼합.
- 팩션 + 액션: 〈암살〉〈밀정〉〈봉오동 전투〉〈남한산성〉 일부
- 팩션 + 코미디: 〈황산벌〉〈방자전〉
- 팩션 + 드라마: 〈사도〉〈관상〉
- 팩션 + 스릴러: 〈밀정〉〈아가씨〉
- 팩션 + 로맨스: 〈황진이〉〈쌍화점〉
자문: 이 작품의 모선 장르는 무엇인가? 모선 재미 먼저, 시대 무게 얹기.

[7. 가공 주인공의 설계]
팩션 주인공 = '시대의 증인'이자 '드라마의 엔진'.
- 실존 인물의 그림자 속에 있되, 자기만의 욕망이 뚜렷해야 함.
- 주인공의 욕망이 역사적 사건과 부딪히며 드라마 발생.
- 주인공의 신분·직업은 시대와 유기적 연결 (단순 현대인을 과거에 옮긴 것이면 실패).
- 주인공이 해당 시대·계층에만 존재할 수 있는 고유한 입장·딜레마를 가져야 함.

예시:
- 〈왕의 남자〉 광대: 조선 신분제 하층 + 예술가 + 왕의 관심 대상이라는 삼중 위치
- 〈관상〉 관상가: 조선 중기 풍수·관상의 문화적 위상 + 정치 소용돌이의 주변인
- 〈암살〉 저격수: 일제강점기 여성 독립운동가의 희귀성 + 개인사의 비극

[8. 팩션역사영화 대사 설계 — sample_lines 반영]
- 시대감과 현대 이해도의 균형. 정통보다 덜 격식.
- 재치·농담·은유 활용 가능 (정통에서 제한되는 것들).
- 주인공은 현대 관객이 감정이입할 수 있는 결의 대사.
- 실존 배경 인물은 좀 더 격식있는 대사.
★ 장르 혼합 팩션의 경우, 모선 장르의 대사 규칙이 우선.
"""


FUSION_HISTORY_RULES = """
[퓨전역사영화 특화 규칙 — FUSION HISTORY]

★ 이 작품은 퓨전역사영화다. 시대 배경만 과거에서 빌려오고 드라마는 완전 자유. ★
★ 레퍼런스: 〈조선명탐정〉〈전우치〉〈군도〉〈바람과 함께 사라지다〉〈조선미녀삼총사〉 ★

[퓨전역사영화의 본질]
시대는 장르의 무대 장치다. 역사적 사실 재현이 목적이 아니다.
현대적 감각과 시대적 이질감의 충돌에서 재미가 나온다.
장르 영화의 재미가 역사의 무게보다 우위에 있다.

[1. 시대는 '무드'이지 '고증 대상'이 아니다]
- 시대의 대략적 분위기는 유지 (의상·공간·기본 제도).
- 세밀한 고증 의무에서 자유.
- 단, 시대의 기본 규칙은 지켜야 함 (조선시대 스마트폰 등장 금지).
★ 관객이 '그럴듯한 조선'으로 받아들이면 충분.

[2. 현대적 감각의 능동적 활용]
퓨전의 강점은 현대성을 과거에 투영하는 자유로움.
- 현대식 유머·대사 리듬 허용 ("대박", "미친" 등은 신중히, 남발 금지).
- 현대적 캐릭터 원형 (시니컬한 형사·수다스러운 버디·츤데레 라이벌).
- 장르 문법 과감한 적용 (수사물·버디·케이퍼·슈퍼히어로물).
- 음악·편집 리듬의 현대화.

[3. 퓨전영화의 장르 혼합 — 거의 필수]
순수 시대극으로서 퓨전은 드물다. 대부분 장르 혼합.
- 퓨전 + 수사물: 〈조선명탐정〉
- 퓨전 + 판타지: 〈전우치〉〈물괴〉
- 퓨전 + 케이퍼/액션: 〈조선미녀삼총사〉
- 퓨전 + 서부극: 〈좋은 놈 나쁜 놈 이상한 놈〉
- 퓨전 + 히어로물: 〈검객〉
자문: 이 작품의 장르 정체성은 무엇인가? 해당 장르 재미를 최우선, 시대 배경은 무대 장치.

[4. 캐릭터 설계의 자유]
- 가공 인물만 주인공 (실존 인물 중심 금지 — 그건 팩션).
- 현대적 성격 원형 자유롭게.
- 시대 규범을 위반하는 인물도 허용 (조선시대 여성 검객 등 — 판타지적 허용).

[5. 시대의 이질감을 재미로 전환]
퓨전의 쾌감: '현대적 감각이 과거에 침입할 때의 웃음·쾌감'.
- 과거 인물이 현대인처럼 반응하는 낙차 (〈조선명탐정〉)
- 현대 사물의 과거판 (〈전우치〉 유사 마법 도구)
- 시대착오적 개그 활용 가능 (단, 전체 톤과 조화)

[6. 고증의 최소선 — 여기까지는 지켜라]
퓨전이라도 아래는 최소 지킬 것:
- 대략의 시대 (조선/고려 구분)
- 기본 계급 구조 (왕·양반·상민·노비)
- 기본 의복의 결 (한복 색감·구성 유지)
- 기본 언어 (완전 현대어만 쓰면 몰입 붕괴)
- 시대를 벗어나는 기술 등장 금지 (판타지 설정으로는 허용).

[7. 역사 왜곡 리스크 대응]
퓨전이라도 심각한 역사 왜곡 논란은 흥행 타격.
- 민족 감정이 강한 역사 사건(임진왜란·일제강점기)은 퓨전 소재로 위험.
- 실존 비극적 인물·민감한 민족 감정의 대상은 가벼운 퓨전 대상으로 삼지 말 것.
- 왕이나 실존 인물의 이름을 빌려 완전히 다른 캐릭터로 만들 때도 논란 가능.
★ 퓨전은 '가벼운 오락'과 '역사 왜곡 논란'의 경계 — 시대·소재의 민감도 신중히.

[8. 퓨전역사영화 대사 설계 — sample_lines 반영]
- 시대감은 최소 유지, 현대 감각은 적극 활용.
- 모선 장르의 대사 규칙이 최우선 (수사물 퓨전이면 수사물 대사 규칙).
- 시대 호칭은 사용하되 톤은 현대적.
- 명백한 시대착오 개그는 의도적 사용 가능 (남발 금지).
★ 퓨전의 대사는 '우리가 아는 그 시대 같지만, 훨씬 말이 잘 통하는 시대' 느낌.
"""


def get_historical_film_rules(historical: bool, film_type: str = "") -> str:
    """
    역사영화 규칙 블록 반환.
    Args:
        historical: 역사영화 체크 여부
        film_type: "정통" / "팩션" / "퓨전" (또는 영문/일부 일치)
    Returns:
        체크 OFF면 빈 문자열. ON이면 BASE + 선택 유형 블록.
    """
    if not historical:
        return ""
    
    parts = [HISTORICAL_FILM_BASE]
    
    t = (film_type or "").lower()
    if "정통" in t or "orthodox" in t:
        parts.append(ORTHODOX_HISTORY_RULES)
    elif "팩션" in t or "faction" in t:
        parts.append(FACTION_HISTORY_RULES)
    elif "퓨전" in t or "fusion" in t:
        parts.append(FUSION_HISTORY_RULES)
    # 유형 미지정 시 BASE만 반환 (관대 처리)
    
    return "\n\n" + "\n\n".join(parts) + "\n"


# ═══════════════════════════════════════════════════
# GENRE OVERRIDE INTEGRATION (v2.0 8장르 완성)
# ═══════════════════════════════════════════════════

# ═══════════════════════════════════════════════════
# OPENING MASTERY v2.2 (신규) — 첫 3분 도파민 설계
# 장르 = 오프닝 DNA. 복합 장르는 "두 번째 장르 = 본질" 법칙.
# 참고: 한국 상업영화 오프닝 6기법
# ═══════════════════════════════════════════════════

OPENING_MASTERY_MODULE = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPENING MASTERY — 첫 3분 도파민 설계
━━━━━━━━━━━━━━━━━━━━━━━━━━━

★ 오프닝은 관객과의 첫 약속이다. 이 약속이 장르와 일치하지 않으면 관객은 100분 내내 기대가 어긋난다. ★
★ 2020년 이후 한국 관객은 첫 3분 안에 영화를 판단한다. 극장표 15,000원 + OTT 스킵 습관 + 숏폼 세대. ★
★ 설명적 오프닝('2024년 봄. 30대 회사원 김형수는...')은 AI의 본능이지만 영화의 죽음이다. ★

[오프닝 6기법 — Opening Types]

① Action Drop — 이미 진행 중인 액션 안으로 떨어뜨리기
   - 싸움·추격·총격·범죄가 이미 한창일 때 카메라가 켜진다
   - 도착 과정·세팅 과정 생략. 관객을 Clock 안에 던진다.
   - 레퍼런스: 〈베테랑〉 중고차 사기단 검거 / 〈범죄도시〉 마석도 조폭 진압 / 〈아저씨〉 전당포 오프닝

② Cold Open — 본편과 다른 시점/장면으로 시작 후 본편 진입
   - 과거 사건, 다른 인물의 관점, 또는 본편과 이질적인 장면으로 오픈
   - 본편과의 연결은 나중에 밝혀진다
   - 레퍼런스: 〈서울의 봄〉 12.12 뉴스 인서트 / 〈곡성〉 일본 낚시꾼 / 〈박쥐〉 병원 프롤로그

③ Tease & Reveal — 수수께끼 이미지로 시작, 나중에 회수
   - 의미 불명의 강렬한 이미지(소품·장소·인물)를 먼저 보여주고
   - 영화 중후반에 그 이미지의 맥락이 드러난다
   - 레퍼런스: 〈파묘〉 LA 비행기 / 〈검은 사제들〉 소녀 각막 / 〈살인의 추억〉 1986년 논두렁

④ In Media Res — 미래의 결정적 순간 먼저, "어떻게 여기까지 왔나"
   - 클라이맥스 직전 또는 결정적 전환점을 오프닝에 먼저 보여주고
   - 플래시백으로 "어떻게 여기까지 왔는지" 역추적
   - 레퍼런스: 〈아가씨〉 지하실 묶인 숙희 / 〈내부자들〉 손 잘린 안상구 / 〈황해〉 개 경주

⑤ Character Reveal Action — 주인공을 정의하는 첫 행동/선택
   - 주인공의 본질(도덕 축·결함·신념·전술)이 드러나는 한 장면
   - 대사가 아니라 행동으로 캐릭터가 서명된다
   - 레퍼런스: 〈범죄도시〉 마석도 1분 진압 / 〈기생충〉 반지하 와이파이 잡기 / 〈엽기적인 그녀〉 지하철 토하기

⑥ Hook Dialogue — 강렬한 한 줄 대사로 시작
   - 맥락 없이 던져지는 한 줄이 작품의 톤과 주제를 선언
   - 다음 씬이 그 대사를 설명하거나 증명한다
   - 레퍼런스: 〈내부자들〉 "어이가 없네" / 〈친구〉 "내가 니 시다바리가?" / 〈올드보이〉 "누구냐 넌"


[장르 = 오프닝 DNA 매핑]

★ 복합 장르 법칙: 두 번째 장르 = 작품의 본질. 오프닝은 본질 쪽의 DNA를 선언한다. ★
★ 장르 이름의 맨 뒤에 붙은 장르가 본질이다. "로맨틱 코미디"는 코미디, "액션 스릴러"는 스릴러. ★
  - 로맨틱 코미디 = 코미디 DNA (본질은 웃음, 로맨틱은 외피)
  - 코믹 로맨스   = 로맨스 DNA (본질은 사랑, 코믹은 외피)
  - 액션 스릴러   = 스릴러 DNA (본질은 긴장·정보 비대칭)
  - 액션 코미디   = 코미디 DNA (본질은 웃음)
  - 범죄 스릴러   = 스릴러 DNA (본질은 긴장)
  - 호러 스릴러   = 스릴러 DNA (본질은 긴장, 순수 호러와 구분)
  - SF 액션      = 액션 DNA (본질은 물리적 쾌감)
  - SF 드라마    = 드라마 DNA (본질은 내면 변화)
  - 판타지 로맨스 = 로맨스 DNA (본질은 사랑)
  - 시대극 액션   = 액션 DNA (본질은 물리적 쾌감)
  - 정통역사영화 = 드라마 DNA (본질은 인물의 역사적 선택)

[장르별 오프닝 DNA]

▸ 호러 / 공포 → 권장 기법: Tease & Reveal / Cold Open
   - 첫 씬에 위협의 '흔적 또는 규칙 위반' (실체는 나중)
   - 감각 순서: 소리 → 온도 → 냄새 → 그림자 → 실체
   - ❌ 주인공 소개로 시작 ❌ 한가로운 일상 풍경
   - ✅ 첫 3분 안에 관객이 "뭔가 이상하다"를 느낌
   - 체크: 첫 3분 안에 공포의 규칙 또는 흔적이 심어졌는가?

▸ 액션 → 권장 기법: Action Drop / Character Reveal Action
   - 주인공이 이미 액션 중이거나, 액션을 선택하는 순간
   - 첫 행동이 캐릭터 원형(정의형/복수형/타락형/각성형)을 선언
   - ❌ 주인공이 운전·출근·사무 보는 풍경
   - ✅ 첫 3분 안에 주인공의 주먹/총/발/칼이 물리적 행동 중
   - 체크: 관객이 주인공의 '싸우는 방식'을 첫 씬에서 봤는가?

▸ 스릴러 / 범죄 / 누아르 → 권장 기법: Cold Open / In Media Res / Tease & Reveal
   - 정보 비대칭을 즉시 가동 (관객은 알고 주인공은 모르거나 그 반대)
   - Clock 장치 암시 (시한·마감·예고)
   - ❌ 평범한 도시 풍경으로 열기
   - ✅ 첫 3분 안에 "누가 무엇을 아는가"의 간극이 작동
   - 체크: 첫 3분 안에 Clock 또는 정보 비대칭이 작동했는가?

▸ 드라마 → 권장 기법: Character Reveal Action / Hook Dialogue
   - 주인공의 Want 또는 결핍이 행동으로 드러나는 순간
   - 한 장면에 인물의 내면이 압축됨 (말하지 않고)
   - ❌ 인물 상황을 내레이션으로 설명
   - ✅ 첫 3분 안에 주인공이 '무엇을 원하는가' 또는 '무엇이 없는가'가 보임
   - 체크: 첫 3분 안에 주인공의 Want/Need가 행동으로 드러났는가?

▸ 로맨스 / 멜로 → 권장 기법: Character Reveal Action / Hook Dialogue
   - 주인공의 '사랑에 대한 태도'가 첫 행동으로 노출
   - 신체 감각·거리·시선의 언어가 첫 씬부터 작동
   - ❌ 주인공의 일상 묘사 후 운명적 만남 준비
   - ✅ 첫 3분 안에 주인공의 '관계 방식'(회피/갈망/방어)이 행동으로 보임
   - 체크: 첫 3분 안에 로맨스의 신체 언어(거리/시선/접촉)가 작동했는가?

▸ 코미디 → 권장 기법: Character Reveal Action / Hook Dialogue
   - 주인공의 코믹 결함(comic flaw)을 즉시 노출
   - 첫 대사 또는 첫 행동이 웃음 포인트
   - ❌ 평범한 일상에서 서서히 코미디로 진입
   - ✅ 첫 3분 안에 관객이 최소 1회 웃음 (첫 대사 또는 첫 상황)
   - 체크: 첫 3분 안에 웃음 포인트 + 주인공의 코믹 결함이 드러났는가?

▸ SF → 권장 기법: Cold Open / Tease & Reveal
   - 이 세계의 핵심 규칙을 이미지로 암시 (설명 대사 금지)
   - 일상화된 기술 — 인물은 놀라지 않음, 관객이 놀람
   - ❌ '2045년 지구는...' 같은 강의식 오프닝
   - ✅ 첫 3분 안에 세계 규칙이 '보여지는' 방식으로 제시
   - 체크: 첫 3분 안에 이 세계의 핵심 규칙이 이미지로 제시되었는가?

▸ 판타지 → 권장 기법: Cold Open / Tease & Reveal
   - 초자연 첫 신호 (마법·신화·규칙의 증거)
   - 일상 공간 옆의 이질적 균열
   - ❌ 긴 세계관 내레이션
   - ✅ 첫 3분 안에 마법 규칙의 첫 증거가 이미지로 제시
   - 체크: 첫 3분 안에 마법/초자연의 첫 증거가 보였는가?


[설명적 오프닝 AI 습관 — 절대 금지 패턴]

AI가 본능적으로 쓰는 나쁜 오프닝:
❌ '서울. 2024년 봄. 30대 회사원 김형수는...' (배경 설명)
❌ '어느 날 아침, 주인공은 눈을 떴다.' (일상 시작)
❌ '오늘도 ○○은 평소처럼...' (관습 서술)
❌ '~년 전, 이 이야기는 시작된다.' (내레이터 개입)
❌ 주인공의 외형·직업·가족관계를 첫 3줄에 나열
❌ 풍경 묘사로 시작해서 천천히 인물로 줌인하는 구조

이 습관은 소설·교과서의 문법이지 영화의 문법이 아니다. 첫 3줄에 반드시
6기법 중 하나가 작동해야 한다.

[도파민 포인트 — 첫 3분 안에 최소 1회]

관객이 느껴야 할 감각 중 하나:
  · 충격 (shock)      — 예상 밖의 이미지·사건
  · 웃음 (laughter)   — 코믹 상황·대사
  · 긴장 (tension)    — 위협·시간 압박·정보 비대칭
  · 경이 (wonder)     — 처음 보는 이미지·세계
  · 호기심 (mystery)  — 풀리지 않는 수수께끼
  · 감정 울림 (empathy) — 인물의 결정적 순간

이 중 최소 1개가 첫 3분 안에 터져야 한다. 하나도 없으면 오프닝 실패.


[오프닝 도파민 ≠ 도발적 사건 — 혼동 금지 ★★★]

★ 오프닝의 첫 3분 도파민은 '사건'이 아니라 '선언'이다. 구분이 안 되면 Set-Up이 사라진다. ★

한국 상업영화 표준 3단 구조:
  · 오프닝 (0~3분)         = 장르·캐릭터·톤의 선언. 관객 붙잡기.
  · Set-Up (3~10분)        = 일상 속 결핍·욕망 축적. 주인공에 공감할 시간.
  · Inciting Incident (10~15분) = 도발적 사건. 이야기가 움직이기 시작.

한국 히트작의 오프닝 vs 도발적 사건 분리 레퍼런스:

  ▸ 〈수상한 그녀〉(2014)
    오프닝(0~3분): 나문희의 독설 = Character Reveal (웃음 도파민)
    Set-Up(3~7분): 가족에게 짐 취급당하는 설움 축적
    Inciting(10분경): 청춘 사진관 → 20대 심은경으로 변신

  ▸ 〈베테랑〉(2015)
    오프닝(0~3분): 중고차 사기단 검거 = Action Drop (경이 도파민)
    Set-Up(3~10분): 서도철 형사의 일상·팀 관계
    Inciting(12분경): 조태오 재벌 2세 사건 인지

  ▸ 〈부산행〉(2016)
    오프닝(0~3분): 트럭 운전사 + 사슴 감염 = Cold Open (호기심 도파민)
    Set-Up(3~10분): 석우와 딸 수안의 관계 결핍
    Inciting(13분경): KTX 탑승 직전 감염자 등장

  ▸ 〈기생충〉(2019)
    오프닝(0~3분): 반지하 와이파이 잡기 = Character Reveal (웃음+결핍 도파민)
    Set-Up(3~10분): 기택 가족의 일상·빈곤
    Inciting(12분경): 민혁이 연교 과외 자리 제안

  ▸ 〈엽기적인 그녀〉(2001)
    오프닝(0~3분): 지하철 토하기 = Character Reveal (웃음 도파민)
    Set-Up(3~10분): 견우의 일상·그녀의 기행 반복
    Inciting(15분경): 견우가 그녀를 업고 내리며 관계 시작

[★ 절대 규칙 — AI가 혼동하기 쉬운 포인트]

① 첫 3분은 '관객 붙잡기 + 장르 선언'이 목적이다. '사건 터뜨리기'가 아니다.
   - 오프닝의 할 일: 이 영화가 어떤 톤인지, 주인공이 어떤 사람인지를 보여주는 것.
   - Inciting의 할 일: 주인공이 돌아올 수 없는 여정에 발을 들이는 것.

② Inciting Incident를 첫 3분에 당겨 붙이면 Set-Up이 사라진다.
   - Set-Up이 없으면 관객이 주인공의 결핍에 공감할 시간이 없다.
   - 공감 없는 Inciting은 '사건'일 뿐 '감동'이 아니다.
   - 〈수상한 그녀〉가 할머니 독설(오프닝)로 먼저 관객을 웃기고, 가족 설움(Set-Up)으로
     공감을 쌓은 뒤, 변신(Inciting)을 보여주기 때문에 관객이 "저 할머니가 젊어지다니!"의
     놀라움과 응원을 동시에 느낀다. 순서가 바뀌면 작동하지 않는다.

③ Beat 1(1막 첫 비트)은 '오프닝 + Set-Up + Inciting' 전체를 담을 수도 있고
   '오프닝 + Set-Up 도입부'만 담을 수도 있다. 작품의 템포에 따라 판단하되,
   오프닝(첫 씬)은 반드시 장르 DNA의 선언이어야 한다.

④ 오프닝 도파민 6종(충격/웃음/긴장/경이/호기심/감정 울림)은 '사건의 크기'가 아니라
   '관객의 감각 자극'이다. 사건 없이도 강렬한 이미지·대사·캐릭터 행동으로 도파민이 작동한다.
   - 〈기생충〉 반지하 와이파이 씬은 '사건'이 없지만 도파민은 충분히 작동한다 —
     주인공의 결핍·유머·창의성이 한 씬에 압축되어 있기 때문이다.

⑤ 로맨틱 코미디·드라마 같은 조용한 장르도 이 공식을 따른다.
   오프닝에 '극적 사건'이 없어도, '극적인 캐릭터 순간'은 반드시 있어야 한다.
""".strip()


def get_opening_mastery() -> str:
    """Opening Mastery 모듈 반환."""
    return "\n\n" + OPENING_MASTERY_MODULE + "\n"


def _resolve_opening_dna(genre: str) -> str:
    """
    복합 장르에서 '두 번째 장르(뒤에 붙은 장르) = 본질' 법칙으로 DNA 결정.
    단일 장르면 그 장르의 DNA 반환.
    반환값: "romance" / "thriller" / "action" / "drama" / "comedy" / "horror" / "sf" / "fantasy"
    """
    g = genre.lower().strip()
    
    # 복합 장르 우선 처리 — 뒤에 붙은 장르가 본질
    # "로맨틱 코미디", "로맨스 코미디", "롬코" → 코미디 DNA (뒤가 코미디)
    if "롬코" in g:
        return "comedy"
    if ("로맨틱" in g or "로맨스" in g or "멜로" in g) and "코미디" in g:
        # 순서 확인: "코미디"가 뒤에 있으면 코미디 DNA
        idx_roman = max(g.find("로맨틱"), g.find("로맨스"), g.find("멜로"))
        idx_comedy = g.find("코미디")
        if idx_comedy > idx_roman:
            return "comedy"
        else:
            return "romance"
    # "코믹 로맨스" → 로맨스 DNA (뒤가 로맨스)
    if "코믹" in g and ("로맨스" in g or "멜로" in g):
        return "romance"
    # "액션 스릴러", "액션 범죄", "액션 누아르" → 스릴러 DNA
    if "액션" in g and ("스릴러" in g or "범죄" in g or "누아르" in g):
        return "thriller"
    # "액션 코미디" → 코미디 DNA
    if "액션" in g and "코미디" in g:
        return "comedy"
    # "호러 스릴러" → 스릴러 DNA (순수 호러와 구분)
    if ("호러" in g or "공포" in g) and "스릴러" in g:
        return "thriller"
    # "SF 액션" → 액션 DNA
    if ("sf" in g or "에스에프" in g) and "액션" in g:
        return "action"
    # "SF 드라마" → 드라마 DNA
    if ("sf" in g or "에스에프" in g) and "드라마" in g:
        return "drama"
    # "판타지 로맨스" → 로맨스 DNA
    if "판타지" in g and ("로맨스" in g or "멜로" in g):
        return "romance"
    # "시대극 액션", "사극 액션" → 액션 DNA
    if ("시대극" in g or "사극" in g) and "액션" in g:
        return "action"
    
    # 단일 장르 또는 명확한 본질 장르
    if _is_horror(genre):
        return "horror"
    if _is_thriller(genre):
        return "thriller"
    if _is_action(genre):
        return "action"
    if _is_sf(genre):
        return "sf"
    if _is_fantasy(genre):
        return "fantasy"
    if _is_comedy(genre) and not _is_romance(genre):
        return "comedy"
    if _is_romance(genre):
        return "romance"
    if _is_drama(genre):
        return "drama"
    
    # 기본값: 드라마 DNA
    return "drama"


def get_opening_dna_instruction(genre: str) -> str:
    """
    Core Build 단계에 주입할 '이 작품의 오프닝 DNA 지시문' 반환.
    _resolve_opening_dna 결과를 받아 구체적 집필 지시로 변환.
    """
    dna = _resolve_opening_dna(genre)
    
    dna_map = {
        "horror": {
            "label": "호러 / 공포",
            "recommended_types": "Tease & Reveal 또는 Cold Open",
            "rule": "첫 3분 안에 위협의 '흔적 또는 규칙 위반'이 제시되어야 한다. 실체는 나중에. 감각 순서는 소리→온도→냄새→그림자→실체.",
            "forbidden": "주인공 소개 / 한가로운 일상 풍경",
            "dopamine": "긴장 또는 호기심 (뭔가 이상하다는 감각)",
        },
        "action": {
            "label": "액션",
            "recommended_types": "Action Drop 또는 Character Reveal Action",
            "rule": "주인공이 이미 액션 중이거나, 액션을 선택하는 순간. 첫 행동이 주인공의 원형(정의형/복수형/타락형/각성형)을 선언해야 한다.",
            "forbidden": "주인공이 운전·출근·사무 보는 풍경",
            "dopamine": "충격 또는 경이 (주인공의 싸우는 방식)",
        },
        "thriller": {
            "label": "스릴러 / 범죄 / 누아르",
            "recommended_types": "Cold Open, In Media Res 또는 Tease & Reveal",
            "rule": "정보 비대칭을 즉시 가동. Clock 장치 암시(시한·마감·예고). 관객과 주인공이 아는 것의 간극이 첫 씬부터 작동해야 한다.",
            "forbidden": "평범한 도시 풍경 / 주인공의 일상",
            "dopamine": "긴장 또는 호기심 (누가 무엇을 아는가)",
        },
        "drama": {
            "label": "드라마",
            "recommended_types": "Character Reveal Action 또는 Hook Dialogue",
            "rule": "주인공의 Want 또는 결핍이 행동으로 드러나는 순간. 한 장면에 인물의 내면이 압축되어야 한다(말하지 않고 보여주기).",
            "forbidden": "인물 상황을 내레이션으로 설명",
            "dopamine": "감정 울림 (주인공의 Want/Need가 보이는 순간)",
        },
        "romance": {
            "label": "로맨스 / 코믹 로맨스 / 멜로",
            "recommended_types": "Character Reveal Action 또는 Hook Dialogue",
            "rule": "주인공의 '사랑에 대한 태도'가 첫 행동으로 노출. 신체 감각·거리·시선의 언어가 첫 씬부터 작동해야 한다. 코믹 로맨스의 경우에도 코미디가 아니라 '로맨스의 신체 언어'가 오프닝의 본질. 코믹은 외피.",
            "forbidden": "주인공의 일상 묘사 후 운명적 만남 준비",
            "dopamine": "감정 울림 또는 호기심 (관계 방식의 첫 노출)",
        },
        "comedy": {
            "label": "코미디 / 로맨틱 코미디 / 액션 코미디",
            "recommended_types": "Character Reveal Action 또는 Hook Dialogue",
            "rule": "주인공의 코믹 결함(comic flaw)을 즉시 노출. 첫 대사 또는 첫 행동이 웃음 포인트. 관객이 첫 3분 안에 최소 1회 웃어야 한다. 로맨틱 코미디의 경우에도 로맨스가 아니라 '코미디의 결함 드러내기'가 오프닝의 본질. 로맨틱은 외피.",
            "forbidden": "평범한 일상에서 서서히 코미디로 진입",
            "dopamine": "웃음 (첫 대사 또는 첫 상황)",
        },
        "sf": {
            "label": "SF",
            "recommended_types": "Cold Open 또는 Tease & Reveal",
            "rule": "이 세계의 핵심 규칙을 이미지로 암시. 설명 대사 절대 금지. 인물들은 일상화된 기술에 놀라지 않음 — 관객이 놀람.",
            "forbidden": "'2045년 지구는...' 강의식 오프닝",
            "dopamine": "경이 또는 호기심 (처음 보는 세계의 작동 원리)",
        },
        "fantasy": {
            "label": "판타지",
            "recommended_types": "Cold Open 또는 Tease & Reveal",
            "rule": "초자연의 첫 신호(마법·신화·규칙의 증거). 일상 공간 옆의 이질적 균열. 긴 세계관 내레이션 금지.",
            "forbidden": "긴 세계관 내레이션 / 선택받은 자 소개",
            "dopamine": "경이 또는 호기심 (마법 규칙의 첫 증거)",
        },
    }
    
    info = dna_map.get(dna, dna_map["drama"])
    
    return f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━
★ 이 작품의 오프닝 DNA — {info['label']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━

[권장 기법] {info['recommended_types']}
[핵심 규칙] {info['rule']}
[절대 금지] {info['forbidden']}
[도파민 포인트] {info['dopamine']}

★ opening_strategy 필드를 작성할 때 이 DNA를 반드시 반영하라. ★
★ 복합 장르인 경우 '두 번째 장르(뒤에 붙은 장르) = 본질' 법칙에 따라 위 DNA가 이미 결정되어 있다.
   예: 로맨틱 코미디 → 코미디 DNA (로맨틱은 외피), 액션 스릴러 → 스릴러 DNA (액션은 외피),
       코믹 로맨스 → 로맨스 DNA (코믹은 외피)
""".strip() + "\n"



    """장르별 특화 규칙 통합 반환 (8장르 지원).
    롬코(로맨틱 코미디)면 코미디+로맨스 이중 활성화."""
    blocks = []
    if _is_comedy(genre):
        blocks.append(COMEDY_RULES)
    if _is_horror(genre):
        blocks.append(HORROR_RULES)
    if _is_romance(genre):
        blocks.append(ROMANCE_RULES)
    if _is_action(genre):
        blocks.append(ACTION_RULES)
    if _is_drama(genre):
        blocks.append(DRAMA_RULES)
    if _is_thriller(genre):
        blocks.append(THRILLER_RULES)
    if _is_sf(genre):
        blocks.append(SF_RULES)
    if _is_fantasy(genre):
        blocks.append(FANTASY_RULES)
    return "\n".join(blocks)


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
# SYSTEM PROMPTS (v1.5: LOCKED 시스템 통합)
# ═══════════════════════════════════════════════════

SYSTEM_RESEARCH = """당신은 콘텐츠 기획 리서처다.
아이디어와 장르를 기반으로 실화/뉴스와 기존 작품을 리서치한다.
관련 작품은 차별화 포인트 분석에 활용한다.
""" + LOCKED_SYSTEM_RULES + "\n\n" + JSON_OUTPUT_RULES_STRICT

SYSTEM_BRAINSTORM_CARDS = """당신은 글로벌 콘텐츠 시장을 이해하는 Development Producer이자 Script Architect다.
기획자의 아이디어를 개발 가능한 컨셉 카드로 정렬한다.
이야기(story)와 분위기(mood)를 구분한다.
타겟 시장과 포맷을 반영한다.
리서치가 있으면 참고하되 기존작을 모방하지 않는다.
""" + LOCKED_SYSTEM_RULES + "\n\n" + SORKIN_CURTIS["but_except_test"] + "\n\n" + ATTRACTION_RULES + "\n\n" + JSON_OUTPUT_RULES_STRICT

SYSTEM_BRAINSTORM_ANALYSIS = """당신은 Development Producer다.
Brainstorm Top 3를 기반으로 시장성/차별화/타이밍을 분석하고 Gate A를 채점한다.
""" + LOCKED_SYSTEM_RULES + "\n\n" + SORKIN_CURTIS["but_except_test"] + """

[Gate A 채점 시 추가 검증]
- 각 컨셉의 로그라인에 BUT/EXCEPT가 있는가? 없으면 conflict_one_line 감점.
- 로그라인이 'and then' 나열형이면 originality 감점.
""" + JSON_OUTPUT_RULES_STRICT


def _get_genre_override(genre: str) -> str:
    """장르별 특화 규칙 통합 반환 (8장르 지원).
    롬코(로맨틱 코미디)면 코미디+로맨스 이중 활성화."""
    blocks = []
    if _is_comedy(genre):
        blocks.append(COMEDY_RULES)
    if _is_horror(genre):
        blocks.append(HORROR_RULES)
    if _is_romance(genre):
        blocks.append(ROMANCE_RULES)
    if _is_action(genre):
        blocks.append(ACTION_RULES)
    if _is_drama(genre):
        blocks.append(DRAMA_RULES)
    if _is_thriller(genre):
        blocks.append(THRILLER_RULES)
    if _is_sf(genre):
        blocks.append(SF_RULES)
    if _is_fantasy(genre):
        blocks.append(FANTASY_RULES)
    return "\n".join(blocks)


def build_system_core(genre: str, fact_based: bool = False, historical: bool = False, film_type: str = "") -> str:
    """Core Build 시스템 프롬프트 — v2.3 최종 (장르 + LOCKED + FACT + OPENING MASTERY + BJND 4축 + 창작자 감성 + 기술 지원)"""
    genre_rules = get_genre_rules(genre)
    genre_override_block = _get_genre_override(genre)
    fact_block = get_fact_based_rules(fact_based)
    historical_block = get_historical_film_rules(historical, film_type)
    opening_mastery = get_opening_mastery()
    opening_dna = get_opening_dna_instruction(genre)
    bjnd_four_axis = get_bjnd_four_axis()
    creator_sensibility = get_creator_sensibility()  # v2.3 Phase 3
    support_modules = get_creator_support_modules()  # v2.3 Phase 4
    return f"""당신은 헐리우드 메이저 스튜디오의 Development Producer이자 Script Architect다.
Brainstorm에서 선정된 컨셉을 기반으로 Core Build를 수행한다.
로그라인을 고정하고, 기획의도와 주제를 정리하고, 세계관과 캐릭터를 설계하고,
주인공의 Goal / Need / Strategy / Cost를 확정하고, 이 작품의 오프닝 전략을 결정한다.
★ 모든 BJND 설계 후 4축 자가 검증을 반드시 수행한다. ★
★ 창작자 감성 3요소와 기술 지원 7모듈을 준수한다. ★

{LOCKED_SYSTEM_RULES}

[장르: {genre}]
{json.dumps(genre_rules, ensure_ascii=False)}

[장르 인식]
- 선택된 장르의 필수 요소가 Core Build에 반영되어야 한다.
- 로그라인에 장르적 Hook이 포함되어야 한다.
- 캐릭터 설계에 장르적 역할이 반영되어야 한다.

{SORKIN_CURTIS["intention_obstacle"]}

{SORKIN_CURTIS["but_except_test"]}

{NARRATIVE_DRIVE}

{bjnd_four_axis}

{creator_sensibility}

{support_modules}

{ATTRACTION_RULES}

{genre_override_block}
{fact_block}
{historical_block}

{SORKIN_CURTIS["planting_payoff"]}

{opening_mastery}

{opening_dna}

{JSON_OUTPUT_RULES_STRICT}

- 작가의 고유한 아이디어를 훼손하지 않는다.
- ★ LOCKED 블록의 캐릭터 소속, 직책, 나이, 핵심 관계를 절대 변경하지 마라. ★
- ★ LOCKED 블록의 기획의도 키워드를 캐릭터/세계관/시놉시스에 반드시 반영하라. ★
- 필수 캐릭터 4인(protagonist/antagonist/ally/mirror)은 characters 배열에.
- 추가 캐릭터(0~4인)는 extended_characters 배열에. 역할명은 자유 (catalyst/subplot_lead/mentor/rival/informant 등).
- 영화는 총 4~5명, 미니시리즈는 6~8명이 적정. 이야기가 필요로 하는 만큼 생성.
- ★ BJND 설계 완료 후 bjnd_four_axis_check 필드에 4축 자가 검증 결과를 반드시 기재하라. ★
- ★ 적대자(antagonist)도 반드시 BJND 4단(Lack/Desire/Strategy/Cost)으로 설계하라 — 평면 빌런 금지. ★
- ★ 테마와 주인공 Strategy의 방향이 일치하는지 자가 검증하라 — 반대 방향이면 재설계. ★"""


SYSTEM_CORE_GATE = """당신은 Development Producer다.
Core Build 결과를 채점한다.
점수는 0.0~10.0, 소수점 1자리 반올림.

[LOCKED 정합성 추가 채점]
- LOCKED 블록의 캐릭터 소속이 변경되었으면 해당 캐릭터 항목 0점.
- LOCKED 블록의 기획의도 키워드가 출력에 없으면 theme 항목 감점.
- LOCKED 블록의 핵심 관계가 변경되었으면 relationship 항목 감점.

[장르 기대 체크리스트 채점 — v2.3.2 추가]
- genre_expectation_check.checklist에서 NO 응답이 1개 이상이면 structure 항목 -1점.
- genre_expectation_check.climax_verdict가 "CLIMAX_FAIL"이면 structure 항목 -2점 (장르 약속 배반).
- genre_expectation_check.genre_fun_alive가 false이면 전체 final_score -1.5점 (장르 재미 소실).
- weak_zones가 3개 이상이면 structure 항목 -0.5점.

[장르-클라이맥스 정렬 엄격 검증]
- 로맨틱 코미디인데 클라이맥스가 부녀 화해/가족 서사/사회적 성공이면 CLIMAX_FAIL 판정.
- 스릴러인데 클라이맥스가 정보 비대칭 해소가 아닌 감정 드라마이면 CLIMAX_FAIL 판정.
- 호러인데 클라이맥스에 공포 규칙 위반이 없으면 CLIMAX_FAIL 판정.
- 액션인데 클라이맥스가 물리적 쾌감 없이 대화로 끝나면 CLIMAX_FAIL 판정.
- 각 장르의 클라이맥스 기대와 실제 설계가 어긋나면 가차없이 감점.
""" + JSON_OUTPUT_RULES_STRICT


def build_system_char_bible(genre: str, fmt: str, others_str: str,
                             fact_based: bool = False, historical: bool = False, film_type: str = "") -> str:
    """Character Bible 시스템 프롬프트 — Tactics = Character + LOCKED + 장르 특화 + FACT/HISTORICAL"""
    fact_block = get_fact_based_rules(fact_based)
    historical_block = get_historical_film_rules(historical, film_type)
    genre_char_block = ""
    if _is_comedy(genre):
        genre_char_block += """
[코미디 캐릭터 특화 — COMEDY CHARACTER OVERRIDE]
★ 이 작품은 코미디다. 캐릭터를 웃기게 설계하라. ★
- flaw는 '코믹 결함'이어야 한다: 이 결함 때문에 매번 사고를 치는 구조.
- backstory에 코믹 모순을 심어라: 캐릭터가 생각하는 자기 vs 실제 자기.
- ★ sample_lines 3개(normal/angry/vulnerable)가 모두 코미디 톤이어야 한다.
  코미디 대사 7기법 중 최소 2개 사용: Misdirection / Callback / Topper / Deadpan / Status Flip / Comic Specificity / Non-sequitur
- tactics에서 최소 1개는 코믹 전술이어야 한다.
- antagonist는 무섭지 않고 웃겨야 한다. 자기만의 미친 논리가 있는 인물.
- Straight Man + Funny Man 역할을 구분하라.
"""
    if _is_horror(genre):
        genre_char_block += """
[호러 캐릭터 특화 — HORROR CHARACTER OVERRIDE]
★ 이 작품은 호러다. 캐릭터의 공포 반응이 관객의 공포다. ★
- 주인공은 관객의 대리인. 관객과 같은 것을 두려워해야 한다.
- backstory에 '이 인물이 가장 두려워하는 것'을 구체적으로. 그것이 공포의 촉매가 된다.
- sample_lines: normal은 평범하게, panic은 문장이 끊기게, aftermath는 건조하게.
  예 normal: '...뭐야 그거.'  panic: '안 돼, 안 돼, 안—'  aftermath: '...가자.'
- 위협(빌런/괴물)은 불완전하게 설계하라. 정체를 다 보여주면 안 무섭다.
  외형 대신 흔적/소리/규칙을 설계하라.
"""
    if _is_romance(genre):
        genre_char_block += """
[로맨스 캐릭터 특화 — ROMANCE CHARACTER OVERRIDE]
★ 이 작품은 로맨스다. 두 사람의 끌림이 구체적이어야 한다. ★
- '끌림의 이유'가 구체적이어야 한다. '그냥 좋아서'는 실패.
  A가 가진 것 = B에게 없는 것. 결핍의 상호 보완 구조.
- sample_lines에 '상대 앞에서의 대사'와 '상대 없을 때의 대사'가 달라야 한다.
  상대 앞: 감정을 숨기거나 돌려 말한다. 상대 없을 때: 본심이 나온다.
  예 앞에서: '커피 좋아해요?' (관심의 위장)  없을 때: '...왜 그런 걸 물었지.'
- 신체 감각을 설계하라: 이 인물이 상대와 가까울 때 어떤 물리적 반응을 보이는가.
  심장, 손끝, 시선, 호흡 — 구체적으로.
"""
    return f"""당신은 헐리우드 A-list 캐릭터 디자이너이자 심리학 전문가다.
Core Build에서 만든 기본 캐릭터 1인을 '캐릭터 바이블' 수준으로 확장한다.

{LOCKED_SYSTEM_RULES}

[목표]
Writer Engine(시나리오 생성 AI)이 80~120씬 동안 이 인물을 일관되게 쓸 수 있도록,
내면·외형·말투·관계·변화를 정밀하게 설계한다.

★ LOCKED 블록에 이 캐릭터의 소속, 직책, 나이, 핵심 관계가 명시되어 있으면
  반드시 그대로 사용하라. 더 재미있는 설정을 위해 변경하는 것은 금지다. ★
★ LOCKED 블록에 기획의도 키워드(예: 취업난, 고시원, 특전사 전역금)가 있으면
  backstory 또는 sample_lines에 구체적으로 반영하라. ★

{SORKIN_CURTIS["tactics_character"]}

[작성 원칙]
1. 백스토리는 현재 행동의 원인이 되어야 한다.
   ★ protagonist일 경우: 서사동력(narrative_drive)의 발생요인이 상실(loss)이면 잃어버린 것이 backstory의 핵심.
     결핍(lack)이면 처음부터 없었던 것이 backstory의 핵심. ★
2. 비밀(secret)은 플롯의 전환점이 될 수 있어야 한다.
3. 말투(speech_pattern)는 구체적 규칙으로 — '거칠다' 같은 추상어 금지.
4. 대사 샘플(sample_lines)은 실제 시나리오에 바로 넣을 수 있는 수준.
5. 관계별 태도(relationship_attitudes)는 상대 캐릭터({others_str})에 따라 달라지는 행동 명시.
6. 변화 궤적(arc_detail)은 1막/미드포인트/클라이맥스 3단계로 구체적.
7. tactics는 이 인물이 장애물을 넘기 위해 선택하는 전술 3가지. 전술의 차이가 캐릭터의 차이다.
8. 장르: {genre} / 포맷: {fmt}

[적대자(antagonist) 전용 — Villain 4 Questions]
이 캐릭터의 role이 antagonist이면 아래를 반드시 설계에 반영하라:
① 흥미로운가? — 뻔한 악역이면 실패. 독특한 동기/배경/성격. 자신만의 논리 안에서 옳다고 믿어야 한다.
② 주인공의 다크 미러인가? — '주인공이 다른 선택을 했다면 이 사람이 된다.' 테마적 연결 필수.
③ 등장 시 주인공의 계획을 뒤엎는가? — 적대자가 등장하면 플롯이 바뀌어야 한다. 단순 위협이 아니라 계획 파괴.
④ 빌런이 이기고 있는가? — 적대자는 클라이맥스 직전까지 거의 모든 대결에서 이겨야 한다. 빌런이 매번 실패하면 클라이맥스에서 아무도 긴장하지 않는다.

{genre_char_block}

{fact_block}
{historical_block}

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
- speech_pattern은 추상어 금지. 구체적 규칙만.
- ★ LOCKED 블록의 캐릭터 정보(소속/직책/나이/관계)를 반드시 준수하라. ★
- ★ 일관성 보호 블록이 있으면 거기 기재된 다른 캐릭터의 사실과 절대 모순되게 쓰지 마라.
  특히 가족 관계의 생사·이혼 여부, 공유 과거 사건의 시점, 학력·출신지의 기본 정보는
  단 하나의 버전으로만 존재해야 한다. 이미 확정된 사실을 재정의하거나 변경하지 마라. ★"""


# ═══════════════════════════════════════════════════
# 캐릭터 일관성 보호 (v2.3.1 신규)
# 목적: 순차 생성 시 이전 캐릭터와의 설정 모순 방지
# 예: 유진(8살 이혼) vs 강회장(11살 위암사망) 같은 모순 차단
# ═══════════════════════════════════════════════════

def extract_char_consistency_facts(char_data: dict) -> dict:
    """이미 생성된 캐릭터에서 '일관성 핵심 사실'만 추출.
    이 사실들은 다른 캐릭터의 백스토리와 모순되어선 안 된다.
    
    Returns:
        {
            "name": "강유진",
            "role": "protagonist",
            "age": 32,
            "key_facts": [추출된 핵심 사실들]
        }
    """
    facts = []
    
    # 나이 (관계 속 나이 차이 계산에 필수)
    age = char_data.get("age", "")
    if age:
        facts.append(f"나이: {age}세")
    
    # 직업 · 소속
    occupation = char_data.get("occupation", "")
    if occupation:
        facts.append(f"직업/위치: {occupation}")
    
    # 학력 · 과거 경력 (backstory에서 추출 — 학력 키워드 포함)
    backstory = char_data.get("backstory", "")
    if backstory:
        # 요약본만 전달 (전체 백스토리를 주면 프롬프트 폭증)
        backstory_summary = backstory[:300] + ("..." if len(backstory) > 300 else "")
        facts.append(f"과거사 요약: {backstory_summary}")
    
    # 가족 관계 (어머니·아버지·형제자매 생사·현존 여부 — 일관성 가장 중요)
    # relations에 가족 관계 정보가 담기므로 그대로 활용
    relations = char_data.get("relations", {})
    if relations:
        for rel_name, rel_data in relations.items():
            if isinstance(rel_data, dict):
                attitude = rel_data.get("attitude", "")
                if attitude:
                    facts.append(f"→ {rel_name}: {attitude[:150]}")
    
    # 비밀 (다른 캐릭터의 비밀과 모순되거나 겹치지 않도록)
    secret = char_data.get("secret", "")
    if secret:
        facts.append(f"비밀: {secret[:200]}")
    
    return {
        "name": char_data.get("name", ""),
        "role": char_data.get("role", ""),
        "age": age,
        "key_facts": facts,
    }


def build_prior_chars_consistency_block(prior_chars: list) -> str:
    """이미 생성된 캐릭터들의 핵심 사실을 프롬프트 블록으로 구성.
    다음 캐릭터 생성 시 모순 방지용.
    
    Args:
        prior_chars: 이미 생성된 캐릭터 데이터 리스트
    
    Returns:
        프롬프트에 주입할 일관성 블록 문자열 (빈 리스트면 빈 문자열)
    """
    if not prior_chars:
        return ""
    
    lines = [
        "",
        "[★ 일관성 보호 — 이미 확정된 설정 ★]",
        "아래는 이미 생성되어 확정된 다른 캐릭터들의 핵심 사실이다.",
        "당신이 지금 생성하는 캐릭터의 백스토리·관계·비밀은 아래와 절대 모순되면 안 된다.",
        "",
        "[특히 다음을 반드시 일치시켜라]",
        "- 가족 관계: 어머니·아버지·형제자매의 생사·이혼 여부·사망 시기는 단 하나의 버전만 존재한다.",
        "- 공유 사건: 같은 사건을 두 캐릭터가 기억할 경우 시점과 세부 사항이 같아야 한다.",
        "- 시간축: 나이 차이, 과거 사건 간 시간 경과는 물리적으로 일관되어야 한다.",
        "- 공간: 같은 장소에 대한 묘사가 서로 충돌하면 안 된다.",
        "",
    ]
    
    for i, fact_dict in enumerate(prior_chars, 1):
        name = fact_dict.get("name", f"캐릭터{i}")
        role = fact_dict.get("role", "")
        age = fact_dict.get("age", "")
        
        header = f"■ 이미 확정된 캐릭터 {i}: {name}"
        if role:
            header += f" ({role})"
        if age:
            header += f" / {age}세"
        lines.append(header)
        
        key_facts = fact_dict.get("key_facts", [])
        for fact in key_facts:
            lines.append(f"  · {fact}")
        lines.append("")
    
    lines.append("★ 위 사실과 모순되는 백스토리/관계/비밀을 쓰면 심각한 결함이다. 반드시 교차 검증하라. ★")
    lines.append("")
    
    return "\n".join(lines)


def build_system_structure_story(fact_based: bool = False, historical: bool = False, film_type: str = "") -> str:
    """Structure Build Story 시스템 프롬프트 — 서브플롯 설계 포함 + LOCKED + FACT/HISTORICAL"""
    fact_block = get_fact_based_rules(fact_based)
    historical_block = get_historical_film_rules(historical, film_type)
    return """당신은 헐리우드 수준의 Story Architect다.
Core Build 결과를 기반으로 시놉시스와 스토리라인을 설계한다.
주인공의 Goal/Need/Strategy가 모든 전개의 중심축이 되어야 한다.

""" + NARRATIVE_DRIVE + "\n\n" + LOCKED_SYSTEM_RULES + "\n\n" + """
★ LOCKED 블록에 확정된 플롯 포인트(촉발 사건, 결말, 핵심 반전 등)가 있으면
  시놉시스와 스토리라인에 반드시 포함하라. 재해석이나 변형 금지. ★
★ LOCKED 블록에 역사적 사건 도입부가 지정된 경우, 해당 에피소드/비트에 반드시 포함하라. ★
""" + SORKIN_CURTIS["probable_impossibility"] + "\n\n" + SORKIN_CURTIS["subplot_design"] + fact_block + historical_block + "\n\n" + JSON_OUTPUT_RULES_STRICT


def build_system_structure_diagnosis(fact_based: bool = False, historical: bool = False, film_type: str = "") -> str:
    """Structure Diagnosis v1.5 — 관객 심리 설계 + 서브플롯 충돌 + LOCKED 검증 + FACT/HISTORICAL"""
    fact_block = get_fact_based_rules(fact_based)
    historical_block = get_historical_film_rules(historical, film_type)
    return """당신은 헐리우드 수준의 Structure Analyst다.
시놉시스와 스토리라인을 기반으로 구조 진단과 캐릭터 변화를 설계한다.

""" + LOCKED_SYSTEM_RULES + "\n\n" + """
[LOCKED 정합성 진단 — 추가 항목]
- LOCKED 블록의 캐릭터 소속이 변경된 비트가 있으면 해당 비트 status '위반', note에 'LOCKED 위반: [항목]'
- LOCKED 블록의 플롯 포인트가 누락된 비트가 있으면 해당 비트 status '누락', note에 'LOCKED 누락: [항목]'
- LOCKED 블록의 기획의도 키워드가 전체 비트에서 1건도 반영되지 않았으면 별도 경고

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

[빌런 승률 설계 — Patriot Games 규칙]
- 적대자가 클라이맥스 직전까지 거의 모든 대결에서 이겨야 한다.
- 비트별로 적대자의 승/패를 추적하라:
  Beat 1~6 (1막): 적대자 주도. 주인공은 반응만 한다.
  Beat 7~12 (2막): 적대자 압도. 주인공의 전략이 매번 무너진다.
  Beat 13~14 (3막): 적대자 최고조 → 주인공이 마지막에 역전.
- 주인공이 중간에 쉽게 이기는 비트가 있으면 status '약함', note에 '빌런 승률 위반 — 긴장감 저하'.
- ★ 빌런이 매번 실패하면 클라이맥스에서 아무도 긴장하지 않는다. ★
""" + SORKIN_CURTIS["probable_impossibility"] + "\n\n" + SORKIN_CURTIS["unified_plot_test"] + fact_block + historical_block + "\n\n" + JSON_OUTPUT_RULES_STRICT


SYSTEM_STRUCTURE_GATE = """당신은 Development Producer다.
Structure Build 결과를 채점한다.
점수는 0.0~10.0, 소수점 1자리 반올림.

[LOCKED 정합성 채점]
- LOCKED 위반 항목이 1건이라도 있으면 해당 카테고리 0점.

[추가 검증]
- 억지 우연에 의존하는 전환점이 있으면 해당 항목 감점.
- ending_inevitable_surprising: 결말이 '필연적이면서 놀라운가' — 우연에 의한 해결이면 0점.
""" + JSON_OUTPUT_RULES_STRICT


def build_system_scene_design(genre: str, fact_based: bool = False, historical: bool = False, film_type: str = "") -> str:
    """Scene Design v2.3 — 장르별 특화 + Hook/Punch + LOCKED + FACT/HISTORICAL + OPENING MASTERY v2.2 + BJND ENFORCER v2.3 + 창작자 감성 v2.3"""
    genre_rules = get_genre_rules(genre)
    fact_block = get_fact_based_rules(fact_based)
    historical_block = get_historical_film_rules(historical, film_type)
    opening_mastery = get_opening_mastery()
    opening_dna = get_opening_dna_instruction(genre)
    bjnd_enforcer = get_bjnd_scene_enforcer()
    creator_sensibility = get_creator_sensibility()  # v2.3 Phase 3
    genre_scene_block = ""
    if _is_comedy(genre):
        genre_scene_block += """
[코미디 장면 설계 — COMEDY SCENE OVERRIDE]
- 매 장면의 dramatic_action에 '이 장면이 왜 웃긴가'를 명시하라.
- 코믹 엔진 유형: 상태 역전 / Rule of Three / 극과 극 대비 / 관객 우월감 중 태그.
- setpiece는 '대형 코믹 셋피스'. key_line은 건조하고 짧은 코믹 대사.
"""
    if _is_horror(genre):
        genre_scene_block += """
[호러 장면 설계 — HORROR SCENE OVERRIDE]
- 매 장면에 감각 디테일(소리/온도/냄새)을 명시하라.
- 가짜 안도(false relief) 장면을 setpiece 직전에 배치하라.
- setpiece는 '공포의 규칙 발견/위반/최종 대면' 장면. 시각보다 감각이 먼저.
- 위협의 등장은 흔적→소리→실루엣→실체 순서로 점진적으로.
"""
    if _is_romance(genre):
        genre_scene_block += """
[로맨스 장면 설계 — ROMANCE SCENE OVERRIDE]
- 매 장면에 두 사람의 물리적 거리(가까워짐/멀어짐)를 명시하라.
- setpiece는 '첫 만남/감정 폭발/이별·재회' 장면.
- key_line은 직접 감정 표현이 아닌 돌려 말하기. '좋아해'보다 '커피 좋아해요?'
- 시선과 침묵 장면을 is_setpiece에 포함하라.
"""
    if _is_action(genre):
        genre_scene_block += """
[액션 장면 설계 — ACTION SCENE OVERRIDE]
- 모든 액션 씬은 Phase 4단계로 설계: Spark / Escalation / Low Point / Turn.
- setpiece는 Opening 액션 / Midpoint 대결 / Climax 최종 대결의 3축.
- dramatic_action에 공간의 고유 소품·제약을 반드시 명시. "목욕탕 액션" 금지, "증기+수건+타일+탕" 식으로.
- key_line은 격투 직전/직후의 짧은 한 줄. 격투 중엔 1~3단어.
- 승리의 방식이 주인공 원형(정의/복수/타락/각성)을 증명해야 한다.
"""
    if _is_drama(genre):
        genre_scene_block += """
[드라마 장면 설계 — DRAMA SCENE OVERRIDE]
- 매 장면에 외적 목적(무엇을 하고 있는가) + 내적 목적(감정적으로 무엇이 일어나는가) 분리.
  예: 외적='이사 짐을 나른다' / 내적='아버지의 늙음을 처음 직면한다'.
- setpiece는 '억눌린 감정이 터지는 순간' 2~3개만 (고백/결별/화해/진실 폭로).
- key_line은 돌려 말하기. '...커피 식었네' 같은 일상어가 감정을 운반.
- '무언가를 하면서 말하는' 씬 배치 (설거지/김장/짐 옮기기).
"""
    if _is_thriller(genre):
        genre_scene_block += """
[스릴러 장면 설계 — THRILLER SCENE OVERRIDE]
- 매 장면에 정보 비대칭 명시: 관객/주인공/빌런 각각이 아는 것.
- setpiece는 Suspense 피크(관객만 아는 폭탄) 또는 반전 폭로.
- Clock 시각화: 벽시계·타이머·뉴스 속 시간·해 그림자 등 visual 요소.
- Escalation 그래프: 직전 씬보다 상황이 어떻게 더 나빠졌는가.
- key_line은 차가운 협박 또는 건조한 정보 전달.
"""
    if _is_sf(genre):
        genre_scene_block += """
[SF 장면 설계 — SF SCENE OVERRIDE]
- 매 장면에서 핵심 규칙이 어떻게 작동하는지 명시.
- setpiece는 비주얼 경이(관객이 처음 보는 이미지) + 규칙의 대가 씬.
- dramatic_action에 'Info Drip' 설계: 세계관 조각을 매 씬 한 개씩.
- Human Anchor 장면: 기술 경이 옆에 평범한 감정 씬 필수 배치.
- key_line은 기술 용어 없이 감정을 말하는 짧은 한 줄 (Blade Runner "Tears in rain" 방식).
"""
    if _is_fantasy(genre):
        genre_scene_block += """
[판타지 장면 설계 — FANTASY SCENE OVERRIDE]
- 매 장면에 마법 규칙의 작동 + 대가 명시.
- setpiece는 '마법의 규칙이 만드는 딜레마' 씬 (사랑하면 사라진다 → 선택의 순간).
- 일상 공간 + 초자연 공간의 경계 설계 (카페 뒷문이 저승).
- key_line은 약속/저주 형식의 짧은 한 줄 ("반드시 돌아오겠다").
- 마법 씬은 대사 줄이고 지문 늘리기.
"""
    return f"""당신은 헐리우드 최고 수준의 Scene Architect다.
Structure Build 결과를 기반으로 핵심 장면(Key Scene)을 설계한다.
'Show, don't tell' 원칙을 따른다.
모든 장면은 설명이 아닌 행동, 선택, 반전으로 드라마를 구현해야 한다.

{LOCKED_SYSTEM_RULES}

[장르: {genre}]
{json.dumps(genre_rules, ensure_ascii=False)}

{SORKIN_CURTIS["drop_in_middle"]}

{SORKIN_CURTIS["dramatic_irony"]}

{SORKIN_CURTIS["information_gap"]}

{SORKIN_CURTIS["mystery_box"]}

{ATTRACTION_RULES}

{genre_scene_block}

{fact_block}
{historical_block}

{opening_mastery}

{opening_dna}

{bjnd_enforcer}

{creator_sensibility}

[오프닝 씬 설계 지시 — 1막 Beat 1~2]
★ Scene Design 단계에서 1막 첫 비트의 key_scenes를 설계할 때, 위 OPENING DNA를 반드시 반영하라. ★
- 1막 Beat 1의 첫 key_scene은 오프닝 6기법 중 하나로 명확히 분류 가능해야 한다.
- 첫 key_scene의 dramatic_action에 '이 씬이 어떤 오프닝 기법인지'를 암묵적으로 구현하라.
  (예: Action Drop이면 이미 진행 중인 액션; Tease & Reveal이면 의미 불명의 강렬한 이미지)
- 첫 key_scene에 도파민 포인트(충격/웃음/긴장/경이/호기심/감정 울림) 중 최소 1개가 반드시 작동해야 한다.
- ❌ 첫 key_scene을 '주인공 소개' 또는 '일상 풍경'으로 설계하지 마라.

[Hook & Punch 규칙]
- HOOK: 매 장면 끝에 관객이 다음 장면을 보지 않을 수 없는 질문/위협/기대를 심는다.
- PUNCH: 장면의 가장 강한 순간 — 대사 한 마디, 행동 하나, 또는 침묵이 씬의 온도를 급변시킨다.
- SETPIECE: 장르의 정체성을 정의하는 대형 장면. 관객이 이 영화를 기억할 때 떠올리는 장면.

{SORKIN_CURTIS["subplot_design"]}

{SORKIN_CURTIS["planting_payoff"]}

{JSON_OUTPUT_RULES}
- 각 필드 1~2문장, 40자 이내.
- 대사는 작은따옴표만 사용.
- ★ LOCKED 블록의 캐릭터 소속과 관계를 장면 설계에서도 준수하라. ★"""


def build_system_treatment(genre: str, act_label: str, fmt: str = "", b_story_context: str = "",
                           fact_based: bool = False, historical: bool = False, film_type: str = "") -> str:
    """Treatment v2.3.6 — Core Build의 장르/BJND/POV/적대자 규칙 모두 Treatment 단계까지 전파.
    
    [v2.3.6 핵심 수정 — 엔진 구조적 공백 해결]
    이전까지 Treatment 시스템 프롬프트는 creator_sensibility(감성 3요소)만 받았음.
    장르 체크리스트(GENRE_FUN_ALIVE), BJND 4축, POV 정치학, 적대자 BJND가 빠져서
    Core Build에서 설계된 장르 재미/서사동력/시선/적대자가 Treatment 집필 시 휘발됨.
    Writer Engine에 넘어가는 시나리오 직전 단계에서 구조적 공백 발생.
    
    이번에 Core Build와 동일한 핵심 모듈 4종을 Treatment에도 주입하여
    매 비트 집필 시 장르 체크리스트 + BJND 4축 + POV 선택 + 적대자 거울 관계가
    실시간 작동하도록 수정.
    """
    genre_rules = get_genre_rules(genre)
    genre_rules_text = json.dumps(genre_rules, ensure_ascii=False)
    is_series = is_series_format(fmt)
    fact_block = get_fact_based_rules(fact_based)
    historical_block = get_historical_film_rules(historical, film_type)
    creator_sensibility = get_creator_sensibility()  # v2.3 Phase 3 — 모든 막에 주입
    
    # v2.3.6 신규 — Core Build에서 휘발되던 장르/BJND/POV/적대자 모듈을 Treatment에도 주입
    genre_fun_check = GENRE_FUN_ALIVE  # 장르 체크리스트 (매 비트 실시간 체크)
    bjnd_four_axis = get_bjnd_four_axis()  # BJND 4축 (씬 레벨 집행)
    pov_politics = POV_POLITICS  # 시선의 정치학 (씬별 POV 선택)
    antagonist_bjnd = ANTAGONIST_BJND  # 적대자 거울 관계 (빌런 비트)

    # OPENING MASTERY는 1막 트리트먼트에만 주입 (2막/3막에는 불필요)
    opening_treatment_block = ""
    if "1막" in act_label or "Act 1" in act_label or "ACT 1" in act_label:
        opening_mastery = get_opening_mastery()
        opening_dna = get_opening_dna_instruction(genre)
        opening_treatment_block = f"""
{opening_mastery}

{opening_dna}

[1막 오프닝 트리트먼트 지시 — 첫 비트 집필 시 절대 규칙]
★ 이 트리트먼트는 1막이다. 첫 비트의 첫 씬은 관객과의 첫 약속이다. ★

[첫 비트 첫 씬 작성 규칙]
- 첫 비트의 첫 씬은 위 OPENING DNA의 '권장 기법' 중 하나를 명확히 구현해야 한다.
- 첫 씬의 narrative 서술이 '설명적 오프닝 AI 습관'의 금지 패턴에 해당하면 다시 써라.
- 첫 씬 안에 도파민 포인트 6감각(충격/웃음/긴장/경이/호기심/감정 울림) 중 최소 1개가 작동해야 한다.

[1막 첫 비트 narrative 체크리스트]
□ 첫 문장이 배경 설명·시대 자막·내레이션이 아닌가?
□ 첫 3줄 안에 6기법(Action Drop/Cold Open/Tease&Reveal/In Media Res/Character Reveal Action/Hook Dialogue) 중 하나가 작동하는가?
□ 주인공의 '일상 묘사'로 시작하지 않는가?
□ 장르 DNA와 오프닝이 일치하는가? (복합 장르는 뒤에 붙은 장르 = 본질)
□ 도파민 포인트가 첫 씬 안에 터지는가?

[설명적 오프닝 절대 금지 — 1막 첫 비트에서 특히 엄격]
❌ '서울. 2024년 봄. 30대 회사원 김○○는...' (배경 설명)
❌ '어느 날 아침, 주인공은 눈을 떴다.' (일상 시작)
❌ '오늘도 ○○은 평소처럼...' (관습 서술)
❌ '~년 전, 이 이야기는 시작된다.' (내레이터 개입)
❌ 주인공의 외형·직업·가족관계를 첫 3줄에 나열
❌ 풍경 묘사로 시작해서 천천히 인물로 줌인하는 구조

★ Core Build에서 결정된 opening_strategy 필드를 참조하여 첫 비트 첫 씬에 그대로 구현하라. ★
"""

    genre_treatment_block = ""
    if _is_comedy(genre):
        genre_treatment_block += """
[코미디 트리트먼트 특화 — COMEDY NARRATIVE OVERRIDE]
★ narrative 줄글 자체가 웃겨야 한다. 구조만 코미디이고 서술이 드라마이면 실패다. ★

[코미디 narrative 서술 7규칙]
1. 물리적 디테일: 고장/넘어짐/쏟아짐 등 물리적 사건으로 웃음.
   ❌ '계산대에 앉는다.' ✅ '앉자마자 POS기가 얼어붙는다. 세 번째에 뜨는 건 윈도우 업데이트.'
2. 기대→결과 격차: '~했는데 ~였다' 구조. 성공 직후 실패.
3. 구체적 숫자: '오래'→'47분'. 숫자 격차가 웃기다.
4. 건조한 대사: 상황이 대사를 웃기게 만든다. 캐릭터는 감정을 말하지 않는다.
5. 빌런=진심: '내가 이렇게 기회를 주는 사장이 어디 있어.' (자기가 옳다고 믿음)
6. 에스컬레이션: 민원 1개→3개→7개+화재. 매 씬마다 숫자/규모 상승.
7. 코믹 이미지 끝: 비트 마지막 문장이 시각적으로 웃겨야 한다.

[★★★ 코미디 절대 규칙 — 이것을 어기면 코미디가 아니다 ★★★]

[대사가 엔진이다]
코미디는 대사가 이끄는 장르다. narrative 안에서 대사의 비중이 최소 50%.
- 대사 없이 서술만 3문장 이상 연속 금지. 대사가 서술 사이사이에 있어야 한다.
- ❌ 코미디가 죽는 패턴:
  '재하가 냉장고를 연다. 두유를 꺼낸다. 마신다. 달력을 본다. 옷장을 연다. 양복을 꺼낸다.'
  → 서술만 나열. 이건 CCTV 영상이지 코미디가 아니다.
- ✅ 코미디가 사는 패턴:
  '재하가 냉장고를 연다. 두유 하나. 유통기한이 이틀 지났다. 재하가 냄새를 맡는다. 괜찮아. 이틀이면 괜찮아. 원샷. 얼굴이 구겨진다. 괜찮아.'
  → 대사가 들어가면 캐릭터가 살아난다. 웃음이 생긴다.

[매 씬 웃음 포인트 필수]
narrative의 모든 씬에 최소 1개의 '관객이 웃는 순간'이 있어야 한다.
씬을 쓴 후 자문하라: '관객이 이 씬에서 어디서 웃는가?'
대답할 수 없으면 그 씬은 코미디가 아니다. 다시 써라.
웃음 유형: 대사 웃음(기대 전복, deadpan) / 상황 웃음(관객만 아는 것) / 리듬 웃음(Rule of Three) / 갭 웃음(진지+사소)

[코미디 서술은 짧다]
코미디의 서술(지문에 해당)은 드라마보다 짧아야 한다. 1~2문장.
타이밍이 살아야 한다. 행동 나열 금지.
- ❌ '재하가 의자를 밀고 일어서서 냉장고로 걸어가 문을 열고 안을 들여다본다.'
- ✅ '냉장고. 두유 하나. 유통기한 D+2.'
→ 짧을수록 다음 대사의 타이밍이 산다.

[체크] narrative 안 관객 웃는 순간 최소 3개 / 대사 비중 50%+ / 서술만 3문장 연속 금지 / 7기법 중 1개 / 숫자 구체적 / 눈덩이 작동
"""
    if _is_horror(genre):
        genre_treatment_block += """
[호러 트리트먼트 특화 — HORROR NARRATIVE OVERRIDE]
★ narrative 줄글이 무서워야 한다. 사건만 나열하면 스릴러지 호러가 아니다. ★

[호러 narrative 서술 7규칙]
1. 감각이 시각보다 먼저: 소리→온도→냄새→그림자→실체 순서로.
   ❌ '문이 열렸다.' ✅ '복도 끝에서 바닥 긁는 소리. 멈춘다. 다시. 이번엔 더 가깝다.'
2. 일상의 균열: 초자연이 아니라 '뭔가 이상하다'는 감각부터.
   ✅ '시계가 3시 14분에 멈춰 있다. 어제도 3시 14분. 그저께도.'
3. 가짜 안도 → 진짜 공포: 매 비트에 false relief 1회 필수.
   긴장→고조→'아 아무것도 아니었네'→진짜 공포.
4. 공간이 숨 쉬듯: 장소를 의지가 있는 것처럼. 벽지 사이 바람, 아무도 없는 2층 삐걱.
5. 대사 적게, 침묵 길게: 말이 많으면 안 무섭다. 대사 밀도 드라마의 절반.
6. 보여주지 마라: 위협의 실체는 최대한 늦게. 흔적/소리/규칙만 보여줘라.
7. 열린 공포로 끝: '소리가 멈췄다. 하지만 창문 김에 손가락 자국이 남아 있다.'

[체크] 감각 묘사 매 비트 2개 이상 / false relief 1회 / 위협 직접 노출 자제 / 침묵 장면 1개
"""
    if _is_romance(genre):
        genre_treatment_block += """
[로맨스 트리트먼트 특화 — ROMANCE NARRATIVE OVERRIDE]
★ narrative 줄글에 설렘이 있어야 한다. 사건만 나열하면 드라마지 로맨스가 아니다. ★

[로맨스 narrative 서술 7규칙]
1. 신체 감각과 거리: 감정 대신 몸의 반응. 심장/손끝/시선/호흡.
   ❌ '마음이 설렜다.' ✅ '손이 닿을 뻔했다. 0.5초 먼저 뺐다. 손끝이 화끈거린다.'
2. 감정 지연: 고백을 최대한 늦춰라. 닿을 듯 안 닿는 시간이 길수록 닿는 순간의 힘이 크다.
3. 시선과 침묵 > 대사: 로맨스의 핵심 장면은 대사 없이도 작동한다.
   ✅ '같은 우산 아래. 아무 말 없다. 비가 세지고 어깨가 닿는다. 피하지 않는다.'
4. 작은 관찰 = 사랑의 증거: 큰 선언보다 작은 디테일.
   ✅ '설탕 두 개. 그가 내가 설탕 두 개를 넣는다는 걸 알고 있었다.'
5. 감정 온도 변주: 따뜻함↔차가움 반복. 평탄하면 우정이지 로맨스가 아니다.
6. 닿지 못한 채로 끝: 매 비트 끝에 감정이 해소되지 않아야 다음 비트를 본다.
7. 이별 후 재회: 2막 끝에 가장 아픈 이별, 3막에 이 이야기만의 재회.

[체크] 신체 감각 매 비트 2개 이상 / 직접 고백 자제 / 거리 변화 명시 / 감정 온도 변주
"""
    if _is_action(genre):
        genre_treatment_block += """
[액션 트리트먼트 특화 — ACTION NARRATIVE OVERRIDE]
★ narrative에 액션 씬이 들어갈 때 반드시 Phase 4단계로 설계하라. ★
★ 감정 없는 액션은 스펙터클. 감정 있는 액션만이 한국 관객에게 통한다. ★

[액션 narrative 서술 7규칙]
1. 액션 직전 1분에 '이놈 맞아도 싸다'의 감정 세팅.
   ❌ '악당이 나타났다. 싸운다.'
   ✅ '악당이 형 사진을 짓밟는다. 주인공의 눈빛이 바뀐다. 주먹이 움직인다.'
2. 한 번의 싸움을 Phase 4단계로 쪼개라:
   Phase 1 Spark (트리거) → Phase 2 Escalation (판 커짐) → Phase 3 Low Point (주인공이 진 것처럼) → Phase 4 Turn (승리).
3. 승리의 방식이 캐릭터의 본질을 증명해야 한다. 정의형=정공법 / 꾼=트릭 / 광인=광기.
4. 공간이 액션이다. "목욕탕 액션"이 아니라 "증기 낀 목욕탕, 수건으로 무기 압수, 탕 물로 시야 차단".
   narrative에 공간의 고유 소품·제약이 반드시 드러나야 한다.
5. 3박자 원칙: 한 타격당 3개 구체 — 타격 부위 / 맞는 부위 / 결과(꺾임·튕김·피·쓰러진 물건).
6. 대사 비중 변화: 격투 중 1~3단어, 격투 직전 한 문장(기억에 남는), 격투 후 침묵 또는 한 문장.
7. 액션-감정-액션-감정 리듬. 비트 전체가 액션이면 관객 피곤. 액션 씬 사이에 숨 고르기 씬 필수.

[체크] Phase 4단계 쪼갬 / 공간 디테일 / 감정 세팅 선행 / 리듬 교차]
"""
    if _is_drama(genre):
        genre_treatment_block += """
[드라마 트리트먼트 특화 — DRAMA NARRATIVE OVERRIDE]
★ narrative 줄글이 '그 사람에게 무슨 일이 일어나는가'를 담아야 한다. 사건만 나열하면 스케치다. ★

[드라마 narrative 서술 8규칙]
1. 매 비트에 주인공 내면의 미세한 변화. '평생 피해온 진실을 건드린다' 수준.
2. Want vs Need: Want(의식적 목표)를 쫓다가 Need(인정하지 않던 진실)를 발견하는 여정.
3. 서브텍스트가 텍스트: 인물은 느끼는 것을 직접 말하지 않는다.
   ❌ '나 지금 슬퍼.' ✅ '...커피 식었네.' (슬픔을 컵 속으로 밀어넣음)
   갈등 두 인물이 표면적으로 다른 주제를 이야기하게 하라 (이별이 불 끄기 문제로 위장).
4. 억눌림→균열→폭발 3단. 울게 만들려면 울지 않는 시간을 길게 써라.
   폭발 씬은 작품에 2~3회만. 남발하면 효과 사라진다.
5. 관계 거리 변화를 매 비트에 명시. "이 비트 끝에 두 인물의 거리가 시작과 어떻게 달라졌는가?"
6. 한국적 구체에서 출발: 추상적 감정 금지. '가족의 사랑' → '어머니가 딸이 돌아올 시간에 된장찌개를 데운다'.
7. '무언가를 하면서' 말하라: 설거지하면서 이별, 김장하면서 화해, 이삿짐 옮기며 고백.
8. 완전 해결 엔딩 금지. 한국 드라마의 힘은 '완전 해결하지 않음'에 있다.

[체크] 내면 변화 매 비트 / Want-Need 갭 / 서브텍스트 / 관계 거리 명시 / 한국적 구체
"""
    if _is_thriller(genre):
        genre_treatment_block += """
[스릴러 트리트먼트 특화 — THRILLER NARRATIVE OVERRIDE]
★ narrative의 엔진은 '정보'다. 누가 무엇을 언제 아는가가 모든 비트의 긴장을 결정한다. ★

[스릴러 narrative 서술 8규칙]
1. 정보 비대칭을 매 비트에 설계: Suspense(관객>주인공) / Surprise(동시 발견) / Mystery(조각만).
   히치콕 원칙: '테이블 아래 폭탄'을 관객이 알면 평범한 대화도 긴장된다.
2. Clock은 반드시 있다. 명시적 시계 / 암시적 압박 / 물리적 제약.
   비트가 진행될수록 시간이 줄어들어 씬 호흡도 짧아진다.
3. Escalation: 매 비트가 직전 비트보다 더 나빠져야 한다.
   위협 범위 확대 / 출구 감소 / 시간 압박 증가 / 잃은 것 누적.
4. 빌런이 똑똑해야 스릴러가 똑똑하다. 빌런은 주인공보다 몇 수 앞서 있어야 한다.
   빌런의 실수는 클라이맥스에서만. 그전에는 주인공이 뚫어야 한다.
5. Low Point에서 주인공은 '거울 속 자기를 못 알아보는' 순간을 맞아야 한다 (누아르일 때).
6. 반전은 충격이 아니라 재해석. Plant-Misdirect-Payoff 3단.
   관객이 '다시 보고 싶게' 만드는 반전이 좋은 반전.
7. 공간의 낯설게 하기: 익숙한 공간(아파트/지하철/시장)을 이상하게 만드는 기술이 한국 스릴러의 강점.
8. 대사는 건조하고 정보가 많다. 빌런의 협박은 차분해야 무섭다. '...그 서류는 어디 있습니까?'(커피 따르며)

[체크] 정보 비대칭 매 비트 명시 / Clock 작동 / Escalation 그래프 / 빌런 우위
"""
    if _is_sf(genre):
        genre_treatment_block += """
[SF 트리트먼트 특화 — SF NARRATIVE OVERRIDE]
★ SF의 핵심은 '세계의 규칙'이다. 그 규칙이 인간 문제의 은유로 작동한다. ★

[SF narrative 서술 7규칙]
1. 핵심 규칙 1개를 한 줄로 요약 가능해야 한다. 매 비트에서 그 규칙이 어떻게 작동하는지 보여라.
   작동하지 않는 비트는 SF가 아니라 일반 드라마 — 넣거나 빼거나.
2. Show Don't Tell: 설명 대사 금지. 인물이 규칙을 사용하는 모습으로 공개.
   강의식 오프닝 절대 금지: '아시다시피 2049년 지구는...'
3. 일상화된 기술: 인물들은 이 세계에 익숙하다. 놀라지 않는다. 관객이 놀라는 것은 인물이 놀라지 않기 때문.
4. 규칙의 대가(Cost) 매번 명시: 신체적(두통·구토) / 관계적(연인이 자기를 모름) / 윤리적 / 사회적.
   대가 없이 해결하면 데우스 엑스 마키나.
5. 규칙의 일관성: 중간에 새 규칙을 만들어 위기를 해결하지 마라. 새 규칙은 1막에서 plant해야.
6. Human Anchor: 경이의 옆에 '평범한 감정을 가진 인간'을 두라. 주인공은 이 세계의 규칙 때문에 다치는 사람.
7. 비주얼 경이 3층위: 큰 그림(도시 실루엣) + 중간(인파·사물 움직임) + 미세(손잡이·표지판·질감).

[체크] 핵심 규칙 매 비트 작동 / 대가 명시 / 설명 대사 없음 / Human Anchor
"""
    if _is_fantasy(genre):
        genre_treatment_block += """
[판타지 트리트먼트 특화 — FANTASY NARRATIVE OVERRIDE]
★ 판타지의 엔진은 '마법의 규칙'이다. 마법이 아니라 '마법의 대가'가 드라마를 만든다. ★

[판타지 narrative 서술 7규칙]
1. 마법 규칙 4요소 명시: 누가 쓸 수 있는가 / 어떻게 쓰는가 / 가능·불가능 / 대가.
   제한이 드라마를 만든다. 만능 마법은 긴장을 죽인다.
2. 공짜 마법 절대 금지: 주인공이 마법을 쓸 때마다 '무엇을 잃는가'를 명시.
   클라이맥스에서 가장 큰 대가를 치르고 이긴다.
3. 작은 세계를 깊게: 대서사시적 세계관 금지. 한 도시/마을/가문 안을 치밀하게.
   세계관 설명은 인물의 일상으로 풀어라. 역사책 내레이션 금지.
4. 한국 판타지는 '감정·관계·한(恨)'의 판타지: 마법은 감정의 증폭기.
   〈도깨비〉사랑과 시간 / 〈호텔 델루나〉미련과 용서 / 〈구미호뎐〉오래된 약속과 환생.
5. 시공간 혼합: 현대 + 고전 / 일상 공간 옆에 초자연 공간 (단골 카페 뒷문이 저승).
6. 플롯 엔진 = 규칙이 만드는 딜레마: '사랑하면 사라진다' → 사랑을 억누를까, 사라질까.
   해결은 '규칙 어겨서'가 아니라 '규칙 안에서 새로운 해석'으로.
7. 약속과 저주는 짧고 강하게: '반드시 돌아오겠다.' '너는 기억할 수 없을 것이다.'

[체크] 마법 4요소 정의 / 대가 매번 명시 / 작은 세계 깊이 / 감정 증폭 구조
"""
    
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

{LOCKED_SYSTEM_RULES}

★ LOCKED 블록의 모든 항목을 트리트먼트에 반영하라. ★
★ 캐릭터 소속/직책/나이/관계가 LOCKED와 1건이라도 다르면 LOCKED 원본으로 되돌려라. ★
★ 기획의도 키워드가 LOCKED에 있으면, 트리트먼트의 대사/행동/배경 묘사에 구체적으로 반영하라.
   추상적 테마로 대체하지 말고, 구체적 장면 디테일로 구현하라. ★
★ 역사적 사건 도입부가 LOCKED에 지정된 경우, 해당 에피소드 시작 비트에 반드시 포함하라. ★

{bjnd_four_axis}

{genre_fun_check}

{pov_politics}

{antagonist_bjnd}

[★ v2.3.6 — 장르 체크리스트 매 비트 실시간 체크 ★]
위 GENRE FUN ALIVE의 해당 장르 체크리스트를 매 비트 작성 전/작성 후 반드시 확인하라.
특히 다음 비트에는 엄격 적용:
  · 2막 후반 비트(Beat 9~11): 장르 중간 지점 약속 충족 여부
  · 3막 비트(Beat 12~16): 클라이맥스가 장르 기대에 맞는지 (CLIMAX_FAIL 방지)
  
호러 장르 Treatment 특별 지시 (바타비아 결함 대응):
  · 2막 후반에 물리적 공포 장면 최소 2개 이상 배치 (추리/대화만으로 2막 마감 금지)
  · 유령·영혼·초자연 존재의 인식·행동 범위를 비트마다 명확히 (논리 비약 금지)
  · 위협 요소(제물 요구, 저주 조건 등)는 1회성이 아니라 비트별로 반복 등장하며 긴장 누적

로맨틱 코미디 Treatment 특별 지시:
  · 2막 Fun and Games 시퀀스 3개 이상을 '사랑 관계의 어긋남'으로 구성
  · 클라이맥스 씬이 '로맨스 완성 순간'인지 확인 (부녀 화해/가족 서사/사회 성공으로 대체 금지)
  · 웃음 포인트 + 설렘 포인트 각각 5회 이상 비트 전체 분산

[★ v2.3.7 — 시대 고증 절대 준수 ★]
Core Build의 world_build.time 필드를 확인하고, 그 시대에 실존하지 않던 요소를
Treatment에 포함하지 마라. 이것은 세계관 논리 검증의 일부이자 독립 체크 항목.

시대별 주요 금지 요소 (참고 기준):
  ■ 1980년대 이전: 스마트폰, 인터넷, 이메일, SNS, AI, 카카오톡 — 모두 없음
  ■ 1990년대 초: 이메일·인터넷은 있지만 대중화 전 (소수 얼리 어답터만)
  ■ 1990년대 후반: PC 통신(하이텔/천리안), 삐삐, 벽돌폰 시작
  ■ 2000년대 초: 2G 피처폰, 싸이월드 시대 (카카오톡·인스타그램 없음)
  ■ 2007년 이전: 아이폰 없음
  ■ 2010년 이전: 카카오톡 없음, 인스타그램 없음
  ■ 2022년 이전: ChatGPT 없음, 상용 AI 생성 도구 매우 제한적

역사 배경(조선/고려/일제강점기/근대):
  · 해당 시대에 없던 기술·제도·언어·개념 등장 금지
  · 예: 조선시대 배경인데 '사진' '카메라' '기차' '전화' 등은 도입 시점 확인 필수

미래 SF 배경:
  · 제시된 미래 시점의 기술 수준을 일관되게 유지
  · 세계관 규칙 내에서 기술이 역행하지 않도록

자가 체크 (매 비트 작성 후):
□ 이 비트에 등장하는 모든 소품/기술/제도/문화가 작품 시대(world_build.time)에 존재했는가?
□ 캐릭터가 사용하는 통신 수단이 시대와 맞는가? (편지/공중전화/삐삐/휴대폰/스마트폰)
□ 대사에 미래 유행어·신조어가 섞이지 않았는가?

[BLUE JEANS 서사동력 — 트리트먼트 적용 (BJND v1.0)]
- Core Build의 narrative_drive에서 주인공의 발생요인(상실/결핍)을 확인하라.
- 상실(loss) 기반이면: 잃어버린 것을 향한 집착·분노·슬픔이 매 비트의 선택을 지배한다.
  비트가 진행될수록 "되찾을 수 없음"의 인식이 깊어져야 한다.
- 결핍(lack) 기반이면: 갈망·열등감·증명 욕구가 매 비트의 선택을 지배한다.
  비트가 진행될수록 "획득해도 채워지지 않음"의 인식이 깊어져야 한다.
- 클라이맥스에서 주인공의 최종 선택은 Goal(외적)과 Need(내적) 사이의 간극을 해소하는 것이어야 한다.

[★ BJND Strategy/Cost 씬 레벨 집행 — v2.3 ★]
Core Build에서 설계한 Strategy는 매 비트 씬에서 '구체적 행동'으로 드러나야 한다.
Core Build에서 설계한 Cost 3축(관계/자기/세계)은 막별로 누적되어야 한다.

막별 Cost 누적 단계 (절대 준수):
  ■ 1막 (Beat 1~4): Cost는 '암시'만. 주변이 감지하되 주인공은 자각 못 함.
  ■ 2막 전반 (Beat 5~8): Cost가 '작은 균열'로 드러남. 주인공 당황하지만 Strategy 고집.
  ■ 2막 후반 (Beat 9~11): Cost가 '실재 손상'으로 누적. 누군가를 실제로 다치게 하거나 잃음.
  ■ 3막 (Beat 12~16): Cost가 더 이상 부정할 수 없는 현실. 
    Strategy_1의 완전한 붕괴 → Strategy_2의 첫 실행 → Strategy_2의 확정.

★ 3막 엔딩 규칙 — Strategy 전환은 내적 전환이어야 한다 ★
Core Build의 ending_payoff가 '내적 깨달음'이라면 엔딩을 '외적 선택'으로 단순화하지 마라.
  - 예: ending_payoff가 '고를 수 없음 자체가 사랑임을 깨달음'이면 → 
    엔딩은 반드시 '고를 수 없음을 선언하는 씬'이어야 한다.
    '한 명 선택'으로 마무리하면 BJND 배반이다. 금지.
  - 예: ending_payoff가 '복수 포기하고 새 삶을 선택'이면 →
    엔딩은 반드시 '복수 기회 앞에서 돌아서는 씬'이어야 한다.
    '빌런을 처단하고 정의 실현'으로 마무리하면 BJND 배반이다. 금지.

매 비트 작성 시 자가 체크:
□ 이 비트에서 주인공의 Strategy가 어떤 행동으로 드러나는가?
□ 이 비트가 배치된 막(1막/2막전반/2막후반/3막)의 Cost 누적 단계와 맞는가?
□ 이 비트 끝에서 주인공은 자기 Strategy에 대해 어떤 감각을 갖는가?
  (자신감/균열/의심/붕괴/전환 중 어느 단계인가)
□ 3막 마지막 비트라면 — ending_payoff를 외적 선택이 아닌 내적 전환으로 구현했는가?

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
□ ★ LOCKED 블록의 캐릭터/설정/기획의도가 모두 준수되고 있는가? ★

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
❌ ★ LOCKED 블록의 캐릭터 소속을 변경하는 것 ★
❌ ★ LOCKED 블록의 기획의도를 추상적 테마로 대체하는 것 ★

[비트 간 중복 금지 — 가장 흔한 실패]
★ 이전 비트에서 이미 한 행동을 다음 비트에서 반복하면 안 된다. ★
특히 Beat 12~14 구간에서 자주 발생하는 실수:
- Beat 12(All Is Lost)에서 이미 증거를 모으고 역공을 결정하면 → Beat 14(클라이맥스)에서 같은 것을 반복하게 된다.
- 올바른 구조:
  Beat 12 = 무너짐. 주인공이 모든 것을 잃고 패배를 인식한다. 아직 반격하지 않는다.
  Beat 13 = 빌런의 승리. 빌런이 최고조에 이르고 주인공은 바닥에 있다.
  Beat 14 = 역전. 주인공이 일어서서 새로운 방식으로 반격한다. 12에서 잃은 것이 무기가 된다.
- 매 비트를 쓴 뒤 자문하라: "이 비트의 핵심 행동이 다른 비트에서 이미 일어났는가?"
  → Yes이면 이 비트의 핵심 행동을 바꿔라.

[작성 규칙]
1. 서술체, 현재형. 대사는 작은따옴표만.
2. 각 씬 전환은 줄바꿈 없이 서술 안에서 자연스럽게 '장소. 시간.' 형식으로 전환.
3. 인물 첫 등장 시 이름(나이).
4. 매 비트 {min_chars}~{max_chars}자.
5. PUNCH: 매 비트 안에 최소 1개.

{series_block}

{b_story_block}

{genre_treatment_block}

{fact_block}
{historical_block}

{opening_treatment_block}

{creator_sensibility}

[관객 심리]
6. Dramatic Irony: 관객에게 먼저 정보를 줘라.
7. Information Gap: 매 비트 최소 1개 열린 질문 유지.
8. Delayed Gratification: 관객이 원하는 장면을 늦춰라.

[비트 구조 변주 — 2막 반복 패턴 방지]
비트의 내부 구조가 직전 비트와 같으면 안 된다.
6가지 비트 구조 유형 중 이 비트에 가장 맞는 것을 택하되, 직전 비트와 반드시 다른 유형을 써라.
  [INV] 조사/발견형 — 단서 수집, 정보 조각, 진실에 접근
  [CON] 대결/충돌형 — 직접 대면, 언쟁, 갈등 폭발
  [REV] 반전/배신형 — 예상 뒤집기, 동맹 붕괴, 새로운 진실
  [EMO] 감정/관계형 — 감정 씬 중심, 관계 변화, 고백, 결별
  [ACT] 행동/추격형 — 물리적 행동, 시간 압박, 도주, 구출
  [SIL] 정적/결심형 — 침묵, 내면, 결심의 순간, 폭풍 전 고요
❌ Beat 6[INV]→7[INV]→8[INV]→9[INV] = 매 비트 '조사→단서→대화' 반복
✅ Beat 6[INV]→7[CON]→8[REV]→9[EMO]→10[ACT]→11[SIL] = 매 비트 다른 리듬
★ 특히 2막(Beat 6~12)에서 같은 유형이 2회 연속이면 무조건 변경하라. ★

[AI 안티패턴 — narrative에서 절대 금지 (A1~A10)]

[A1. 감정 설명 서술 금지]
❌ '불안한 마음으로' '두려움이 온몸을' → 카메라에 안 보인다.
✅ '손잡이를 잡았다 놓았다. 손등에 땀.' → 행동으로 보여준다.

[A2. 방금 서술한 것을 대사로 반복 금지]
관객은 이미 읽었다. 반응을 보여줘라.
❌ (서술: 재중이 USB를 발견한다) 재중: '이게 USB네. 아버지의 USB.'
✅ (서술: 재중이 USB를 발견한다) 재중이 USB를 집는다. 손이 멈춘다. 최이호를 본다.

[A3. 총칭적 감각 금지]
❌ '바람이 불었다' '어둠이 깔렸다' — 아무 작품에나 들어간다.
✅ '커튼이 빨려 들어간다. 목덜미에 소름.' — 이 작품에만 있다.

[A4. 같은 씬에서 긴장 생성+해소 금지]
긴장을 비트 경계 너머로 끌고 가라. 같은 비트에서 위기가 생기고 같은 비트에서 풀리면 관성이 끊긴다.

[A5. 편의적 정보 전달 대사 금지 (Writer Engine A5 역주입)]
두 사람이 다 아는 것을 서로에게 설명하면 안 된다.
❌ '네가 알다시피, 이 저수지는 20년 전에 마을을 수몰시켜서 만든 거야.'
   → 상대도 이미 아는 정보. AI가 관객을 위해 쓰는 편의적 대사.
✅ '할머니가 그러셨어. 물 밑에 아직 집들이 있대.' → 제3자의 말을 빌려 자연스럽게.
   → 정보가 필요하면 '들었다' '봤다' '읽었다'의 형식으로, 또는 상대는 모르고 나만 아는 것을.

[A6. 침묵이 없는 서술 금지 (Writer Engine A6 역주입)]
비트 전체가 대사 → 대사 → 대사로만 채워지면 안 된다.
- 비트 narrative 안에 '대사 없이 3~5줄 행동만'이 최소 1구간 있어야 한다.
- 대사 없는 30초가 대사 10줄보다 강할 때가 있다. 침묵을 두려워하지 마라.
- 특히 호러/스릴러/드라마 비트: 침묵 구간이 긴장의 엔진.
- Scene Design의 is_setpiece가 Y인 씬에는 침묵 구간 1개 이상 설계.

[A7. 관찰자 없는 숫자 금지 (Writer Engine A12 역주입)]
AI가 숫자를 그냥 지문에 박아 넣는 습관. 관객이 이 숫자를 어디서 보는가를 명시하라.
❌ '소율의 팔로워 321,047명. 체크카드 잔액 3,200원. 이력서 1,234번 탈락.'
   → 관객이 어디서 보는가? 그냥 지문에 나열하면 안 된다.
✅ '소율의 폰 화면, 인스타그램. 팔로워 321,047. / ATM 화면, 출금 실패. 잔액 3,200원.
   / 고시원 벽에 붙은 이력서 인쇄물, 삼각형 도장 13줄. 마지막 줄 끝, 숫자 1234.'
   → 숫자는 반드시 '보여지는 곳'이 있어야 한다. narrative = 카메라의 눈.

[A8. 원인 없는 결과 금지 (Writer Engine A13 역주입)]
AI는 A가 일어나면 곧바로 B가 일어났다고 쓴다. 하지만 그 사이의 연결 고리가 보여야 한다.
❌ '소율이 라운지에 들어선다. 팔로워가 32만이 된다.'
   → 들어서는 것과 팔로워 증가가 어떻게 연결되는가?
✅ '소율이 라운지에 들어선다. 테이블 위 시식 마카롱을 들고 셀카. 업로드.
   몇 초 후, 폰 화면. 팔로워 321,050 → 321,090 → 321,150.'
   → A→B 사이의 행동/반응 고리가 반드시 보여야 한다.
- 특히 대사/감정 전환: '분노했다 → 화해했다' 사이에 무엇이 있었는가를 쓰지 않으면 실패.

[A9. 동작·정보 반복 루프 금지 (Writer Engine A15+A16 역주입)]
AI가 강박·집착·중요성을 표현하려고 같은 행동/숫자/물체를 4번 이상 반복하는 습관.
2~3번까지는 리듬, 4번부터는 분량 낭비.

❌ 루프 패턴:
'재중이 USB를 꺼낸다. 넣는다. 두 걸음. 또 꺼낸다. 넣는다. 한 걸음. 또 꺼낸다.'
→ 꺼내고 넣기 3~4회 반복. 독자가 '그만 해'라고 느낌.

✅ 2회로 압축 (Rule of Two):
'재중이 USB를 꺼낸다. 넣는다. 두 걸음 걷고 다시 꺼낸다. 그대로다. 주머니에 넣고 양손을 봉투 위에 올린다.'
→ 2번이면 충분. 세 번째는 반드시 다른 행동으로 변주.

❌ 정보 반복: '팔로워 321,047. (몇 줄 뒤) 팔로워 321,047. 같다. (몇 줄 뒤) 321,047.'
✅ 한 번만, 변주로: '소율이 폰을 본다. 321,047. 엘리베이터 기다리며 한 번 더. 같다.'
원칙: 같은 행동·숫자·물체의 반복은 최대 2회. 3번째는 반드시 변주 또는 다른 행동으로 전환.

[A10. 캐릭터 재소개 금지 (Writer Engine A14 역주입)]
이미 등장한 캐릭터는 이름만 써라. 비트가 새로 시작한다고 인물을 다시 소개하지 마라.

❌ 비트 5: 재중(28)이 폰을 든다. ← 최초 등장 시
   비트 8: 재중(28)이 다시 전화한다. ← 또 (28) 표시
   비트 11: 재중(28)이 최이호를 본다. ← 또또 (28) 표시
→ AI가 비트마다 인물을 재소개하는 습관. 관객은 이미 재중이 누군지 안다.

✅ 비트 5: 재중(28)이 폰을 든다. ← 최초 등장 시에만 나이/직업
   비트 8: 재중이 다시 전화한다. ← 이름만
   비트 11: 재중이 최이호를 본다. ← 이름만
→ 첫 등장에만 나이/직업/소개 표기. 이후는 이름만.

- 이 규칙은 Writer Engine으로 넘길 비트 줄글 품질을 결정한다. Treatment 단계에서
  이미 재소개 패턴이 굳어지면 Writer Engine도 그 습관을 이어받는다.

[기능적 조연 — 세계를 살리는 인물들]
주요 캐릭터(4~8명)만으로 모든 비트를 채우면 세계가 비어 보인다.
기능적 조연 = 바이블이 필요 없는 1~3비트 등장 인물. 이름과 역할만 있으면 된다.
- 정보 제공자: 주인공이 모르는 것을 알려주는 사람 (동네 주민, 오래된 직원, 택시 기사)
- 세계 넓히기: 주인공 밖의 세계가 존재함을 보여주는 사람 (카페 직원, 행인, 이웃)
- 거울 역할: 주인공의 선택을 다른 관점에서 비추는 사람
- 희생자/목격자: 사건의 대가를 보여주는 사람
- 장애물: 주인공의 행동을 방해하는 사람 (경비원, 관료)
- 유머/이완: 긴장 씬 사이 숨을 쉬게 해주는 사람
규칙: 1막에서 최소 2명, 2막에서 최소 3명의 기능적 조연을 배치하라.
기능적 조연은 이름(성+직함 또는 별명) + 나이 + 한 줄 역할만 표기.
★ 주요 캐릭터만으로 모든 씬을 채우면 세계가 비어 보인다. 조연이 세계를 살린다. ★

[서사동력 비트별 체크 — Narrative Drive]
매 비트에서 아래를 확인하라:
- Goal(외적 욕망)을 향한 전진이 있는가? (주인공은 Goal을 계속 쫓는다)
- 동시에 Need(내적 필요)와는 멀어지고 있는가? (1~2막에서는 멀어져야 긴장)
- 미드포인트 이후: Goal 추구가 좌절되면서 Need를 인식하기 시작하는가?
- 클라이맥스: Goal을 포기하고 Need를 선택하는가, 또는 Goal과 Need가 합치되는가?
※ 서사동력(상실/결핍)에 따라 감정 방향이 달라진다:
  상실(Loss): 되찾으려는 시도 → 되찾을 수 없음 → 수용/파멸
  결핍(Lack): 쟁취하려는 시도 → 대가 인식 → 진짜 필요한 것 발견

{SORKIN_CURTIS["unified_plot_test"]}

{SORKIN_CURTIS["too_wet"]}

{SORKIN_CURTIS["emotion_chain"]}

[장르 규칙: {genre}]
{genre_rules_text}

{JSON_OUTPUT_RULES}"""


def build_system_tone_document(genre: str, fmt: str,
                                fact_based: bool = False, historical: bool = False, film_type: str = "") -> str:
    """Tone Document 시스템 프롬프트 — Curtis 3% 법칙 + 감정 연쇄 + LOCKED + FACT/HISTORICAL"""
    fact_block = get_fact_based_rules(fact_based)
    historical_block = get_historical_film_rules(historical, film_type)
    return f"""당신은 헐리우드 최고 수준의 톤 디자이너(Tone Designer)이자 비주얼 스토리텔러다.
기획개발 패키지를 기반으로, Writer Engine이 시나리오를 쓸 때 참조할 '톤 & 연출 문서'를 작성한다.

{LOCKED_SYSTEM_RULES}

[목표]
이 문서가 있으면 AI가 80~120씬 동안 일관된 톤·분위기·연출 스타일을 유지할 수 있다.

[장르: {genre} / 포맷: {fmt}]

{SORKIN_CURTIS["curtis_3pct"]}

{SORKIN_CURTIS["emotion_chain"]}

{fact_block}
{historical_block}

{JSON_OUTPUT_RULES}"""


# ═══════════════════════════════════════════════════
# JSON SCHEMAS
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

# ─── Treatment Beat 스키마 (v1.5: 5단계 서술 구조 + LOCKED 검증 + 에피소드 태그) ───
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
            "open_question": "열리는 새 질문 1문장",
            "villain_beat": "이 비트에서 적대자가 한 구체적 행동 + 승/패 (빌런이 이겼는가?) — 적대자가 없는 비트면 빈 문자열",
            "plant_payoff": "이 비트에서 심는 것(plant) 또는 회수하는 것(payoff) 1문장. 없으면 빈 문자열",
            "locked_check": "LOCKED 항목 준수 여부 — 'OK' 또는 위반 항목 명시"
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
- villain_beat: 적대자가 이 비트에서 구체적으로 무엇을 했는가 + 승/패. 직접 등장 안 해도 영향 느껴야 함.
  ★ 클라이맥스 전까지 적대자가 계속 이기고 있어야 한다. 빌런이 매번 실패하면 긴장감 사라진다. ★
- plant_payoff: 1막 비트에서 심은 것(plant)이 3막 비트에서 회수(payoff)되어야 한다.
  Core Build의 planting_payoff 설계를 참고하라. 회수 없는 plant는 관객의 불만족을 만든다. Plant 없는 payoff는 데우스 엑스 마키나다.
- Too Wet 금지: 감정 직접 서술 금지. 행동으로.
- 1분짜리 장면 하나를 상세히 묘사해서 분량을 채우지 마라. 비트는 7~20분의 스크린타임을 커버한다.
- ★ locked_check: 매 비트 작성 후 LOCKED 항목 준수 여부를 확인하라. 위반 시 수정. ★
- ★ 비트 간 중복 금지: 이전 비트에서 한 핵심 행동(증거 수집, 결정, 대결 등)을 다음 비트에서 반복하면 실패. 특히 Beat 12(무너짐)와 Beat 14(역전)는 반드시 다른 행동이어야 한다. ★"""


# ─── Scene Design 스키마 (v1.5: hook/punch/setpiece + LOCKED 태그) ───
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
            "plant_payoff_tag": "plant(심기) / payoff(회수) / 빈 문자열 — plant이면 무엇을 심는지, payoff이면 무엇을 회수하는지 1문장",
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
- 서브플롯이 메인플롯의 테마를 다른 각도에서 비춰야 한다. 테마와 무관한 서브플롯은 삭제
- plant_payoff_tag: Core Build의 planting_payoff 설계를 참고하여, 이 장면이 plant(심기)인지 payoff(회수)인지 태그. 최소 3개 plant + 최소 3개 payoff가 전체 장면에 분포해야 한다. plant는 1막에 집중, payoff는 2막 후반~3막에 집중.
- ★ LOCKED 블록의 캐릭터 소속과 관계를 장면 설계에서도 준수하라. ★"""

# ─── 보조 함수 시스템 프롬프트 ───
SYSTEM_STRUCTURE_PROSE = "당신은 숙련된 시나리오 작가다. 유효한 단일 JSON만 출력. 후행 쉼표 금지."
SYSTEM_TREATMENT_META = "당신은 Development Producer다. 유효한 단일 JSON만 출력. 후행 쉼표 금지."
SYSTEM_TREATMENT_GATE = """당신은 Development Producer이자 Script Doctor다.
제공된 Treatment를 Core Build 설계와 대조하여 엄격 검증한다.

[v2.3.7 검증 기준 — 엄격 적용]

1. cinematic_reading (영화적 가독성): narrative가 장면으로 떠오르는가
2. scene_emotion_match (씬-감정 정합): 각 비트의 감정 흐름이 서사와 맞는가
3. beat_completeness (비트 완성도): 각 비트가 SCOPE MANDATE 충족하는가 (3~5개 씬)
4. screenplay_ready (시나리오 전환 가능성): Writer Engine이 바로 받아 쓸 수 있는가

[v2.3.6 신규 검증 3축]

5. genre_expectation_alignment (장르 기대 정합 — 가장 중요):
   - 호러: 2막 후반에 물리적 공포 장면이 실제 등장하는가? 추리·대화만으로 채워졌다면 감점.
   - 로맨틱 코미디: 클라이맥스가 로맨스 완성 순간인가? 부녀 화해/가족 서사로 대체되었다면 감점.
   - 스릴러: 정보 비대칭이 2막 전반에 설계되었는가? 타이머가 작동하는가?
   - 액션: Setpiece 액션 시퀀스가 실제로 비트 안에 배치되었는가?
   - 각 장르의 체크리스트를 실제 narrative 내용으로 확인하라. 장르 약속 배반은 심각 감점.

6. ending_coherence (엔딩 정합):
   - Core Build의 Ending Payoff가 Treatment 3막 마지막 비트에 구체 씬으로 구현되었는가?
   - Ending Payoff가 '내적 전환'이면 엔딩 씬도 '내적 전환'이어야 한다.
     ('외적 선택'으로 단순화되었으면 감점)
   - 엔딩 이미지가 Ending Payoff를 배반하거나 애매하게 만들면 감점.
     (예: '해방' Payoff인데 엔딩 이미지가 '아직 구속된 상태' 암시 → 배반)

7. logic_consistency (논리·세계관 일관성):
   - 세계관 규칙 내에서 불가능한 사건이 발생하는가? (예: 1874년 유령이 150년 후 브랜드 로고 읽기)
   - 캐릭터가 이유 없이 원래 설정과 다르게 행동하는가?
   - 긴장 요소가 등장 후 사라지는가? (예: 제물 요구 같은 핵심 위협이 1회로 끝남)
   - 구체 비트 번호와 함께 critical_issues에 기록.

[v2.3.7 신규 검증 1축]

8. period_consistency (시대 고증 — 치명적 검증):
   - Core Build의 world_build.time 필드 확인: 작품 시대가 언제인가?
   - 그 시대에 존재하지 않는 요소가 Treatment에 포함되면 치명적 감점.
   
   시대별 주요 금지 요소 참고:
   ■ 1960년대 이전: 컬러 TV 흔치 않음, 유선전화만, PC 없음
   ■ 1970년대: 워크맨 이전, 비디오테이프 초기
   ■ 1980년대: 스마트폰 없음, 인터넷 없음, 컴퓨터는 기업용, AI/로봇 상용 없음,
               카드 결제 드물게, 무선호출기(삐삐)는 1990년대 후반
   ■ 1990년대 초: 이메일·인터넷 대중화 전, 휴대폰 소수 (벽돌폰)
   ■ 1990년대 후반: PC 통신(하이텔/천리안) 전성기, 삐삐 대중화, 휴대폰 확산 시작
   ■ 2000년대 초: 스마트폰 없음, SNS 없음, 2G 피처폰, 카카오톡 없음
   ■ 2007년 이전: 아이폰 없음
   ■ 2010년 이전: 카카오톡 없음, 인스타그램 없음, 유튜브 초기
   ■ 2020년대 이전: AI 생성 도구 상용화 전 (ChatGPT는 2022년 11월)
   
   역사 배경(조선/고려/일제강점기 등)인 경우:
   - 해당 시대의 복식·언어·제도·기술 고증 오류 감점
   - 예: 조선시대 배경인데 '스마트폰' '사진' '미국 영화 이야기' 등 등장
   
   미래 SF 배경인 경우:
   - 제시된 미래 시점에 맞지 않는 과거 기술 등장 점검
   - 세계관 규칙 내 기술 수준 일관성 점검
   
   critical_issues에 구체 기록: "Beat 7: 1985년 배경인데 주인공이 카카오톡 메시지 확인 — 시대 고증 오류"

[채점 원칙]
- 각 항목 0.0 ~ 10.0, 소수점 1자리.
- average = 8항목 평균 (v2.3.7: 시대 고증 축 추가로 7→8).
- genre_expectation_alignment, ending_coherence, logic_consistency, period_consistency 중
  하나라도 6.0 미만이면 feedback에 "재생성 권고"를 명시.
- period_consistency가 4.0 미만이면 "시대 고증 치명적 오류 — 전면 재작성 권고" 별도 명시.
- critical_issues 배열에 문제 비트를 구체 기록. "Beat 10: 엘시가 브랜드 로고 인식 — 세계관 범위 비약" 형식.

[출력 규칙]
유효한 단일 JSON만 출력. 후행 쉼표 금지. 주석 금지."""
