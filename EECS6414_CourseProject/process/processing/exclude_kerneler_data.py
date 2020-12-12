# -*- coding: utf-8 -*-
import sys, os, json
DATA_STORE = "J:/EECS_6414/Data/19-01-17"

kernel_ids = []
counter = 0
limit = 3
for fn in os.listdir(DATA_STORE):
    if "KernelInfo" not in fn:
        continue
    print(fn)
    # counter += 1
    if counter >= limit:
        break
    #####
    with open(os.path.join(DATA_STORE, fn), "r") as f:
        kernels = json.load(f)
    for kernel in kernels:
        key = list(kernel.keys())[0]
        value = kernel[key]
        if value["author"]["displayName"] == "Kaggle Kerneler":
            continue
        title = value["scriptUrl"].replace("/", "_")[1:]
        id = key
        info = value
        new_item = {
            "id": id,
            "info": info,
            "title": title
        }
        kernel_ids.append(new_item)
        # counter+=1

with open(os.path.join(DATA_STORE, "combined_v1.json"), "w") as f:
    kernels = json.dump(kernel_ids, f)
print(len(kernel_ids))



# with open(os.path.join(DATA_STORE, "combined_v1.json"), "r") as f:
#     kernels = json.load(f)
# print(len(kernels))