# 👖 BLUE JEANS Creative Development Engine

> 아이디어 → 기획개발 패키지 · Creative Development SaaS

---

## 시작하기

### 1. 저장소 클론 / 파일 배치
```bash
bjcde/
├── main.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
└── README.md
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

### 4. 실행
```bash
streamlit run main.py
```

---

## Streamlit Cloud 배포

1. GitHub 저장소에 push
2. Streamlit Cloud에서 저장소 연결
3. **Secrets** 탭에 `ANTHROPIC_API_KEY` 등록
4. Deploy

---

## 사용 흐름

```
1. 아이디어 입력 (자유 텍스트 + 장르 + 타겟 시장 + 포맷)
      ↓
2. [선택] 🔍 리서치 — 실화/뉴스 + 기존 작품 검색
      ↓
3. 🧠 Brainstorm — 컨셉 카드 10~15개 생성
      ↓
4. Gate A 자동 채점 → 통과 시 Core Build로
```

---

## 기술 스택

| 항목 | 스펙 |
|------|------|
| 프레임워크 | Streamlit |
| AI 엔진 | Claude Sonnet (Anthropic API) |
| 테마 | 다크 모드 + Stitch Yellow (#FFCB05) |

---

© 2026 BLUE JEANS PICTURES. All rights reserved.
