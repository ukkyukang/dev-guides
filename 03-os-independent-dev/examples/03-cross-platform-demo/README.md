# 예제 03: 크로스 플랫폼 통합 데모 (Streamlit) ⭐

pathlib, platformdirs, pydantic-settings, shutil을 **모두** 사용하여
OS 독립적 코드의 실제 동작을 시각적으로 보여주는 Streamlit 앱입니다.

## 실행

```bash
# 의존성 설치
uv sync

# Streamlit 앱 실행
uv run streamlit run src/demo/app.py

# http://localhost:8501
```

## 이 앱에서 확인할 수 있는 것

1. **현재 OS 정보** — 어떤 OS에서 실행 중인지
2. **platformdirs 4가지 경로** — config, data, cache, log가 현재 OS에서 어디를 가리키는지
3. **pydantic-settings** — `.env` 파일과 환경 변수가 어떻게 로드/병합되는지
4. **pathlib** — 경로 연산, 파일 쓰기/읽기 실시간 데모
5. **shutil.which** — 시스템 도구 설치 여부 확인

## Docker에서 실행하면?

같은 코드를 Docker 안에서 실행하면 경로가 Linux 표준으로 바뀌는 것을 확인할 수 있습니다!
