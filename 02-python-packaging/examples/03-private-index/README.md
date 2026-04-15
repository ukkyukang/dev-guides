# 예제 03: 사설 PyPI 인덱스 배포

이 예제는 사내 사설 PyPI 인덱스에 패키지를 배포하고 설치하는 전체 워크플로우를 안내합니다.

> ⚠️ 이 예제는 실제 사설 인덱스 서버가 필요합니다. 아래 가이드를 참고하세요.

## 사설 인덱스 서버 옵션

| 도구 | 특징 | 비용 |
|------|------|------|
| [DevPI](https://devpi.net/) | 가볍고 간단, 캐싱 프록시 지원 | 무료 (오픈소스) |
| [Artifactory](https://jfrog.com/artifactory/) | 엔터프라이즈급, 다중 형식 지원 | 유료 / 무료 플랜 |
| [Nexus Repository](https://www.sonatype.com/products/sonatype-nexus-repository) | 다양한 저장소 형식 지원 | 유료 / 무료(OSS) |
| [GitHub Packages](https://github.com/features/packages) | GitHub 통합 | GitHub 플랜에 포함 |
| [GitLab Package Registry](https://docs.gitlab.com/ee/user/packages/pypi_repository/) | GitLab 통합 | GitLab 플랜에 포함 |
| [Google Artifact Registry](https://cloud.google.com/artifact-registry) | GCP 통합 | 사용량 기반 |
| [AWS CodeArtifact](https://aws.amazon.com/codeartifact/) | AWS 통합 | 사용량 기반 |

## 1단계: 패키지 빌드

```bash
# 프로젝트 디렉토리에서
uv build

# 결과 확인
ls dist/
# my-package-1.0.0.tar.gz
# my_package-1.0.0-py3-none-any.whl
```

## 2단계: 사설 인덱스에 배포

### DevPI에 배포

```bash
# DevPI 서버 URL과 인증 정보 설정
uv publish \
  --publish-url http://devpi.company.com/company/prod/+simple/ \
  --username deployer \
  --password $DEVPI_TOKEN
```

### Artifactory에 배포

```bash
uv publish \
  --publish-url https://company.jfrog.io/artifactory/api/pypi/pypi-local/ \
  --username deployer \
  --password $ARTIFACTORY_TOKEN
```

### GitLab Package Registry에 배포

```bash
uv publish \
  --publish-url https://gitlab.company.com/api/v4/projects/{project_id}/packages/pypi \
  --username __token__ \
  --password $GITLAB_TOKEN
```

## 3단계: 소비자 프로젝트에서 설치

### `pyproject.toml` 설정

```toml
[project]
name = "consumer-app"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "company-core>=1.0.0",       # 사설 인덱스의 패키지
    "company-utils>=1.0.0",
    "fastapi>=0.115.0",          # 공식 PyPI 패키지
]

# ─── uv 인덱스 설정 ───
[[tool.uv.index]]
name = "company"
url = "https://pypi.company.com/simple/"

# 특정 패키지를 사설 인덱스에서 가져오기
[tool.uv.sources]
company-core = { index = "company" }
company-utils = { index = "company" }
```

### 환경 변수로 인증

```bash
# 방법 1: 환경 변수 (권장)
export UV_INDEX_COMPANY_USERNAME="reader"
export UV_INDEX_COMPANY_PASSWORD="$TOKEN"

# 방법 2: .env 파일 (Git에 커밋하지 마세요!)
echo 'UV_INDEX_COMPANY_USERNAME=reader' >> .env
echo 'UV_INDEX_COMPANY_PASSWORD=your-token' >> .env
```

### 설치 실행

```bash
uv sync
```

## 4단계: CI/CD 자동 배포

### GitHub Actions 예시

```yaml
name: Publish Package

on:
  push:
    tags:
      - 'v*'

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v5

      - name: Build
        run: uv build

      - name: Publish to private index
        run: |
          uv publish \
            --publish-url ${{ secrets.PYPI_PUBLISH_URL }} \
            --username ${{ secrets.PYPI_USERNAME }} \
            --password ${{ secrets.PYPI_PASSWORD }}
```

## 버전 관리 워크플로우

```
1. pyproject.toml에서 version 업데이트
2. CHANGELOG.md 업데이트
3. Git 커밋 & 태그
   git add .
   git commit -m "release: v1.2.0"
   git tag v1.2.0
   git push --tags
4. CI/CD가 자동으로 빌드 & 배포
```

## 주요 학습 포인트

1. **`uv build`**: wheel과 sdist 생성
2. **`uv publish`**: 사설 인덱스에 배포
3. **`[[tool.uv.index]]`**: 사설 인덱스 등록
4. **`[tool.uv.sources]`**: 패키지별 인덱스 매핑
5. **환경 변수 인증**: 보안 토큰 관리
