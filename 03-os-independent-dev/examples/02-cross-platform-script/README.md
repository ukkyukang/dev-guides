# 예제 02: 크로스 플랫폼 자동화 스크립트

이 예제는 OS에 독립적인 개발 자동화 방법을 보여줍니다.

## 파일 구성

- `Taskfile.yml` — [Task](https://taskfile.dev/) 기반 (크로스 플랫폼 권장)
- `dev.py` — 순수 Python 자동화 스크립트 (추가 도구 설치 불필요)
- `.gitattributes` — 줄바꿈 정규화 설정

## 실행

```bash
# Python 스크립트 방식 (추가 도구 불필요)
uv run python dev.py test
uv run python dev.py lint
uv run python dev.py format
uv run python dev.py check    # lint + test 함께

# Task 방식 (task 설치 필요: https://taskfile.dev)
task test
task lint
task check
```
