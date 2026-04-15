"""핵심 데이터 모델 정의.

조직 전체에서 공유하는 공통 모델을 정의합니다.
다른 company.* 패키지에서 이 모델들을 import하여 사용합니다.
"""

from pydantic import BaseModel, field_validator


class Product(BaseModel):
    """상품 모델.

    Attributes:
        name: 상품명
        price: 가격 (원)
        category: 카테고리 (기본값: "general")

    Example:
        >>> product = Product(name="키보드", price=150000)
        >>> product.formatted_price
        '₩150,000'
    """

    name: str
    price: int
    category: str = "general"

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: int) -> int:
        """가격은 양수여야 합니다."""
        if v < 0:
            raise ValueError("가격은 0 이상이어야 합니다")
        return v

    @property
    def formatted_price(self) -> str:
        """원화 형식으로 가격을 반환합니다."""
        return f"₩{self.price:,}"


class Order(BaseModel):
    """주문 모델.

    Attributes:
        order_id: 주문 번호
        products: 주문 상품 목록
        customer_name: 고객명
    """

    order_id: str
    products: list[Product]
    customer_name: str

    @property
    def total_price(self) -> int:
        """총 주문 금액을 계산합니다."""
        return sum(p.price for p in self.products)

    @property
    def formatted_total(self) -> str:
        """원화 형식으로 총 금액을 반환합니다."""
        return f"₩{self.total_price:,}"
