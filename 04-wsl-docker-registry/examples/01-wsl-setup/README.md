# WSL2 설정 체크리스트

WSL2 개발 환경을 처음 설정할 때 참고하세요.

## 설치 순서

```powershell
# 1. Windows Terminal 설치 (Microsoft Store에서)
# 2. WSL 설치
wsl --install -d Ubuntu-24.04
# 3. 재부팅 후 Ubuntu 사용자 설정
```

## Ubuntu 초기 설정 스크립트

```bash
#!/bin/bash
# setup.sh — WSL2 Ubuntu 초기 설정

set -e

echo "📦 패키지 업데이트..."
sudo apt update && sudo apt upgrade -y

echo "🔧 개발 도구 설치..."
sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    unzip \
    jq \
    tree

echo "🐍 uv 설치..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env

echo "🐍 Python 3.12 설치..."
uv python install 3.12

echo "⚙️ Git 설정..."
git config --global core.autocrlf input
git config --global init.defaultBranch main

echo "✅ 설정 완료!"
echo "   Python: $(uv run python --version)"
echo "   Git:    $(git --version)"
echo "   uv:     $(uv --version)"
```

## 핵심 주의사항

1. **프로젝트는 ~/projects/에 저장** (/mnt/c/ 사용 금지)
2. **Git autocrlf = input** 으로 설정 (CRLF 방지)
3. **VS Code에서 `code .`** 로 WSL 프로젝트 열기
