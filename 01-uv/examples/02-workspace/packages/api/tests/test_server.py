"""API 서버 테스트.

FastAPI의 TestClient를 사용하여 API 엔드포인트를 테스트합니다.
core 패키지와의 통합이 올바르게 작동하는지 검증합니다.
"""

from fastapi.testclient import TestClient

from api.server import app

client = TestClient(app)


def test_root():
    """루트 엔드포인트가 올바른 응답을 반환하는지 테스트."""
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "success"
    assert data["data"]["service"] == "api"


def test_health():
    """헬스 체크 엔드포인트가 정상 응답을 반환하는지 테스트."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data


def test_add_numbers():
    """core 패키지의 add 함수가 API를 통해 올바르게 동작하는지 테스트."""
    response = client.get("/add/3/5")
    assert response.status_code == 200

    data = response.json()
    assert data["data"]["a"] == 3
    assert data["data"]["b"] == 5
    assert data["data"]["result"] == 8


def test_add_negative_numbers():
    """음수 계산이 올바르게 작동하는지 테스트."""
    response = client.get("/add/-10/3")
    assert response.status_code == 200

    data = response.json()
    assert data["data"]["result"] == -7
