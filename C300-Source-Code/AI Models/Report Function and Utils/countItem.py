import os
def count_items_in_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return
    
    item_count = 0
    for _, _, files in os.walk(folder_path):
        item_count += len(files)
    
    return item_count




