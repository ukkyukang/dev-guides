# 예제 03: 개발/프로덕션 설정 분리

`compose.override.yml`로 개발 전용 설정을 자동 적용하는 패턴입니다.

## 실행

```bash
# 개발 모드 (compose.yml + compose.override.yml 자동 병합)
docker compose up --build
# → 소스코드 바인드 마운트 + 핫 리로드 + DB 포트 노출

# 프로덕션 모드 (compose.yml만 사용)
docker compose -f compose.yml up --build -d
```
