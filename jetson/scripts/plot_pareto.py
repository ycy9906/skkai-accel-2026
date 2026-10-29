"""results/results.csv -> 파레토 그래프 (x: tg128 속도, y: perplexity)
사용: python scripts/plot_pareto.py [week] [base]   예) python scripts/plot_pareto.py 2 1.5B
"""
import csv, sys, os
import matplotlib.pyplot as plt

here = os.path.dirname(os.path.abspath(__file__))
week = sys.argv[1] if len(sys.argv) > 1 else None
base = sys.argv[2] if len(sys.argv) > 2 else "1.5B"

rows = [r for r in csv.DictReader(open(os.path.join(here, "..", "results", "results.csv"), encoding="utf-8"))
        if r["tg128"] and r["ppl"] and r["base"] == base and (week is None or int(r["week"]) <= int(week))]
if not rows:
    sys.exit("tg128과 ppl이 둘 다 채워진 행이 없습니다.")

fig, ax = plt.subplots(figsize=(8, 5))
for method in sorted({r["method"] for r in rows}):
    pts = [r for r in rows if r["method"] == method]
    ax.scatter([float(r["tg128"]) for r in pts], [float(r["ppl"]) for r in pts], label=method, s=50)
    for r in pts:
        ax.annotate(r["model_id"], (float(r["tg128"]), float(r["ppl"])), fontsize=8, xytext=(4, 4), textcoords="offset points")
ax.set_xlabel("tg128 (tok/s) - higher is faster")
ax.set_ylabel("perplexity (wikitext-2, c512, 40 chunks) - lower is better")
ax.set_title(f"Qwen2.5-{base} on Jetson Orin Nano: speed vs accuracy")
ax.grid(alpha=0.3)
ax.legend()
out = os.path.join(here, "..", "results", f"week{week or 'all'}_pareto.png")
fig.tight_layout()
fig.savefig(out, dpi=150)
print("saved", out)
