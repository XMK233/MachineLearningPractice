import os, csv, wget, tqdm, time
from os.path import join 
import shutil

split_list_dir = r"J:\EECS6414\process\Pipeline\code_split"
files = os.listdir(split_list_dir)

#catalog_file_name = "code_split_voted_{}.csv"
#code_output_dir = r"J:\EECS_6414\Data\19-02-24\code_split\voted"
## if you want to change to non-voted, please look into this file(s).
catalog_file_name = "code_split_{}.csv"
code_output_dir = r"J:\EECS_6414\Data\19-02-24\code_split\noVoted"

if not os.path.exists(code_output_dir):
    os.makedirs(code_output_dir)

download_failed = join(code_output_dir, "fail_file.csv")
progress_file = join(code_output_dir, "progress.csv")
#download_temp_path = r"J:\EECS_6414\Data\19-02-24\code_split\tmp"

for num in tqdm.tqdm(range(579, 579 + 1)):
    with open(progress_file, "a") as p:
        p.write("{},{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), num))
    file_name = catalog_file_name.format(num)
    if not os.path.exists(join(split_list_dir, file_name)):
        continue
    code_path = join(code_output_dir, "{}".format(num))
    if not os.path.exists(code_path):
        os.makedirs(code_path)
    file_path = join(split_list_dir, file_name)
    with open(file_path, "r") as f:
        code_ids = csv.reader(f)
        print("in file {}: ".format(num))
        for code_id in tqdm.tqdm(code_ids):
            name = code_id[0]
            print(name)
            try:
                author = name.split("/")[1]
                id = code_id[1]
                url = "https://www.kaggle.com/kernels/scriptcontent/{}/download".format(id)
                time.sleep(2)
                code_name = wget.download(url)
                new_file_name = "{}_{}".format(author, code_name)
                shutil.move(code_name, os.path.join(code_path, new_file_name))
            except:
                with open(download_failed, "a") as fail:
                    fail.write("{},{},{}\n".format(num, name, id))