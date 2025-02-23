import os
import sys

# Add the directory of my_module.py to sys.path
#sys.path.append(os.path.abspath("../Mapping/zedtoppkl/"))
abs_path = os.path.abspath("../Mapping/zedtoppkl/")
print(os.path.exists(abs_path))

