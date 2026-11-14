"""Validate JSON translation catalogs against a reference locale."""
import argparse, json, re, sys
from pathlib import Path
PLACEHOLDER=re.compile(r"\{([A-Za-z_][A-Za-z0-9_]*)\}|%\(([A-Za-z_][A-Za-z0-9_]*)\)[sdif]")
def flatten(obj,prefix=""):
    out={}
    if isinstance(obj,dict):
        for k,v in obj.items(): out.update(flatten(v,f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(obj,str): out[prefix]=obj
    else: out[prefix]=obj
    return out
def placeholders(value):
    if not isinstance(value,str): return set()
    return {a or b for a,b in PLACEHOLDER.findall(value)}
def validate(reference,candidate):
    base=flatten(reference); other=flatten(candidate); issues=[]
    for key in sorted(base.keys()-other.keys()): issues.append({"key":key,"kind":"missing"})
    for key in sorted(other.keys()-base.keys()): issues.append({"key":key,"kind":"extra"})
    for key in sorted(base.keys() & other.keys()):
        if placeholders(base[key]) != placeholders(other[key]):
            issues.append({"key":key,"kind":"placeholder_mismatch","expected":sorted(placeholders(base[key])),"actual":sorted(placeholders(other[key]))})
    return issues
def load(path):
    with Path(path).open(encoding="utf-8") as f: return json.load(f)
def main(argv=None):
    p=argparse.ArgumentParser(description="Check translation JSON files against a source locale.")
    p.add_argument("reference"); p.add_argument("locales",nargs="+"); p.add_argument("--json",action="store_true")
    a=p.parse_args(argv); ref=load(a.reference); results={}; failed=False
    for name in a.locales:
        issues=validate(ref,load(name)); results[name]=issues; failed |= bool(issues)
    if a.json: print(json.dumps(results,ensure_ascii=False,indent=2))
    else:
        for name,items in results.items():
            print(f"{name}: {'OK' if not items else str(len(items))+' issue(s)'}")
            for item in items: print("  "+json.dumps(item,ensure_ascii=False))
    return int(failed)
if __name__=="__main__": sys.exit(main())
