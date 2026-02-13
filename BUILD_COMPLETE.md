# 🎉 네이버 이미지 크롤러 - 빌드 완료!

## ✅ 완성된 기능

### 1. 크롤러 엔진
- ✅ 네이버 이미지 검색 자동 크롤링
- ✅ 여러 CSS 선택자를 통한 안정적인 이미지 감지
- ✅ 자동 페이지 전환 및 무한 스크롤 지원
- ✅ Headless 모드로 백그라운드 실행 가능

### 2. GUI 인터페이스
- ✅ tkinter 기반 사용자 친화적 인터페이스
- ✅ 단일 키워드 검색
- ✅ 여러 키워드 일괄 검색
- ✅ 실시간 진행률 표시 및 로그
- ✅ 폴더 선택 기능
- ✅ 언제든 중지 가능한 스레드 기반 실행

### 3. ChromeDriver 자동 관리
- ✅ webdriver-manager로 자동 다운로드
- ✅ Chrome 버전 자동 감지
- ✅ 캐시된 드라이버 재사용
- ✅ download_chromedriver.py 유틸리티

### 4. 애플리케이션 빌드
- ✅ PyInstaller로 독립실행 .app 파일 생성
- ✅ macOS 앱 번들 형식 (.app)
- ✅ 커스텀 아이콘 및 파비콘 포함
- ✅ 자동 설치 스크립트

### 5. 아이콘 및 파비콘
- ✅ 256x256 메인 아이콘
- ✅ 다양한 크기 아이콘 (16, 32, 64, 128)
- ✅ macOS용 ICNS 포맷
- ✅ Windows용 ICO 포맷
- ✅ 웹용 파비콘

## 📦 생성된 파일 목록

### 소스 코드
| 파일 | 크기 | 설명 |
|------|------|------|
| `crawler.py` | 11K | 메인 크롤러 클래스 |
| `gui.py` | 13K | GUI 애플리케이션 |
| `download_chromedriver.py` | 3.9K | ChromeDriver 설정 |
| `create_icon.py` | 4.8K | 아이콘 생성 스크립트 |
| `build.py` | 5.0K | 빌드 스크립트 |
| `install.sh` | 2.3K | 설치 스크립트 |
| `examples.py` | 2.1K | 사용 예제 |
| `requirements.txt` | 118B | Python 의존성 |

### 리소스
- `assets/icon.png` - 메인 아이콘 (256x256)
- `assets/icon-*.png` - 다양한 크기
- `assets/icon.icns` - macOS 아이콘
- `assets/icon.ico` - Windows 아이콘
- `assets/favicon.ico` - 웹 파비콘

### 빌드 결과
- `dist/NaverImageCrawler.app/` - **macOS 실행 가능 앱 (48MB)** ⭐
- `dist/NaverImageCrawler/` - 디렉토리 형식 버전

## 🚀 빠른 시작 가이드

### 방법 1️⃣ : GUI 앱 직접 실행 (가장 간편)

```bash
# 빌드된 앱 실행
open dist/NaverImageCrawler.app

# 또는 클릭으로 실행
# dist/NaverImageCrawler.app 더블클릭
```

### 방법 2️⃣ : Applications 폴더에 설치

```bash
# 자동 설치 (권장)
bash install.sh

# 또는 수동 설치
cp -r dist/NaverImageCrawler.app /Applications/

# Spotlight에서 실행
# Cmd + Space → NaverImageCrawler 입력 → Enter
```

### 방법 3️⃣ : Python 스크립트로 실행

```bash
# GUI 버전
python3 gui.py

# 또는 CLI 버전
python3 crawler.py
```

## 📊 시스템 요구사항

- **OS**: macOS 10.13 이상 (또는 Windows/Linux)
- **Python**: 3.7 이상 (소스 코드 실행 시)
- **Chrome 브라우저**: 최신 버전
- **디스크**: 약 200MB (전체 설치)

## 🎯 주요 기능 데모

### 1. GUI로 단일 키워드 검색
```
1. NaverImageCrawler.app 실행
2. 키워드 입력: "고양이"
3. 다운로드 개수: 50
4. "단일 검색" 클릭
5. 진행률 확인 후 완료
```

### 2. 여러 키워드 일괄 검색
```
1. 텍스트 박스에 키워드 입력 (줄 단위)
   고양이
   강아지
   새
2. "일괄 검색" 클릭
3. 순차적으로 검색 진행
```

### 3. 다운로드 폴더 확인
```
downloads/
├── 고양이/
│   ├── 고양이_1.jpg
│   ├── 고양이_2.jpg
│   └── ...
├── 강아지/
│   └── ...
└── ...
```

## 📁 빌드 후 정리

불필요한 파일을 제거하여 용량을 절약할 수 있습니다:

```bash
# 빌드 중간 파일 제거
rm -rf build/ NaverImageCrawler.spec

# 소스 코드 제거 (앱만 남길 경우)
# dist/NaverImageCrawler.app만 필요함
```

## 🛠️ 커스터마이징

### 앱 아이콘 변경
1. `create_icon.py`를 편집하여 색상 변경
2. `python3 create_icon.py` 실행
3. `python3 build.py`로 다시 빌드

### 앱 이름 변경
1. `build.py`의 `--name=NaverImageCrawler` 수정
2. `python3 build.py` 실행

### 더 작은 빌드
```python
# build.py에서 `--onefile` 옵션 사용 (Windows/Linux)
# macOS에서는 자동으로 최적화됨
```

## 📚 추가 문서

- [README.md](README.md) - 상세 사용 설명서
- [examples.py](examples.py) - 코드 예제

## 🐛 문제 해결

### "앱이 손상되었습니다" 오류 (macOS)
```bash
# 다음 명령 실행
xattr -rd com.apple.quarantine /Applications/NaverImageCrawler.app
```

### ChromeDriver 버전 불일치
```bash
# 캐시 삭제
rm -rf ~/.wdm/

# 다시 실행하면 최신 버전 자동 다운로드
```

### GUI가 응답하지 않음
- 진행 중인 크롤링이 있는지 확인
- "중지" 버튼으로 중지한 후 다시 실행

## 📝 라이선스

이 프로젝트는 교육 목적으로 제공됩니다.

## 🎓 기술 스택

- **언어**: Python 3.14
- **웹 크롤링**: Selenium 4.40
- **GUI**: tkinter
- **빌드**: PyInstaller 6.18
- **이미지 처리**: Pillow
- **HTTP 요청**: Requests
- **드라이버 관리**: webdriver-manager

## 📞 지원

문제가 발생하면:
1. README.md의 문제 해결 섹션 확인
2. download_chromedriver.py로 ChromeDriver 설정 확인
3. Chrome 브라우저 설치 확인

---

**빌드 완료 일시**: 2026년 2월 13일  
**빌드 버전**: 1.0.0
