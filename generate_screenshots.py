import os
from PIL import Image, ImageDraw, ImageFont

FONT_BOLD = "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc"
FONT_REGULAR = "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc"

def get_font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def draw_window_frame(draw, x, y, w, h, bg_color=(255, 255, 255), border_color=(226, 232, 240)):
    # Outer window with rounded rectangle and shadow border
    draw.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=bg_color, outline=border_color, width=2)
    # Header bar
    draw.rounded_rectangle([x, y, x + w, y + 44], radius=12, fill=(241, 245, 249))
    draw.rectangle([x, y + 32, x + w, y + 44], fill=(241, 245, 249))
    draw.line([x, y + 44, x + w, y + 44], fill=(226, 232, 240), width=1)
    # Window controls (macOS style dots)
    draw.ellipse([x + 16, y + 16, x + 28, y + 28], fill=(239, 68, 68))
    draw.ellipse([x + 36, y + 16, x + 48, y + 28], fill=(245, 158, 11))
    draw.ellipse([x + 56, y + 16, x + 68, y + 28], fill=(16, 185, 129))

def create_screenshot_1():
    # 1280 x 800 RGB (24-bit PNG, no alpha)
    img = Image.new("RGB", (1280, 800), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    f_title = get_font(FONT_BOLD, 36)
    f_sub = get_font(FONT_REGULAR, 20)
    f_card_t = get_font(FONT_BOLD, 18)
    f_card_d = get_font(FONT_REGULAR, 14)
    f_tab = get_font(FONT_REGULAR, 14)
    f_bm = get_font(FONT_REGULAR, 13)
    f_badge = get_font(FONT_BOLD, 14)
    f_hero = get_font(FONT_BOLD, 22)
    f_hero_sub = get_font(FONT_REGULAR, 16)

    # Top Header Banner
    draw.rectangle([0, 0, 1280, 130], fill=(255, 255, 255))
    draw.line([0, 130, 1280, 130], fill=(226, 232, 240), width=2)

    # Badge
    draw.rounded_rectangle([70, 28, 260, 56], radius=14, fill=(238, 242, 255))
    draw.text((85, 33), "Chrome 拡張機能", font=f_badge, fill=(79, 70, 229))

    # Main Title & Subtitle
    draw.text((70, 68), "ブックマークを常に新しいタブで自動展開", font=f_title, fill=(15, 23, 42))
    draw.text((280, 32), "閲覧中の作業ページを上書きせず、並行してスムーズに閲覧", font=f_sub, fill=(100, 116, 139))

    # Browser Window Mockup
    wx, wy, ww, wh = 70, 160, 1140, 450
    draw_window_frame(draw, wx, wy, ww, wh)

    # Tabs in window header
    # Tab 1: Current Page (Inactive / Main)
    draw.rounded_rectangle([wx + 85, wy + 8, wx + 260, wy + 44], radius=6, fill=(255, 255, 255))
    draw.text((wx + 105, wy + 18), "作業中のWebサイト", font=f_tab, fill=(71, 85, 105))

    # Tab 2: New Tab opened from bookmark (Active & Highlighted)
    draw.rounded_rectangle([wx + 268, wy + 8, wx + 470, wy + 44], radius=6, fill=(238, 242, 255), outline=(99, 102, 241), width=2)
    draw.ellipse([wx + 280, wy + 20, wx + 292, wy + 32], fill=(99, 102, 241))
    draw.text((wx + 300, wy + 18), "新規タブ: Google 検索", font=f_tab, fill=(67, 56, 202))

    # Address bar
    draw.rounded_rectangle([wx + 20, wy + 54, wx + ww - 20, wy + 88], radius=6, fill=(241, 245, 249))
    draw.text((wx + 40, wy + 64), "https://www.google.com/search?q=...", font=f_tab, fill=(100, 116, 139))

    # Bookmark Bar
    draw.rectangle([wx + 20, wy + 96, wx + ww - 20, wy + 130], fill=(255, 255, 255))
    draw.line([wx + 20, wy + 130, wx + ww - 20, wy + 130], fill=(226, 232, 240), width=1)

    # Bookmark items
    bookmarks = [
        ("★ Google", True),
        ("★ GitHub", False),
        ("★ 技術ドキュメント", False),
        ("★ カレンダー", False),
        ("★ ニュースポータル", False)
    ]
    bx_cursor = wx + 30
    clicked_rect = None
    for title, is_clicked in bookmarks:
        tw = int(draw.textlength(title, font=f_bm))
        box_w = tw + 20
        if is_clicked:
            draw.rounded_rectangle([bx_cursor, wy + 100, bx_cursor + box_w, wy + 126], radius=4, fill=(224, 231, 255), outline=(99, 102, 241), width=1)
            draw.text((bx_cursor + 10, wy + 106), title, font=f_bm, fill=(67, 56, 202))
            clicked_rect = (bx_cursor + box_w // 2, wy + 126)
        else:
            draw.text((bx_cursor + 10, wy + 106), title, font=f_bm, fill=(71, 85, 105))
        bx_cursor += box_w + 14

    # Click Action Visual Pointer & Connecting Arrow
    if clicked_rect:
        cx, cy = clicked_rect
        # Mouse Click Icon Simulation
        draw.ellipse([cx - 8, cy + 12, cx + 8, cy + 28], fill=(239, 68, 68))
        draw.text((cx + 16, cy + 12), "クリック！", font=f_badge, fill=(220, 38, 38))

        # Curved connection arrow from clicked bookmark to Tab 2
        # Target Tab 2 center
        tx, ty = wx + 370, wy + 48
        draw.line([cx, cy + 8, cx, cy + 50], fill=(99, 102, 241), width=3)
        draw.line([cx, cy + 50, tx, ty + 100], fill=(99, 102, 241), width=3)
        draw.line([tx, ty + 100, tx, ty], fill=(99, 102, 241), width=3)
        draw.polygon([(tx, ty), (tx - 8, ty + 14), (tx + 8, ty + 14)], fill=(99, 102, 241))

    # Inside page content mockup
    draw.rounded_rectangle([wx + 50, wy + 170, wx + ww - 50, wy + wh - 40], radius=8, fill=(248, 250, 252))
    draw.text((wx + 80, wy + 210), "ブックマーククリックを自動検知して新しいタブを生成", font=f_hero, fill=(15, 23, 42))
    draw.text((wx + 80, wy + 250), "現在の作業画面を閉じることなく、ブックマーク先を別タブで素早く参照できます。", font=f_hero_sub, fill=(71, 85, 105))

    # Graphic representation in content
    draw.rounded_rectangle([wx + 80, wy + 300, wx + 480, wy + 380], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((wx + 100, wy + 320), "元のタブ: 状態を完全に保持", font=f_card_t, fill=(15, 23, 42))
    draw.text((wx + 100, wy + 348), "編集中データや閲覧履歴を上書きしません", font=f_card_d, fill=(100, 116, 139))

    draw.rounded_rectangle([wx + 510, wy + 300, wx + 910, wy + 380], radius=8, fill=(255, 255, 255), outline=(99, 102, 241), width=2)
    draw.text((wx + 530, wy + 320), "新しいタブ: 自動で即座に展開", font=f_card_t, fill=(67, 56, 202))
    draw.text((wx + 530, wy + 348), "フォアグラウンド / バックグラウンドの選択可能", font=f_card_d, fill=(100, 116, 139))

    # Bottom 3 Feature Cards
    card_w = 360
    card_h = 130
    gap = 30
    start_x = 70
    card_y = 635

    features = [
        ("元のページを上書きしない", "作業中のWebページやフォーム入力内容を失うことなく、ブックマーク先を開くことができます。"),
        ("自然なクリック操作", "キーボードのCmd/Ctrlキーを押さなくても、通常の左クリックだけで自動的に新規タブ化されます。"),
        ("スマートな空タブ判定", "新規タブ（chrome://newtab/）などの空白状態でクリックした際は、不要な空タブを残さず遷移します。")
    ]

    for i, (title, desc) in enumerate(features):
        cx = start_x + i * (card_w + gap)
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + card_h], radius=8, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
        # Colored small accent bar on top
        draw.rounded_rectangle([cx, card_y, cx + card_w, card_y + 4], radius=2, fill=(79, 70, 229))
        draw.text((cx + 18, card_y + 18), title, font=f_card_t, fill=(15, 23, 42))
        
        # Multiline text wrap for description
        lines = []
        if len(desc) > 24:
            lines.append(desc[:24])
            lines.append(desc[24:])
        else:
            lines.append(desc)
        for li, line in enumerate(lines):
            draw.text((cx + 18, card_y + 50 + li * 22), line, font=f_card_d, fill=(100, 116, 139))

    out_path = "/Volumes/AppsDrive/open_bookmarks_in_new_tab/screenshots/screenshot1_main.png"
    img.save(out_path, "PNG")
    print("Screenshot 1 saved to:", out_path)

def create_screenshot_2():
    # 1280 x 800 RGB (24-bit PNG, no alpha)
    img = Image.new("RGB", (1280, 800), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    f_title = get_font(FONT_BOLD, 36)
    f_sub = get_font(FONT_REGULAR, 20)
    f_badge = get_font(FONT_BOLD, 14)
    f_tab = get_font(FONT_REGULAR, 14)
    f_pop_t = get_font(FONT_BOLD, 16)
    f_pop_sub = get_font(FONT_REGULAR, 12)
    f_label = get_font(FONT_REGULAR, 14)
    f_bm = get_font(FONT_REGULAR, 13)
    f_card_t = get_font(FONT_BOLD, 22)
    f_card_d = get_font(FONT_REGULAR, 16)

    # Top Header Banner
    draw.rectangle([0, 0, 1280, 130], fill=(255, 255, 255))
    draw.line([0, 130, 1280, 130], fill=(226, 232, 240), width=2)

    # Badge
    draw.rounded_rectangle([70, 28, 240, 56], radius=14, fill=(238, 242, 255))
    draw.text((85, 33), "ポップアップ機能", font=f_badge, fill=(79, 70, 229))

    # Main Title & Subtitle
    draw.text((70, 68), "直感的な動作設定とブックマーク検索", font=f_title, fill=(15, 23, 42))
    draw.text((260, 32), "好みに合わせて開き方をカスタマイズ。ツールバーから即座にブックマーク検索も可能", font=f_sub, fill=(100, 116, 139))

    # Browser Window Mockup
    wx, wy, ww, wh = 70, 160, 1140, 580
    draw_window_frame(draw, wx, wy, ww, wh)

    # Window header
    draw.rounded_rectangle([wx + 85, wy + 8, wx + 280, wy + 44], radius=6, fill=(255, 255, 255))
    draw.text((wx + 105, wy + 18), "ブックマーク設定", font=f_tab, fill=(71, 85, 105))

    # Address bar & extension icon area
    draw.rounded_rectangle([wx + 20, wy + 54, wx + ww - 140, wy + 88], radius=6, fill=(241, 245, 249))
    draw.text((wx + 40, wy + 64), "https://chrome.google.com/webstore", font=f_tab, fill=(100, 116, 139))

    # Extension button in toolbar
    btn_x = wx + ww - 120
    draw.rounded_rectangle([btn_x, wy + 54, btn_x + 90, wy + 88], radius=6, fill=(238, 242, 255), outline=(99, 102, 241), width=2)
    # Icon
    draw.ellipse([btn_x + 10, wy + 63, btn_x + 26, wy + 79], fill=(37, 99, 235))
    draw.text((btn_x + 32, wy + 64), "設定", font=f_tab, fill=(67, 56, 202))

    # Popup Modal / Dropdown Dialog
    pw, ph = 380, 430
    px, py = btn_x - pw + 90, wy + 98
    # Dropdown shadow / border
    draw.rounded_rectangle([px - 2, py - 2, px + pw + 2, py + ph + 2], radius=12, fill=(203, 213, 225))
    draw.rounded_rectangle([px, py, px + pw, py + ph], radius=10, fill=(255, 255, 255))

    # Popup Header
    draw.ellipse([px + 20, py + 18, px + 44, py + 42], fill=(37, 99, 235))
    draw.text((px + 54, py + 16), "ブックマーク設定", font=f_pop_t, fill=(15, 23, 42))
    draw.text((px + 54, py + 38), "ブックマーククリック時の動作を制御します", font=f_pop_sub, fill=(100, 116, 139))
    draw.line([px + 20, py + 62, px + pw - 20, py + 62], fill=(241, 245, 249), width=1)

    # Setting Items
    # 1. Enable Toggle
    draw.text((px + 24, py + 80), "機能の有効化", font=f_label, fill=(51, 65, 85))
    # Toggle switch (ON)
    draw.rounded_rectangle([px + pw - 70, py + 78, px + pw - 24, py + 100], radius=11, fill=(16, 185, 129))
    draw.ellipse([px + pw - 44, py + 80, px + pw - 26, py + 98], fill=(255, 255, 255))

    draw.line([px + 20, py + 114, px + pw - 20, py + 114], fill=(241, 245, 249), width=1)

    # 2. Background Toggle
    draw.text((px + 24, py + 128), "バックグラウンドで開く", font=f_label, fill=(51, 65, 85))
    # Toggle switch (OFF / Unchecked)
    draw.rounded_rectangle([px + pw - 70, py + 126, px + pw - 24, py + 148], radius=11, fill=(203, 213, 225))
    draw.ellipse([px + pw - 68, py + 128, px + pw - 50, py + 146], fill=(255, 255, 255))

    draw.line([px + 20, py + 162, px + pw - 20, py + 162], fill=(241, 245, 249), width=1)

    # Quick Search Section
    draw.text((px + 24, py + 176), "ブックマーククイック検索", font=f_pop_t, fill=(51, 65, 85))
    # Search input box
    draw.rounded_rectangle([px + 20, py + 204, px + pw - 20, py + 238], radius=6, fill=(248, 250, 252), outline=(203, 213, 225), width=1)
    draw.text((px + 32, py + 212), "🔍 ブックマークを検索...", font=f_bm, fill=(148, 163, 184))

    # Bookmark List Container
    draw.rounded_rectangle([px + 20, py + 248, px + pw - 20, py + 380], radius=6, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    bm_items = [
        "🌐 Google 検索",
        "💻 GitHub - Dashboard",
        "📚 技術仕様リファレンス",
        "📰 最新ニュースポータル"
    ]
    for idx, item in enumerate(bm_items):
        iy = py + 254 + idx * 30
        if idx == 0:
            draw.rounded_rectangle([px + 22, iy - 2, px + pw - 22, iy + 26], radius=4, fill=(238, 242, 255))
            draw.text((px + 30, iy + 2), item, font=f_bm, fill=(67, 56, 202))
        else:
            draw.text((px + 30, iy + 2), item, font=f_bm, fill=(71, 85, 105))

    # Popup Footer Tip
    draw.text((px + 24, py + 394), "ヒント: ポップアップ一覧クリック時も新規タブ展開", font=f_pop_sub, fill=(100, 116, 139))

    # Left Side Explanatory Cards
    lx = wx + 40
    draw.rounded_rectangle([lx, wy + 120, lx + 580, wy + 260], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([lx, wy + 120, lx + 580, wy + 126], radius=3, fill=(16, 185, 129))
    draw.text((lx + 30, wy + 146), "ワンクリックで機能のオン/オフ切り替え", font=f_card_t, fill=(15, 23, 42))
    draw.text((lx + 30, wy + 184), "一時的に標準動作に戻したい場合も、ポップアップ画面から", font=f_card_d, fill=(100, 116, 139))
    draw.text((lx + 30, wy + 214), "チェックボックス1つで簡単に切り替えられます。", font=f_card_d, fill=(100, 116, 139))

    draw.rounded_rectangle([lx, wy + 290, lx + 580, wy + 430], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.rounded_rectangle([lx, wy + 290, lx + 580, wy + 296], radius=3, fill=(99, 102, 241))
    draw.text((lx + 30, wy + 316), "バックグラウンド展開に対応", font=f_card_t, fill=(15, 23, 42))
    draw.text((lx + 30, wy + 354), "「バックグラウンドで開く」を有効にすると、現在のタブに", font=f_card_d, fill=(100, 116, 139))
    draw.text((lx + 30, wy + 384), "フォーカスを残したまま背面に新規タブを作成します。", font=f_card_d, fill=(100, 116, 139))

    draw.rounded_rectangle([lx, wy + 460, lx + 580, wy + 550], radius=10, fill=(255, 255, 255), outline=(226, 232, 240), width=1)
    draw.text((lx + 30, wy + 480), "ポップアップ内クイック検索", font=f_card_t, fill=(15, 23, 42))
    draw.text((lx + 30, wy + 514), "ブックマーク数が多い場合でも、インクリメンタル検索ですぐに見つかります。", font=f_card_d, fill=(100, 116, 139))

    out_path = "/Volumes/AppsDrive/open_bookmarks_in_new_tab/screenshots/screenshot2_popup.png"
    img.save(out_path, "PNG")
    print("Screenshot 2 saved to:", out_path)

if __name__ == "__main__":
    create_screenshot_1()
    create_screenshot_2()
