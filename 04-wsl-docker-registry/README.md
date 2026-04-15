# 04. WSL과 Docker & Docker Registry

> Windows에서 Linux 개발 환경을 구축하는 WSL, 컨테이너 기술의 핵심인 Docker,  
> 그리고 사설 Docker Registry 구축까지 다룹니다.


<!-- TOC -->
## 📑 목차

- [📋 사전 요구사항](#사전-요구사항)
- [🎯 학습 목표](#학습-목표)
- [📖 본문](#본문)
  - [1. WSL2 (Windows Subsystem for Linux)](#1-wsl2-windows-subsystem-for-linux)
    - [1.1 WSL2란?](#11-wsl2란)
    - [1.2 WSL2 설치](#12-wsl2-설치)
    - [1.3 WSL2 개발 환경 설정](#13-wsl2-개발-환경-설정)
    - [1.4 WSL2 파일 시스템 주의사항](#14-wsl2-파일-시스템-주의사항)
    - [1.5 VS Code + WSL 연동](#15-vs-code-wsl-연동)
  - [2. Docker 핵심 개념](#2-docker-핵심-개념)
    - [2.1 Docker란?](#21-docker란)
    - [2.2 핵심 용어](#22-핵심-용어)
    - [2.3 이미지 레이어 구조](#23-이미지-레이어-구조)
  - [3. Docker 설치](#3-docker-설치)
    - [Windows (WSL2 기반)](#windows-wsl2-기반)
    - [macOS](#macos)
    - [Linux (Ubuntu)](#linux-ubuntu)
  - [4. Docker 기본 명령어](#4-docker-기본-명령어)
    - [4.1 이미지 관리](#41-이미지-관리)
    - [4.2 컨테이너 실행](#42-컨테이너-실행)
    - [4.3 컨테이너 관리](#43-컨테이너-관리)
    - [4.4 명령어 요약 치트시트](#44-명령어-요약-치트시트)
  - [5. 사설 Docker Registry](#5-사설-docker-registry)
    - [5.1 왜 사설 Registry가 필요한가?](#51-왜-사설-registry가-필요한가)
    - [5.2 간단한 Registry 구축 (Docker 공식 이미지)](#52-간단한-registry-구축-docker-공식-이미지)
    - [5.3 프로덕션 Registry 옵션](#53-프로덕션-registry-옵션)
- [❓ 자주 묻는 질문 (FAQ)](#자주-묻는-질문-faq)
  - [Q1: WSL2와 Docker Desktop은 꼭 함께 써야 하나요?](#q1-wsl2와-docker-desktop은-꼭-함께-써야-하나요)
  - [Q2: `docker run`과 `docker exec`의 차이는?](#q2-docker-run과-docker-exec의-차이는)
  - [Q3: 볼륨(`-v`)과 바인드 마운트의 차이는?](#q3-볼륨-v과-바인드-마운트의-차이는)
  - [Q4: Docker 이미지 크기를 줄이려면?](#q4-docker-이미지-크기를-줄이려면)
  - [Q5: `docker system prune`은 안전한가요?](#q5-docker-system-prune은-안전한가요)
- [🏗️ 예제 프로젝트](#예제-프로젝트)
- [🔗 참고 자료](#참고-자료)
- [⏭️ 다음 강의](#다음-강의)

<!-- /TOC -->

---

## 📋 사전 요구사항

- [03. OS Independent 개발 방법론](../03-os-independent-dev/README.md) 강의 완료
- Windows 10/11 (WSL 관련) 또는 macOS/Linux (Docker 관련)

## 🎯 학습 목표

1. WSL2의 아키텍처를 이해하고 개발 환경을 구성할 수 있다
2. Docker의 핵심 개념 (이미지, 컨테이너, 레이어)을 이해한다
3. Docker 기본 명령어를 능숙하게 사용할 수 있다
4. 사설 Docker Registry를 구축하고 운영할 수 있다

---

## 📖 본문

### 1. WSL2 (Windows Subsystem for Linux)

#### 1.1 WSL2란?

WSL2는 Windows에서 실제 Linux 커널을 실행하는 기술입니다.

| 항목 | WSL1 | WSL2 |
|------|------|------|
| 아키텍처 | 번역 레이어 | 실제 Linux 커널 (VM) |
| 시스템 호출 | 일부만 지원 | 100% 호환 |
| 파일 성능 (Linux FS) | 빠름 | 매우 빠름 |
| 파일 성능 (Windows FS) | 빠름 | 느림 ⚠️ |
| Docker | ❌ | ✅ 네이티브 지원 |
| GPU | ❌ | ✅ CUDA 지원 |

#### 1.2 WSL2 설치

```powershell
# PowerShell (관리자 권한)

# 1. WSL 설치 (Ubuntu가 기본 배포판)
wsl --install

# 2. 특정 배포판 설치
wsl --install -d Ubuntu-24.04

# 3. 설치된 배포판 확인
wsl --list --verbose

# 4. 기본 배포판을 WSL2로 설정
wsl --set-default-version 2
```

#### 1.3 WSL2 개발 환경 설정

```bash
# Ubuntu 안에서 실행

# 1. 패키지 업데이트
sudo apt update && sudo apt upgrade -y

# 2. 기본 개발 도구 설치
sudo apt install -y build-essential git curl wget

# 3. uv 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 4. Python 설치 (uv 이용)
uv python install 3.12
```

#### 1.4 WSL2 파일 시스템 주의사항

```
✅ 빠름: Linux 파일시스템 내 작업 (/home/user/projects/)
❌ 느림: Windows 파일시스템 접근 (/mnt/c/Users/...)

# 프로젝트는 반드시 Linux 파일시스템에 저장하세요!
cd ~
mkdir -p projects
cd projects
git clone https://github.com/your/repo.git
```

> ⚠️ **핵심 규칙**: `/mnt/c/` 경로에서 작업하면 I/O 성능이 10배 이상 느려집니다. 프로젝트 코드는 항상 `~/` 아래에 두세요.

#### 1.5 VS Code + WSL 연동

```bash
# WSL 안에서 VS Code 열기
code .

# VS Code가 자동으로 "Remote - WSL" 확장을 사용하여 연결됩니다
```

---

### 2. Docker 핵심 개념

#### 2.1 Docker란?

Docker는 애플리케이션을 **컨테이너**로 패키징하여, 어떤 환경에서든 동일하게 실행할 수 있게 해주는 플랫폼입니다.

```
"내 노트북에서는 되는데..." → 컨테이너로 해결!
```

#### 2.2 핵심 용어

```
┌─────────────────────────────────┐
│         Docker Registry          │  ← 이미지 저장소 (Docker Hub, 사설)
│  ┌─────────┐  ┌─────────┐      │
│  │ Image A │  │ Image B │      │
│  └─────────┘  └─────────┘      │
└─────────────────────────────────┘
         │ pull              │ push
         ▼                   ▲
┌─────────────────────────────────┐
│         Docker Engine            │  ← 로컬 Docker 데몬
│                                  │
│  ┌──────────┐  ┌──────────┐     │
│  │Container │  │Container │     │
│  │ (from A) │  │ (from B) │     │
│  └──────────┘  └──────────┘     │
└─────────────────────────────────┘
```

| 용어 | 설명 | 비유 |
|------|------|------|
| **Image** | 읽기 전용 템플릿. 앱 + 의존성 + 설정 포함 | 클래스 (설계도) |
| **Container** | 이미지의 실행 인스턴스 | 객체 (인스턴스) |
| **Layer** | 이미지를 구성하는 각 단계 (캐싱 단위) | 레이어 케이크 |
| **Registry** | 이미지를 저장하고 공유하는 서버 | GitHub (코드 대신 이미지) |
| **Dockerfile** | 이미지 빌드 레시피 | 레시피 (요리법) |
| **Volume** | 컨테이너의 데이터를 호스트에 영속 저장 | USB 드라이브 |

#### 2.3 이미지 레이어 구조

```
┌──────────────────────────────┐
│  Layer 4: COPY . .           │  ← 앱 소스코드 (자주 변경)
├──────────────────────────────┤
│  Layer 3: RUN uv sync        │  ← 의존성 설치
├──────────────────────────────┤
│  Layer 2: COPY pyproject.toml│  ← 의존성 정의
├──────────────────────────────┤
│  Layer 1: FROM python:3.12   │  ← 베이스 이미지 (거의 변경 안 됨)
└──────────────────────────────┘
```

> 💡 **레이어 캐싱**: 변경되지 않은 레이어는 재빌드하지 않습니다. 자주 변경되는 파일(소스코드)은 나중에 COPY하세요.

---

### 3. Docker 설치

#### Windows (WSL2 기반)

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) 설치
2. Settings → General → "Use the WSL 2 based engine" ✅
3. Settings → Resources → WSL Integration → 사용할 배포판 활성화

#### macOS

```bash
# Homebrew
brew install --cask docker

# 또는 Docker Desktop 직접 다운로드
```

#### Linux (Ubuntu)

```bash
# 공식 설치 스크립트
curl -fsSL https://get.docker.com | sh

# 현재 사용자를 docker 그룹에 추가 (sudo 없이 사용하기 위해)
sudo usermod -aG docker $USER
newgrp docker

# 설치 확인
docker --version
docker run hello-world
```

---

### 4. Docker 기본 명령어

#### 4.1 이미지 관리

```bash
# 이미지 검색
docker search python

# 이미지 다운로드 (pull)
docker pull python:3.12-slim
docker pull ubuntu:24.04

# 로컬 이미지 목록
docker images

# 이미지 삭제
docker rmi python:3.12-slim

# 미사용 이미지 정리
docker image prune -a
```

#### 4.2 컨테이너 실행

```bash
# 기본 실행
docker run python:3.12-slim python -c "print('Hello Docker!')"

# 인터랙티브 모드 (-it)
docker run -it python:3.12-slim bash

# 백그라운드 실행 (-d) + 포트 매핑 (-p)
docker run -d -p 8080:80 --name my-nginx nginx

# 환경 변수 전달 (-e)
docker run -e DB_HOST=localhost -e DB_PORT=5432 my-app

# 볼륨 마운트 (-v)
docker run -v $(pwd):/app -w /app python:3.12-slim python main.py

# 자동 삭제 (--rm)
docker run --rm python:3.12-slim python -c "print('임시 실행')"
```

#### 4.3 컨테이너 관리

```bash
# 실행 중인 컨테이너 목록
docker ps

# 모든 컨테이너 목록 (중지된 것 포함)
docker ps -a

# 컨테이너 로그 확인
docker logs my-nginx
docker logs -f my-nginx    # 실시간 추적

# 실행 중인 컨테이너에 명령 실행
docker exec -it my-nginx bash

# 컨테이너 중지 / 시작 / 재시작
docker stop my-nginx
docker start my-nginx
docker restart my-nginx

# 컨테이너 삭제
docker rm my-nginx

# 모든 중지된 컨테이너 삭제
docker container prune
```

#### 4.4 명령어 요약 치트시트

```bash
# 이미지
docker pull <image>           # 다운로드
docker images                 # 목록
docker rmi <image>            # 삭제
docker build -t <tag> .       # 빌드

# 컨테이너
docker run <image>            # 실행
docker ps                     # 실행 중 목록
docker stop <container>       # 중지
docker rm <container>         # 삭제
docker logs <container>       # 로그
docker exec -it <container> bash  # 접속

# 정리
docker system prune -a        # 미사용 리소스 전체 정리
docker system df              # 디스크 사용량 확인
```

---

### 5. 사설 Docker Registry

#### 5.1 왜 사설 Registry가 필요한가?

- **보안**: 회사 코드가 포함된 이미지를 외부에 공개하지 않음
- **속도**: 사내 네트워크에서 빠른 이미지 전송
- **관리**: 이미지 접근 권한 및 보존 정책 통제

#### 5.2 간단한 Registry 구축 (Docker 공식 이미지)

```bash
# 1. Registry 컨테이너 실행
docker run -d \
  -p 5000:5000 \
  --name registry \
  --restart=always \
  -v registry-data:/var/lib/registry \
  registry:2

# 2. 이미지에 태그 추가
docker tag my-app:latest localhost:5000/my-app:latest

# 3. 사설 Registry에 push
docker push localhost:5000/my-app:latest

# 4. 사설 Registry에서 pull
docker pull localhost:5000/my-app:latest

# 5. Registry 카탈로그 확인
curl http://localhost:5000/v2/_catalog
```

#### 5.3 프로덕션 Registry 옵션

| 솔루션 | 특징 | 추천 상황 |
|--------|------|----------|
| **Harbor** | 오픈소스, 취약점 스캔, RBAC | 사내 온프레미스 |
| **Docker Hub** (유료) | 공식, 간편 | 소규모 팀 |
| **AWS ECR** | AWS 통합 | AWS 사용 조직 |
| **GCP Artifact Registry** | GCP 통합 | GCP 사용 조직 |
| **Azure ACR** | Azure 통합 | Azure 사용 조직 |
| **GitLab Container Registry** | GitLab 통합 | GitLab 사용 조직 |
| **GitHub Container Registry** | GitHub 통합 | GitHub 사용 조직 |

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1: WSL2와 Docker Desktop은 꼭 함께 써야 하나요?

**A**: Windows에서는 Docker Desktop이 WSL2를 백엔드로 사용하므로 함께 설치하는 것이 가장 편합니다. 또는 WSL2 Ubuntu 안에서 Docker Engine을 직접 설치할 수도 있습니다.

### Q2: `docker run`과 `docker exec`의 차이는?

**A**:
- `docker run`: **새 컨테이너를 생성**하고 실행
- `docker exec`: **이미 실행 중인 컨테이너** 안에서 추가 명령 실행

### Q3: 볼륨(`-v`)과 바인드 마운트의 차이는?

**A**:
- **바인드 마운트** (`-v /호스트/경로:/컨테이너/경로`): 호스트 디렉토리를 직접 마운트
- **볼륨** (`-v volume-name:/컨테이너/경로`): Docker가 관리하는 영속 저장소

개발 시에는 바인드 마운트, 프로덕션 데이터에는 볼륨을 사용합니다.

### Q4: Docker 이미지 크기를 줄이려면?

**A**:
1. `slim` 또는 `alpine` 베이스 이미지 사용
2. 멀티스테이지 빌드 (강의 05에서 상세히 다룸)
3. `.dockerignore`로 불필요한 파일 제외
4. 레이어 수 최소화 (`RUN` 명령어 병합)

### Q5: `docker system prune`은 안전한가요?

**A**: 중지된 컨테이너, 미사용 네트워크, 댕글링 이미지를 삭제합니다. `-a` 옵션 추가 시 사용 중이 아닌 **모든** 이미지를 삭제하므로 주의하세요.

---

## 🏗️ 예제 프로젝트

| 예제 | 설명 |
|------|------|
| [01-wsl-setup](./examples/01-wsl-setup/) | WSL2 설정 체크리스트 및 스크립트 |
| [02-private-registry](./examples/02-private-registry/) | 사설 Docker Registry 구축 |

---

## 🔗 참고 자료

- [WSL 공식 문서](https://learn.microsoft.com/ko-kr/windows/wsl/)
- [Docker 공식 문서](https://docs.docker.com/)
- [Docker Registry 문서](https://docs.docker.com/registry/)
- [Harbor 오픈소스 Registry](https://goharbor.io/)

---

## ⏭️ 다음 강의

[05. Dockerfile →](../05-dockerfile/README.md)
