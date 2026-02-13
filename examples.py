"""
네이버 이미지 크롤러 - 고급 예제
다양한 기능을 보여주는 예제 파일
"""

from crawler import NaverImageCrawler
import os


def example_1_basic_crawl():
    """예제 1: 기본 크롤링"""
    print("\n=== 예제 1: 기본 크롤링 ===")
    
    crawler = NaverImageCrawler(headless=False)
    
    try:
        crawler.crawl_images(
            keyword="벚꽃",
            num_images=30,
            save_dir="downloads"
        )
    finally:
        crawler.close()


def example_2_multiple_keywords():
    """예제 2: 여러 키워드로 크롤링"""
    print("\n=== 예제 2: 여러 키워드 크롤링 ===")
    
    keywords = ["강아지", "고양이", "새"]
    
    for keyword in keywords:
        crawler = NaverImageCrawler(headless=True)  # headless 모드로 빠르게 실행
        
        try:
            crawler.crawl_images(
                keyword=keyword,
                num_images=20,
                save_dir="downloads"
            )
        finally:
            crawler.close()


def example_3_headless_mode():
    """예제 3: Headless 모드 (빠른 크롤링)"""
    print("\n=== 예제 3: Headless 모드 ===")
    
    crawler = NaverImageCrawler(headless=True)
    
    try:
        crawler.crawl_images(
            keyword="라면",
            num_images=50,
            save_dir="downloads"
        )
    finally:
        crawler.close()


def example_4_check_downloads():
    """예제 4: 다운로드된 이미지 확인"""
    print("\n=== 예제 4: 다운로드 현황 ===")
    
    downloads_dir = "downloads"
    
    if os.path.exists(downloads_dir):
        for keyword_dir in os.listdir(downloads_dir):
            path = os.path.join(downloads_dir, keyword_dir)
            if os.path.isdir(path):
                images = os.listdir(path)
                print(f"\n{keyword_dir}: {len(images)}개 이미지")
    else:
        print("downloads 디렉토리가 없습니다.")


if __name__ == "__main__":
    # 실행할 예제 선택
    # example_1_basic_crawl()
    # example_2_multiple_keywords()
    example_3_headless_mode()
    example_4_check_downloads()
