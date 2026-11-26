"""Lightweight mutation testing: mutates sports_tms.py via AST, runs pytest on each mutant."""
import ast, copy, subprocess, sys, shutil, os, tempfile, json

SRC = open("sports_tms.py").read()
CMP = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt, ast.Eq: ast.NotEq, ast.NotEq: ast.Eq}

class Collector(ast.NodeVisitor):
    def __init__(self): self.sites = []
    def visit_Compare(self, n):
        for i, op in enumerate(n.ops):
            if type(op) in CMP: self.sites.append(("cmp", n.lineno, n, i))
        self.generic_visit(n)
    def visit_Constant(self, n):
        if type(n.value) is int and not isinstance(n.value, bool): self.sites.append(("const", n.lineno, n, None))
    def visit_BoolOp(self, n): self.sites.append(("bool", n.lineno, n, None)); self.generic_visit(n)

tree = ast.parse(SRC)
c = Collector(); c.visit(tree)
n_sites = len(c.sites)
results = []
for idx in range(n_sites):
    t = ast.parse(SRC); col = Collector(); col.visit(t)
    kind, line, node, i = col.sites[idx]
    if kind == "cmp": node.ops[i] = CMP[type(node.ops[i])]()
    elif kind == "const": node.value += 1
    else: node.op = ast.Or() if isinstance(node.op, ast.And) else ast.And()
    ast.fix_missing_locations(t)
    d = tempfile.mkdtemp()
    open(os.path.join(d, "sports_tms.py"), "w").write(ast.unparse(t))
    shutil.copy("test_sports_tms.py", d)
    r = subprocess.run([sys.executable, "-m", "pytest", "-x", "-q", "-p", "no:cacheprovider"], cwd=d, capture_output=True)
    results.append({"id": idx + 1, "line": line, "kind": kind, "killed": r.returncode != 0})
    shutil.rmtree(d)
killed = sum(r["killed"] for r in results)
print(f"mutants={len(results)} killed={killed} survived={len(results)-killed} score={100*killed/len(results):.1f}%")
for r in results:
    if not r["killed"]: print("SURVIVED:", r)
json.dump(results, open("../06_Test_Reports/mutation_results.json", "w"), indent=1)
