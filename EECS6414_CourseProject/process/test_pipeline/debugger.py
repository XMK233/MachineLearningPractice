import csv
import os
from os.path import join

file_dir = "C:\\Users\\xmk233\\PycharmProjects\\EECS6414\\process\\Pipeline"
file_name = "datasource_datasets_noNone.csv"
split_dir = "C:\\Users\\xmk233\\PycharmProjects\\EECS6414\\process\\Pipeline\\dataset_split"
split_file_name = "dataset_split_{}.txt"
single_file_limit = 200
if not os.path.exists(split_dir):
    os.makedirs(split_dir)

# counter = 0
with open(join(file_dir, file_name), "r") as reader:
    r = csv.reader(reader)
    line_count = 0
    file_count = 0
    writer = open(join(split_dir, split_file_name.format(file_count)), "w")
    for i in r:
        if r.line_num == 1:
            continue
        url = i[1]
        writer.write(url + "\n")
        line_count += 1
        if line_count >= single_file_limit:
            line_count = 0
            writer.close()
            file_count += 1
            writer = open(join(split_dir, split_file_name.format(file_count)), "w")
    writer.close()

        # counter += 1
        # if counter >= 10:
        #     break