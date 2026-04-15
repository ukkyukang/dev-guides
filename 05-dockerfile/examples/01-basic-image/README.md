# 예제 01: 기본 Dockerfile

가장 기본적인 Dockerfile 작성법을 보여줍니다.

## 빌드 및 실행

```bash
docker build -t basic-app .
docker run --rm -p 8000:8000 basic-app
# http://localhost:8000 에서 확인
# http://localhost:8000/docs 에서 API 문서 확인
```
