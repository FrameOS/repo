#!/usr/bin/python3
import os
import zipfile
import json

base_path = "./repositories"

repo_links = []

repositories = [os.path.join(base_path, d) for d in os.listdir(base_path) if
                os.path.isdir(os.path.join(base_path, d))]

for repo in repositories:
    repo_name = os.path.basename(repo)
    repo_folders = [d for d in os.listdir(repo) if
                    os.path.isdir(os.path.join(repo, d))]

    all_template_json_data = []

    for folder in repo_folders:
        full_folder_path = os.path.join(repo, folder)
        zip_filename = os.path.join(repo, f"{folder}.zip")

        # Compress folder to .zip
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            for foldername, subfolders, filenames in os.walk(full_folder_path):
                for filename in filenames:
                    filepath = os.path.join(foldername, filename)
                    arcname = os.path.relpath(filepath, start=repo)
                    zipf.write(filepath, arcname)

        # Prepare data for repository.json
        template_data = {"name": folder, "zip": f"./{folder}.zip"}
        all_template_json_data.append(template_data)

    # Save combined data to repository.json
    combined_json_path = os.path.join(repo, "repository.json")
    with open(combined_json_path, 'w') as cjf:
        json.dump(all_template_json_data, cjf, indent=2)

    # Create index.html for the repository
    index_html_path = os.path.join(repo, "index.html")
    with open(index_html_path, 'w') as ihf:
        ihf.write(f"<html><body><h1>{repo_name}</h1>\n<h2>templates</h2>\n")
        ihf.write(f'<a href="repository.json">repository.json</a><br>\n')
        for data in all_template_json_data:
            ihf.write(f'<a href="{data["zip"]}">{data["name"]}.zip</a><br>\n')
        ihf.write("</body></html>\n")

    repo_links.append(repo_name)

# Create index.html in the base path
index_html_base_path = os.path.join(base_path, "index.html")
with open(index_html_base_path, 'w') as ihf:
    ihf.write("<html><body><h1>Repositories</h1>")
    for link in repo_links:
        ihf.write(f'<a href="{link}/">{link}</a><br>')
    ihf.write("</body></html>")

print("Processing finished!")
