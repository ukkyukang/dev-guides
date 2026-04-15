# 예제 02: 멀티스테이지 빌드

빌드 도구를 최종 이미지에서 제거하여 이미지 크기를 최소화합니다.

## 빌드 및 실행

```bash
docker build -t multistage-app .
docker run --rm -p 8000:8000 multistage-app

# 이미지 크기 비교
docker images | grep -E "basic-app|multistage-app"
```
