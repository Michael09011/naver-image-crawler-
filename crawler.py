import os
import time
import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from urllib.parse import urlparse


class NaverImageCrawler:
    """네이버 이미지 크롤러 클래스"""
    
    def __init__(self, headless=False):
        """
        크롤러 초기화
        
        Args:
            headless (bool): 브라우저 헤드리스 모드 여부 (기본값: False)
        """
        self.driver = None
        self.headless = headless
        self.setup_driver()
    
    def setup_driver(self):
        """크롬 드라이버 설정"""
        chrome_options = Options()
        
        # 헤드리스 모드 설정
        if self.headless:
            chrome_options.add_argument("--headless=new")
        
        # 기본 옵션
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # User-Agent 설정
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        
        # ChromeDriver 자동 설치 및 실행
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
    
    def get_search_url(self, keyword, start=0):
        """
        검색 URL 생성
        
        Args:
            keyword (str): 검색 키워드
            start (int): 시작 이미지 번호
        
        Returns:
            str: 네이버 이미지 검색 URL
        """
        return f"https://search.naver.com/search.naver?where=image&sm=tab_jum&query={keyword}&start={start}"
    
    def scroll_and_load_images(self, num_scrolls=10):
        """
        페이지 스크롤하여 이미지 로드
        
        Args:
            num_scrolls (int): 스크롤 횟수
        """
        for i in range(num_scrolls):
            # 페이지 끝까지 스크롤
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(0.5)
            
            # 더보기 버튼 클릭 시도
            try:
                # 여러 가능한 더보기 버튼 선택자
                button_selectors = [
                    "a.api_more_btn",
                    "button.more_btn",
                    ".btn_more",
                    "a.moreBtn"
                ]
                
                button_found = False
                for selector in button_selectors:
                    try:
                        buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if buttons:
                            self.driver.execute_script("arguments[0].click();", buttons[0])
                            button_found = True
                            time.sleep(0.5)
                            break
                    except:
                        continue
                
                if not button_found and i == 0:
                    # 첫 시도에서 버튼을 못 찾으면 계속 진행
                    pass
                    
            except Exception as e:
                # 더보기 버튼이 없으면 계속
                pass
            
            time.sleep(0.5)
    
    def get_image_urls(self):
        """
        현재 페이지에서 이미지 URL 추출
        
        Returns:
            list: 이미지 URL 리스트
        """
        image_urls = []
        
        try:
            # 다양한 선택자로 이미지 요소 찾기
            selectors = [
                "img.lazyimg",
                "img.image",
                "img._image",
                "a.thumb img",
                "div.thumb img",
                "img[alt]"
            ]
            
            images = []
            for selector in selectors:
                try:
                    images.extend(self.driver.find_elements(By.CSS_SELECTOR, selector))
                except:
                    continue
            
            # 중복 제거
            seen_urls = set()
            
            for img in images:
                try:
                    # 여러 속성에서 URL 찾기
                    src = img.get_attribute("src") or img.get_attribute("data-src")
                    
                    # 부모 요소에서도 찾기
                    if not src:
                        parent = img.find_element(By.XPATH, "./ancestor::a[@href]")
                        href = parent.get_attribute("href")
                        if href and "imgurl=" in href:
                            src = href
                    
                    if src and "http" in src and src not in seen_urls:
                        image_urls.append(src)
                        seen_urls.add(src)
                except Exception as e:
                    continue
        
        except Exception as e:
            print(f"이미지 요소 찾기 실패: {e}")
        
        return image_urls
    
    def download_image(self, image_url, save_path, filename):
        """
        이미지 다운로드
        
        Args:
            image_url (str): 이미지 URL
            save_path (str): 저장 경로
            filename (str): 파일명
        
        Returns:
            bool: 다운로드 성공 여부
        """
        try:
            # 이미지 다운로드 (타임아웃 설정)
            response = requests.get(image_url, timeout=10, allow_redirects=True)
            response.raise_for_status()
            
            # 파일 저장
            file_path = os.path.join(save_path, filename)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            return True
        
        except Exception as e:
            print(f"이미지 다운로드 실패 ({image_url}): {e}")
            return False
    
    def crawl_images(self, keyword, num_images=50, save_dir="downloads"):
        """
        이미지 크롤링 실행
        
        Args:
            keyword (str): 검색 키워드
            num_images (int): 다운로드할 이미지 개수
            save_dir (str): 저장 디렉토리
        """
        # 저장 경로 생성
        save_path = os.path.join(save_dir, keyword)
        Path(save_path).mkdir(parents=True, exist_ok=True)
        
        print(f"'{keyword}' 이미지 크롤링 시작...")
        print(f"저장 경로: {save_path}")
        print(f"목표 이미지 개수: {num_images}")
        
        downloaded_count = 0
        page_start = 0
        consecutive_failures = 0
        
        try:
            while downloaded_count < num_images and consecutive_failures < 3:
                # 검색 URL로 이동
                search_url = self.get_search_url(keyword, page_start)
                print(f"\n페이지 로드 중: {search_url}")
                self.driver.get(search_url)
                
                # 페이지 로드 대기
                time.sleep(4)
                
                # 이미지 로드를 위해 스크롤
                self.scroll_and_load_images(num_scrolls=5)
                
                # 이미지 URL 추출
                image_urls = self.get_image_urls()
                print(f"현재 페이지에서 {len(image_urls)}개의 이미지 URL 추출됨")
                
                if len(image_urls) == 0:
                    consecutive_failures += 1
                    page_start += 30
                    continue
                else:
                    consecutive_failures = 0
                
                # 이미지 다운로드
                for idx, image_url in enumerate(image_urls):
                    if downloaded_count >= num_images:
                        break
                    
                    # 파일명 생성
                    file_extension = self.get_file_extension(image_url)
                    filename = f"{keyword}_{downloaded_count + 1}{file_extension}"
                    
                    # 이미지 다운로드
                    if self.download_image(image_url, save_path, filename):
                        downloaded_count += 1
                        print(f"[{downloaded_count}/{num_images}] {filename} 다운로드 완료")
                    
                    time.sleep(0.3)  # 요청 간 지연
                
                # 다음 페이지로 이동
                page_start += 30
        
        except Exception as e:
            print(f"크롤링 중 오류 발생: {e}")
        
        finally:
            print(f"\n크롤링 완료!")
            print(f"총 {downloaded_count}개의 이미지 다운로드됨")
            print(f"저장 위치: {os.path.abspath(save_path)}")
    
    @staticmethod
    def get_file_extension(url):
        """
        URL에서 파일 확장자 추출
        
        Args:
            url (str): 이미지 URL
        
        Returns:
            str: 파일 확장자 (.jpg, .png 등)
        """
        try:
            # URL에서 파일명 추출
            parsed_url = urlparse(url)
            path = parsed_url.path
            
            # 쿼리 스트링 제거
            if '?' in path:
                path = path.split('?')[0]
            
            # 확장자 추출
            if '.' in path:
                ext = '.' + path.split('.')[-1].lower()
                if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    return ext
        
        except Exception:
            pass
        
        return '.jpg'  # 기본값
    
    def close(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()


def main():
    """메인 함수"""
    # 크롤러 초기화 (headless=True로 설정하면 브라우저 창이 뜨지 않음)
    crawler = NaverImageCrawler(headless=False)
    
    try:
        # 크롤링 실행
        keyword = "고양이"  # 검색 키워드 변경 가능
        crawler.crawl_images(keyword=keyword, num_images=50)
    
    finally:
        # 드라이버 종료
        crawler.close()


if __name__ == "__main__":
    main()
