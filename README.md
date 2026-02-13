# 네이버 이미지 크롤러
<img width="1012" height="840" alt="스크린샷 2026-02-13 오후 2 37 51" src="https://github.com/user-attachments/assets/eaff0769-bd33-48e9-bc89-237095dcad28" />


네이버 이미지 검색 결과를 자동으로 다운로드하는 Python 크롤러입니다. **GUI 버전과 CLI 버전**을 모두 제공합니다.

## 주요 기능

✅ **GUI 인터페이스** - 마우스 클릭으로 검색  
✅ **일괄 검색** - 여러 키워드 동시 처리  
✅ **자동 ChromeDriver 관리** - 복잡한 설정 없음  
✅ **진행률 표시** - 실시간 로그 및 진행 상황 확인  
✅ **Headless 모드** - 백그라운드에서 빠르게 실행  
✅ **독립실행 앱** - PyInstaller로 빌드한 .app 파일 포함

## 설치

### 1. 패키지 설치

```bash
cd /Users/michael/Workspace/naver-image-crawler
pip install -r requirements.txt
```

### 2. ChromeDriver 자동 설정 (선택사항)

```bash
python3 download_chromedriver.py
```

> 💡 참고: `webdriver-manager`가 ChromeDriver를 자동으로 관리하므로 수동 설치는 선택사항입니다.

## 🎯 빠른 시작

### 방법 1: 독립실행 앱 (macOS) - 가장 간편함 ⭐⭐⭐

빌드된 `NaverImageCrawler.app` 사용:

```bash
# 1단계: Applications 폴더에 설치
bash install.sh

# 또는 직접 실행
open dist/NaverImageCrawler.app
```

또는 Finder에서 `dist/NaverImageCrawler.app` 더블클릭

### 방법 2: GUI 버전 (권장) ⭐⭐

```bash
python3 gui.py
```

**GUI 기능:**
- 🔍 단일 키워드 검색
- 📋 여러 키워드 일괄 검색
- 📊 진행률 실시간 표시
- 🛑 언제든지 중지 가능
- 📁 저장 폴더 선택

### 방법 2: 터미널 (CLI 버전)

```bash
python3 crawler.py
```

코드에서 키워드를 수정해야 합니다:

```python
if __name__ == "__main__":
    crawler = NaverImageCrawler(headless=False)
    
    try:
        crawler.crawl_images(keyword="강아지", num_images=100)
    finally:
        crawler.close()
```

### 방법 3: Python 스크립트에서 사용

```python
from crawler import NaverImageCrawler

# 크롤러 초기화
crawler = NaverImageCrawler(headless=True)  # 백그라운드 실행

try:
    # 이미지 크롤링
    crawler.crawl_images(
        keyword="고양이",
        num_images=100,
        save_dir="downloads"
    )
finally:
    crawler.close()
```

## 폴더 구조

```
naver-image-crawler/
├── crawler.py                 # 메인 크롤러 클래스
├── gui.py                     # GUI 애플리케이션
├── download_chromedriver.py   # ChromeDriver 다운로드 유틸리티
├── create_icon.py             # 아이콘 생성 스크립트
├── build.py                   # 애플리케이션 빌드 스크립트
├── install.sh                 # 설치 스크립트 (macOS)
├── examples.py                # 사용 예제
├── requirements.txt           # Python 의존성
├── README.md                  # 이 파일
├── assets/                    # 아이콘 리소스
│   ├── icon.png
│   ├── icon.icns              # macOS 아이콘
│   ├── icon.ico               # Windows 아이콘
│   ├── favicon.ico            # 파비콘
│   └── ...
├── dist/                      # 빌드된 애플리케이션
│   ├── NaverImageCrawler.app  # macOS 앱
│   └── NaverImageCrawler/     # 디렉토리 버전
└── downloads/                 # 다운로드된 이미지 저장 위치
    ├── 고양이/
    ├── 강아지/
    └── ...
```

## 🏗️ 애플리케이션 빌드

Python 소스 코드를 독립실행 가능한 macOS 앱으로 빌드할 수 있습니다.

### 빌드 전 준비

```bash
# PyInstaller 설치
pip install pyinstaller pillow
```

### 빌드 실행

```bash
# 1. 아이콘 생성 (첫 빌드 시에만)
python3 create_icon.py

# 2. 애플리케이션 빌드
python3 build.py
```

### 빌드 결과

빌드가 완료되면:
- `dist/NaverImageCrawler.app` - macOS 실행 가능 앱 (48MB)
- `dist/NaverImageCrawler/` - 실행 파일 디렉토리

### 애플리케이션 설치 (macOS)

```bash
# 자동 설치 스크립트 사용
bash install.sh

# 또는 수동 설치
cp -r dist/NaverImageCrawler.app /Applications/

# 또는 직접 실행
open dist/NaverImageCrawler.app
```

### Spotlight 검색으로 실행

앱을 Applications 폴더에 설치한 후:

```bash
# Cmd + Space → "NaverImageCrawler" 검색 → Enter
```

### 삭제

```bash
# Finder → Applications → NaverImageCrawler.app → 휴지통으로 이동
# 또는 터미널
rm -rf /Applications/NaverImageCrawler.app
```

### 아이콘 커스터마이징

[create_icon.py](create_icon.py)를 수정하여 아이콘을 변경할 수 있습니다:

```python
def create_icon(size=256):
    # 배경색 변경
    bg_color = (0, 150, 76)  # RGB 값 (네이버 그린)
    
    # 텍스트 색상 변경
    text_color = (255, 255, 255)  # 흰색
    
    # 악센트 색상 변경
    accent_color = (255, 195, 0)  # 금색
```

## 옵션 설정

### NaverImageCrawler 옵션

```python
crawler = NaverImageCrawler(headless=False)
```

- `headless=True`: 브라우저 창 없이 백그라운드에서 실행 (더 빠름)
- `headless=False`: 브라우저 창을 보며 실행

### crawl_images() 옵션

```python
crawler.crawl_images(
    keyword="검색어",           # 검색 키워드
    num_images=50,            # 다운로드할 이미지 개수
    save_dir="downloads"      # 저장 디렉토리
)
```

## ChromeDriver 정보

### 자동 관리
`webdriver-manager` 라이브러리가 다음을 자동으로 처리합니다:
- 현재 Chrome 버전 감지
- 일치하는 ChromeDriver 다운로드
- 캐시된 드라이버 사용

### 캐시 위치
```
macOS: ~/.wdm/drivers/chromedriver
Windows: ~\AppData\Local\wdm\drivers\chromedriver
Linux: ~/.wdm/drivers/chromedriver
```

### 수동 설정 (선택사항)
1. [ChromeDriver 다운로드](https://chromedriver.chromium.org/)
   - 자신의 Chrome 버전에 맞는 드라이버 선택

2. 설치:
   ```bash
   # macOS
   chmod +x chromedriver
   mv chromedriver /usr/local/bin/
   
   # 또는 프로젝트 폴더에 저장
   mv chromedriver ./
   ```

## 주의사항

### ⚠️ 법률 및 윤리
- 다운로드한 이미지는 **개인 용도에만** 사용하세요
- **저작권을 존중**하고 필요시 출처를 명시하세요
- 네이버 이용약관을 준수하세요

### ⚠️ 성능
- 너무 많은 이미지를 한 번에 다운로드하지 마세요
- 크롤러는 요청 간에 적절한 지연을 두고 있습니다
- 서버 부하를 고려해 과도한 요청을 피하세요

## 문제 해결

### ChromeDriver 버전 불일치
```
SessionNotCreatedException: Message: session not created
```

**해결책:**
```bash
# 캐시된 드라이버 삭제
rm -rf ~/.wdm/

# 다시 실행하면 자동으로 다시 다운로드됩니다
python3 gui.py
```

### 이미지 로드 실패
- 인터넷 연결 확인
- 네이버 서버 상태 확인
- 검색 키워드가 유효한지 확인

### GUI가 실행되지 않음
```bash
# X11 디스플레이 문제 (원격 서버의 경우)
# 대신 headless CLI 버전 사용
python3 crawler.py
```

## 성능 최적화

### 빠른 크롤링
```python
# 1. Headless 모드 사용
crawler = NaverImageCrawler(headless=True)

# 2. 스크롤 횟수 감소 (소스 수정)
crawler.scroll_and_load_images(num_scrolls=3)

# 3. 요청 간 지연 감소 (소스 수정)
time.sleep(0.2)  # 기본값: 0.3
```

### 안정적인 크롤링
```python
# 스크롤 횟수 증가로 더 많은 이미지 로드
crawler.scroll_and_load_images(num_scrolls=10)
```

## 예제

### 예제 1: 단일 키워드
```python
from crawler import NaverImageCrawler

crawler = NaverImageCrawler(headless=True)
try:
    crawler.crawl_images("벚꽃", num_images=50)
finally:
    crawler.close()
```

### 예제 2: 여러 키워드
```python
from crawler import NaverImageCrawler

keywords = ["고양이", "강아지", "새"]

for keyword in keywords:
    crawler = NaverImageCrawler(headless=True)
    try:
        crawler.crawl_images(keyword, num_images=30)
    finally:
        crawler.close()
```

더 많은 예제는 `examples.py`를 참고하세요.

## 라이선스

이 프로젝트는 교육 목적으로 제공됩니다.

## 지원

문제가 발생하면 다음을 확인하세요:
1. Python 3.7 이상 설치 확인
2. 모든 패키지 설치 확인: `pip list`
3. 인터넷 연결 확인
4. Chrome 브라우저 설치 확인
