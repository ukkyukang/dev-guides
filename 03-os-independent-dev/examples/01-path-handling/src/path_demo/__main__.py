"""path_demo를 python -m path_demo로 실행합니다."""

from path_demo.utils import get_config_path, get_data_path, get_system_info

print("🖥️  시스템 정보")
print("=" * 40)
for key, value in get_system_info().items():
    print(f"  {key:12s}: {value}")

print()
print("📁 OS별 경로")
print("=" * 40)
print(f"  설정 경로: {get_config_path()}")
print(f"  데이터 경로: {get_data_path()}")
