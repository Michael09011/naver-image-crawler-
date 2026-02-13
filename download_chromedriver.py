"""
ChromeDriver 자동 다운로드 및 설치 스크립트
"""

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager


def get_chrome_version():
    """설치된 Chrome 버전 확인"""
    try:
        if sys.platform == "darwin":  # macOS
            result = subprocess.run([
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "--version"
            ], capture_output=True, text=True)
        elif sys.platform == "win32":  # Windows
            result = subprocess.run([
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "--version"
            ], capture_output=True, text=True)
        else:  # Linux
            result = subprocess.run([
                "google-chrome",
                "--version"
            ], capture_output=True, text=True)
        
        version_string = result.stdout.strip()
        print(f"Chrome 버전: {version_string}")
        return version_string
    
    except Exception as e:
        print(f"Chrome 버전 확인 실패: {e}")
        return None


def download_chromedriver():
    """ChromeDriver 다운로드"""
    print("\n=== ChromeDriver 다운로드 시작 ===")
    
    try:
        # Chrome 버전 확인
        chrome_version = get_chrome_version()
        
        # ChromeDriver 다운로드
        print("ChromeDriver 다운로드 중...")
        driver_path = ChromeDriverManager().install()
        
        print(f"\n✅ ChromeDriver 다운로드 완료!")
        print(f"위치: {driver_path}")
        
        # 현재 프로젝트에도 복사
        local_driver_path = os.path.join(
            os.path.dirname(__file__),
            "chromedriver"
        )
        
        shutil.copy(driver_path, local_driver_path)
        os.chmod(local_driver_path, 0o755)
        
        print(f"프로젝트 폴더에도 복사: {local_driver_path}")
        
        return driver_path
    
    except Exception as e:
        print(f"❌ ChromeDriver 다운로드 실패: {e}")
        print("webdriver-manager가 자동으로 관리합니다.")
        return None


def setup_driver_info():
    """드라이버 정보 출력"""
    print("\n=== ChromeDriver 설정 정보 ===")
    print(f"OS: {platform.system()}")
    print(f"Python 버전: {sys.version.split()[0]}")
    print(f"플랫폼: {platform.platform()}")
    
    # 캐시 경로 (일반적인 위치)
    if sys.platform == "darwin":
        cache_path = os.path.expanduser("~/.wdm/drivers/chromedriver")
    elif sys.platform == "win32":
        cache_path = os.path.expanduser("~\\AppData\\Local\\wdm\\drivers\\chromedriver")
    else:
        cache_path = os.path.expanduser("~/.wdm/drivers/chromedriver")
    
    print(f"캐시 경로: {cache_path}")
    
    # 이미 다운로드된 드라이버 확인
    if os.path.exists(cache_path):
        try:
            drivers = os.listdir(cache_path)
            print(f"캐시된 드라이버: {len(drivers)}개")
            for driver in drivers[:5]:  # 처음 5개만 표시
                print(f"  - {driver}")
        except Exception as e:
            print(f"캐시 확인 실패: {e}")


def main():
    """메인 함수"""
    print("=" * 50)
    print("네이버 이미지 크롤러 - ChromeDriver 설정")
    print("=" * 50)
    
    try:
        setup_driver_info()
        download_chromedriver()
        
        print("\n" + "=" * 50)
        print("✅ 설정 완료!")
        print("=" * 50)
        print("\n이제 crawler.py를 실행할 수 있습니다:")
        print("  python3 crawler.py")
        print("  또는")
        print("  python3 gui.py  (GUI 버전)")
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
