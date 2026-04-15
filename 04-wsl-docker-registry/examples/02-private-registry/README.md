# 사설 Docker Registry 구축

Docker 공식 `registry:2` 이미지를 사용한 간단한 사설 Registry 구성입니다.

## 실행

```bash
# Registry 시작
docker compose up -d

# 상태 확인
curl http://localhost:5000/v2/_catalog

# 이미지 push 테스트
docker pull nginx:alpine
docker tag nginx:alpine localhost:5000/nginx:alpine
docker push localhost:5000/nginx:alpine

# 카탈로그에서 확인
curl http://localhost:5000/v2/_catalog
# {"repositories":["nginx"]}

# 종료
docker compose down
```

## compose.yml

아래 `compose.yml`에서 Registry를 포트 5000으로 실행합니다.
데이터는 Docker 볼륨 `registry-data`에 영속 저장됩니다.
