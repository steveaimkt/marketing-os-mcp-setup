#!/usr/bin/env python3
"""
gsheet-ad-report · 범용 광고 리포트 집계기
어떤 광고 엑셀/CSV든 헤더를 자동 감지해 6개 분석 표를 JSON으로 출력한다.

사용법:
    python3 analyze.py [데이터파일경로] [--top N] [--out 출력JSON경로]
    # 경로 생략 시 ../실습 데이터/ 에서 .xlsx/.csv 자동 탐색

출력: report_tables.json (요약·키워드·일별·지면·캠페인·효자·낭비)
의존성: openpyxl (xlsx) — pip3 install openpyxl --break-system-packages
"""
import sys, os, json, glob, argparse
from collections import defaultdict

# ---- 컬럼 자동 감지 규칙 (우선순위 순, 부분일치) ----
# 매출/주문은 '1일' 기여도 우선 (쿠팡/네이버 리포트는 1일·14일 둘 다 존재)
RULES = {
    "date":     ["날짜", "일자", "date"],
    "keyword":  ["키워드", "검색어", "keyword"],
    "campaign": ["캠페인명", "캠페인 이름", "캠페인", "campaign"],
    "area":     ["노출 지면", "노출지면", "지면", "매체", "placement"],
    "imp":      ["노출수", "노출", "impression"],
    "clk":      ["클릭수", "클릭", "click"],
    "cost":     ["광고비", "비용", "지출", "cost", "spend"],
    "ord":      ["총 주문수(1일)", "주문수(1일)", "주문수", "총 전환수(1일)", "전환수", "전환", "conversion", "order"],
    "rev":      ["총 전환매출액(1일)", "전환매출액(1일)", "전환매출", "매출", "revenue", "sales"],
}

def detect_columns(header):
    """헤더(list[str])에서 역할→인덱스 매핑. 부분일치, 규칙 내 앞 항목 우선."""
    idx = {}
    norm = [str(h).strip() if h is not None else "" for h in header]
    for role, keys in RULES.items():
        found = None
        for key in keys:                       # 규칙 우선순위대로
            for i, h in enumerate(norm):
                if i in idx.values():
                    continue
                if key.lower() in h.lower():
                    found = i
                    break
            if found is not None:
                break
        if found is not None:
            idx[role] = found
    return idx

def load_rows(path):
    """xlsx/csv → (header:list, rows:list[tuple])"""
    if path.lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        ws = wb.active
        it = ws.iter_rows(values_only=True)
        header = list(next(it))
        rows = [r for r in it]
        return header, rows
    elif path.lower().endswith(".csv"):
        import csv
        with open(path, encoding="utf-8-sig") as f:
            r = list(csv.reader(f))
        return r[0], [tuple(x) for x in r[1:]]
    raise SystemExit(f"지원하지 않는 형식: {path}")

def num(v):
    if v is None or v == "" or v == "-":
        return 0
    if isinstance(v, (int, float)):
        return v
    try:
        return float(str(v).replace(",", "").replace("%", "").replace("원", "").strip())
    except ValueError:
        return 0

def pct(n, d): return f"{n/d*100:.1f}%" if d else "0.0%"
def won(n, d): return round(n/d) if d else 0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default=None)
    ap.add_argument("--top", type=int, default=40)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    path = a.path
    if not path:
        here = os.path.dirname(os.path.abspath(__file__))
        cands = []
        for pat in ("*.xlsx", "*.csv"):
            cands += glob.glob(os.path.join(here, "..", "실습 데이터", pat))
            cands += glob.glob(os.path.join(here, "..", "실습데이터", pat))
        if not cands:
            raise SystemExit("데이터 파일을 찾지 못했습니다. 경로를 직접 지정하세요.")
        path = sorted(cands, key=os.path.getmtime)[-1]

    header, rows = load_rows(path)
    idx = detect_columns(header)
    required = ["imp", "clk", "cost"]
    missing = [r for r in required if r not in idx]
    if missing:
        raise SystemExit(f"필수 컬럼 미감지: {missing}\n감지된 헤더: {header}")

    def g(row, role):
        return num(row[idx[role]]) if role in idx and idx[role] < len(row) else 0
    def gs(row, role):
        return str(row[idx[role]]) if role in idx and idx[role] < len(row) and row[idx[role]] is not None else "-"

    kw = defaultdict(lambda: [0, 0, 0, 0, 0.0])   # imp, clk, cost, ord, rev
    day = defaultdict(lambda: [0, 0, 0, 0, 0.0])
    area = defaultdict(lambda: [0, 0, 0, 0, 0.0])
    camp = defaultdict(lambda: [0, 0, 0, 0, 0.0])
    T = [0, 0, 0, 0, 0.0]

    for r in rows:
        vals = (g(r, "imp"), g(r, "clk"), g(r, "cost"), g(r, "ord"), g(r, "rev"))
        for i in range(5):
            T[i] += vals[i]
        kw[gs(r, "keyword")] = [x + y for x, y in zip(kw[gs(r, "keyword")], vals)]
        if "date" in idx:
            day[gs(r, "date")] = [x + y for x, y in zip(day[gs(r, "date")], vals)]
        if "area" in idx:
            area[gs(r, "area")] = [x + y for x, y in zip(area[gs(r, "area")], vals)]
        if "campaign" in idx:
            camp[gs(r, "campaign")] = [x + y for x, y in zip(camp[gs(r, "campaign")], vals)]

    out = {"meta": {"file": os.path.basename(path), "rows": len(rows),
                    "detected": {k: header[v] for k, v in idx.items()}}}

    out["summary"] = {
        "노출": int(T[0]), "클릭": int(T[1]), "광고비": int(T[2]),
        "주문": int(T[3]), "매출": int(T[4]),
        "ROAS": pct(T[4], T[2]), "CTR": pct(T[1], T[0]), "CVR": pct(T[3], T[1]),
        "CPC": won(T[2], T[1]), "CPA": won(T[2], T[3]),
        "키워드수": len(kw),
    }

    ks = sorted(kw.items(), key=lambda x: -x[1][2])[:a.top]
    out["kw"] = [["순위", "키워드", "노출수", "클릭수", "광고비", "주문수", "매출", "CTR", "CVR", "CPC", "CPA", "ROAS"]]
    for i, (k, v) in enumerate(ks, 1):
        out["kw"].append([i, k, int(v[0]), int(v[1]), int(v[2]), int(v[3]), int(v[4]),
                          pct(v[1], v[0]), pct(v[3], v[1]), won(v[2], v[1]), won(v[2], v[3]), pct(v[4], v[2])])

    if day:
        out["day"] = [["날짜", "노출수", "클릭수", "광고비", "주문수", "매출", "ROAS"]]
        for k in sorted(day):
            v = day[k]
            out["day"].append([k, int(v[0]), int(v[1]), int(v[2]), int(v[3]), int(v[4]), pct(v[4], v[2])])

    if area:
        out["area"] = [["노출지면", "노출수", "클릭수", "광고비", "주문수", "매출", "CTR", "CVR", "ROAS"]]
        for k, v in sorted(area.items(), key=lambda x: -x[1][2]):
            out["area"].append([k, int(v[0]), int(v[1]), int(v[2]), int(v[3]), int(v[4]),
                               pct(v[1], v[0]), pct(v[3], v[1]), pct(v[4], v[2])])

    if camp:
        out["camp"] = [["캠페인", "노출수", "클릭수", "광고비", "주문수", "매출", "ROAS"]]
        for k, v in sorted(camp.items(), key=lambda x: -x[1][2]):
            out["camp"].append([k, int(v[0]), int(v[1]), int(v[2]), int(v[3]), int(v[4]), pct(v[4], v[2])])

    # 효자: 광고비 상위 의미구간(전체의 0.7% 이상) 중 ROAS 상위 10
    thr = max(50000, T[2] * 0.007)
    big = [(k, v) for k, v in kw.items() if v[2] >= thr]
    out["hero"] = [["키워드", "광고비", "매출", "ROAS"]]
    for k, v in sorted(big, key=lambda x: -(x[1][4] / x[1][2] if x[1][2] else 0))[:10]:
        out["hero"].append([k, int(v[2]), int(v[4]), pct(v[4], v[2])])

    # 낭비: 매출 0 키워드 (광고비순 TOP15) + 총액·개수
    waste_all = [(k, v) for k, v in kw.items() if v[4] == 0 and v[2] > 0]
    out["waste"] = [["키워드", "노출수", "클릭수", "광고비(낭비)"]]
    for k, v in sorted(waste_all, key=lambda x: -x[1][2])[:15]:
        out["waste"].append([k, int(v[0]), int(v[1]), int(v[2])])
    out["waste_total"] = int(sum(v[2] for _, v in waste_all))
    out["waste_count"] = len(waste_all)

    out_path = a.out or os.path.join(os.path.dirname(os.path.abspath(path)), "report_tables.json")
    json.dump(out, open(out_path, "w"), ensure_ascii=False, indent=1)

    print(f"✅ 집계 완료 → {out_path}")
    print(f"   파일: {out['meta']['file']} ({out['meta']['rows']}행)")
    print(f"   감지 컬럼: {out['meta']['detected']}")
    s = out["summary"]
    print(f"   광고비 {s['광고비']:,}원 · 매출 {s['매출']:,}원 · ROAS {s['ROAS']} · 키워드 {s['키워드수']}개")
    print(f"   낭비 키워드 {out['waste_count']}개 · {out['waste_total']:,}원")

if __name__ == "__main__":
    main()
