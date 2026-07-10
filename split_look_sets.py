"""탭별 촬영 세트(3카드 합본 이미지)를 카드별 look_<id>.png 12장으로 분할.

사용법
1) 최종 세트 이미지 4장을 이 폴더에 아래 이름으로 저장한다.
   - set_date.png      (소개팅 탭 세트)
   - set_interview.png (면접 탭 세트)
   - set_work.png      (출근 탭 세트)
   - set_weekend.png   (주말 약속 탭 세트)
2) python split_look_sets.py 실행 → look_f1.png ~ look_f12.png 생성.
3) 앱은 look_<id>.png 를 자동 인식해 해당 카드에 원본 사진을 그대로 사용한다
   (SVG 합성·필터는 자동으로 꺼짐).

분할 규칙: 배경색 세로 굴착(gutter)을 탐지해 카드 3장의 x 경계를 찾고,
각 카드에서 사진 영역(카드 상단부터 4:5 비율)만 잘라낸다 — 원본 픽셀은
크롭·리사이즈 외에 일절 수정하지 않는다.
"""

import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow가 필요합니다: python -m pip install pillow")

HERE = Path(__file__).parent
# 세트 파일 → 카드 id 매핑 (좌→우 순서)
SETS = {
    "set_date.png": ["f1", "f2", "f3"],
    "set_interview.png": ["f4", "f5", "f6"],
    "set_work.png": ["f7", "f8", "f9"],
    "set_weekend.png": ["f10", "f11", "f12"],
}
PHOTO_ASPECT = 5 / 4  # .feed-photo 비율(가로:세로 = 4:5)


def find_card_columns(img: Image.Image):
    """배경색과 같은 세로줄(gutter)을 찾아 카드 x 구간 3개를 반환."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    # 배경 기준점: 좌상단은 헤더/여백 톤이 다를 수 있어 좌측 모서리 중앙에서 샘플
    bg = rgb.getpixel((2, h // 2))

    def is_gutter(x):
        # 세로 샘플의 90% 이상이 배경색이면 gutter로 판단(헤더 텍스트 등 소량 관용)
        bad = total = 0
        for y in range(int(h * 0.2), int(h * 0.85), max(1, h // 60)):
            total += 1
            p = rgb.getpixel((x, y))
            if sum(abs(a - b) for a, b in zip(p, bg)) > 30:
                bad += 1
        return total > 0 and bad <= total * 0.1

    cols, run = [], None
    for x in range(w):
        if is_gutter(x):
            if run is None:
                run = x
        else:
            if run is not None:
                cols.append((run, x - 1))
                run = None
    if run is not None:
        cols.append((run, w - 1))

    # gutter 사이 구간 = 카드
    cards, prev_end = [], 0
    for gs, ge in cols:
        if gs - prev_end > w * 0.15:
            cards.append((prev_end, gs - 1))
        prev_end = ge + 1
    if w - prev_end > w * 0.15:
        cards.append((prev_end, w - 1))
    return cards


def find_cards_top(img: Image.Image, cards) -> int:
    """세 카드의 중앙 열이 동시에 배경이 아니게 되는 첫 행 = 카드 상단.

    페이지 헤더 텍스트는 일부 열에만 걸치므로(전체 카드 폭에 걸치지 않음)
    세 열 동시 조건이면 헤더를 건너뛰고 카드 상단을 정확히 찾는다."""
    rgb = img.convert("RGB")
    bg = rgb.getpixel((2, rgb.size[1] // 2))
    mids = [(x0 + x1) // 2 for x0, x1 in cards]

    def nonbg(x, y):
        p = rgb.getpixel((x, y))
        return sum(abs(a - b) for a, b in zip(p, bg)) > 30

    for y in range(rgb.size[1]):
        if all(nonbg(x, y) for x in mids):
            return y
    return 0


def main() -> int:
    made = 0
    for fname, ids in SETS.items():
        src = HERE / fname
        if not src.exists():
            print(f"[split] {fname} 없음 — 건너뜀")
            continue
        img = Image.open(src)
        cards = find_card_columns(img)
        if len(cards) != 3:
            print(f"[split] {fname}: 카드 경계 탐지 실패(발견 {len(cards)}개) — 3등분 폴백 사용")
            w = img.size[0]
            pad = int(w * 0.015)
            step = w // 3
            cards = [(i * step + pad, (i + 1) * step - pad) for i in range(3)]
        top_all = find_cards_top(img, cards)
        for (x0, x1), cid in zip(cards, ids):
            top = top_all
            cw = x1 - x0 + 1
            ph = int(cw * PHOTO_ASPECT)
            box = (x0, top, x1 + 1, min(top + ph, img.size[1]))
            crop = img.crop(box).convert("RGB")
            # 카드 표시 크기(레티나 2배) 기준으로 축소 → data URI 임베드 용량 절약
            if crop.size[0] > 720:
                crop = crop.resize((720, int(crop.size[1] * 720 / crop.size[0])), Image.LANCZOS)
            out = HERE / f"look_{cid}.jpg"
            crop.save(out, "JPEG", quality=86)
            made += 1
            print(f"[split] {fname} → {out.name} ({crop.size[0]}x{crop.size[1]}, {out.stat().st_size // 1024}KB)")
    if not made:
        print("[split] 처리된 세트가 없습니다. set_*.png 파일명을 확인하세요.")
        return 1
    print(f"[split] 완료: {made}장 생성. 앱을 새로고침하면 자동 반영됩니다.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
