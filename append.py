#!/usr/bin/env python

import nbformat

nb = nbformat.read("model.ipynb", nbformat.NO_CONVERT)

cell = nbformat.v4.new_code_cell(""" 
import cloudpickle
validator = "validator" in globals() and globals()["validator"] or (lambda x: True)
with open("model.pickle", "wb") as f:
    f.write(cloudpickle.dumps((validator, globals()["predictor"])))

with open("extra-requirements.txt", "w") as f:
    f.write("\n".join(["%s==%s" % (k,v) for k,v in globals()["requirements"]]))
""")

nb.cells.append(cell)

nbformat.write(nb, "patched-model.ipynb")
