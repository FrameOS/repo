# repo.frameos.net

This repository contains the source for https://repo.frameos.net/

As of November 2025, this repository is deprecated. The files here are now bundled together with FrameOS as included sample scenes, and are part of the [main repo](https://github.com/FrameOS/frameos/).

- https://repo.frameos.net/samples/repository.json
- https://repo.frameos.net/gallery/repository.json

Hosted on CloudFlare Pages.

## Make your own repository

This repository remains an example on how to set up a custom repository, and import it into FrameOS.

1. Copy the `bin/build.py` script
2. Create a `repo/` folder, and follow the structure `repo/category/template-name/`
3. Export scenes from FrameOS as .zip files, and extract them as folders under `repo/category/`
4. Optionally create `repo/category/repository.json` to name your repository.
5. Publish to CloudFlare Pages, Netlify, or wherever you host your static sites.
  - Run `bin/build.py` on deploy
  - Publish the `dist/` folder
