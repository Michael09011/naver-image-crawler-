#!/bin/bash
#
# 네이버 이미지 크롤러 - 설치 및 배포 스크립트
#

set -e

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
APP_NAME="NaverImageCrawler"
DIST_DIR="$PROJECT_DIR/dist"
APP_PATH="$DIST_DIR/$APP_NAME.app"
APPLICATIONS_DIR="/Applications"

echo "============================================================"
echo "네이버 이미지 크롤러 - 애플리케이션 설치"
echo "============================================================"
echo ""

# 빌드 파일 확인
if [ ! -d "$APP_PATH" ]; then
    echo "❌ 오류: $APP_PATH를 찾을 수 없습니다."
    echo "먼저 다음을 실행하세요:"
    echo "  python3 build.py"
    exit 1
fi

echo "📦 빌드된 애플리케이션: $APP_PATH"
echo "크기: $(du -sh "$APP_PATH" | cut -f1)"
echo ""

# 기존 앱 확인
if [ -d "$APPLICATIONS_DIR/$APP_NAME.app" ]; then
    echo "⚠️  기존 애플리케이션을 찾았습니다."
    echo "   경로: $APPLICATIONS_DIR/$APP_NAME.app"
    read -p "제거 후 다시 설치하시겠습니까? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "기존 애플리케이션 제거 중..."
        sudo rm -rf "$APPLICATIONS_DIR/$APP_NAME.app"
        echo "✓ 제거됨"
    else
        echo "설치를 취소했습니다."
        exit 0
    fi
fi

# 애플리케이션 설치
echo ""
echo "🔧 설치 중..."
echo "   $APP_PATH → $APPLICATIONS_DIR/"
cp -r "$APP_PATH" "$APPLICATIONS_DIR/"

# 권한 설정
chmod +x "$APPLICATIONS_DIR/$APP_NAME.app/Contents/MacOS/$APP_NAME"

# 론치패드 업데이트
echo "💾 론치패드 업데이트 중..."
defaults write com.apple.dock RecentlyUsedApps -array-add "{name=$APP_NAME; path=$APPLICATIONS_DIR/$APP_NAME.app/;}"
killall Dock 2>/dev/null || true

echo ""
echo "============================================================"
echo "✅ 설치 완료!"
echo "============================================================"
echo ""
echo "📍 설치 위치: $APPLICATIONS_DIR/$APP_NAME.app"
echo ""
echo "🚀 실행 방법:"
echo "   1. Spotlight 검색: Cmd + Space → NaverImageCrawler 검색"
echo "   2. Finder → Applications → NaverImageCrawler.app 더블클릭"
echo "   3. 터미널: open /Applications/$APP_NAME.app"
echo ""
echo "삭제 방법:"
echo "   Finder → Applications → $APP_NAME.app → 휴지통으로 이동"
echo ""
