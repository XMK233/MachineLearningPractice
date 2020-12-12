import json, os

DATA_DIR = "C:\\Users\\xmk233\\PycharmProjects\\EECS6414\\crawler\\crawler\\Data"
DATA_DIR_1 = "J:\\EECS_6414\\Data\\19-01-17"

def Distribution_KI(file_name = "KernelInfo"):
    def add_to_table(table, key, value):
        if key in table:
            table[key].append(value)
        else:
            table[key] = [value]
    ##############################
    #define data structure
    nVote_kernel = {}
    author_kernel = {}
    dataset_kernel = {}
    ##############################
    files = os.listdir(DATA_DIR)
    for file in files:
        ############
        if file_name not in file:
            continue
        ############
        with open(os.path.join(DATA_DIR, file)) as f:
            kernels = json.load(f)
        ###### the last file can be empty. So be careful
        if len(kernels) == 0:
            continue
        #####
        for kernel in kernels:
            ###########
            #get vote information
            kernelId = kernel["id"]
            nVotes = kernel["info"]["totalVotes"]
            '''if nVotes in nVote_kernel:
                nVote_kernel[nVotes].append(kernelId)
            else:
                nVote_kernel[nVotes] = [kernelId]'''
            add_to_table(nVote_kernel, nVotes, kernelId)
            ##########
            #get information about author
            authorId = kernel["info"]["author"]["id"]
            '''if authorId in author_kernel:
                author_kernel[authorId].append(kernelId)
            else:
                author_kernel[authorId] = [kernelId]'''
            add_to_table(author_kernel, authorId, kernelId)
            ###########
            # get information about dataset
            dataSources = kernel["info"]["dataSources"] # get a list
            for dataSource in dataSources:
                sourceId = dataSource["sourceId"]
                add_to_table(dataset_kernel, sourceId, kernelId)


    ######################
    vl = []
    al = []
    dl = []
    for key in nVote_kernel:
        vl.extend([key] * len(nVote_kernel[key]))
    for key in author_kernel:
        al.append(len(author_kernel[key]))
    for key in dataset_kernel:
        dl.append(len(dataset_kernel[key]))

    def change(l, x = "", y = ""):
        l.sort()
        from collections import Counter
        result = Counter(l)
        import csv
        with open("{}_{}.csv".format(x, y), 'w', newline='') as f:
            w = csv.writer(f)
            #w.writerows((x, y))
            w.writerows(dict(result).items())
        #return list(result.keys()), list(result.values())

    def show(l, color= "red"):
        l.sort()
        from collections import Counter
        result = Counter(l)
        plt.bar(list(result.keys()), list(result.values()), edgecolor=color)
        plt.show()
        return


    print(nVote_kernel)
    print(vl)
    #change(vl, "TheNumberOfVoteAKernelHas", "nKernel")

    print(author_kernel)
    print(al)
    #change(al, "TheNumberOfKernelAnAuthorHas", "nAuth")

    print(dataset_kernel)
    print(dl)
    #change(dl, "UsedByHowManyKernels", "nDataset")

def Distribution_KI_1(file_name = "KernelInfo"):
    def add_to_table(table, key, value):
        if key in table:
            table[key].append(value)
        else:
            table[key] = [value]
    ##############################
    #define data structure
    nVote_kernel = {}
    author_kernel = {}
    dataset_kernel = {}
    ##############################
    files = os.listdir(DATA_DIR_1)
    for file in files:
        ############
        if file_name not in file:
            continue
        ############
        with open(os.path.join(DATA_DIR_1, file)) as f:
            kernels = json.load(f)
        ###### the last file can be empty. So be careful
        if len(kernels) == 0:
            continue
        #####
        for kernel in kernels:
            kernelId = list(kernel.keys())[0]
            info = kernel[kernelId]
            ###########
            #get vote information
            nVotes = info["totalVotes"]
            add_to_table(nVote_kernel, nVotes, kernelId)
            ##########
            authorId = info["author"]["id"]
            add_to_table(author_kernel, authorId, kernelId)
            #########
            dataSources = info["dataSources"]  # get a list
            for dataSource in dataSources:
                sourceId = dataSource["sourceId"]
                add_to_table(dataset_kernel, sourceId, kernelId)
    ############################################
    vl = []
    al = []
    dl = []
    for key in nVote_kernel:
        vl.extend([key] * len(nVote_kernel[key]))
    for key in author_kernel:
        al.append(len(author_kernel[key]))
    for key in dataset_kernel:
        dl.append(len(dataset_kernel[key]))

    def show(l, color= "red", chart_type = "bar"):
        l.sort()
        from collections import Counter
        result = Counter(l)
        if chart_type == "bar":
            plt.bar(list(result.keys()), list(result.values()), edgecolor=color)
            plt.show()
        elif chart_type == "hist":
            plt.hist(l, bins=100)
            plt.show()
        return

    def change1d(l, x=""):
        l.sort()
        import csv
        with open("{}.csv".format(x), 'w', newline='') as f:
            for i in l:
                f.write("%d\n"%(i))

    def change2d(l, x = "", y = ""):
        l.sort()
        from collections import Counter
        result = Counter(l)
        import csv
        with open("{}_{}.csv".format(x, y), 'w', newline='') as f:
            w = csv.writer(f)
            w.writerows(dict(result).items())

    # change2d(vl, "TheNumberOfVoteAKernelHas", "nKernel")
    # change2d(al, "TheNumberOfKernelAnAuthorHas", "nAuth")
    # change2d(dl, "UsedByHowManyKernels", "nDataset")

    # show(vl, chart_type= "hist")
    # show(al, chart_type="hist")
    # show(dl, chart_type="hist")

    change1d(vl, "VoteNumberThatEachKernelHas")
    change1d(al, "KernelNumberThatEachAuthorHas")
    change1d(dl, "KernelNumberThatEachDatasetHas")

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab

def draw_pie_chart(file, discard = 0):
    a = pd.read_csv(file, header=-1)

    if isinstance(discard, int):# discard the foremost "discard" raws.
        a.drop([i for i in range(discard)], inplace= True)
    elif isinstance(discard, list):
        a.drop(discard, inplace= True)
    else:
        pass

    explodes = [k % 5 / 50 for k in range(len(a))]
    plt.figure(figsize=(15,15))
    plt.pie(
        a[1],
        explode= explodes,
        labels=a[0]
    )
    plt.show()

def draw_histogram(file, discard = 0, bin_size = -1, image_wide= 15):
    # discard the foremost "discard" raws.
    # set the bin_size to be larger than 0, you can use the bin,
    # otherwise, the bin size will be default 1.
    a = pd.read_csv(file, header=-1)
    ##########
    if isinstance(discard, int):
        a.drop([i for i in range(discard)], inplace= True)
    elif isinstance(discard, list):
        a.drop(discard, inplace= True)
    else:
        pass
    print(a[1].iloc[0], a[1].iloc[-1])
    #########
    if bin_size >= 0:
        mn = int(a[0].min())
        mx = int(a[0].max())
        bin_num = (mx - mn + 1) // bin_size + 1
        tp = mn
        new_a = pd.DataFrame()
        for i in range(bin_num):
            sum_ = a[(a[0] >= tp) & (a[0] <= tp + bin_size - 1)][1].sum()
            upbound = tp + bin_size - 1
            _ = pd.DataFrame([[upbound,sum_]])
            new_a = new_a.append(_)
            tp += bin_size
        new_a.reset_index(drop= True, inplace= True)
        new_a[1].replace(to_replace= 0, value= 0.1, inplace= True)
        new_a[1] = np.log(new_a[1])

        plt.figure(figsize=(image_wide, 15))
        plt.bar(new_a[0],new_a[1], width= bin_size - 2)
        plt.savefig(file.split(".")[0] + "_bin_size_{}.jpg".format(bin_size))
        #plt.show()
    else:
        plt.figure(figsize=(image_wide,15))
        plt.bar(a[0], np.log(np.log(a[1]).replace(to_replace= 0.1, value= 0.1)))
        plt.savefig(file.replace(file.split(".")[1], "jpg"))
        #plt.show()

def draw_histogram_bin(file):
    a = pd.read_csv(file, header=-1)
    #unique_count = len(a[0].unique())
    max_num = a[0].max()
    min_num = a[0].min()
    plt.figure(figsize=(15, 15))
    plt.hist(np.log(a[0]), bins=((max_num - min_num) // 50 + 1))
    plt.show()

def Distribution_KI_Counter2(file, stop_value = 1):
    a = pd.read_csv(file, header=-1)
    print(
        sum([a[1].iloc[i] for i in range (stop_value)])
        /
        a[1].sum())

def Distribution_KI_Counter3(file_name = "KernelInfo"):
    files = os.listdir(DATA_DIR_1)
    authors = set()
    kernel_sum = 0
    datasets = set()
    for file in files:
        ############
        if file_name not in file:
            continue
        ############
        with open(os.path.join(DATA_DIR_1, file)) as f:
            kernels = json.load(f)
        ###### the last file can be empty. So be careful
        if len(kernels) == 0:
            continue
        ######
        kernel_sum += len(kernels)
        for kernel in kernels:
            kernelId = list(kernel.keys())[0]
            info = kernel[kernelId]
            #########
            authorId = info["author"]["displayName"]
            authors.add(authorId)
            #########
            dataSources = info["dataSources"]  # get a list
            for dataSource in dataSources:
                sourceId = dataSource["sourceId"]
                datasets.add(sourceId)
    print("total number of kernels: ", kernel_sum)
    print("total number of authors: ", len(authors))
    print("total number of datasets: ", len(datasets))

def Distribution_KI_Counter1(file_name = "KernelInfo"):
    def add_to_table(table, key, value):
        if key in table:
            table[key].append(value)
        else:
            table[key] = [value]
    ##############################
    #define data structure
    nVote_kernel = {}
    author_kernel = {}
    dataset_kernel = {}
    ##############################
    files = os.listdir(DATA_DIR_1)
    for file in files:
        ############
        if file_name not in file:
            continue
        ############
        with open(os.path.join(DATA_DIR_1, file)) as f:
            kernels = json.load(f)
        ###### the last file can be empty. So be careful
        if len(kernels) == 0:
            continue
        #####
        for kernel in kernels:
            kernelId = list(kernel.keys())[0]
            info = kernel[kernelId]
            ###########
            #get vote information
            nVotes = info["totalVotes"]
            add_to_table(nVote_kernel, nVotes, kernelId)
            ##########
            authorId = info["author"]["displayName"]
            add_to_table(author_kernel, authorId, kernelId)
            #########
            dataSources = info["dataSources"]  # get a list
            for dataSource in dataSources:
                sourceId = dataSource["sourceId"]
                add_to_table(dataset_kernel, sourceId, kernelId)
    ############################################
    vl = []
    al = []
    dl = []
    for key in nVote_kernel:
        vl.extend([key] * len(nVote_kernel[key]))
    for key in author_kernel:
        al.append(len(author_kernel[key]))
        if len(author_kernel[key]) > 9000:
            print(key)
    for key in dataset_kernel:
        dl.append(len(dataset_kernel[key]))

if __name__ == "__main__":
    # Distribution_KI()

    # Distribution_KI_1()

    # draw_pie_chart("bar_chart_nested_log/TheNumberOfKernelAnAuthorHas_nAuth.csv")
    # draw_pie_chart("bar_chart_nested_log/TheNumberOfVoteAKernelHas_nKernel.csv")
    # draw_pie_chart("bar_chart_nested_log/UsedByHowManyKernels_nDataset.csv")

    # draw_histogram("bar_chart_nested_log/TheNumberOfKernelAnAuthorHas_nAuth.csv", bin_size= 50)
    # draw_histogram("bar_chart_nested_log/TheNumberOfVoteAKernelHas_nKernel.csv", bin_size= 50)
    # draw_histogram("bar_chart_nested_log/UsedByHowManyKernels_nDataset.csv", bin_size= 50)

    # draw_histogram("bar_chart_nested_log/TheNumberOfKernelAnAuthorHas_nAuth.csv", image_wide= 150)
    # draw_histogram("bar_chart_nested_log/TheNumberOfVoteAKernelHas_nKernel.csv", image_wide= 150)
    # draw_histogram("bar_chart_nested_log/UsedByHowManyKernels_nDataset.csv", image_wide= 150)

    #Distribution_KI_Counter1()
    Distribution_KI_Counter2("bar_chart_nested_log/TheNumberOfVoteAKernelHas_nKernel.csv", 2)
    #Distribution_KI_Counter3()