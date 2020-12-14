from os.path import join
import os
catalog_dir = "/home/seasun/eecs6414/catalog/dataset_split/"
catalog_file_name = "dataset_split_{}.txt"
webpage_dir = "/home/seasun/eecs6414/webpage/dataset_split/"
failed_file_name = "data_failded_{}.txt"
failed_pages = []

file_count = 0
line_count = 0
writer = open(join(catalog_dir, failed_file_name).format(file_count),
              "w")

for num in range(0, 78 + 1):
    file_name = catalog_file_name.format(num)
    # print(join(catalog_dir, file_name))
    if not os.path.exists(join(catalog_dir, file_name)):
        continue
    print(file_name)
    downloaded_pages = os.listdir(join(webpage_dir, "{}".format(num)))
    with open(join(catalog_dir, file_name), "r") as f:
        urls = f.readlines()
        for url in urls:
            page = url.replace("/", "_")[1:].strip() + ".html"
            if page not in downloaded_pages:
                failed_pages.append(url)
                print(page)
                writer.write(url)
                line_count += 1
                if line_count >= 200:
                    writer.close()
                    line_count = 0
                    file_count += 1
                    writer = open(join(catalog_dir, "data_failded_{}.txt").format(file_count),
                                  "w")
writer.close()
print(failed_pages)