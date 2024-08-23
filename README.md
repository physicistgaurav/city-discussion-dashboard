# City News Dashboard

## Approach

The goal of this project is to build a dashboard that provides insights into current discussions and sentiments in a specific city. The first task involved fetching the top news topics for a given city using NewsApi.org. To ensure relevance, the sortBy and language parameters were used to retrieve English articles, and the fetched news articles were saved to a file. In the second task, each headline from the file generated in Task 1 was used to fetch discussions from Reddit via the PRAW(Python Reddit API Wrapper) with relevant sortby filter and limits. Before fetching, a search prompt was generated using the openai/gpt-4o-mini-2024-07-18 model. If relevant data was not found, a search for hot data was conducted applying sort filter, with limits set on post age and the number of comments fetched. The comments were sorted by descending score, and the formatted data was saved locally. The third task involved iterating over the files generated in Task 2 to analyze sentiments, summarize discussions, and identify actionable needs using the openrouter microsoft/phi-3-mini-128k-instruct:free model with appropriate parameters. The analysis results were also saved locally. Finally, the fourth task was to build a minimal frontend using React (Vite) and create a backend server with Django to serve the data via an API. The frontend communicates with the local API to visually display the fetched and analyzed data. This project structure allows for a comprehensive overview of city-specific discussions and sentiments, providing valuable insights in a user-friendly interface.

### Task 1: Gather News Data

1. **Data Collection**:

   - Use NewsAPI to gather the top news headlines for a given city. This involves making HTTP requests to the NewsAPI endpoint with parameters and processing the JSON response to extract relevant news headlines.

2. **General Strategy**:
   - **Fetching News**: Implement a Python script to fetch news headlines using the NewsAPI. The script will take the name of a city as input and retrieve the top 5 news headlines related to that city.
   - **Error Handling**: Include error handling to manage any issues related to API requests or data processing.
   - **Output**: Display the top news headlines in a user-friendly format.It saves the file to data/{city}.json

### Task 2: Gather Reddit Discussion

1. **Data Collection**:

   - Use PRAW(Python Reddit API Wrapper) to get the discussion for given headlines. This involves making api request to reddit with parameters and processing the JSON response to extract relevant discussion.

2. **General Strategy**:

   - **Fetching Disucssion**: Implement a Python script to fetch reddit discussion using the PRAW. The script will take filepath generated from task 1 as input and retrieve the discussion related to that headline
   - **Search Prompting**: It includes generating the search prompt of the headline which can be used to search in reddit API. It uses openai/gpt-4o-mini-2024-07-18 llm from OpenRouter
   - **Error Handling**: Include error handling to manage any issues related to API requests or data processing.
   - **Output**: Display the top discussion in a user-friendly format and save to data/reddit/{headline}\_comments.csv

### Task 3: Analyse Reddit Discussion

1. **Data Collection**:

   - Use microsoft/phi-3-mini-128k-instruct:free to get the summary,sentiment and actionable needs for given discussion. This involves making api request to openRouter with parameters and processing the JSON response to extract relevant information.

2. **General Strategy**:

   - **Fetching Disucssion**: Implement a Python script to fetch analysis on reddit discussion using OpenRouter with appropriate parameters. The script will take filepath generated from task 2 as input and retrieve the analysis related to that discussion
   - **Error Handling**: Include error handling to manage any issues related to API requests.
   - **Output**: Display the top discussion in a user-friendly format and save to data/analysis/{topic}\_analysis.json

### Task 4: Build a small front-end

- Use React(vite) with tailwind to create a frontend which displays the work from task 1, task 2 and task 3.
- API calls are made to the local backend server to get the relevant data.
- Include error handling to manage any issues related to API requests.
- Used conditional rendering and loading signal for smooth interaction on the webpage.

## Setup Instructions

### Project Setup

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/physicistgaurav/city-discussion-dashboard.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd city-discussion-dashboard
   ```

3. **Install Conda**:

   - Follow the instructions on the [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/individual) website to install Conda on your system.
   - For Linux:
     ```bash
     wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
     bash Miniconda3-latest-Linux-x86_64.sh
     source ~/.bashrc
     ```

4. **Create and Activate Conda Environment**:

   ```bash
   conda create --name city_discussion_env python=3.12.4
   conda activate city_discussion_env
   ```

5. **Install the Packages**:

   ```bash
   conda install --file requirements.txt
   ```

6. **Obtain NewsAPI Key, Reddit API key and OpenRouter API Key**:

   - Sign up for an API key at [newsapi.org](https://newsapi.org) and update your API key in the environment:
   - Sign up for an API key at [old.reddit](https://old.reddit.com/prefs/apps/) and update your API key in the environment:
   - Sign up for an API key at [openrouter.ai](https://openrouter.ai/sign-in) and update your API key in the environment:

   Note: Please update your environment files : NEWS_API_KEY, REDDIT_CLIENT_ID , REDDIT_CLIENT_SECRET , REDDIT_USER_AGENT , OPENROUTER_API_KEY API keys.

   For example: you can activate them by

   ```bash
   export NEWS_API_KEY='your_api_key'
   export REDDIT_CLIENT_ID='your_api_key'
   export REDDIT_CLIENT_SECRET='your_api_key'
   export REDDIT_USER_AGENT='your_application_name'
   export OPENROUTER_API_KEY='your_api_key'
   ```

## Running the Script

Execute the script to input a city name and display the top 5 news:

Note: Please update your environment variables before running the script.

```bash
python3 backend/src/fetch_news_topic.py
python3 backend/src/test_fetch_reddit_discussion.py
python3 backend/src/test_analyze_gathered_info.py
```

## Running the Frontend

Navigate to:

```bash
cd frontend/city-discussion
npm i
npm run dev
```

This will start the frontend server on localhost port 5473

## Running the Backend

Navigate to:

```bash
cd backend/
python3 manage.py runserver
```

This will start the backend server on localhost port 8000

Note: Please update your environment variables before using the APIs.

## Test Cases

Test cases are written using unitest.

```bash
python3 -m unittest backend.tests.test_fetch_news_topic
python3 -m unittest backend.tests.test_fetch_reddit_discussion
python3 -m unittest backend.tests.test_analyze_gathered_info
```

This will start the backend server on localhost port 8000

Note: Please update your environment variables before using the APIs.

## File Structure

    backend/: This directory is used to store all the backend part in one place

    backend/data/: This directory is used to store any data files or cached results if needed.It caontains reddit folder
    for reddit related file and analysis folder for analysis related file.

    backend/src/:
        fetch_news_topic.py: Script to fetch and display the top 5 news headlines for a given city.
        fetch_reddit_discussion.py: Script to fetch and display the reddit discussion from news headline.
        analyze_gathered_info.py: Script to analyze the discussion extracted from reddit discussion.

    backend/project/: This directory contains our backend project created using django.

    tests/: This directory will contain unit tests for key functions.

    env/: This directory contains the Conda environment file (environment.yml) used to create and manage the project's Conda environment.

    README.md: Project documentation with setup instructions and usage details.

    .gitignore: This file ensures that unnecessary files are not included in version control.

    requirements.txt: Lists the required Python packages.

## Usage

    1. Clone the repository and set up the Conda environment as described in the setup instructions.

    2. Obtain your NewsAPI key, RedditAPI Key and OpenRouterAPI key and set it as an environment variable.

    3. Run the scripts as mentioned in Running the Script to get the output data

    4.Run the Frontend server followed by Backend server if youu want to see on web.
