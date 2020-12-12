# -*- coding: utf-8 -*-
import json, os, shutil
json_path = "J:\\EECS_6414\\Data\\TEST_DATASET\\combined_v1.json"
file_from = "J:\\EECS_6414\\Data\\19-02-03\\files"
file_to = "J:\EECS_6414\Data\TEST_DATASET\\files"
if not os.path.exists(file_to):
    os.makedirs(file_to)
with open(json_path, "r") as j:
    kernels = json.load(j)
for kernel in kernels:
   title = kernel["title"]
   shutil.copytree(os.path.join(file_from, title),
                   os.path.join(file_to, title))
print("ok")
