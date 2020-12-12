import os
import pandas as pd
def get_votes_for_items(col, empty_item, mt):
    item_votes = {}
    for index, row in mt.iterrows():
        print(index)
        votes = row["km_votes"]
        item_string = row[col]
        if not isinstance(item_string, str):
            items_of_this_kernel = [empty_item]
        else:
            items_of_this_kernel = item_string.split(";")
        for item in items_of_this_kernel:
            #####
            if item in item_votes:
                item_votes[item].append(votes)
            else:
                item_votes[item] = [votes]
    return item_votes
# cvo: code_voted_original
# cvp: code_voted_pyscript
# km: kernel_measures
merged_table = r"J:\EECS6414\process\Pipeline\Data_cleaning\kernel_datssource_code.csv"
mt = pd.read_csv(merged_table, encoding="utf-8")
xxx = get_votes_for_items("km_tags", "<(no_tags)>", mt)
print(xxx)