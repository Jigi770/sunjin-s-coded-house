"""올리브영 카테고리 랭킹 수집 배치.

하루 1회(cron 등) 실행해 oy_ranking.json 을 갱신한다. 앱(app.py)은 이 파일이
있으면 그것을, 없으면 내장 시드 스냅샷을 사용하므로 배치 실패가 서비스를
깨뜨리지 않는다.

준수 사항
- 실행 전 robots.txt 를 확인해 수집 대상 경로가 허용될 때만 요청한다.
- 요청 간격(REQUEST_INTERVAL_SEC)을 두어 서버에 부담을 주지 않는다.
- 올리브영은 봇 차단(403)을 쓰는 경우가 있어 요청이 거부될 수 있다. 그 경우
  기존 oy_ranking.json 을 건드리지 않고 종료한다(캐시/시드 유지).
- 상업적 이용 전 올리브영 이용약관 확인 및 공식 데이터 제휴 검토를 권장한다.

수집 결과 스키마 (oy_ranking.json)
{
  "updatedAt": "YYYY-MM-DD HH:MM",
  "source": "batch(oliveyoung getBestList)",
  "segmented": false,          # 연령/성별 세분화 랭킹 확보 시 true
  "entries": [
    {"cat": "toner", "rank": 1, "brand": "...", "name": "..."},
    # matchId 없이 brand+name 만 있으면 앱이 카탈로그와 자동 매칭한다.
    # segmented=true 인 entries 는 "ageGroup": "30대", "gender": "男" 를 추가한다.
  ]
}
"""

import json
import re
import sys
import time
import urllib.robotparser
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

BASE = "https://www.oliveyoung.co.kr"
BEST_PATH = "/store/main/getBestList.do"
# 올리브영 베스트 페이지의 카테고리 파라미터 → 내부 카테고리 키
CATEGORIES = {
    "toner": {"dispCatNo": "10000010001", "label": "스킨/토너"},
    "serum": {"dispCatNo": "10000010002", "label": "에센스/세럼"},
    "cream": {"dispCatNo": "10000010003", "label": "크림"},
    "sun": {"dispCatNo": "10000010011", "label": "선케어"},
    "cushion": {"dispCatNo": "10000010101", "label": "쿠션"},
    "brow": {"dispCatNo": "10000010104", "label": "아이브로우"},
    "eye": {"dispCatNo": "10000010103", "label": "아이섀도우"},
    "perfume": {"dispCatNo": "10000010401", "label": "향수"},
    "bodylotion": {"dispCatNo": "10000010301", "label": "바디로션"},
    "foot": {"dispCatNo": "10000010305", "label": "풋케어"},
    "deo": {"dispCatNo": "10000010304", "label": "데오드란트"},
}
REQUEST_INTERVAL_SEC = 2.0  # rate limit: 카테고리당 1요청, 2초 간격
TIMEOUT_SEC = 15
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
OUT = Path(__file__).parent / "oy_ranking.json"


def robots_allows(path: str) -> bool:
    try:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(BASE + "/robots.txt")
        rp.read()
        return rp.can_fetch(UA, BASE + path)
    except Exception:
        # robots.txt 확인 불가 시 보수적으로 중단
        return False


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": UA, "Accept-Language": "ko"})
    with urlopen(req, timeout=TIMEOUT_SEC) as r:
        return r.read().decode("utf-8", errors="replace")


def parse_top1(html: str):
    """베스트 목록 HTML에서 1위 상품의 (brand, name)을 추출."""
    brand = re.search(r'class="tx_brand"[^>]*>\s*([^<]+)', html)
    name = re.search(r'class="tx_name"[^>]*>\s*([^<]+)', html)
    if brand and name:
        return brand.group(1).strip(), name.group(1).strip()
    return None


def main() -> int:
    if not robots_allows(BEST_PATH):
        print("[fetch_oy_ranking] robots.txt가 수집을 허용하지 않아 중단합니다. 기존 캐시/시드를 유지합니다.")
        return 1

    entries = []
    for cat, conf in CATEGORIES.items():
        url = f"{BASE}{BEST_PATH}?dispCatNo={conf['dispCatNo']}"
        try:
            html = fetch(url)
            top = parse_top1(html)
            if top:
                entries.append({"cat": cat, "rank": 1, "brand": top[0], "name": top[1]})
                print(f"[fetch_oy_ranking] {conf['label']}: 1위 = {top[0]} {top[1]}")
            else:
                print(f"[fetch_oy_ranking] {conf['label']}: 파싱 실패(페이지 구조 변경 가능)")
        except Exception as e:
            print(f"[fetch_oy_ranking] {conf['label']}: 요청 실패 — {e}")
        time.sleep(REQUEST_INTERVAL_SEC)

    if not entries:
        print("[fetch_oy_ranking] 수집된 항목이 없어 기존 캐시/시드를 유지합니다 (봇 차단 403 가능성).")
        return 1

    OUT.write_text(
        json.dumps(
            {
                "updatedAt": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "source": "batch(oliveyoung getBestList)",
                "segmented": False,
                "entries": entries,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[fetch_oy_ranking] {len(entries)}개 카테고리 랭킹 저장 → {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
