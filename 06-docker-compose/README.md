# 06. Docker Compose

> 다중 컨테이너 애플리케이션을 정의하고 관리하는 Docker Compose를 배웁니다.  
> 서비스 간 통신, 볼륨, 네트워크, 그리고 개발/프로덕션 환경 분리까지 다룹니다.

---

## 📋 사전 요구사항

- [05. Dockerfile](../05-dockerfile/README.md) 강의 완료
- Dockerfile 작성 경험

## 🎯 학습 목표

1. Docker Compose 파일 구조를 이해하고 작성할 수 있다
2. 다중 서비스를 정의하고 네트워킹을 구성할 수 있다
3. 볼륨과 바인드 마운트로 데이터를 관리할 수 있다
4. `compose.override.yml`로 개발/프로덕션 환경을 분리할 수 있다

---

## 📖 본문

### 1. Docker Compose란?

Docker Compose는 **여러 컨테이너를 하나의 YAML 파일로 정의하고 동시에 관리**하는 도구입니다.

```
API 서버 + 데이터베이스 + 캐시 + 리버스 프록시
= 하나의 compose.yml로 관리
```

#### 1.1 왜 필요한가?

```bash
# ❌ 컨테이너마다 개별 실행 (복잡하고 실수하기 쉬움)
docker run -d --name db -e POSTGRES_PASSWORD=secret postgres:16
docker run -d --name redis redis:7
docker run -d --name api -p 8000:8000 --link db --link redis my-api
docker run -d --name nginx -p 80:80 --link api nginx

# ✅ Compose로 한 번에 (선언적, 재현 가능)
docker compose up -d
```

---

### 2. `compose.yml` 구조

> 💡 Docker Compose V2부터 파일 이름은 `compose.yml`이 권장됩니다. (`docker-compose.yml`도 여전히 지원)

```yaml
# compose.yml 기본 구조
services:
  api:                              # 서비스 이름
    build: .                        # Dockerfile 빌드
    ports:
      - "8000:8000"                 # 포트 매핑
    environment:
      - DB_HOST=db                  # 환경 변수
    depends_on:
      - db                          # 의존성 순서

  db:
    image: postgres:16              # 이미지 사용
    volumes:
      - db-data:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: secret
      POSTGRES_DB: mydb

volumes:
  db-data:                          # 네임드 볼륨
```

#### 2.1 주요 옵션 레퍼런스

| 옵션 | 설명 | 예시 |
|------|------|------|
| `image` | 사용할 이미지 | `image: postgres:16` |
| `build` | Dockerfile 빌드 | `build: ./api` |
| `ports` | 포트 매핑 (호스트:컨테이너) | `ports: ["8000:8000"]` |
| `volumes` | 볼륨 마운트 | `volumes: ["./data:/app/data"]` |
| `environment` | 환경 변수 | `environment: {DB_HOST: db}` |
| `env_file` | 환경 변수 파일 | `env_file: .env` |
| `depends_on` | 서비스 의존 순서 | `depends_on: [db, redis]` |
| `restart` | 재시작 정책 | `restart: unless-stopped` |
| `networks` | 네트워크 연결 | `networks: [backend]` |
| `command` | CMD 오버라이드 | `command: ["--reload"]` |
| `healthcheck` | 헬스 체크 | 아래 예시 참조 |

---

### 3. 서비스 간 네트워킹

Docker Compose는 자동으로 **브리지 네트워크**를 생성하며, 서비스 이름으로 서로를 참조할 수 있습니다.

```yaml
services:
  api:
    build: .
    environment:
      # 'db'는 서비스 이름 = 자동 DNS 이름
      DATABASE_URL: postgresql://user:pass@db:5432/mydb
      REDIS_URL: redis://redis:6379

  db:
    image: postgres:16

  redis:
    image: redis:7-alpine
```

```python
# api 코드에서 — 서비스 이름으로 접근
import httpx

# 같은 Compose 네트워크 안에서 서비스 이름이 호스트명
db_url = "postgresql://user:pass@db:5432/mydb"  # ✅ 'db'가 호스트명
redis_url = "redis://redis:6379"                 # ✅ 'redis'가 호스트명
```

---

### 4. 볼륨과 데이터 관리

#### 4.1 네임드 볼륨 (데이터 영속성)

```yaml
services:
  db:
    image: postgres:16
    volumes:
      - db-data:/var/lib/postgresql/data    # 네임드 볼륨

volumes:
  db-data:    # Docker가 관리하는 영속 볼륨
```

#### 4.2 바인드 마운트 (개발용 파일 동기화)

```yaml
services:
  api:
    build: .
    volumes:
      - ./src:/app/src    # 호스트의 src/를 컨테이너의 /app/src에 마운트
      # → 코드 변경이 컨테이너에 즉시 반영 (핫 리로드 가능)
```

---

### 5. 헬스 체크

```yaml
services:
  db:
    image: postgres:16
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build: .
    depends_on:
      db:
        condition: service_healthy    # DB가 건강할 때만 시작
```

---

### 6. 환경별 설정 분리

#### 6.1 `compose.override.yml` (개발 설정 자동 병합)

```yaml
# compose.yml — 기본 설정 (프로덕션)
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=false

  db:
    image: postgres:16
    volumes:
      - db-data:/var/lib/postgresql/data

volumes:
  db-data:
```

```yaml
# compose.override.yml — 개발 전용 (자동 병합됨)
services:
  api:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - ./src:/app/src              # 소스 바인드 마운트
    environment:
      - DEBUG=true
    command: ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0"]

  db:
    ports:
      - "5432:5432"                 # 개발시에만 DB 포트 노출
    environment:
      POSTGRES_PASSWORD: devpassword
```

```bash
# 개발: compose.yml + compose.override.yml 자동 병합
docker compose up

# 프로덕션: compose.yml만 사용
docker compose -f compose.yml up

# 또는 별도 프로덕션 파일 사용
docker compose -f compose.yml -f compose.prod.yml up
```

---

### 7. 주요 명령어

```bash
# 시작
docker compose up              # 포그라운드 실행
docker compose up -d           # 백그라운드(detached) 실행
docker compose up --build      # 이미지 재빌드 후 실행
docker compose up api          # 특정 서비스만 실행

# 중지
docker compose down            # 컨테이너 + 네트워크 삭제
docker compose down -v         # + 볼륨까지 삭제
docker compose stop            # 컨테이너만 중지 (삭제 안 함)

# 상태
docker compose ps              # 서비스 상태
docker compose logs            # 전체 로그
docker compose logs -f api     # 특정 서비스 실시간 로그

# 실행
docker compose exec api bash   # 실행 중인 서비스에 접속
docker compose run api pytest  # 일회성 명령 실행

# 스케일링
docker compose up -d --scale api=3  # API 서비스 3개 인스턴스

# 정리
docker compose down --rmi all  # 이미지까지 전부 삭제
```

---

## ❓ 자주 묻는 질문 (FAQ)

### Q1: `docker-compose.yml` vs `compose.yml` 어떤 것을 써야 하나요?

**A**: **`compose.yml`**을 사용하세요. Docker Compose V2(현재 표준)에서 권장하는 파일명입니다. `docker-compose.yml`도 하위 호환으로 지원됩니다.

### Q2: `depends_on`은 서비스가 "준비"될 때까지 기다리나요?

**A**: 기본적으로 **아닙니다**. 컨테이너가 "시작"되면 바로 다음 서비스를 시작합니다. 실제로 준비될 때까지 기다리려면 `healthcheck` + `condition: service_healthy`를 사용하세요.

### Q3: `docker compose run`과 `docker compose exec`의 차이는?

**A**:
- `run`: **새 컨테이너를 생성**하여 명령 실행 (일회성 작업)
- `exec`: **이미 실행 중인 컨테이너**에서 명령 실행

### Q4: 환경 변수는 어디에 정의해야 하나요?

**A**: 우선순위 (높은 것이 덮어씀):
1. 셸 환경 변수
2. `.env` 파일
3. `env_file` 옵션
4. `environment` 옵션
5. Dockerfile의 `ENV`

개발 시크릿은 `.env` 파일에, 일반 설정은 `environment`에 넣으세요.

### Q5: `restart: unless-stopped` vs `restart: always`의 차이는?

**A**:
- `always`: Docker 데몬 재시작 시 항상 컨테이너를 다시 시작
- `unless-stopped`: 수동으로 `docker compose stop`한 경우에는 재시작하지 않음

프로덕션에서는 `unless-stopped`를 권장합니다.

---

## 🏗️ 예제 프로젝트

| 예제 | 설명 | 핵심 학습 |
|------|------|----------|
| [01-single-service](./examples/01-single-service/) | 단일 서비스 | 기본 compose.yml 작성 |
| [02-multi-service](./examples/02-multi-service/) | API + PostgreSQL + Redis | 서비스 간 통신, 볼륨 |
| [03-dev-override](./examples/03-dev-override/) | 개발/프로덕션 분리 | override, 핫 리로드 |

---

## 🔗 참고 자료

- [Docker Compose 공식 문서](https://docs.docker.com/compose/)
- [Compose 파일 레퍼런스](https://docs.docker.com/reference/compose-file/)
- [Compose 네트워킹](https://docs.docker.com/compose/how-tos/networking/)

---

## ⏭️ 다음 강의

[07. 컨테이너 안에서 개발하기 →](../07-dev-containers/README.md)
