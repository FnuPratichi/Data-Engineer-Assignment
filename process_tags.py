import pandas as pd
from collections import Counter

cb_df = pd.read_excel("CB_Output1_Constituents.xlsx")

all_tags_names = []
for tags_str in cb_df["CB Tags"]:
    if pd.notna(tags_str) and tags_str.strip() != "":
        tags_list = [tag.strip() for tag in tags_str.split(",")]
        all_tags_names.extend(tags_list)

tag_counts = Counter(all_tags_names)

tags_df = pd.DataFrame({
    "CB Tag Name": list(tag_counts.keys()),
    "CB Tag Count": list(tag_counts.values())
})

tags_df = tags_df.sort_values(by="CB Tag Count", ascending=False).reset_index(drop=True)
tags_df.to_excel("CB_Output2_Tags.xlsx", sheet_name="CB Tags Summary", index=False)

