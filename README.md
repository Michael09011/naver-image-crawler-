***
# Google Image Crawler

![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.14-blue)
![License](https://img.shields.io/badge/license-Educational-lightgrey)

Google Image Crawler는 Google 이미지 검색 결과에서 이미지를 자동으로 다운로드하는 Python 도구입니다. GUI(`gui.py`)와 CLI(`crawler.py`)를 제공합니다.

## 주요 기능

- GUI 기반 실행 및 일괄 검색 지원
- Headless 모드(브라우저 창 없이 실행)
- 자동 ChromeDriver 관리(`webdriver-manager` 사용)
- PyInstaller로 독립 실행형 macOS 앱 빌드

## 설치

1. 리포지토리 루트로 이동

```bash
cd path/to/google-image-crawler-
```

2. 의존성 설치

```bash
python3 -m pip install -r requirements.txt
```

3. (선택) ChromeDriver 수동 설정

```bash
python3 download_chromedriver.py
```

> 참고: `webdriver-manager`가 ChromeDriver를 자동으로 관리하므로 수동 설치는 보통 필요하지 않습니다.

## 빠른 시작

### GUI 실행

```bash
python3 gui.py
```

### CLI 실행 (스크립트)

```bash
python3 crawler.py
```

`crawler.py`의 `main()`에서 키워드, 이미지 개수 등을 설정할 수 있습니다. 코드에서 직접 사용할 경우:

```python
from crawler import GoogleImageCrawler

crawler = GoogleImageCrawler(headless=True)
try:
    crawler.crawl_images(keyword="cat", num_images=50, save_dir="downloads")
finally:
    crawler.close()
```

## 애플리케이션 빌드 (macOS)

1. 아이콘 생성

```bash
python3 create_icon.py
```

2. 빌드

```bash
python3 build.py
```

빌드 결과는 `dist/GoogleImageCrawler.app` 또는 `dist/GoogleImageCrawler/`에 생성됩니다. 앱 실행:

```bash
open dist/GoogleImageCrawler.app
```

## 폴더 구조

```
google-image-crawler-/
├── crawler.py
├── gui.py
├── examples.py
├── build.py
├── create_icon.py
├── install.sh
├── requirements.txt
├── README.md
├── assets/
└── dist/
```

## 사용 시 유의사항

- 다운로드한 이미지는 저작권이 있을 수 있으니 개인/교육 목적 외 사용 시 주의하세요.
- 과도한 요청은 서버에 부담을 줄 수 있으니 `crawl_images` 실행 시 적절한 지연을 사용하세요.

---

빌드/실행 관련 추가 수정 원하시면 알려주세요.

### ⚠️ 성능
- 너무 많은 이미지를 한 번에 다운로드하지 마세요
- 크롤러는 요청 간에 적절한 지연을 두고 있습니다

### ChromeDriver 버전 불일치

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

## 성능 최적화

### 빠른 크롤링
```python
# 1. Headless 모드 사용
crawler = NaverImageCrawler(headless=True)

# 2. 스크롤 횟수 감소 (소스 수정)
crawler.scroll_and_load_images(num_scrolls=3)

# 3. 요청 간 지연 감소 (소스 수정)
time.sleep(0.2)  # 기본값: 0.3
crawler = NaverImageCrawler(headless=True)

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

crawler = NaverImageCrawler(headless=True)
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
