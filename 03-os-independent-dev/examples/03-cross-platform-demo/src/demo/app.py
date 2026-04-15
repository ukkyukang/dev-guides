"""크로스 플랫폼 개발 요소 통합 데모 — Streamlit 앱.

pathlib, platformdirs, pydantic-settings, shutil을 모두 사용하여
OS 독립적 코드의 실제 동작을 시각적으로 보여줍니다.

실행:
    uv run streamlit run src/demo/app.py
"""

import platform
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st
from platformdirs import user_cache_dir, user_config_dir, user_data_dir, user_log_dir

from demo import __version__
from demo.settings import AppSettings

# ============================================================
# 페이지 설정
# ============================================================
st.set_page_config(
    page_title="크로스 플랫폼 데모",
    page_icon="🌍",
    layout="wide",
)

st.title("🌍 OS Independent 개발 — 통합 데모")
st.caption(f"v{__version__} · Python {platform.python_version()} · {platform.system()} {platform.release()}")
st.markdown("---")

# ============================================================
# 1. 현재 OS 정보
# ============================================================
st.header("1️⃣ 현재 시스템 정보")

col1, col2, col3 = st.columns(3)

with col1:
    os_name = platform.system()
    os_emoji = {"Windows": "🪟", "Darwin": "🍎", "Linux": "🐧"}.get(os_name, "❓")
    st.metric("OS", f"{os_emoji} {os_name}")

with col2:
    st.metric("Python", platform.python_version())

with col3:
    st.metric("Architecture", platform.machine())

with st.expander("상세 시스템 정보"):
    st.json({
        "platform": platform.platform(),
        "python_executable": sys.executable,
        "home": str(Path.home()),
        "cwd": str(Path.cwd()),
        "temp_dir": tempfile.gettempdir(),
        "encoding_default": sys.getdefaultencoding(),
        "filesystem_encoding": sys.getfilesystemencoding(),
    })

st.markdown("---")

# ============================================================
# 2. platformdirs — OS별 표준 디렉토리
# ============================================================
st.header("2️⃣ platformdirs — OS별 표준 디렉토리 매핑")

st.info(
    "💡 `platformdirs`는 앱 이름만 주면 각 OS의 표준 규약에 맞는 디렉토리를 자동으로 반환합니다. "
    "하드코딩(`C:\\temp` 또는 `/tmp`) 없이도 어떤 OS에서든 안전하게 동작합니다."
)

app_input = st.text_input("앱 이름을 입력하세요", value="MyApp")

dirs_data = {
    "구분": ["📁 Config", "💾 Data", "⚡ Cache", "📝 Log"],
    "용도": [
        "설정 파일 (settings.json)",
        "앱 데이터 (DB, 사용자 파일)",
        "캐시 (지워져도 괜찮은 임시 데이터)",
        "로그 파일",
    ],
    "함수": [
        "user_config_dir()",
        "user_data_dir()",
        "user_cache_dir()",
        "user_log_dir()",
    ],
    f"현재 OS ({platform.system()}) 경로": [
        user_config_dir(app_input),
        user_data_dir(app_input),
        user_cache_dir(app_input),
        user_log_dir(app_input),
    ],
}

st.table(dirs_data)

with st.expander("💻 다른 OS에서는 어떻게 될까?"):
    st.markdown(f"""
| 디렉토리 | Windows | macOS | Linux (Docker) |
|---------|---------|-------|----------------|
| **Config** | `C:\\Users\\user\\AppData\\Local\\{app_input}` | `~/Library/Application Support/{app_input}` | `~/.config/{app_input}` |
| **Data** | `C:\\Users\\user\\AppData\\Local\\{app_input}` | `~/Library/Application Support/{app_input}` | `~/.local/share/{app_input}` |
| **Cache** | `C:\\Users\\user\\AppData\\Local\\{app_input}\\Cache` | `~/Library/Caches/{app_input}` | `~/.cache/{app_input}` |
| **Log** | `C:\\Users\\user\\AppData\\Local\\{app_input}\\Log` | `~/Library/Logs/{app_input}` | `~/.local/state/{app_input}/log` |
    """)

st.markdown("---")

# ============================================================
# 3. pydantic-settings — 환경 변수 + .env 관리
# ============================================================
st.header("3️⃣ pydantic-settings — 타입 안전한 설정 관리")

st.info(
    "💡 `pydantic-settings`는 `.env` 파일과 시스템 환경 변수를 자동으로 읽고, "
    "타입 변환/검증까지 해줍니다. `os.environ.get()`을 직접 쓸 필요가 없습니다."
)

try:
    settings = AppSettings()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("로드된 설정값")
        st.json({
            "app_name": settings.app_name,
            "debug": settings.debug,
            "port": settings.port,
            "database_url": settings.database_url,
            "log_level": settings.log_level,
            "secret_key": settings.secret_key[:8] + "..." if len(settings.secret_key) > 8 else settings.secret_key,
        })

    with col2:
        st.subheader("타입 검증 결과")
        st.markdown(f"""
| 필드 | 값 | 타입 | 자동 변환 |
|------|-----|------|---------|
| `app_name` | `{settings.app_name}` | `{type(settings.app_name).__name__}` | str → str |
| `debug` | `{settings.debug}` | `{type(settings.debug).__name__}` | "true"/"false" → bool ✅ |
| `port` | `{settings.port}` | `{type(settings.port).__name__}` | "8501" → int ✅ |
| `log_level` | `{settings.log_level}` | `{type(settings.log_level).__name__}` | str → str |
        """)

    with st.expander("📄 .env 파일 만들어보기 (설정 변경 테스트)"):
        st.markdown("""
프로젝트 루트에 `.env` 파일을 생성하고 아래 내용을 저장한 뒤 새로고침 하세요:

```
APP_NAME=내프로젝트
DEBUG=true
PORT=3000
DATABASE_URL=postgresql://user:pass@localhost/mydb
LOG_LEVEL=DEBUG
SECRET_KEY=super-secret-key-12345
```

→ 설정값이 자동으로 바뀌는 것을 확인할 수 있습니다!
        """)

except Exception as e:
    st.error(f"❌ 설정 로드 실패: {e}")
    st.markdown("→ 필수 환경 변수가 누락되었거나 타입이 잘못되었습니다. pydantic이 즉시 잡아냅니다!")

st.markdown("---")

# ============================================================
# 4. pathlib — 경로 처리 + 인코딩 방어
# ============================================================
st.header("4️⃣ pathlib — 경로 처리 + UTF-8 인코딩 방어")

col1, col2 = st.columns(2)

with col1:
    st.subheader("경로 연산 데모")

    base = Path("src") / "my_package" / "config.json"
    st.code(f"""
from pathlib import Path

path = Path("src") / "my_package" / "config.json"

path.name     = "{base.name}"
path.stem     = "{base.stem}"
path.suffix   = "{base.suffix}"
path.parent   = "{base.parent}"
path.parts    = {base.parts}
    """, language="python")

with col2:
    st.subheader("UTF-8 파일 쓰기/읽기 테스트")

    test_text = st.text_area("한글을 입력하세요 (인코딩 테스트)", value="안녕하세요! 🇰🇷\n크로스 플랫폼 테스트입니다.")

    if st.button("✍️ 파일 쓰기 + 읽기 테스트"):
        tmp_dir = Path(tempfile.gettempdir()) / "cross-platform-demo"
        tmp_dir.mkdir(parents=True, exist_ok=True)
        test_file = tmp_dir / "encoding_test.txt"

        # pathlib으로 UTF-8 명시적 쓰기
        test_file.write_text(test_text, encoding="utf-8")

        # 다시 읽기
        read_back = test_file.read_text(encoding="utf-8")

        if read_back == test_text:
            st.success(f"✅ UTF-8 쓰기/읽기 성공!")
            st.code(f"저장 위치: {test_file}", language="text")
        else:
            st.error("❌ 인코딩 불일치!")

st.markdown("---")

# ============================================================
# 5. shutil.which — 시스템 도구 확인
# ============================================================
st.header("5️⃣ shutil.which — 시스템 도구 설치 확인")

tools = ["python", "git", "uv", "docker", "node", "code", "npm", "kubectl"]

cols = st.columns(4)
for i, tool in enumerate(tools):
    with cols[i % 4]:
        found = shutil.which(tool)
        if found:
            st.success(f"✅ `{tool}`")
            st.caption(f"{found}")
        else:
            st.error(f"❌ `{tool}`")
            st.caption("미설치")

st.markdown("---")

# ============================================================
# 요약
# ============================================================
st.header("📊 요약: 레거시 vs 모던")

st.markdown("""
| 작업 | ❌ 레거시 | ✅ 모던 (이 데모) |
|------|---------|-------------------|
| 경로 합치기 | `os.path.join("a", "b")` | `Path("a") / "b"` |
| 파일 읽기 | `open("f.txt")` | `Path("f.txt").read_text(encoding="utf-8")` |
| 로그 경로 | `"C:\\\\temp\\\\log"` 하드코딩 | `user_log_dir("MyApp")` |
| 환경 변수 | `os.environ.get("PORT")` | `AppSettings().port` (타입 검증 포함) |
| 명령 찾기 | `os.system("which git")` | `shutil.which("git")` |

**핵심**: 위 테이블의 "모던" 방식은 코드 한 글자 수정 없이 Windows에서도 Docker에서도 동작합니다.
""")
