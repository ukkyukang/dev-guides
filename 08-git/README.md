# 08. Git — 초보자를 위한 실전 가이드

> 프로젝트의 모든 변경 이력을 기록하고, 팀원과 안전하게 협업하는 버전 관리 도구를 배웁니다.  
> `git init`부터 브랜치 전략, 태깅, 그리고 초보자가 가장 많이 겪는 30가지 상황별 해결법까지 다룹니다.

---

## 📋 사전 요구사항

- 터미널(쉘) 기본 사용법
- GitHub / GitLab 계정

## 🎯 학습 목표

1. Git의 핵심 개념 (커밋, 브랜치, 머지)을 이해한다
2. 실무에서 사용하는 Git 워크플로우를 따라할 수 있다
3. 브랜치를 나누고, 머지하고, 태그를 다는 전체 흐름을 이해한다
4. 초보자가 자주 겪는 문제 상황을 스스로 해결할 수 있다

---

## 📖 본문

### 1. Git이란?

Git은 **파일의 변경 이력을 추적하는 분산 버전 관리 시스템**입니다.

```
"어제 작업한 파일이 더 나았는데..."  →  git으로 되돌리기!
"누가 이 코드를 바꿨지?"           →  git log로 추적!
"내 작업이 동료 작업과 충돌!"       →  git merge로 해결!
```

#### 1.1 핵심 개념

| 개념 | 설명 | 비유 |
|------|------|------|
| **Repository (저장소)** | 프로젝트의 모든 파일과 변경 이력을 담는 공간 | 프로젝트 폴더 + 타임머신 |
| **Commit (커밋)** | 변경사항의 스냅샷 (저장 포인트) | 게임의 세이브 포인트 |
| **Branch (브랜치)** | 독립적인 작업 흐름 | 평행 우주 |
| **Merge (머지)** | 두 브랜치를 합치기 | 평행 우주 합체 |
| **Remote (원격)** | GitHub/GitLab 서버의 저장소 | 클라우드 백업 |
| **Tag (태그)** | 특정 커밋에 이름 붙이기 (v1.0.0) | 책갈피 |

#### 1.2 Git의 3가지 영역

```
┌──────────────┐     git add     ┌──────────────┐    git commit    ┌──────────────┐
│  Working Dir │ ──────────────► │ Staging Area │ ────────────────► │  Repository  │
│  (작업 디렉토리) │               │  (스테이징)    │                 │  (저장소)      │
│              │ ◄────────────── │              │                  │              │
│  파일 수정     │   git restore  │  커밋할 파일    │                  │  커밋 이력     │
└──────────────┘                └──────────────┘                  └──────────────┘
```

1. **Working Directory**: 현재 편집 중인 파일들
2. **Staging Area**: 다음 커밋에 포함시킬 파일들 (`git add`로 올림)
3. **Repository**: 커밋된 변경 이력 (`git commit`으로 확정)

---

### 2. Git 설치 및 초기 설정

```bash
# 설치 확인
git --version

# 사용자 정보 설정 (최초 1회)
git config --global user.name "홍길동"
git config --global user.email "gildong@company.com"

# 기본 브랜치를 main으로 설정
git config --global init.defaultBranch main

# 줄바꿈 설정
git config --global core.autocrlf input    # macOS/Linux
git config --global core.autocrlf true     # Windows

# 설정 확인
git config --list
```

---

### 3. 🗺️ 실무 개발 워크플로우 전체 순서도

**이 순서도가 이 강의의 핵심입니다.** 처음부터 태깅까지의 전체 흐름을 외우세요.

```
                        ┌─────────────────────────────────────────────┐
                        │         ❶ 프로젝트 시작                       │
                        │                                              │
                        │   git init                                   │
                        │   git add .                                  │
                        │   git commit -m "Initial commit"             │
                        │   git remote add origin <URL>                │
                        │   git push -u origin main                   │
                        └─────────────────┬───────────────────────────┘
                                          │
                        ┌─────────────────▼───────────────────────────┐
                        │         ❷ 개발 브랜치 생성                     │
                        │                                              │
                        │   git checkout -b dev                       │
                        │   git push -u origin dev                    │
                        └─────────────────┬───────────────────────────┘
                                          │
              ┌───────────────────────────▼───────────────────────────┐
              │              ❸ 기능 개발 (반복)                         │
              │                                                        │
              │   git checkout -b feature/login dev                   │
              │                                                        │
              │   ... 코드 작성 ...                                    │
              │                                                        │
              │   git add .                                            │
              │   git commit -m "feat: 로그인 기능 추가"                │
              │   git push origin feature/login                       │
              └───────────────────────────┬───────────────────────────┘
                                          │
              ┌───────────────────────────▼───────────────────────────┐
              │              ❹ PR/MR → dev에 머지                      │
              │                                                        │
              │   GitHub에서 Pull Request 생성                         │
              │   feature/login → dev                                 │
              │                                                        │
              │   # 또는 로컬에서:                                     │
              │   git checkout dev                                    │
              │   git merge feature/login                             │
              │   git push origin dev                                 │
              │   git branch -d feature/login   # feature 브랜치 삭제  │
              └───────────────────────────┬───────────────────────────┘
                                          │
                                          │  (❸→❹ 반복...)
                                          │
              ┌───────────────────────────▼───────────────────────────┐
              │              ❺ 릴리스: dev → main 머지                 │
              │                                                        │
              │   git checkout main                                   │
              │   git merge dev                                       │
              │   git push origin main                                │
              └───────────────────────────┬───────────────────────────┘
                                          │
              ┌───────────────────────────▼───────────────────────────┐
              │              ❻ 태그 달기 (버전 표시)                    │
              │                                                        │
              │   git tag -a v1.0.0 -m "v1.0.0 첫 번째 릴리스"        │
              │   git push origin v1.0.0                              │
              └───────────────────────────┬───────────────────────────┘
                                          │
                                          ▼
                                    🎉 릴리스 완료!
                                   (❸부터 다시 반복)
```

#### 3.1 요약: 한 줄로 보는 전체 흐름

```
init → push main → branch dev → branch feature → commit → merge to dev → merge to main → tag
```

#### 3.2 브랜치 구조 시각화

```
main     ●────────────────────────●──────────────●  (v1.0.0)  ●  (v1.1.0)
              \                  / \            /
dev            ●──●──●──●──●──●    ●──●──●──●──●
                 \      /            \      /
feature/login     ●──●──●             |    |
                                      |    |
feature/signup                        ●──●─●
```

---

### 4. 기본 명령어 상세 설명

#### 4.1 저장소 초기화

```bash
# 새 프로젝트 시작
mkdir my-project && cd my-project
git init

# 기존 프로젝트 가져오기
git clone https://github.com/user/repo.git
git clone https://github.com/user/repo.git my-folder-name
```

#### 4.2 변경사항 스테이징 & 커밋

```bash
# 상태 확인 (수시로 확인!)
git status

# 변경된 내용 확인
git diff                    # 스테이징 전 변경사항
git diff --staged           # 스테이징된 변경사항

# 스테이징 (커밋 준비)
git add file.py             # 특정 파일
git add src/                # 특정 폴더
git add .                   # 모든 변경사항
git add -p                  # 변경사항을 하나씩 확인하며 선택적 추가

# 커밋
git commit -m "feat: 로그인 기능 추가"
git commit -am "fix: 버그 수정"   # add + commit 한 번에 (추적 중인 파일만)
```

#### 4.3 커밋 메시지 컨벤션

```
<타입>: <설명>

# 타입 종류:
feat:     새로운 기능 추가
fix:      버그 수정
docs:     문서 수정
style:    코드 포맷팅 (세미콜론, 공백 등)
refactor: 리팩토링 (기능 변경 없이 코드 구조 개선)
test:     테스트 추가/수정
chore:    빌드 설정, 패키지 매니저 등
```

```bash
# 좋은 커밋 메시지 예시
git commit -m "feat: 사용자 로그인 API 추가"
git commit -m "fix: 비밀번호 검증 로직 오류 수정"
git commit -m "docs: README에 설치 방법 추가"
git commit -m "refactor: DB 조회 함수를 별도 모듈로 분리"
```

#### 4.4 이력 확인

```bash
# 커밋 이력 보기
git log                     # 전체 로그
git log --oneline           # 한 줄씩 요약
git log --oneline -10       # 최근 10개만
git log --oneline --graph   # 브랜치 그래프로 보기
git log --author="홍길동"    # 특정 사람의 커밋만

# 특정 파일의 변경 이력
git log -- src/main.py
git log -p -- src/main.py   # 변경 내용까지 보기

# 누가 이 줄을 수정했는지 (blame)
git blame src/main.py
```

#### 4.5 원격 저장소 (Remote)

```bash
# 원격 저장소 연결
git remote add origin https://github.com/user/repo.git

# 원격 저장소 확인
git remote -v

# 푸시 (로컬 → 원격)
git push                    # 현재 브랜치
git push origin main        # 특정 브랜치
git push -u origin main     # 업스트림 설정 (최초 1회, 이후 git push만 입력 가능)

# 풀 (원격 → 로컬)
git pull                    # fetch + merge
git pull --rebase           # fetch + rebase (히스토리 깔끔)

# 원격 변경사항 가져오기만 (머지 안 함)
git fetch
```

---

### 5. 브랜치

#### 5.1 브랜치 기본 명령어

```bash
# 브랜치 목록 보기
git branch              # 로컬 브랜치
git branch -a           # 로컬 + 원격 브랜치
git branch -v           # 마지막 커밋 메시지 포함

# 브랜치 생성
git branch dev          # 생성만 (이동 안 함)
git checkout -b dev     # 생성 + 이동
git switch -c dev       # 생성 + 이동 (최신 방식)

# 브랜치 이동
git checkout dev
git switch dev          # 최신 방식

# 브랜치 삭제
git branch -d feature/login     # 머지 완료된 브랜치 삭제
git branch -D feature/login     # 강제 삭제 (머지 안 했어도)
git push origin --delete feature/login  # 원격 브랜치 삭제
```

#### 5.2 브랜치 네이밍 컨벤션

```bash
# 기능 개발
feature/login
feature/user-profile
feature/payment-system

# 버그 수정
fix/login-crash
fix/typo-in-readme
hotfix/critical-security-fix

# 릴리스
release/v1.0.0
release/v1.1.0
```

---

### 6. 머지 (Merge)

#### 6.1 기본 머지

```bash
# dev 브랜치의 내용을 main에 합치기
git checkout main           # 받을 쪽으로 이동
git merge dev               # dev를 main에 합침
git push origin main        # 원격에 반영
```

#### 6.2 Merge vs Rebase

| | Merge | Rebase |
|---|---|---|
| 히스토리 | 머지 커밋 생성 (분기가 보임) | 일직선으로 정리 |
| 안전성 | ✅ 안전 (이력 보존) | ⚠️ 공유 브랜치에서 사용 주의 |
| 사용 시점 | PR 머지, main 으로 합칠 때 | 내 feature 브랜치를 최신화할 때 |

```bash
# Merge (안전, 항상 사용 가능)
git checkout main
git merge feature/login

# Rebase (히스토리 정리, 개인 브랜치에서만!)
git checkout feature/login
git rebase dev              # dev의 최신 커밋 위로 재배치
```

> ⚠️ **규칙**: `main`이나 `dev` 같은 공유 브랜치에서는 **절대 rebase하지 마세요**. 혼자 쓰는 feature 브랜치에서만 사용하세요.

#### 6.3 머지 충돌 해결

```bash
# 머지 시 충돌 발생
git merge feature/login
# CONFLICT (content): Merge conflict in src/main.py

# 1. 충돌 파일 열어서 수정
# <<<<<<< HEAD
# 현재 브랜치의 코드
# =======
# 머지하려는 브랜치의 코드
# >>>>>>> feature/login
#
# → 원하는 코드만 남기고 마커(<<<, ===, >>>)를 삭제

# 2. 해결한 파일을 스테이징
git add src/main.py

# 3. 머지 커밋 완료
git commit -m "merge: feature/login 충돌 해결"
```

---

### 7. 태그 (Tag)

릴리스 버전을 표시할 때 사용합니다.

```bash
# 태그 생성 (Annotated — 권장)
git tag -a v1.0.0 -m "v1.0.0 첫 번째 릴리스"
git tag -a v1.1.0 -m "v1.1.0 로그인 기능 추가"

# 태그 푸시
git push origin v1.0.0          # 특정 태그
git push origin --tags          # 모든 태그

# 태그 목록
git tag
git tag -l "v1.*"               # 패턴 검색

# 태그 삭제
git tag -d v1.0.0               # 로컬
git push origin --delete v1.0.0 # 원격

# 특정 태그로 이동 (읽기 전용)
git checkout v1.0.0
```

#### 7.1 Semantic Versioning (SemVer)

```
v1.2.3
 │ │ │
 │ │ └── Patch: 버그 수정 (하위 호환)
 │ └──── Minor: 기능 추가 (하위 호환)
 └────── Major: 호환 안 되는 변경 (Breaking Change)
```

---

### 8. `.gitignore`

Git이 추적하지 않을 파일을 지정합니다:

```gitignore
# Python
__pycache__/
*.pyc
*.pyo
.venv/
*.egg-info/
dist/
build/

# IDE
.vscode/
.idea/
*.swp

# OS
.DS_Store
Thumbs.db

# 환경 변수 (비밀번호, API 키 등)
.env
.env.local

# Docker
docker-compose.override.yml
```

> ⚠️ **중요**: `.env` 파일(비밀번호, API 키)은 **절대** Git에 올리지 마세요!

---

### 9. 명령어 치트시트

```bash
# === 기본 ===
git init                        # 저장소 초기화
git clone <URL>                 # 원격 저장소 복제
git status                      # 상태 확인 (자주 쓰세요!)
git add .                       # 모든 변경사항 스테이징
git commit -m "메시지"           # 커밋
git push                        # 원격에 푸시
git pull                        # 원격에서 풀

# === 브랜치 ===
git branch                      # 브랜치 목록
git checkout -b <name>          # 브랜치 생성 + 이동
git switch <name>               # 브랜치 이동
git merge <branch>              # 브랜치 합치기
git branch -d <name>            # 브랜치 삭제

# === 확인 ===
git log --oneline               # 커밋 이력
git diff                        # 변경사항 확인
git blame <file>                # 누가 수정했는지

# === 태그 ===
git tag -a v1.0.0 -m "메시지"   # 태그 생성
git push origin v1.0.0          # 태그 푸시

# === 되돌리기 ===
git restore <file>              # 파일 수정 취소
git restore --staged <file>     # 스테이징 취소
git reset --soft HEAD~1         # 마지막 커밋 취소 (변경 유지)
git reset --hard HEAD~1         # 마지막 커밋 취소 (변경 삭제!)
git revert <commit>             # 특정 커밋 되돌리기 (새 커밋 생성)
```

---

## ❓ 초보자가 겪는 30가지 상황별 해결법 (FAQ)

### 🔥 커밋 실수

#### Q1: 방금 커밋 메시지를 잘못 썼어요

```bash
git commit --amend -m "올바른 커밋 메시지"
```

#### Q2: 커밋에 파일을 빼먹었어요

```bash
git add forgot-file.py
git commit --amend --no-edit   # 메시지는 유지하고 파일만 추가
```

#### Q3: 방금 커밋을 취소하고 싶어요 (코드는 유지)

```bash
git reset --soft HEAD~1
# → 코드는 그대로, 스테이징 상태로 되돌아감
```

#### Q4: 방금 커밋을 완전히 삭제하고 싶어요

```bash
git reset --hard HEAD~1
# ⚠️ 주의: 변경사항이 완전히 사라집니다!
```

#### Q5: 이미 push한 커밋을 취소하고 싶어요

```bash
# 안전한 방법: 되돌리는 새 커밋을 생성
git revert <commit-hash>
git push

# ⚠️ 위험한 방법: 히스토리 강제 수정 (팀원에게 영향!)
# git push --force  ← 가급적 사용하지 마세요
```

---

### 🔥 파일 수정 실수

#### Q6: 수정한 파일을 원래대로 되돌리고 싶어요 (커밋 전)

```bash
git restore src/main.py            # 특정 파일
git restore .                      # 모든 파일
```

#### Q7: `git add`한 것을 취소하고 싶어요 (스테이징 해제)

```bash
git restore --staged src/main.py   # 특정 파일
git restore --staged .             # 모든 파일
```

#### Q8: 삭제한 파일을 복구하고 싶어요

```bash
git restore deleted-file.py
```

#### Q9: 특정 커밋의 파일 상태로 되돌리고 싶어요

```bash
git restore --source=<commit-hash> src/main.py
```

#### Q10: `.gitignore`에 추가했는데 파일이 계속 추적돼요

```bash
# 이미 추적 중인 파일을 캐시에서 제거
git rm --cached secret.env
git rm --cached -r __pycache__/
git commit -m "chore: 불필요한 파일 추적 해제"
```

---

### 🔥 브랜치 문제

#### Q11: 현재 어떤 브랜치에 있는지 모르겠어요

```bash
git branch          # 별표(*)가 현재 브랜치
git status          # 첫 줄에 "On branch main" 표시
```

#### Q12: 브랜치를 만들고 안 옮겨갔어요

```bash
git checkout -b feature/new-feature
# 또는
git switch -c feature/new-feature
```

#### Q13: 잘못된 브랜치에서 작업했어요 (아직 커밋 안 함)

```bash
# 변경사항을 임시 저장
git stash

# 올바른 브랜치로 이동
git checkout correct-branch

# 임시 저장한 변경사항 복원
git stash pop
```

#### Q14: 잘못된 브랜치에 커밋해버렸어요

```bash
# 1. 커밋을 올바른 브랜치로 옮기기
git checkout correct-branch
git cherry-pick <commit-hash>

# 2. 잘못된 브랜치에서 커밋 제거
git checkout wrong-branch
git reset --hard HEAD~1
```

#### Q15: 원격 브랜치를 로컬로 가져오고 싶어요

```bash
git fetch
git checkout feature/someone-else     # 자동으로 원격 브랜치 추적
```

#### Q16: 브랜치를 삭제하려는데 에러가 나요

```bash
# "not fully merged" 에러 → 강제 삭제
git branch -D feature/old-branch

# 원격 브랜치 삭제
git push origin --delete feature/old-branch
```

---

### 🔥 머지 & 충돌

#### Q17: merge 충돌이 났어요! 어떻게 해요?

```bash
# 1. 충돌 파일 확인
git status   # "both modified" 표시된 파일

# 2. 파일을 열어서 충돌 마커 해결
#    <<<<<<< HEAD
#    내 코드
#    =======
#    상대방 코드
#    >>>>>>> feature/xxx
#    → 원하는 코드만 남기고 마커 삭제

# 3. 해결 후
git add .
git commit -m "merge: 충돌 해결"
```

#### Q18: 머지를 취소하고 싶어요 (충돌 해결 중)

```bash
git merge --abort    # 머지 이전 상태로 되돌림
```

#### Q19: 머지했는데 되돌리고 싶어요 (이미 커밋됨)

```bash
git revert -m 1 <merge-commit-hash>
```

#### Q20: dev 브랜치의 최신 내용을 내 feature 브랜치에 반영하고 싶어요

```bash
# 방법 1: Merge (안전)
git checkout feature/my-work
git merge dev

# 방법 2: Rebase (히스토리 깔끔)
git checkout feature/my-work
git rebase dev
```

---

### 🔥 push & pull 문제

#### Q21: `git push`가 rejected 됐어요

```bash
# 원격에 내가 없는 커밋이 있음 → 먼저 pull
git pull --rebase
git push

# 그래도 안 되면 (force push — ⚠️ 주의!)
# git push --force-with-lease   # --force보다 안전한 버전
```

#### Q22: `git pull`하니까 머지 커밋이 자꾸 생겨요

```bash
# pull할 때 rebase 사용 (히스토리 깔끔)
git pull --rebase

# 항상 rebase로 pull하도록 설정
git config --global pull.rebase true
```

#### Q23: 원격 저장소 URL을 변경하고 싶어요

```bash
git remote set-url origin https://github.com/new-user/new-repo.git
git remote -v   # 확인
```

---

### 🔥 되돌리기 & 복구

#### Q24: 특정 커밋으로 돌아가서 코드를 보고 싶어요

```bash
# 읽기 전용으로 특정 커밋 확인
git checkout <commit-hash>

# 다시 최신으로 돌아오기
git checkout main
```

#### Q25: `reset --hard`를 잘못 써서 코드를 날려버렸어요!

```bash
# 구원투수: reflog (Git이 내부적으로 모든 것을 기록!)
git reflog

# 돌아가고 싶은 시점 찾기
git reset --hard <reflog-hash>
```

#### Q26: 특정 커밋의 변경사항만 가져오고 싶어요

```bash
git cherry-pick <commit-hash>
```

---

### 🔥 임시 저장 (Stash)

#### Q27: 작업 중인데 급하게 다른 브랜치로 가야 해요

```bash
# 현재 작업 임시 저장
git stash

# 다른 브랜치에서 작업...
git checkout main
# ... 작업 후 ...

# 돌아와서 복원
git checkout feature/my-work
git stash pop
```

#### Q28: stash가 여러 개 쌓였어요

```bash
# 목록 확인
git stash list

# 특정 stash 복원
git stash pop stash@{2}

# 특정 stash 삭제
git stash drop stash@{0}

# 전부 삭제
git stash clear
```

---

### 🔥 기타 자주 겪는 상황

#### Q29: 대용량 파일을 실수로 커밋해버렸어요 (100MB+)

```bash
# 최근 커밋에서 대용량 파일 제거
git reset --soft HEAD~1
git rm --cached large-file.zip
echo "large-file.zip" >> .gitignore
git add .
git commit -m "chore: 대용량 파일 제거"
```

#### Q30: 커밋 이력에서 민감한 정보(API 키 등)를 완전히 삭제하고 싶어요

```bash
# ⚠️ 히스토리를 다시 쓰는 위험한 작업 — 팀원과 반드시 협의!

# 방법 1: git filter-repo (권장 — 별도 설치 필요)
pip install git-filter-repo
git filter-repo --path secret.env --invert-paths

# 방법 2: BFG Repo-Cleaner
# https://rtyley.github.io/bfg-repo-cleaner/
```

> ⚠️ **첫째도 예방, 둘째도 예방!** → `.gitignore`에 `.env`를 반드시 등록하고, 커밋 전 `git status`를 습관화하세요.

---

## 📊 명령어 빈도 순위 (실무 기준)

일상 개발에서 가장 자주 사용하는 명령어 순서입니다:

| 순위 | 명령어 | 빈도 | 용도 |
|------|--------|------|------|
| 1 | `git status` | ⭐⭐⭐⭐⭐ | 항상 현재 상태 확인 |
| 2 | `git add .` | ⭐⭐⭐⭐⭐ | 변경사항 스테이징 |
| 3 | `git commit -m ""` | ⭐⭐⭐⭐⭐ | 커밋 |
| 4 | `git push` | ⭐⭐⭐⭐ | 원격에 반영 |
| 5 | `git pull` | ⭐⭐⭐⭐ | 원격에서 가져오기 |
| 6 | `git checkout -b` | ⭐⭐⭐ | 브랜치 생성 |
| 7 | `git merge` | ⭐⭐⭐ | 브랜치 합치기 |
| 8 | `git log --oneline` | ⭐⭐⭐ | 이력 확인 |
| 9 | `git stash` | ⭐⭐ | 임시 저장 |
| 10 | `git tag` | ⭐ | 릴리스 태그 |

---

## 🔗 참고 자료

- [Git 공식 문서](https://git-scm.com/doc)
- [GitHub Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Learn Git Branching (대화형 연습)](https://learngitbranching.js.org/?locale=ko)
- [Oh Shit, Git!?! (실수 복구 가이드)](https://ohshitgit.com/ko)
- [Conventional Commits (커밋 메시지 규약)](https://www.conventionalcommits.org/ko/)

---

## ⏭️ 학습 순서

이전: [07. 컨테이너 안에서 개발하기 ←](../07-dev-containers/README.md)

🎉 축하합니다! 모든 강의를 완료했습니다. [메인 페이지로 돌아가기 →](../README.md)
