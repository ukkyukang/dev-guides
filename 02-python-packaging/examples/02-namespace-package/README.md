# 예제 02: 네임스페이스 패키지

이 예제는 **implicit namespace package**를 사용하여 `company` 네임스페이스 아래에 두 개의 독립 패키지를 구성합니다.

## 프로젝트 구조

```
02-namespace-package/
├── README.md
├── pyproject.toml                     # 워크스페이스 루트
├── packages/
│   ├── company-core/                  # company.core 패키지
│   │   ├── pyproject.toml
│   │   └── src/
│   │       └── company/               # ❌ __init__.py 없음!
│   │           └── core/
│   │               ├── __init__.py    # ✅ 여기부터 __init__.py
│   │               └── models.py
│   └── company-utils/                 # company.utils 패키지
│       ├── pyproject.toml
│       └── src/
│           └── company/               # ❌ __init__.py 없음!
│               └── utils/
│                   ├── __init__.py    # ✅
│                   └── helpers.py
```

## 핵심 개념

### Implicit Namespace Package란?

Python 3.3+ (PEP 420)에서 도입된 기능으로, `__init__.py`가 없는 디렉토리도 패키지로 인식됩니다.
이를 통해 같은 최상위 이름(`company`)을 여러 독립 배포 패키지가 공유할 수 있습니다.

### 규칙

1. 네임스페이스 디렉토리(`company/`)에는 `__init__.py`를 **절대 넣지 마세요**
2. 실제 패키지 디렉토리(`company/core/`, `company/utils/`)에만 `__init__.py`를 넣으세요
3. 각 패키지는 독립적으로 설치 가능해야 합니다

## 실행하기

```bash
# 1. 의존성 설치
uv sync

# 2. 두 패키지가 같은 네임스페이스에서 import되는지 확인
uv run python -c "
from company.core.models import Product
from company.utils.helpers import slugify

product = Product(name='테스트 상품', price=10000)
print(f'상품: {product}')
print(f'슬러그: {slugify(product.name)}')
"
```

## 주요 학습 포인트

1. **`__init__.py` 없음**: `company/` 디렉토리에는 `__init__.py`가 없어야 합니다
2. **독립 배포**: 각 패키지는 별도의 `pyproject.toml`로 독립 배포 가능
3. **통합 import**: `from company.core import ...`, `from company.utils import ...`
4. **hatch 빌드 설정**: `packages = ["src/company"]`로 네임스페이스 루트를 지정
