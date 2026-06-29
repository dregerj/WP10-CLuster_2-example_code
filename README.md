# Using Scraping and RAG to Predict NACE Categories
## Introduction

This project uses three data sources: 
1. **Scrap Data** company descriptions collected from a list of URLs,
2. **Sythetic data** generated based on the scraped data,
3. **Norwegian dataset** company descriptions translated into Polish and summarized to create shorter texts suitable for LLM processing.

This project is built using:
1. **Python** - versin 3.14.2
2. **ChromaDB** - vector database for storing embeddings
3. **Transformers** - library for working with LLMs
4. **Playwright** - library for scraping dynamic web pages

---

# Step 1 – Scraping data

## Goal
- Get comapanys description to predict NACE (in Poland PKD) category 
## Pipeline

1. Add the URLs to be scraped to the WWW column in source.csv located in the Scraping folder.

2. Navigate to the Scraping folder and run:

    `py scrap.py`

3. The results will be saved to output.csv. The output file contains three columns:
- WebPage
- Description
- ScrapedWebPage

4. If a URL does not include a protocol (`http://` or `https://`), the scraper will attempt to detect and use the correct protocol automatically.

---

# Step 2 Summarize the scrapped data
## Goal
- Generate short, high-quality descriptions that improve RAG retrieval and LLM performance.

## Pipeline

1. Navigate to the Summary folder.
2. Open `conf.py`, which contains the project's configuration, global variables, and settings. Here you can:
- change the LLM model,
- specify input file names,
- adjust the temperature parameter.
3. Run:
`py index.py`

---

# Step 3 - RAG 
## Goal 
- Predict the NACE category using all three data sources.

## Pipeline

1. Navigate to the RAG folder.

2. Run:
`py index.py`
3. The program prepares a DataFrame based on `rag_source.csv`.
4. It then builds the vector database using the three data sources. Configuration parameters and global variables are defined in `rag_database.py`.
5. Finally, the application retrieves the three most similar NACE codes for each test record and saves the results to a CSV file.
---

# Example code in Onyxia

You can test our example code on Onyxia. Click the button below to launch Onyxia with the Visual Studio Code service and our repository already loaded.

<a href="https://datalab.sspcloud.fr/launcher/ide/vscode-python?name=vscode-python&version=2.5.7&s3=default&git.repository=«https%3A%2F%2Fgithub.com%2Fdregerj%2FWP10-CLuster_2-example_code.git»&autoLaunch=true" target="_blank" rel="noopener" data-original-href="https://datalab.sspcloud.fr/launcher/ide/vscode-python?name=vscode-python&version=2.5.7&s3=default&git.repository=«https%3A%2F%2Fgithub.com%2Fdregerj%2FWP10-CLuster_2-example_code.git»&autoLaunch=true"><img src="https://custom-icon-badges.demolab.com/badge/SSP%20Cloud-Launch_with_VSCode-blue?logo=vsc&amp;logoColor=white" alt="Onyxia"></a>



## How to set enviorment

1. Open a new terminal and navigate to the repository directory:

    `cd WP10-CLuster_2-example_code/`

2. Run command:

    `uv sync`

3. Next open Command Palette and change Python interpreter:

    *ctr+schift+p  or f1*

    *Python: Select Interpreter > Enter interpreter path > /home/onyxia/work/WP10-CLuster_2-example_code/.venv/bin/python*

4. Open Jupyter notebook file and change kernel:

    *change kernel  -> Select another kernel > Python enviorments > .venv*
