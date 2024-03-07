# repo.frameos.net

This repository contains the source for https://repo.frameos.net/

The repository is currently shared through GitHub pages.

## Make your own repository

To create your own repo:

1. Clone https://github.com/FrameOS/repo/
2. Clean the `repositories/` folder, and follow the structure `repositories/repository-name/template-name/`
3. Export scenes from FrameOS as .zip files, extract them as folders under `repositories/repository-name/`
4. Publish to GitHub, watch the GitHub actions runner recompress and consolidate the templates, then push them to the `gh-actions` branch.
5. Make sure your ([and your organization's!](https://github.com/JamesIves/github-pages-deploy-action/issues/1110#issuecomment-1124172063)) GitHub actions have read and write permissions.
6. Enable GitHub pages on the `gh-actions` branch, and set the source to the root of the `gh-actions` branch.
7. Done! Your repository is now available at https://your-username.github.io/repo/repository-name/

