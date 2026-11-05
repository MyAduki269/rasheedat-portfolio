# Rasheedat Animashaun — Portfolio Hub

Business analysis, project management and data analytics portfolio.

## Contents

- `dist/` — complete website: HTML, CSS, JavaScript, project data and images.
- `projects.py` — editable case-study content.
- `build.py` — generates the hub and six detailed case-study pages.
- `check.py` — checks local links, assets, headings, image alternatives and text contrast.

## Put the project in your GitHub account

1. Extract this ZIP and open the `rasheedat-portfolio` folder.
2. Sign in to GitHub and create a repository named `rasheedat-portfolio`.
3. Select **Private**. Create the repository without an additional README, license or gitignore, since this package already contains the project files.
4. On the empty repository page, choose **uploading an existing file**. In an initialized repository, choose **Add file > Upload files**.
5. Drag the CONTENTS of the extracted folder into the upload area. Include the `dist` directory and the files beside it. Do not upload only the ZIP.
6. Commit the files with the message `Add portfolio website`.

These steps store the source in your account. They do not enable website publication or automatic synchronization with the existing private site.

## Preview locally

Python 3 is required. In this folder, run:

    python3 -m http.server 8000 --directory dist

Open http://localhost:8000 in a browser. Use a local server rather than double-clicking `index.html`, because the summaries load project data with fetch.

## Edit and rebuild

Edit content in `projects.py`, then run:

    python3 build.py

Edit styling in `dist/style.css` and interactions in `dist/app.js`.
To run the optional source checks, install Python's `lxml` package, then run:

    python3 check.py

## Hosting and privacy

The existing website remains at https://rasheedat-project-hub.whitebunting.chatgpt.site with its existing private access controls.

ChatGPT sign-in is provided by the current hosting platform; it is not implemented in these static files. A private GitHub repository protects access to the source code, not necessarily access to a separately published website. Keep GitHub Pages disabled until you choose to publish.

The website currently uses root-relative URLs. Hosting at a GitHub Pages repository subpath requires adapting links, assets and fetch URLs for that base path. The `dist` directory is the deployable website output.

## Projects

- Dynamic Enterprise — HR Process Optimization
- Zerling Trust Bank — Business Intelligence & Performance Analysis
- Peakline Logistics — Operations & Delivery Performance
- Robphil Energy — Fleet Management Platform
- CAA Atlantic — Member Value for New Canadians
- CAA Atlantic — New Canadian Customer & Survey Analysis

Proposed benefits and research findings are distinguished from measured implementation outcomes within the case studies.
