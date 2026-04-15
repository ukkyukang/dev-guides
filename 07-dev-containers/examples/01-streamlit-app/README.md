# 예제: Streamlit 앱 — 컨테이너 안에서 개발하기

이 예제는 컨테이너 개발의 핵심을 보여줍니다:  
**이미지에 의존성을 굽고, 소스코드는 마운트한다.**

## 프로젝트 구조

```
01-streamlit-app/
├── pyproject.toml        # 프로젝트 정의 (uv --lib 구조)
├── uv.lock               # 의존성 Lock 파일
├── Dockerfile            # 의존성이 설치된 이미지
├── compose.dev.yml       # 개발용 (소스 마운트 + 핫 리로드)
└── src/
    └── my_app/
        ├── __init__.py
        └── app.py        # Streamlit 앱
```

## 실행

```bash
# 1. 이미지 빌드 + 실행 (처음 한 번)
docker compose -f compose.dev.yml up --build

# 2. 브라우저에서 확인
# http://localhost:8501

# 3. src/my_app/app.py를 수정해 보세요
#    → 브라우저가 자동으로 리로드됩니다!

# 4. 종료
docker compose -f compose.dev.yml down
```

## 핵심 포인트

1. `Dockerfile`은 **의존성만 설치**합니다 (이미지에 굽기)
2. `compose.dev.yml`은 **소스코드를 마운트**합니다 (`./src:/app/src`)
3. 코드를 수정해도 **이미지를 재빌드할 필요가 없습니다**
4. `pyproject.toml`에 의존성을 추가하면 그때만 `--build`로 재빌드합니다

## 직접 확인해보기

`src/my_app/app.py`를 열고 제목이나 내용을 수정한 뒤 저장하세요.  
브라우저에서 Streamlit이 자동으로 변경을 감지하고 리로드합니다.
