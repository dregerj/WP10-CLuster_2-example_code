# Using scraping and RAG for predict NACE category
## Introduction

For this work we used 3 data sources: 
1. **Scrap Data** from our sources of URL`s 
2. **Sythetic data** this source it was generated based on scrapeed data
3. **Norwegian dataset** we translate to polisch some descriptions and use a summarize function to build shorter texts to LLM

For work we used:
1. **Python** - versin 3.14.2
2. **ChromaDB** - for embeding data base
3. **Transformers** - library for use LLM models
4. **Playwright** - library to scrap dynamic webpages 

---

# Step 1 – Scraping data

## Main goal of scraping
- Get comapanys description to predict NACE (in poland PKD) category 
## Pipeline

1. Set a URL's to scrap in file column WWW in source.csv on the Scrapping folder,
2. Go to Scraping file and start scrap.py with command **py scrap.py**,
3. The results will be saved in output.csv file. I output file it was 3 kolumns, WebPage, Desription, ScrapedWebPage ,
4. If links to scrap doesnt have a protocol like HTTP or HTTPS, webscraper try find right protocol
---

# Step 2 Summarize the scrapped data
## Main goal summarize
- Get the shortest much more better textest for RAG and LLM teach. 

## Pipeline

1. Go to the Summary folder
2. In conf.py file you have a definitions, settings, global varibles used in our program. Here you can change the LLM model, input files names, change the temperature parameter for less precision text. 
3. Run file **index.py** in summary filder whith command: **py index.py** 

---

# Step 3 - RAG 
## Mail goal 
- Predict a NACE based on 3 sources of data

## Pipeline

1. Go to RAG folder. 
2. Run the index.py file whith command: **py index.py** 
3. First step we prepare dataframe based on **rag_source.csv** file. 
4. Next step it's a build database using 3 step. Parameters and global varibles are in **rag_databas.py** file.
5. Last step it's return the 3 similar NACE codes to test file records and save the result to csv file
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
