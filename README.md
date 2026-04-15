# 🚀 사내 개발자 가이드 (Dev Guides)

> **"개발은 Windows(WSL)에서, 배포는 Docker(Linux)로"** — 클라우드 네이티브 시대의 사내 개발 표준 가이드입니다.

Python 기초부터 컨테이너 기반 개발까지, 실무에 바로 적용할 수 있는 7개의 강의로 구성되어 있습니다.  
각 강의는 **개념 설명 → 코드 예제 → FAQ** 순서로, 예제 프로젝트를 직접 실행하며 배울 수 있습니다.

---

## 📚 강의 목차

| # | 강의 | 설명 | 핵심 도구 |
|---|------|------|----------|
| 01 | [uv](./01-uv/README.md) | 차세대 Python 패키지 매니저 | `uv`, `uvx` |
| 02 | [Python 패키징](./02-python-packaging/README.md) | 현대적 패키지 구조 및 배포 | `pyproject.toml`, `hatchling` |
| 03 | [OS Independent 개발](./03-os-independent-dev/README.md) | 크로스 플랫폼 개발 방법론 | `pathlib`, `platformdirs`, `pydantic-settings` |
| 04 | [WSL & Docker & Registry](./04-wsl-docker-registry/README.md) | WSL 환경, Docker 기초, 사설 레지스트리 | `docker`, `registry` |
| 05 | [Dockerfile](./05-dockerfile/README.md) | 효율적인 Docker 이미지 빌드 | `Dockerfile`, 멀티스테이지 빌드 |
| 06 | [Docker Compose](./06-docker-compose/README.md) | 다중 컨테이너 애플리케이션 관리 | `compose.yml`, 네트워크, 볼륨 |
| 07 | [컨테이너 안에서 개발하기](./07-dev-containers/README.md) | 이미지에 의존성을 굽고, 소스를 마운트 | `compose.dev.yml`, 핫 리로드 |
| 08 | [Git](./08-git/README.md) | 초보자를 위한 Git 실전 가이드 | `git`, 브랜치 전략, 태그 |

---

## 🎯 학습 순서

```
[01. uv]  →  [02. Python 패키징]  →  [03. OS Independent 개발]
                                              ↓
[04. WSL & Docker]  →  [05. Dockerfile]  →  [06. Docker Compose]
                                                      ↓
                                          [07. 컨테이너 안에서 개발하기]

[08. Git] ← 언제든 참고 가능 (독립 모듈)
```

- **01~03**: Python 개발의 기초 체력 — 패키지 관리, 패키징, 크로스 플랫폼
- **04~06**: Docker 기초 — 컨테이너, 이미지 빌드, 다중 서비스
- **07**: 최종 목표 — 컨테이너 안에서 개발하는 실무 워크플로우
- **08**: Git — 모든 강의에서 필요한 버전 관리 (독립적으로 학습 가능)

---

## 🗂️ 디렉토리 구조

```
dev-guides/
├── README.md                         ← 지금 이 파일
├── CONTRIBUTING.md                   ← 기여 가이드
├── 01-uv/
│   ├── README.md                     # 강의 본문
│   └── examples/                     # 예제 (basic-project, workspace)
├── 02-python-packaging/
│   ├── README.md
│   └── examples/                     # 예제 (basic-package, namespace, private-index)
├── 03-os-independent-dev/
│   ├── README.md
│   └── examples/                     # 예제 (path-handling, cross-platform, Streamlit 데모 ⭐)
├── 04-wsl-docker-registry/
│   ├── README.md
│   └── examples/                     # 예제 (wsl-setup, private-registry)
├── 05-dockerfile/
│   ├── README.md
│   └── examples/                     # 예제 (basic, multistage, uv-docker)
├── 06-docker-compose/
│   ├── README.md
│   └── examples/                     # 예제 (single, multi, dev-override)
├── 07-dev-containers/
│   ├── README.md
│   └── examples/                     # 예제 (Streamlit 컨테이너 개발 ⭐)
└── 08-git/
    └── README.md                     # 워크플로우 순서도, 30가지 FAQ
```

---

## ⚡ 빠른 시작

```bash
# 저장소 클론
git clone https://github.com/ukkyukang/dev-guides.git
cd dev-guides

# 01-uv 강의부터 시작
cat 01-uv/README.md

# 예제 실행 (uv 설치 후)
cd 01-uv/examples/01-basic-project
uv sync
uv run python -m my_app
```

---

## 🤝 기여하기

새 강의를 추가하거나 기존 강의를 수정하고 싶다면 [CONTRIBUTING.md](./CONTRIBUTING.md)를 참고하세요.
