"""Streamlit 앱 — 컨테이너 안에서 개발하기.

이 파일을 수정하고 저장하면, 컨테이너 안의 Streamlit이
자동으로 변경을 감지하여 브라우저를 리로드합니다.
"""

import streamlit as st

from my_app import __version__

st.set_page_config(page_title="Container Dev Demo", page_icon="🐳")

st.title("🐳 컨테이너 안에서 개발하기")
st.caption(f"v{__version__}")

st.markdown("---")

st.header("이 앱은 Docker 컨테이너 안에서 실행되고 있습니다")

st.markdown("""
**핵심 원리:**
1. **이미지에 의존성을 굽는다** → Dockerfile에서 `uv sync`
2. **소스코드는 마운트한다** → `compose.dev.yml`에서 `./src:/app/src`
3. **코드를 수정하면 바로 반영된다** → 지금 이 파일을 수정해 보세요!
""")

st.markdown("---")

# 이 아래를 자유롭게 수정해 보세요!
st.subheader("✏️ 여기를 수정해 보세요")

name = st.text_input("이름을 입력하세요", value="개발자")
st.write(f"안녕하세요, **{name}**님! 👋")

if st.button("🎉 축하합니다"):
    st.balloons()
    st.success("컨테이너 개발 환경이 정상적으로 작동합니다!")
