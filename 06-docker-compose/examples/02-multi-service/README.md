# 예제 02: 다중 서비스 (API + PostgreSQL + Redis)

실무에서 가장 자주 보는 패턴입니다. API 서버가 DB와 캐시에 연결됩니다.

## 실행
```bash
docker compose up --build -d
# http://localhost:8000/docs

# 로그 확인
docker compose logs -f api

# 종료 (볼륨 유지)
docker compose down

# 종료 (볼륨까지 삭제)
docker compose down -v
```
