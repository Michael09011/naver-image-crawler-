"""
구글 이미지 크롤러 - 아이콘 생성 스크립트
"""

from PIL import Image, ImageDraw, ImageFont
import os


def create_icon(size=256):
    """
    애플리케이션 아이콘 생성
    
    Args:
        size (int): 아이콘 크기 (pixels)
    """
    # 배경색: Google Blue
    bg_color = (66, 133, 244)  # Google Blue
    text_color = (255, 255, 255)  # White
    accent_color = (255, 195, 0)  # Gold
    
    # 이미지 생성
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    
    try:
        # 시스템 폰트 사용 시도
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(size * 0.4))
        small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", int(size * 0.15))
    except:
        # 기본 폰트 사용
        font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # 이미지 다운로드 아이콘 그리기 (삼각형 모양의 화살표)
    margin = size * 0.15
    
    # 다운로드 화살표
    arrow_x1 = size // 2
    arrow_y1 = margin
    arrow_x2 = size * 0.35
    arrow_y2 = size * 0.4
    arrow_x3 = size * 0.65
    arrow_y3 = size * 0.4
    
    # 화살표 머리
    draw.polygon([
        (arrow_x1, arrow_y1),
        (arrow_x2, arrow_y2),
        (arrow_x3, arrow_y3)
    ], fill=accent_color)
    
    # 화살표 막대
    bar_width = size * 0.15
    bar_height = size * 0.35
    draw.rectangle([
        (arrow_x1 - bar_width//2, arrow_y2),
        (arrow_x1 + bar_width//2, arrow_y2 + bar_height)
    ], fill=accent_color)
    
    # 하단: 이미지 폴더 모양
    folder_x1 = size * 0.2
    folder_y1 = size * 0.55
    folder_x2 = size * 0.8
    folder_y2 = size * 0.9
    
    # 폴더 배경
    draw.rectangle([
        (folder_x1, folder_y1),
        (folder_x2, folder_y2)
    ], fill=text_color, outline=accent_color, width=3)
    
    # 폴더 탭
    tab_x1 = folder_x1
    tab_y1 = folder_y1 - size * 0.08
    tab_x2 = folder_x1 + size * 0.25
    tab_y2 = folder_y1
    
    draw.polygon([
        (tab_x1, tab_y2),
        (tab_x2, tab_y2),
        (tab_x2, tab_y1),
        (tab_x1 + size * 0.02, tab_y1)
    ], fill=accent_color)
    
    # 폴더 내부 이미지 아이콘들 (작은 사각형들)
    icon_size = size * 0.08
    spacing = size * 0.12
    
    icons_x_start = folder_x1 + size * 0.08
    icons_y_start = folder_y1 + size * 0.08
    
    for i in range(2):
        for j in range(2):
            x = icons_x_start + i * spacing
            y = icons_y_start + j * spacing
            if x + icon_size < folder_x2 - size * 0.05:
                draw.rectangle([
                    (x, y),
                    (x + icon_size, y + icon_size)
                ], fill=bg_color, outline=accent_color, width=2)
    
    return img


def create_all_sizes():
    """다양한 크기의 아이콘 생성"""
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    print("=" * 50)
    print("아이콘 생성 중...")
    print("=" * 50)
    
    # 다양한 크기의 아이콘 생성
    sizes = {
        "icon.png": 256,           # 일반 아이콘
        "icon-128.png": 128,       # 작은 아이콘
        "icon-64.png": 64,         # 매우 작은 아이콘
        "icon-32.png": 32,         # 파비콘용
        "icon-16.png": 16,         # 파비콘용
    }
    
    for filename, size in sizes.items():
        img = create_icon(size)
        filepath = os.path.join(assets_dir, filename)
        img.save(filepath)
        print(f"✅ {filename} ({size}x{size}) 생성 완료")
    
    # ICNS 파일 생성 (macOS용)
    try:
        img = create_icon(1024)
        icns_path = os.path.join(assets_dir, "icon.icns")
        img.save(icns_path, format='ICNS')
        print(f"✅ icon.icns 생성 완료 (macOS)")
    except Exception as e:
        print(f"⚠️ ICNS 파일 생성 실패: {e}")
        print("   macOS에서는 iconutil을 사용하여 생성합니다.")
    
    # ICO 파일 생성 (Windows용)
    try:
        img = create_icon(256)
        ico_path = os.path.join(assets_dir, "icon.ico")
        img.save(ico_path, format='ICO', sizes=[(16, 16), (32, 32), (64, 64), (128, 128), (256, 256)])
        print(f"✅ icon.ico 생성 완료 (Windows)")
    except Exception as e:
        print(f"⚠️ ICO 파일 생성 실패: {e}")
    
    # 파비콘 생성
    favicon_path = os.path.join(assets_dir, "favicon.ico")
    img = create_icon(32)
    img.save(favicon_path)
    print(f"✅ favicon.ico 생성 완료")
    
    print("\n" + "=" * 50)
    print(f"모든 아이콘이 {assets_dir}에 생성되었습니다.")
    print("=" * 50)
    
    return assets_dir


if __name__ == "__main__":
    assets_dir = create_all_sizes()
    print(f"\n아이콘 경로: {assets_dir}")
