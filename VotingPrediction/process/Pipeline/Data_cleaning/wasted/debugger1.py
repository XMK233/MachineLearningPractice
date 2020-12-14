import json, os, shutil, re, time
from lxml import etree
from tqdm import tqdm
import pygount, ast
from _ast import *
START_NUMBERS = [i for i in range(300,450)]

def parse_notebook(path):
    num_of_cell = 0
    num_of_output = 0
    ####据统计，就只有这么四种输出了。
    output_type_count = {"display_data": 0, "stream": 0, "execute_result": 0, "error": 0}  #
    try:
        #####################
        ## why try here?
        ## because if it is not a notebook, it will not open by json.load, and it will return error.
        ## retunr error, we will just simply return multiple 0s.
        #####################
        with open(path, "r", encoding="utf-8") as f:
            j = json.load(f)
        for cell in j["cells"]:
            num_of_cell += 1
            if "outputs" not in cell:
                continue
            for output in cell["outputs"]:
                num_of_output += 1
                output_type = output["output_type"]
                if output_type in output_type_count:
                    output_type_count[output_type] += 1
    except:
        pass

    new_list = [num_of_cell, num_of_output]
    new_list.extend(list(output_type_count.values()))
    return new_list


Author_path = r"J:\EECS_6414\Data\19-02-24\code_split\noVoted\origin_code"

cleaning_result_path = r"J:\EECS_6414\Data\19-02-24\code_split\noVoted\origin_code_clean_result\measures_from_origin"
competition_file = os.path.join(cleaning_result_path, "code_stats_origin_{}.csv")
if not os.path.exists(cleaning_result_path):
    os.makedirs(cleaning_result_path)

log_file = os.path.join(cleaning_result_path, "logs.txt")
process_file = os.path.join(cleaning_result_path,
                            "process.txt")  # time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
header_info = "kernel,author,num_of_cell,num_of_output,display_data,stream,execute_result,error\n"

counter = 0

flag = True
for folder in tqdm(START_NUMBERS):
    if not os.path.isdir(
            os.path.join(Author_path, "{}".format(folder))
    ):
        continue
    c = open(competition_file.format(folder), "w", encoding="utf-8")
    c.write(header_info)  # ",kernels" was the last feature.
    files_path = os.path.join(Author_path, "{}".format(folder))
    for page_name in (os.listdir(files_path)):
        try:
            suffix = page_name.split(".")[-1]
            if "py" not in suffix:
                continue
            #########################
            #             if (".ipynb" in page_name or ".xpynb" in page_name):
            #                 # something related to python notebook

            #                 pass
            #             elif ".py" in page_name:
            #                 # something related to py script

            #                 pass
            parse_result = parse_notebook(
                os.path.join(files_path, page_name)
            )
            c.write("{},{},".format(page_name.split("_")[-1].split(".")[0], page_name.split("_")[-2]) +
                    ",".join(["{}".format(item) for item in parse_result]) +
                    "\n")
        except:
            with open(log_file, "a") as log:
                log.write("{},{},{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                              folder,
                                              page_name)
                          )
            continue
    with open(process_file, "a") as pro:
        pro.write("{},{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                   folder
                                   )
                  )
    c.close()
    print("The {} is хорошо.".format(folder))