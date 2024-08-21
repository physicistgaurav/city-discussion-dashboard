# City News Dashboard

## Approach

The goal of this project is to build a small dashboard that provides insights into current discussions and sentiments in a specific city. The initial task involves fetching and displaying the top news topics for a given city using NewsApi.org.

### Task1: Gather Data

1. **Data Collection**:
   - Use NewsAPI to gather the top news headlines for a given city. This involves making HTTP requests to the NewsAPI endpoint and processing the JSON response to extract relevant news headlines.

2. **General Strategy**:
   - **Fetching News**: Implement a Python script to fetch news headlines using the NewsAPI. The script will take the name of a city as input and retrieve the top 5 news headlines related to that city.
   - **Error Handling**: Include error handling to manage any issues related to API requests or data processing.
   - **Output**: Display the top news headlines in a user-friendly format.


## Setup Instructions

### Project setup 

1. Clone the repository 

```<git clone https://github.com/physicistgaurav/city-discussion-dashboard.git>```

2. Navigate to the project directory:

```cd city-discussion-dashboard```

3. **Install Conda**:
   - Follow the instructions on the [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/individual) website to install Conda on your system.
   - If linux, 
   ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh
    source ~/.bashrc 

4. **Create and Activate Conda Environment**:
   ```bash
   conda create --name city_discussion_env python=3.12.4
   conda activate city_discussion_env

5. **Install the packages**:
   ```bash
    conda install --file requirements.txt

6. **Obtain NewsAPI Key**:
   - Sign up for an API key at newsapi.org and update your api-key in the environment
   ```bash
    export NEWS_API_KEY='your_api_key'

## Running the Script
    - Execute the script to input a city name and display the top 5 news 
    ```bash
    python3 src/fetch_news_topic.py     

## File Structure
    - data/: This directory is used to store any data files or cached results if needed.  

    - env/: This directory contains the Conda environment file (environment.yml) used to create and manage the project's Conda environment.

    - src/:
        - fetch_news_topic.py: Script to fetch and display the top 5 news headlines for a given city.

    - tests/: This directory will contain unit tests for key functions. 

    - README.md: Project documentation with setup instructions and usage details.

    - .gitignore: This file ensures that unnecessary files are not included in version control.

    - requirements.txt: Lists the required Python packages.
