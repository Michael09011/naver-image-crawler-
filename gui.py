"""
네이버 이미지 크롤러 GUI 버전
tkinter를 사용한 그래픽 인터페이스
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import os
from pathlib import Path
from crawler import NaverImageCrawler


class CrawlerGUI:
    """크롤러 GUI 클래스"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("네이버 이미지 크롤러")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # 스타일 설정
        style = ttk.Style()
        style.theme_use('clam')
        
        self.crawler = None
        self.is_running = False
        
        self.setup_ui()
    
    def setup_ui(self):
        """UI 구성"""
        
        # === 상단: 설정 영역 ===
        settings_frame = ttk.LabelFrame(self.root, text="검색 설정", padding=10)
        settings_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 키워드 입력
        ttk.Label(settings_frame, text="검색 키워드:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.keyword_var = tk.StringVar(value="고양이")
        keyword_entry = ttk.Entry(settings_frame, textvariable=self.keyword_var, width=30, font=("Arial", 11))
        keyword_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        # 이미지 개수
        ttk.Label(settings_frame, text="다운로드 개수:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.num_images_var = tk.StringVar(value="50")
        num_images_spinbox = ttk.Spinbox(
            settings_frame,
            from_=1,
            to=1000,
            textvariable=self.num_images_var,
            width=30,
            font=("Arial", 11)
        )
        num_images_spinbox.grid(row=1, column=1, sticky=tk.EW, padx=5)
        
        # 저장 경로
        ttk.Label(settings_frame, text="저장 경로:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.save_dir_var = tk.StringVar(value="downloads")
        save_dir_entry = ttk.Entry(settings_frame, textvariable=self.save_dir_var, width=30, font=("Arial", 11))
        save_dir_entry.grid(row=2, column=1, sticky=tk.EW, padx=5)
        
        browse_btn = ttk.Button(settings_frame, text="찾아보기", command=self.browse_folder)
        browse_btn.grid(row=2, column=2, padx=5)
        
        # 옵션
        self.headless_var = tk.BooleanVar(value=True)
        headless_check = ttk.Checkbutton(
            settings_frame,
            text="백그라운드 모드 (Headless)",
            variable=self.headless_var
        )
        headless_check.grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # === 중단: 키워드 목록 ===
        keywords_frame = ttk.LabelFrame(self.root, text="여러 키워드 검색", padding=10)
        keywords_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        ttk.Label(keywords_frame, text="아래에 키워드를 입력하세요 (줄 단위로 구분):").pack(fill=tk.X, pady=5)
        
        self.keywords_text = scrolledtext.ScrolledText(keywords_frame, height=8, font=("Courier", 10))
        self.keywords_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # 버튼 행
        button_frame = ttk.Frame(keywords_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="단일 검색", command=self.start_single_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="일괄 검색", command=self.start_batch_search).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="중지", command=self.stop_crawler).pack(side=tk.LEFT, padx=5)
        
        # === 하단: 로그 ===
        log_frame = ttk.LabelFrame(self.root, text="실행 로그", padding=10)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=12, font=("Courier", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # 진행률 표시
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.root,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5)
        
        self.progress_label = ttk.Label(self.root, text="준비 완료", justify=tk.CENTER)
        self.progress_label.pack(fill=tk.X, padx=10)
        
        self.log("크롤러가 준비되었습니다.\n단일 검색 또는 일괄 검색을 선택하세요.")
    
    def browse_folder(self):
        """폴더 선택"""
        folder = filedialog.askdirectory(title="저장 폴더 선택")
        if folder:
            self.save_dir_var.set(folder)
    
    def log(self, message):
        """로그 출력"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def start_single_search(self):
        """단일 검색 시작"""
        if self.is_running:
            messagebox.showwarning("경고", "이미 실행 중입니다.")
            return
        
        keyword = self.keyword_var.get().strip()
        if not keyword:
            messagebox.showerror("오류", "키워드를 입력하세요.")
            return
        
        try:
            num_images = int(self.num_images_var.get())
            if num_images <= 0:
                raise ValueError("1 이상의 숫자를 입력하세요.")
        except ValueError as e:
            messagebox.showerror("오류", f"유효한 개수를 입력하세요: {e}")
            return
        
        save_dir = self.save_dir_var.get()
        
        # 스레드에서 실행
        thread = threading.Thread(
            target=self._crawl_single,
            args=(keyword, num_images, save_dir)
        )
        thread.daemon = True
        thread.start()
    
    def start_batch_search(self):
        """일괄 검색 시작"""
        if self.is_running:
            messagebox.showwarning("경고", "이미 실행 중입니다.")
            return
        
        keywords_text = self.keywords_text.get("1.0", tk.END).strip()
        if not keywords_text:
            messagebox.showerror("오류", "최소 하나의 키워드를 입력하세요.")
            return
        
        keywords = [k.strip() for k in keywords_text.split("\n") if k.strip()]
        
        try:
            num_images = int(self.num_images_var.get())
            if num_images <= 0:
                raise ValueError("1 이상의 숫자를 입력하세요.")
        except ValueError as e:
            messagebox.showerror("오류", f"유효한 개수를 입력하세요: {e}")
            return
        
        save_dir = self.save_dir_var.get()
        
        # 스레드에서 실행
        thread = threading.Thread(
            target=self._crawl_batch,
            args=(keywords, num_images, save_dir)
        )
        thread.daemon = True
        thread.start()
    
    def _crawl_single(self, keyword, num_images, save_dir):
        """단일 크롤링 실행"""
        self.is_running = True
        self.progress_var.set(0)
        
        try:
            self.log(f"\n{'='*50}")
            self.log(f"검색 시작: '{keyword}'")
            self.log(f"목표 개수: {num_images}개")
            self.log(f"저장 경로: {save_dir}")
            self.log(f"{'='*50}\n")
            
            # 크롤러 실행
            crawler = NaverImageCrawler(headless=self.headless_var.get())
            
            # 로그 콜백을 위해 원본 crawl_images 메서드를 래핑
            self._run_crawler(crawler, keyword, num_images, save_dir)
            
        except Exception as e:
            self.log(f"\n❌ 오류 발생: {e}")
            messagebox.showerror("오류", f"크롤링 중 오류 발생:\n{e}")
        
        finally:
            self.is_running = False
            self.progress_var.set(100)
            self.progress_label.config(text="완료!")
    
    def _crawl_batch(self, keywords, num_images, save_dir):
        """일괄 크롤링 실행"""
        self.is_running = True
        
        try:
            self.log(f"\n{'='*50}")
            self.log(f"일괄 검색 시작")
            self.log(f"키워드: {', '.join(keywords)}")
            self.log(f"각 키워드당 개수: {num_images}개")
            self.log(f"{'='*50}\n")
            
            total_keywords = len(keywords)
            
            for idx, keyword in enumerate(keywords):
                if not self.is_running:
                    self.log("\n검색이 중단되었습니다.")
                    break
                
                progress = (idx / total_keywords) * 100
                self.progress_var.set(progress)
                self.progress_label.config(
                    text=f"진행률: {progress:.1f}% ({idx}/{total_keywords})"
                )
                
                self.log(f"\n[{idx+1}/{total_keywords}] '{keyword}' 검색 중...")
                
                crawler = NaverImageCrawler(headless=self.headless_var.get())
                self._run_crawler(crawler, keyword, num_images, save_dir)
            
            if self.is_running:
                self.log(f"\n{'='*50}")
                self.log("✅ 모든 검색이 완료되었습니다!")
                self.log(f"{'='*50}")
                self.progress_var.set(100)
                self.progress_label.config(text="완료!")
        
        except Exception as e:
            self.log(f"\n❌ 오류 발생: {e}")
            messagebox.showerror("오류", f"크롤링 중 오류 발생:\n{e}")
        
        finally:
            self.is_running = False
    
    def _run_crawler(self, crawler, keyword, num_images, save_dir):
        """크롤러 실행 (로그 출력 포함)"""
        try:
            # 저장 경로 생성
            save_path = os.path.join(save_dir, keyword)
            Path(save_path).mkdir(parents=True, exist_ok=True)
            
            self.log(f"저장 경로: {save_path}")
            
            downloaded_count = 0
            page_start = 0
            consecutive_failures = 0
            
            while downloaded_count < num_images and consecutive_failures < 3:
                if not self.is_running:
                    break
                
                # 검색 URL로 이동
                search_url = crawler.get_search_url(keyword, page_start)
                self.log(f"페이지 로드: {search_url}")
                crawler.driver.get(search_url)
                
                import time
                time.sleep(4)
                
                # 이미지 로드를 위해 스크롤
                crawler.scroll_and_load_images(num_scrolls=5)
                
                # 이미지 URL 추출
                image_urls = crawler.get_image_urls()
                self.log(f"  → {len(image_urls)}개의 이미지 URL 추출됨")
                
                if len(image_urls) == 0:
                    consecutive_failures += 1
                    page_start += 30
                    continue
                else:
                    consecutive_failures = 0
                
                # 이미지 다운로드
                for idx, image_url in enumerate(image_urls):
                    if not self.is_running or downloaded_count >= num_images:
                        break
                    
                    # 파일명 생성
                    file_extension = crawler.get_file_extension(image_url)
                    filename = f"{keyword}_{downloaded_count + 1}{file_extension}"
                    
                    # 이미지 다운로드
                    if crawler.download_image(image_url, save_path, filename):
                        downloaded_count += 1
                        progress = (downloaded_count / num_images) * 100
                        self.progress_var.set(min(progress, 99))
                        self.progress_label.config(
                            text=f"다운로드: {downloaded_count}/{num_images}"
                        )
                        
                        if downloaded_count % 5 == 0:  # 5개마다 로그
                            self.log(f"  [{downloaded_count}/{num_images}] {filename} 완료")
                    
                    time.sleep(0.3)
                
                page_start += 30
            
            self.log(f"'{keyword}' 크롤링 완료: {downloaded_count}개 다운로드")
            
        finally:
            crawler.close()
    
    def stop_crawler(self):
        """크롤링 중지"""
        if self.is_running:
            self.is_running = False
            self.log("\n⏹️  크롤링을 중지하고 있습니다...")
            self.progress_label.config(text="중지됨")
        else:
            messagebox.showinfo("안내", "실행 중인 크롤링이 없습니다.")


def main():
    """메인 함수"""
    root = tk.Tk()
    app = CrawlerGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
