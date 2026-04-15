# 예제 03: uv 기반 Docker 이미지

uv 공식 Docker 이미지와 lock 파일을 활용한 최적의 Python 이미지 빌드입니다.

## 빌드 및 실행

```bash
docker build -t uv-app .
docker run --rm -p 8000:8000 uv-app

# 이미지 크기 비교
docker images | grep -E "basic-app|multistage-app|uv-app"
```
