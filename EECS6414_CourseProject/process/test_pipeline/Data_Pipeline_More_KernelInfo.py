
# coding: utf-8

# # This is a pipeline for parsing multiple KernelInfo files. 

# # Exclude Kerneler

# In[12]:


# -*- coding: utf-8 -*-
import sys, os, json
DATA_STORE = "J:\\EECS_6414\\Data\\TEST_DATASET1"
DATA_SOURCE = "J:\\EECS_6414\\Data\\19-02-03"
available_file_number = [i for i in range(13)]#
available_file_number.extend([21, 22, 23, 31, 32, 33, 34, 35])

kernel_ids = []
counter = 0
limit = 3
for fn in available_file_number:
    print(os.path.join(DATA_SOURCE, "KernelInfo_{}.json".format(fn)))
    with open(os.path.join(DATA_SOURCE, "KernelInfo_{}.json".format(fn)), "r") as f:
        kernels = json.load(f)
    for kernel in kernels:
        value = kernel["info"]
        if value["author"]["displayName"] == "Kaggle Kerneler":
            continue
        kernel_ids.append(kernel)
        # counter+=1

with open(os.path.join(DATA_STORE, "combined_v1.json"), "w") as f:
    kernels = json.dump(kernel_ids, f)
print(len(kernel_ids))


# # get files of kernels for this pipeline

# In[14]:


# -*- coding: utf-8 -*-
import json, os, shutil
json_path = "J:\\EECS_6414\\Data\\TEST_DATASET1\\combined_v1.json"
file_from = "J:\\EECS_6414\\Data\\19-02-03\\files"
file_to = "J:\EECS_6414\Data\TEST_DATASET1\\files"
if not os.path.exists(file_to):
    os.makedirs(file_to)
with open(json_path, "r") as j:
    kernels = json.load(j)
for kernel in kernels:
    title = kernel["title"]
    ###############
    ## sometimes there is something wrong in it. 
    ###############
    try: 
        shutil.copytree(os.path.join(file_from, title),
                       os.path.join(file_to, title))
    except:
        pass
print("хорошо ok")


# # Download Authors and Datasets from Kaggle using Spider in "crawler"
# * I don't know why, only 1 item in all of the 2 will be download. Whatever, this is not the top concern now. 
# * 2019年2月9日 in terms of the result I got now, I can say that the author gathering is OK now. 

# # Move the author and dataset to Test Directory

# * Don't worry. Take it easy. 

# In[21]:


json_path = "J:\\EECS_6414\\Data\\TEST_DATASET1\\combined_v1.json"

author_path = "J:\\EECS_6414\\Data\\19-02-03\\test_pages\\author_pages"
target_author_path = "J:\\EECS_6414\\Data\\TEST_DATASET1\\author_pages"
dataset_path = "J:\\EECS_6414\\Data\\19-02-03\\test_pages\\dataset_pages"
target_dataset_path = "J:\\EECS_6414\\Data\\TEST_DATASET1\\dataset_pages"

with open(json_path, "r") as j:
    kernels = json.load(j)
authorUrls = []
datasetUrls = []
for kernel in kernels:
    info = kernel["info"]
    title = kernel["title"]

    #item = OverallDownload()
    authorUrls.append(info["author"]["profileUrl"])
    datasetUrls.extend([ds["dataSourceUrl"] for ds in info["dataSources"] if ds is not None])

authorUrls = list(set(authorUrls))
print("author urls. this number is approximate: ", len(authorUrls))
datasetUrls = list(set(datasetUrls))
print("dataset urls. this number is approximate: ", len(datasetUrls))



# In[22]:


print(authorUrls)


# In[23]:


print(datasetUrls)


# In[30]:


#############################
### I don't know why there is 
### some file missing. 
#############################

for a in authorUrls: 
    a_ = a.replace("/", "") + ".html"
    try:
        shutil.copy(
            os.path.join(author_path, a_), 
            os.path.join(target_author_path, a_)
        )
    except:
        pass

for d in datasetUrls: 
    if d is None:
        continue
    d_ = d.replace("/", "_")[1:] + ".html"
    #print(d_)
    try: 
#         print(d_)
        shutil.copy(
            os.path.join(dataset_path, d_), 
            os.path.join(target_dataset_path, d_)
        )
    except:
        pass


# # Parse Author

# * 这个脚本里面的东西还算靠谱。可以改进。This script is relatively complete. You can furtherly work on this. 

# In[32]:


import json, os, shutil, re
from lxml import etree
from tqdm import tqdm 

Author_path = "J:\\EECS_6414\\Data\\19-02-03\\test_pages\\author_pages"
csv_file = "J:\\EECS_6414\\Data\\TEST_DATASET2\\stats\\author_stats.csv"
c = open(csv_file, "w")
c.write("author,competition,cmp_tier,kernel,scpt_tier,discussion,dsc_tier,follower,following\n")
counter = 0
flag = True
for page_name in tqdm(os.listdir(Author_path)):
    author = page_name.split(".")[0]
    # # tester:
    # if author != "breakfastpirate" and flag:
    #     continue
    # flag = False
    # ##############
    with open(os.path.join(Author_path, page_name), "r", encoding="utf-8") as f:
        html = f.read()
    page_source = etree.HTML(html)
    ###########
    # this part is for dealing with the problem
    # of: too many request.
    # we have to abondon those "too many requests" pages temprarily.
    ###########
    if page_source.xpath("/html/body/pre/text()") != []:
        continue
    ############
    _ = page_source.xpath("//div[@class='site-layout__main-content']/script[1]/text()")[0]
    p = re.compile("Kaggle\.State\.push\(\{[\s\S]*\}\)\;")
    try:
        s = p.findall(_)[0].replace("Kaggle.State.push(", "")[0:-2]
        info = json.loads(s)
    except:
        ##############################
        # this place occurs because
        # we will fail to crawl such information
        ##############################
        print("{} failed: cannot get info.".format(author))
        continue
    try:
        c.write("{},{},{},{},{},{},{},{},{}\n".format(
            info["userName"],
            info["competitionsSummary"]["totalResults"],info["competitionsSummary"]["tier"],
            info["scriptsSummary"]["totalResults"],info["scriptsSummary"]["tier"],
            info["discussionsSummary"]["totalResults"],info["discussionsSummary"]["tier"],
            info["followers"]["count"], info["following"]["count"]
            ).replace("novice", "1").replace("contributor", "2").replace("expert", "3").replace("grandmaster", "5").replace("master", "4")
        )
    except:
        print("{} info is bad.".format(author))
        continue
c.close()
print("хорошо, total number is: {}".format(counter))


# # Parse Dataset

# * 2019年2月10日. This is OK now. Can be further modified. 

# In[1]:


import json, os, shutil, re
from lxml import etree
from tqdm import tqdm

def get_ajax_json(parameter, page_size):
    # parameter is the parameter of json url.
    # it looks like "&competition=9988"
    import requests
    num = 0
    url = "https://www.kaggle.com/kernels.json?sortBy=hotness&group=everyone{}&pageSize={}".format(parameter,page_size)
    next_url = url
    while True:
        r = requests.get(next_url,
                         auth=('user', 'pass')).json()
        if len(r) == 0:
            break
        elif len(r) > 0 and len(r) < page_size:
            num += len(r)
            break
        else:
            num += len(r)
            last_id = r[len(r) - 1]["id"]
            next_url = url + "&after={}".format(last_id)
    return num

Author_path = "J:\\EECS_6414\\Data\\19-02-03\\test_pages\\dataset_pages"
competition_file = "J:\\EECS_6414\\Data\\TEST_DATASET2\\stats\\competition_stats.csv"
dataset_file = "J:\\EECS_6414\\Data\\TEST_DATASET2\\stats\\dataset_stats.csv"
c = open(competition_file, "w", encoding="utf-8")
c.write("competition,organization,size,discussion,competitors\n")#",kernels" was the last feature.
d = open(dataset_file, "w", encoding="utf-8")
d.write("dataset,author,size,discussions,kernels,downloads,views,vote,version\n")
# dataset: name
# author: name
# competition: yes or not
# size: how many bytes
# discussion: how many discussions if applicable. in "discussion"
# kernel: how many kernels if applicable
# vote: how many votes if applicable
# version: how many versions of dataset if applicable

counter = 0

flag = True
for page_name in tqdm(os.listdir(Author_path)):
    ################################
    ### some kernel pages' name is "kernels_deleted_xxxxxxx".
    ### I don't know why this kind of pages comes into being.
    ### maybe this kernel is just deleted. Simple as it is.
    ### Just ignore it first.
    ################################
    # if page_name != "del=cd0be45190c25545_glove.42b.300d.html" and flag:
    #     continue
    if "kernels_deleted_" in page_name:
        continue
    # #### testing:
    # if page_name != "matschiner_nationmaster.html" and flag:
    #     continue
    # flag = False
    ##################################
    author = page_name.split(".")[0]
    with open(os.path.join(Author_path, page_name), "r", encoding="utf-8") as f:
        html = f.read()
    page_source = etree.HTML(html)
    ###########
    # this part is for dealing with the problem
    # of: too many request.
    # we have to abondon those "too many requests" pages temprarily.
    ###########
    if page_source.xpath("/html/body/pre/text()") != []:
        continue
    ############

    print(page_name)
    try:
        _ = page_source.xpath("//div[@class='site-layout__main-content']/script[1]/text()")[0]
    except:
        ##############################
        # this place occurs because
        # we will fail to crawl such information
        ##############################
        print("{} failed: json information cannot be parsed".format(author))
        continue
    p = re.compile("Kaggle\.State\.push\(\{[\s\S]*\}\)\;")
    try:
        s = p.findall(_)[0].replace("Kaggle.State.push(", "")[0:-2]
        info = json.loads(s)
    except:
        ##############################
        # this place occurs because
        # we will fail to crawl such information
        ##############################
        print("{} failed: cannot get info".format(author))
        continue
    #####################
    ## some pages will contain kernel page infomation.
    ## this is supposed to be the error of scrapy.
    ## for now, lets' just skip this kind of error.
    #####################
    if "kernel" in info:
        continue
    ##########################
    ##Some pages will still have problem, so let's just
    ## skip them.
    ##########################
    try:
        if "competitionId" in info:
            # it is a competition
            c.write("{},{},{},{},{}\n".format(#,{}
                info["competitionSlug"], info["organizationSlug"],
                info["databundle"]["totalSize"], info["totalDiscussions"],
                info["totalCompetitors"] #,get_ajax_json("&competitionId={}".format(info["competitionId"]), 200)
                )
            )
            pass
        else:
            d.write("{},{},{},{},{},{},{},{},{}\n".format(
                info["slug"],
                info["owner"]["slug"],info["data"]["totalSize"],
                info["numberOfTopics"],info["numberOfScripts"],
                info["numberOfDownloads"], info["numberOfViews"],
                info["voteCount"],info["datasetVersionTotalCount"]
                )
            )
    except:
        print("{} info is bad.".format(author))
        continue
c.close()
d.close()
print("хорошо")


# # Parse Kernel
# * there is a problem. If a kernel uses several datasets, we cannot fit all information into measures. How to manage corresponding data in measures? Here is my solution: how many datasets they used, information of the first one dataset (what dataset it is, the type of this dataset). 

# * 2019年2月10日. First version of kernel parse. You can add more features like code and comment features.  
# * 2019年2月20日 If you are not intented to move any files, you can skip all of the previous steps and go directly from here. 

# In[3]:


import json, os, shutil, re
from lxml import etree
import tqdm

Author_path = "J:\\EECS_6414\\Data\\19-02-03\\files"
csv_file = "J:\\EECS_6414\\Data\\TEST_DATASET2\\stats\\kernel_stats.csv"
c = open(csv_file, "w", encoding="utf-8")
c.write("kernel,author,datasets,source1st,sourceType1st,versions,forks,comments,views,votes\n")
#kernel: "kernel""slug"
#author: "kernel""author""userName"
#competition: if this kernel is for competition.
#versions: "menuLinks", "title" is "Versions", "count"
#forks: "menuLinks", "title" is "Forks", "count"
#comments: "menuLinks", "title" is "Comments", "count"
#views: "kernel""viewCount"
#votes: "kernel""upvoteCount"
#about source: because a kernel may use several datasets, so here I just take the first dataset into consideration.
counter = 0

for page_name in tqdm.tqdm(os.listdir(Author_path)):
    try:
        with open(os.path.join(Author_path, page_name + "\\webpages.html"), "r", encoding="utf-8") as f:
            html = f.read()
        page_source = etree.HTML(html)
        ##################
        # sometimes, the html parsing can get none.
        # just skip this kind of situation
        ##################
        if page_source == None:
            continue
    except:
        print("no such file: {}".format(page_name))
        continue
    ###########
    # this part is for dealing with the problem
    # of: too many request.
    # we have to abondon those "too many requests" pages temprarily.
    ###########
    if page_source.xpath("/html/body/pre/text()") != []:
        print("bad file: {}".format(page_name))
        continue
    ############
    try:
        _ = page_source.xpath("//div[@class='site-layout__main-content']/script[1]/text()")[0]
    except:
        print("cannot parse json: {}".format(page_name))
        continue
    p = re.compile("Kaggle\.State\.push\(\{[\s\S]*\}\)\;")
    try:
        s = p.findall(_)[0].replace("Kaggle.State.push(", "")[0:-2]
        info = json.loads(s)
    except:
        ##############################
        # this place occurs because
        # we will fail to crawl such information
        ##############################
        print("{} failed: cannot get info".format(page_name))
        continue
    ## about versions and comments
    versions = 0
    comments = 0
    try:
        for menulink in info["menuLinks"]:
            if menulink["title"] == "Versions":
                versions = menulink["count"]
            elif menulink["title"] == "Comments":
                comments = menulink["count"]
            else:
                pass
    except:
        ##############################
        # this place occurs because
        # we will fail to crawl such information
        ##############################
        print("{} failed: bad info at version and comments".format(page_name))
        continue
    ####about dataset
    try:
        source = None
        sourceType = None
        tmp = info["dataSources"]
        datasets = len(tmp)
        print(page_name)
        if tmp != []:
            source = tmp[0]["slug"]
            sourceType = tmp[0]["sourceType"]
    except:
        ##############################
        # this place occurs because
        # we will fail to crawl such information
        ##############################
        print("{} failed: bad info at data sources".format(page_name))
        continue
    # saving to file
    try:
        c.write("{},{},{},{},{},{},{},{},{},{}\n".format(
            info["kernel"]["slug"],
            info["kernel"]["author"]["userName"],
            datasets, source, sourceType,
            versions, info["kernel"]["forkCount"], comments,
            info["kernel"]["viewCount"], info["kernel"]["upvoteCount"]
            )
        )
    except:
        print("{} failed. Some bad info".format(page_name))
        continue
c.close()
print("хорошо, total number is: {}".format(counter))


# # Model Fitting Parts

# * join the tables

# In[2]:


import pandas as pd
import os
os.chdir("J:\\EECS_6414\\Data\\TEST_DATASET2")
author = pd.read_csv("stats/author_stats.csv", encoding="utf-8")
author.rename(index=str, 
              columns={"competition": "author_competitions", 
                                  "kernel": "author_kernels", 
                                  "discussion": "author_discussions", 
                                  "follower": "author_followers",
                                  "following": "author_following"}, 
              inplace=True)

competition = pd.read_csv("stats/competition_stats.csv",encoding ='latin1') ## very strange
competition.rename(index=str, 
             columns={"discussion": "competition_discussion"#, 
                      }, #"kernels": "competition_kernels"
             inplace= True)

dataset = pd.read_csv("stats/dataset_stats.csv",encoding ='utf-8')
dataset.rename(index=str, 
              columns={"author": "dataset_author", 
                                  "discussions": "dataset_discussions", 
                                  "kernels": "dataset_kernels", 
                                "downloads": "dataset_downloads", 
                               "views": "dataset_views", 
                               "vote": "dataset_votes", 
                                  "version": "dataset_versions"}, 
              inplace=True)

kernel = pd.read_csv("stats/kernel_stats.csv", encoding="utf-8")
kernel.rename(index=str, 
             columns={"datasets": "kernel_datasets", 
                      "versions": "kernel_versions"}, 
             inplace= True)

# kernel_competition_author.csv generating: 
kernel_competition = kernel[kernel["sourceType1st"]=="competition"]
kernel_competition = kernel_competition.drop(['sourceType1st'], axis=1)
kernel_competition.rename(index=str, columns={"source1st": "competition"}, inplace=True)

a = pd.merge(kernel_competition, competition, on='competition')
b = pd.merge(a, author, on='author')
b.to_csv("kernel_competition_author.csv", index=None)

# kernel_dataset_author.csv generating: 
kernel_dataset = kernel[kernel["sourceType1st"]=="dataset"]
kernel_dataset = kernel_dataset.drop(['sourceType1st'], axis=1)
kernel_dataset.rename(index=str, columns={"source1st": "dataset"}, inplace=True)

a = pd.merge(kernel_dataset, dataset, on='dataset')
b = pd.merge(a, author, on='author')
b.to_csv("kernel_dataset_author.csv", index=None)

print("хорошо, total number is: {}".format(counter))

# See if the multi-dataset is prevalent
