"""범용 유틸리티 함수 모음.

문자열 처리, 데이터 변환 등 공통 유틸리티를 제공합니다.
"""

import re
import unicodedata


def slugify(text: str) -> str:
    """텍스트를 URL 친화적인 슬러그로 변환합니다.

    Args:
        text: 변환할 텍스트

    Returns:
        슬러그 문자열

    Example:
        >>> slugify("Hello World!")
        'hello-world'
        >>> slugify("  Multiple   Spaces  ")
        'multiple-spaces'
    """
    # 소문자로 변환
    text = text.lower().strip()
    # 특수문자를 하이픈으로 대체 (유니코드 문자는 유지)
    text = re.sub(r"[^\w\s-]", "", text)
    # 연속된 공백/하이픈을 단일 하이픈으로
    text = re.sub(r"[-\s]+", "-", text)
    # 앞뒤 하이픈 제거
    return text.strip("-")


def truncate(text: str, max_length: int = 50, suffix: str = "...") -> str:
    """텍스트를 지정된 길이로 자릅니다.

    Args:
        text: 자를 텍스트
        max_length: 최대 길이 (suffix 포함)
        suffix: 잘린 경우 추가할 접미사

    Returns:
        잘린 텍스트

    Example:
        >>> truncate("이것은 매우 긴 텍스트입니다", max_length=10)
        '이것은 매우 ...'
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def chunk_list(items: list, chunk_size: int) -> list[list]:
    """리스트를 지정된 크기의 청크로 나눕니다.

    Args:
        items: 나눌 리스트
        chunk_size: 청크 크기

    Returns:
        청크 리스트

    Example:
        >>> chunk_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """
    return [items[i : i + chunk_size] for i in range(0, len(items), chunk_size)]


def flatten(nested: list) -> list:
    """중첩된 리스트를 1차원으로 펼칩니다.

    Args:
        nested: 중첩 리스트

    Returns:
        펼쳐진 리스트

    Example:
        >>> flatten([[1, 2], [3, [4, 5]]])
        [1, 2, 3, 4, 5]
    """
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result
