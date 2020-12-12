# -*- coding: utf-8 -*-
import sys, os, json
DATA_STORE = "J:\\EECS_6414\\Data\\TEST_DATASET"

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
        # key = list(kernel.keys())[0]
        value = kernel["info"]
        if value["author"]["displayName"] == "Kaggle Kerneler":
            continue
        kernel_ids.append(kernel)
        # counter+=1

with open(os.path.join(DATA_STORE, "combined_v1.json"), "w") as f:
    kernels = json.dump(kernel_ids, f)
print(len(kernel_ids))

# with open(os.path.join(DATA_STORE, "combined_v1.json"), "r") as j:
#     kernels = json.load(j)
# authorUrls = []
# datasetUrls = []
# for kernel in kernels:
#     info = kernel["info"]
#     title = kernel["title"]
#
#     # item = OverallDownload()
#     authorUrls.append(info["author"]["profileUrl"])
#     datasetUrls.extend([ds["dataSourceUrl"] for ds in info["dataSources"] if ds is not None])
# print(len(set(authorUrls)))
# print(len(set(datasetUrls)))