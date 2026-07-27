# 📰 AI News Curator

> 멀티 에이전트 기반 AI 뉴스 큐레이션 시스템

AI News Curator는 최신 뉴스를 수집하고, 사용자의 관심사에 맞게 분석 및 요약하여 하나의 뉴스레터 형태로 제공하는 AI 기반 뉴스 큐레이션 시스템입니다.

LLM과 Multi-Agent 구조를 활용하여 뉴스 검색부터 요약, 편집, 최종 뉴스레터 생성까지의 과정을 자동화하였습니다.

---

## 📌 프로젝트 소개

기존 뉴스 서비스는 단순한 기사 제공에 집중되어 있어 사용자가 원하는 정보를 선별하기 어렵다는 문제가 있습니다.

본 프로젝트는 여러 AI Agent가 각각의 역할을 수행하여

- 최신 뉴스 검색
- 뉴스 분석 및 요약
- 중요도 평가
- 뉴스레터 생성

과정을 자동으로 수행하는 AI 뉴스 큐레이션 시스템을 구현하였습니다.

---

## ✨ 주요 기능

### 🔍 뉴스 검색

- 키워드 기반 최신 뉴스 검색
- 다양한 뉴스 기사 수집

### 🤖 AI 뉴스 큐레이션

- 기사 내용 분석
- 핵심 내용 요약
- 중요 뉴스 선별

### 📝 뉴스레터 생성

- 여러 기사를 하나의 뉴스레터로 통합
- 읽기 쉬운 형식으로 재구성

### 👨‍💻 멀티 에이전트 기반 처리

각 Agent가 독립적인 역할을 수행하여 작업을 분담합니다.

- Search Agent
- Curator Agent
- Editor Agent
- Master Agent

---

# 🏗 시스템 구조

```
                  User
                    │
                    ▼
             Master Agent
                    │
      ┌─────────────┼─────────────┐
      │             │             │
      ▼             ▼             ▼
 Search Agent  Curator Agent  Editor Agent
      │             │             │
      └─────────────┼─────────────┘
                    │
                    ▼
           Newsletter Generator
                    │
                    ▼
              Streamlit UI
```

---

# ⚙ 기술 스택

| 구분 | 기술 |
|------|------|
| Language | Python |
| LLM | OpenAI GPT |
| Framework | Streamlit |
| Agent | LangChain |
| Workflow | LangGraph |
| Retrieval | RAG |
| Evaluation | LangSmith / Evaluation Module |

---

# 📂 프로젝트 구조

```
ai-news-curator/

├── agents/
│   ├── master_agent.py
│   ├── search_agent.py
│   ├── curator_agent.py
│   └── editor_agent.py
│
├── evaluation/
│
├── prompts/
│
├── utils/
│
├── app.py
├── requirements.txt
└── README.md
```

(프로젝트 구조는 일부 생략되었습니다.)

---

# 🔄 시스템 동작 과정

1. 사용자가 키워드를 입력합니다.

2. Search Agent가 관련 뉴스를 검색합니다.

3. Curator Agent가 뉴스를 분석하고 요약합니다.

4. Editor Agent가 뉴스레터 형식으로 편집합니다.

5. Master Agent가 전체 결과를 통합합니다.

6. 최종 뉴스레터를 사용자에게 제공합니다.

---

# 🚀 실행 방법

## 1. 프로젝트 다운로드

```bash
git clone <repository-url>

cd ai-news-curator
```

## 2. 라이브러리 설치

```bash
pip install -r requirements.txt
```

## 3. 환경 변수 설정

`.env`

```env
OPENAI_API_KEY=YOUR_API_KEY
```

필요한 API Key를 설정합니다.

---

## 4. 실행

```bash
streamlit run app.py
```

브라우저에서 실행된 Streamlit 페이지를 통해 서비스를 사용할 수 있습니다.

---

# 📊 프로젝트 특징

- Multi-Agent 구조 적용
- 뉴스 자동 요약
- 뉴스레터 자동 생성
- RAG 기반 정보 활용
- Streamlit 기반 UI
- LLM 기반 자연어 처리

---

# 📈 기대 효과

- 뉴스 탐색 시간 단축
- 사용자 맞춤형 정보 제공
- 뉴스 소비 효율 향상
- AI 기반 자동 뉴스레터 생성

---

# 🔧 향후 개선 사항

- 개인 맞춤형 뉴스 추천 기능
- 관심 분야 학습 기능
- 뉴스 중요도 자동 평가 개선
- 다양한 뉴스 API 연동
- 이메일 뉴스레터 자동 발송 기능

---

# 📚 개발 환경

| 항목 | 내용 |
|------|------|
| Python | 3.x |
| Streamlit | 최신 버전 |
| OpenAI API | GPT |
| LangChain | 최신 버전 |
| LangGraph | 최신 버전 |

---
- 홍승범
- 차승언
