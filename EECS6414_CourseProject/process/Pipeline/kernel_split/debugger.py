from os.path import join
import os
catalog_dir = "/home/hdp/eecs6414/catalog/kernel_split/"
catalog_file_name = "kernel_split_{}.txt"
webpage_dir = "/home/hdp/eecs6414/catalog/kernel_webpages/"
failed_file_name = "data_failded_{}.txt"
failed_pages = []

# line_count = 0
# writer = open(join(catalog_dir, failed_file_name).format(file_count),
#               "w")
writer = None

for num in range(0, 9 + 1):
    file_name = catalog_file_name.format(num)
    # print(join(catalog_dir, file_name))
    if not os.path.exists(join(catalog_dir, file_name)):
        continue
    print(file_name)
    downloaded_pages = os.listdir(join(webpage_dir, "{}".format(num)))
    writer = open(join(catalog_dir, failed_file_name).format(num),
                  "w")

    with open(join(catalog_dir, file_name), "r") as f:
        urls = f.readlines()

        for url in urls:
            page = url.replace("/", "_")[1:].strip() + ".html"
            if page not in downloaded_pages:
                writer.write(url)

    writer.close()