#!/usr/bin/env python

import nbformat
import sys

if len(sys.argv) != 3:
  print("usage: %s INFILE OUTFILE" % sys.argv[0])
  print(sys.argv)
  sys.exit(1)

nb = nbformat.read(sys.argv[1], nbformat.NO_CONVERT)

cell = nbformat.v4.new_code_cell(""" 
import cloudpickle
validator = "validator" in globals() and globals()["validator"] or (lambda x: True)
with open("model.pickle", "wb") as f:
    f.write(cloudpickle.dumps((validator, globals()["predictor"])))

with open("extra-requirements.txt", "w") as f:
    reqs = "requirements" in globals() and globals()["requirements"] or []
    f.write("\n".join(["%s==%s" % (k,v) for k,v in reqs]))
""")

nb.cells.append(cell)

nbformat.write(nb, sys.argv[2])
