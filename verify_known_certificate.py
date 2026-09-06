"""Exhaustively verify the 17x17 C_10c certificate in the sibling checkout."""
from itertools import product
from pathlib import Path

source = Path(__file__).parents[1] / "optimizationproblems/constants/10c.md"
text = source.read_text()
block = text.split("## Certificate for the $7/\sqrt{17}$ lower bound", 1)[1].split("```text", 1)[1].split("```", 1)[0]
rows = [[int(x) for x in line.split()] for line in block.splitlines() if line.strip()]
assert len(rows) == 17 and all(len(r) == 17 for r in rows)
best = min(max(abs(sum(a*x for a,x in zip(row, signs))) for row in rows) for signs in product((-1,1), repeat=17))
print(f"rows={len(rows)} cols={len(rows[0])} exact_discrepancy={best}")
assert best == 7
print(f"certified lower bound = {best}/sqrt(17) = {best/(17**0.5):.12f}")
