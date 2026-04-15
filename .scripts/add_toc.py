"""모든 강의 README.md에 TOC(Table of Contents)를 자동 삽입하는 스크립트."""

import re
from pathlib import Path

BASE = Path("/Users/ukkyukang/dev/antigravity/dev-guides")

# 강의 README 파일 목록
READMES = [
    BASE / "01-uv" / "README.md",
    BASE / "02-python-packaging" / "README.md",
    BASE / "03-os-independent-dev" / "README.md",
    BASE / "04-wsl-docker-registry" / "README.md",
    BASE / "05-dockerfile" / "README.md",
    BASE / "06-docker-compose" / "README.md",
    BASE / "07-dev-containers" / "README.md",
    BASE / "08-git" / "README.md",
]

TOC_START = "<!-- TOC -->"
TOC_END = "<!-- /TOC -->"


def slugify(text: str) -> str:
    """헤더 텍스트를 GitHub 앵커 링크로 변환."""
    text = text.lower().strip()
    # 이모지 및 특수문자 제거 (알파벳, 숫자, 한글, 하이픈, 공백 유지)
    text = re.sub(r'[^\w\s가-힣-]', '', text)
    text = re.sub(r'\s+', '-', text)
    text = text.strip('-')
    return text


def extract_headers(content: str) -> list[tuple[int, str]]:
    """마크다운 헤더를 추출 (## ~ ####)."""
    headers = []
    in_code_block = False

    for line in content.split('\n'):
        # 코드 블록 안의 # 무시
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        match = re.match(r'^(#{2,4})\s+(.+)$', line)
        if match:
            level = len(match.group(1))
            title = match.group(2).strip()
            headers.append((level, title))

    return headers


def generate_toc(headers: list[tuple[int, str]]) -> str:
    """헤더 목록에서 TOC 마크다운을 생성."""
    lines = [TOC_START, "## 📑 목차", ""]

    for level, title in headers:
        # TOC 자체의 "목차" 헤더는 건너뛰기
        if title.startswith("📑 목차"):
            continue

        indent = "  " * (level - 2)
        slug = slugify(title)
        # 제목에서 이모지 제거하여 깔끔한 링크 텍스트
        clean_title = title
        lines.append(f"{indent}- [{clean_title}](#{slug})")

    lines.append("")
    lines.append(TOC_END)
    return '\n'.join(lines)


def insert_toc(filepath: Path) -> bool:
    """README에 TOC를 삽입 (기존 TOC가 있으면 교체)."""
    content = filepath.read_text(encoding="utf-8")

    # 헤더 추출
    headers = extract_headers(content)
    if not headers:
        return False

    toc = generate_toc(headers)

    # 기존 TOC가 있으면 교체
    if TOC_START in content:
        pattern = re.compile(
            re.escape(TOC_START) + r'.*?' + re.escape(TOC_END),
            re.DOTALL
        )
        new_content = pattern.sub(toc, content)
    else:
        # 제목(# ...) 바로 다음, --- 구분선 앞에 삽입
        # 패턴: 첫 번째 --- 앞에 삽입
        lines = content.split('\n')
        insert_idx = None

        for i, line in enumerate(lines):
            if line.strip() == '---' and i > 0:
                insert_idx = i
                break

        if insert_idx is None:
            # --- 가 없으면 첫 번째 ## 앞에 삽입
            for i, line in enumerate(lines):
                if line.startswith('## ') and not line.startswith('## 📑'):
                    insert_idx = i
                    break

        if insert_idx is None:
            return False

        lines.insert(insert_idx, "")
        lines.insert(insert_idx + 1, toc)
        lines.insert(insert_idx + 2, "")
        new_content = '\n'.join(lines)

    filepath.write_text(new_content, encoding="utf-8")
    print(f"✅ {filepath.relative_to(BASE)}")
    return True


def main():
    count = 0
    for readme in READMES:
        if readme.exists():
            if insert_toc(readme):
                count += 1
        else:
            print(f"❌ 파일 없음: {readme}")

    print(f"\n총 {count}개 파일에 TOC 삽입 완료")


if __name__ == "__main__":
    main()
