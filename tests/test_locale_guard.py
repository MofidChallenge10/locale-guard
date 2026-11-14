import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"src"))
from locale_guard import validate
class Tests(unittest.TestCase):
 def test_valid(self): self.assertEqual([],validate({"hi":"Hello {name}"},{"hi":"Hallo {name}"}))
 def test_missing(self): self.assertEqual("missing",validate({"a":"A"},{"b":"B"})[0]["kind"])
 def test_placeholder(self): self.assertEqual("placeholder_mismatch",validate({"a":"Hi {name}"},{"a":"Hi {user}"})[0]["kind"])
 def test_nested(self): self.assertEqual([],validate({"x":{"y":"ok"}},{"x":{"y":"gut"}}))
if __name__=="__main__": unittest.main()
