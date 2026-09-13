"""Deterministic numerical illustration; not a proof of the theorem."""
from pathlib import Path
import json
import numpy as np
r=Path(__file__).resolve().parent/'simulation_results';r.mkdir(exist_ok=True)
rng=np.random.default_rng(23);error=0.0
for n in [1,2,3,10,100]:
 for _ in range(20):
  x=rng.normal(size=n);a=float(rng.normal());mean=float(x.mean());lhs=float(np.mean((x-a)**2));rhs=float(np.mean((x-mean)**2)+(a-mean)**2);error=max(error,abs(lhs-rhs));assert np.isclose(lhs,rhs)
(r/'checks.json').write_text(json.dumps(dict(seed=23,cases=100,max_absolute_error=error,role='Illustration; not a proof'),indent=2)+'\n')
print('100 numerical checks passed; maximum absolute error',error)
