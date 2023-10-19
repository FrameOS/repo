#!/usr/bin/python3
import os
import zipfile
import json

base_path = "./repo/versions"
repo_path = "./repo"

repo_links = []
version_links = []

version_folders = [os.path.join(base_path, d) for d in os.listdir(base_path) if
                   os.path.isdir(os.path.join(base_path, d))]

for version_folder in version_folders:
    template_folder_path = os.path.join(version_folder, "templates")
    if not os.path.exists(template_folder_path):
        continue

    version_links.append(os.path.basename(version_folder))
    all_template_json_data = []
    zip_links = []

    # Step 1: Get all the folders under "templates/"
    template_folders = [d for d in os.listdir(template_folder_path) if
                        os.path.isdir(os.path.join(template_folder_path, d))]


    for folder in template_folders:
        full_folder_path = os.path.join(template_folder_path, folder)

        # Step 2: Compress folder to .zip
        zip_filename = os.path.join(template_folder_path, f"{folder}.zip")
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for foldername, subfolders, filenames in os.walk(full_folder_path):
                for filename in filenames:
                    print(foldername)
                    filepath = os.path.join(foldername, filename)
                    zipf.write(filepath, os.path.relpath(filepath, template_folder_path))

        zip_links.append(f"{folder}.zip")

        # Step 3: Extract and combine template.json contents
        json_file_path = os.path.join(full_folder_path, "template.json")
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as jf:
                data = json.load(jf)
                data["zip"] = f"./templates/{folder}.zip"
                data.pop("config")
                all_template_json_data.append(data)

    # Save combined template.json
    combined_json_path = os.path.join(version_folder, "templates.json")
    with open(combined_json_path, 'w') as cjf:
        json.dump(all_template_json_data, cjf, indent=2)

    # Step 4: Create index.html
    index_html_path = os.path.join(version_folder, "index.html")
    with open(index_html_path, 'w') as ihf:
        ihf.write(f"<html><body><h1>{version_folder}</h1>\n<h2>templates</h2>\n")
        ihf.write(f'<a href="templates.json">templates.json</a><br>\n')
        for link in zip_links:
            ihf.write(f'<a href="templates/{link}">{link}</a><br>\n')
        ihf.write("</body></html>\n")


# Create index.html in the versions folder
index_html_versions_path = os.path.join(base_path, "index.html")
with open(index_html_versions_path, 'w') as ihf:
    ihf.write(f"<html><body><h1>versions</h1>")
    for link in version_links:
        ihf.write(f'<a href="{link}/">{link}</a><br>')
    ihf.write("</body></html>")

# Create index.html in the repo folder
repo_links.append("versions")
index_html_repo_path = os.path.join(repo_path, "index.html")
with open(index_html_repo_path, 'w') as ihf:
    ihf.write("<html><body><h1>repo</h1>")
    for link in repo_links:
        ihf.write(f'<a href="{link}/">{link}</a><br>')
    ihf.write("</body></html>")

print("Processing finished!")
