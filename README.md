# repo.frameos.net

This repository contains the source for https://repo.frameos.net/

Hosted on CloudFlare Pages.

## Make your own repository

To create your own repo:

1. Copy the `bin/build.py` script
2. Create a `repo/` folder, and follow the structure `repo/category/template-name/`
3. Export scenes from FrameOS as .zip files, and extract them as folders under `repo/category/`
4. Optionally create `repo/category/repository.json` to name your repository.
5. Publish to CloudFlare Pages, Netlify, or wherever you host your static sites.
  - Run `bin/build.py` on deploy
  - Publish the `repo/` folder