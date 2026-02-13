"""
네이버 이미지 크롤러 - PyInstaller 빌드 스크립트
"""

import subprocess
import os
import sys
import shutil
from pathlib import Path


def get_platform():
    """현재 플랫폼 반환"""
    if sys.platform == "darwin":
        return "macOS"
    elif sys.platform == "win32":
        return "Windows"
    else:
        return "Linux"


def build_application():
    """PyInstaller를 사용한 애플리케이션 빌드"""
    
    project_dir = "/Users/michael/Workspace/naver-image-crawler"
    assets_dir = os.path.join(project_dir, "assets")
    gui_file = os.path.join(project_dir, "gui.py")
    
    # 아이콘 경로
    if sys.platform == "darwin":
        icon_file = os.path.join(assets_dir, "icon.icns")
    elif sys.platform == "win32":
        icon_file = os.path.join(assets_dir, "icon.ico")
    else:
        icon_file = os.path.join(assets_dir, "icon.png")
    
    print("=" * 60)
    print("네이버 이미지 크롤러 - 애플리케이션 빌드")
    print("=" * 60)
    print(f"플랫폼: {get_platform()}")
    print(f"프로젝트: {project_dir}")
    print(f"GUI 파일: {gui_file}")
    print(f"아이콘: {icon_file}")
    print()
    
    # PyInstaller 명령 구성
    cmd = [
        "pyinstaller",
        "--windowed",                         # GUI 모드 (콘솔 창 숨김)
        "--add-data", f"assets:assets",       # 아이콘 포함
        "--add-data", f"downloads:downloads", # 다운로드 폴더 포함
        f"--icon={icon_file}",               # 아이콘 설정
        "--name=NaverImageCrawler",          # 애플리케이션 이름
        gui_file
    ]
    
    # macOS 특정 설정
    if sys.platform == "darwin":
        # macOS에서는 .app 번들 생성 (onefile은 제외)
        cmd.extend([
            "--osx-bundle-identifier=com.naver.imagecrawler"  # macOS Bundle ID
        ])
    else:
        # 다른 OS에서는 onefile 옵션 사용
        cmd.insert(1, "--onefile")
    
    print("빌드 명령:")
    print(" ".join(cmd))
    print()
    
    try:
        print("🔨 빌드 시작 중...")
        result = subprocess.run(cmd, cwd=project_dir, check=True)
        
        print("\n" + "=" * 60)
        print("✅ 빌드 완료!")
        print("=" * 60)
        
        # 빌드 결과 확인
        dist_dir = os.path.join(project_dir, "dist")
        build_dir = os.path.join(project_dir, "build")
        
        if os.path.exists(dist_dir):
            print(f"\n📦 빌드 결과 (dist 폴더):")
            for item in os.listdir(dist_dir):
                item_path = os.path.join(dist_dir, item)
                if os.path.isfile(item_path):
                    size_mb = os.path.getsize(item_path) / (1024 * 1024)
                    print(f"  ✓ {item} ({size_mb:.1f} MB)")
                elif os.path.isdir(item_path):
                    print(f"  📁 {item}/")
        
        # 실행 명령 제시
        print(f"\n🚀 실행 방법:")
        if sys.platform == "darwin":
            print(f"  open dist/NaverImageCrawler.app")
        elif sys.platform == "win32":
            print(f"  dist\\NaverImageCrawler.exe")
        else:
            print(f"  ./dist/NaverImageCrawler")
        
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 빌드 실패!")
        print(f"오류: {e}")
        return False
    
    except Exception as e:
        print(f"\n❌ 오류 발생: {e}")
        return False


def cleanup_build_files():
    """빌드 중간 파일 정리"""
    project_dir = "/Users/michael/Workspace/naver-image-crawler"
    
    cleanup_items = [
        os.path.join(project_dir, "build"),
        os.path.join(project_dir, "*.spec"),
    ]
    
    print("\n정리 중...")
    for item in cleanup_items:
        if "*" in item:
            # glob 패턴 처리
            import glob
            for file in glob.glob(item):
                try:
                    os.remove(file)
                    print(f"  ✓ {os.path.basename(file)} 삭제됨")
                except:
                    pass
        else:
            if os.path.exists(item):
                try:
                    shutil.rmtree(item)
                    print(f"  ✓ {os.path.basename(item)} 삭제됨")
                except Exception as e:
                    print(f"  ⚠️ {os.path.basename(item)} 삭제 실패: {e}")


def main():
    """메인 함수"""
    
    # 아이콘 확인
    assets_dir = "/Users/michael/Workspace/naver-image-crawler/assets"
    if not os.path.exists(assets_dir):
        print("❌ assets 폴더가 없습니다.")
        print("먼저 create_icon.py를 실행하세요:")
        print("  python3 create_icon.py")
        sys.exit(1)
    
    # 빌드 실행
    success = build_application()
    
    # 정리 (선택사항)
    cleanup_build_files()
    
    if success:
        print("\n" + "=" * 60)
        print("빌드 완료!")
        print("=" * 60)
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
