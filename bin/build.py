#!/usr/bin/python3
import os
import zipfile
import json

src_path = "./repo"
base_path = "./dist"

# Tailwind CSS template for the index files
tailwind_css = """
<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
"""

# Create base_path directory if it does not exist
if not os.path.exists(base_path):
    os.makedirs(base_path)

os.system(f"cp -r {src_path}/* {base_path}")

repo_links = []

repositories = [os.path.join(base_path, d) for d in os.listdir(base_path) if
                os.path.isdir(os.path.join(base_path, d))]

for repo in repositories:
    repo_name = os.path.basename(repo)
    repo_folders = [d for d in os.listdir(repo) if
                    os.path.isdir(os.path.join(repo, d))]

    # Attempt to load existing repository.json if it exists
    existing_repo_data = {"name": repo_name, "templates": []}  # Default structure
    combined_json_path = os.path.join(repo, "repository.json")
    if os.path.exists(combined_json_path):
        with open(combined_json_path, 'r') as f:
            existing_repo_data = json.load(f)
        if "templates" not in existing_repo_data:
            existing_repo_data["templates"] = []
        existing_repo_data["name"] = existing_repo_data.get("name", repo_name)

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

        template_json_path = os.path.join(full_folder_path, "template.json")
        template_data = {"name": folder, "zip": f"./{folder}.zip"}
        if os.path.exists(template_json_path):
            with open(template_json_path, 'r') as f:
                template = json.load(f)
                template_data['name'] = template.get('name', template_data['name'])
                if template.get('image', None):
                    template_data['image'] = template.get('image', None)
                    if template_data['image'].startswith('./'):
                        template_data['image'] = "./" + folder + "/" + template_data['image'][2:]
                if template.get('description', None):
                    template_data['description'] = template.get('description', None)

        # Append data for this template to the "templates" key
        existing_repo_data["templates"].append(template_data)

    # Save or update repository.json with combined data
    with open(combined_json_path, 'w') as cjf:
        json.dump(existing_repo_data, cjf, indent=2)

    # Create index.html for the repository
    index_html_path = os.path.join(repo, "index.html")
    with open(index_html_path, 'w') as ihf:
        ihf.write(f"<html><head>{tailwind_css}</head><body class='p-6'>\n")
        ihf.write(f"<h1 class='text-3xl font-bold mb-4'>{repo_name}</h1>\n")
        ihf.write(f'<a href="repository.json" class="text-blue-500 underline mb-4 block">repository.json</a>\n')
        ihf.write("<div class='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4'>\n")
        for data in existing_repo_data["templates"]:
            img_path = data.get("image", "https://via.placeholder.com/150")
            ihf.write(f"""
            <div class="border rounded-lg overflow-hidden shadow-lg">
                <img src="{img_path}" alt="{data['name']}" class="w-full h-48 object-cover">
                <div class="p-4">
                    <h2 class="font-semibold text-lg">{data['name']}</h2>
                    <a href="{data['zip']}" class="text-blue-500 underline mt-2 block">Download</a>
                </div>
            </div>
            """)
        ihf.write("</div></body></html>\n")

    repo_links.append(repo_name)

# Create index.html in the base path
index_html_base_path = os.path.join(base_path, "index.html")
with open(index_html_base_path, 'w') as ihf:
    ihf.write(f"<html><head>{tailwind_css}</head><body class='p-6'>\n")
    ihf.write("<h1 class='text-3xl font-bold mb-4'>Repositories</h1>\n")
    for link in repo_links:
        ihf.write(f'<a href="{link}/" class="text-blue-500 underline block mb-2">{link}</a>\n')
    ihf.write("</body></html>")

print("Processing finished!")
