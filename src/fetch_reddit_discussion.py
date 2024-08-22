import praw
import json
from datetime import datetime, timedelta
import os
from openai import OpenAI

def configure_reddit_api():
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT')
    
    # Check if any of the required environment variables are missing
    if not client_id or not client_secret or not user_agent:
        missing_vars = []
        if not client_id:
            missing_vars.append('REDDIT_CLIENT_ID')
        if not client_secret:
            missing_vars.append('REDDIT_CLIENT_SECRET')
        if not user_agent:
            missing_vars.append('REDDIT_USER_AGENT')
        
        missing_vars_str = ', '.join(missing_vars)
        raise EnvironmentError(f"Missing required environment variables: {missing_vars_str}")
    
    # If all required variables are present, configure the Reddit API
    reddit = praw.Reddit(
        client_id=client_id,
        client_secret=client_secret,
        user_agent=user_agent
    )
    return reddit


# extracting keywords function
# def extract_keywords(title):
#     words = re.findall(r'\w+', title.lower())
#     stopwords = {'the', 'of', 'in', 'and', 'on', 'for', 'as', 'its'}
#     keywords = [word for word in words if word not in stopwords]
    
#     return ' '.join(keywords)


openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise EnvironmentError("Missing required environment variable: OPENAI_API_KEY")

client = OpenAI(
    api_key=openai_api_key
)


def generate_search_prompt(topic):
    prompt = f"""
Generate a JSON object with a single field named "query". The value of this field should be a concise and effective search query for the topic '{topic}' to use on Reddit. The query should not include any additional explanations, extra quotes, or other text—just the query itself.
"""

    response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
)   
    search_prompt = response.choices[0].message.content
    try:
        search_prompt_json = json.loads(search_prompt)
        return search_prompt_json['query']
    except (KeyError, json.JSONDecodeError):
        raise RuntimeError("Error processing the response: invalid JSON or missing 'query' field.")


def fetch_comments_for_topic(topic, reddit, subreddits=['all'], limit=5, max_age_days=45):
    comments_data = []
    current_time = datetime.now()
    max_age = timedelta(days=max_age_days)

    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)

        #  openai to get search query
        search_query = generate_search_prompt(topic)  

        reddit_search = subreddit.search(search_query, sort='Relevance', limit=limit)
        for submission in reddit_search:
            post_title = submission.title
            post_id = submission.id

            post_time = datetime.fromtimestamp(submission.created_utc)
            post_age = current_time - post_time


            if post_age > max_age:
                continue

            submission = reddit.submission(id=post_id)
            submission.comments.replace_more(limit=0)  
            
            for comment in submission.comments.list()[:5]:
                comments_data.append({
                    'Subreddit': f"r/{submission.subreddit}",
                    'Post Title': post_title,
                    'Comment Body': comment.body,
                    'Author': comment.author.name if comment.author else 'Unknown',
                    'Score': comment.score,
                    'Post Age (days)': post_age.days,
                    'Comment Age (days)': (current_time - datetime.fromtimestamp(comment.created_utc)).days
                })
    
    # Sort comments by score and return the top comments
    comments_data.sort(key=lambda x: x['Score'], reverse=True)
    return comments_data[:limit]

def save_comments_to_file(comments, filename):
    with open(filename, 'w') as f:
        json.dump(comments, f, indent=4)

def main():
    with open('data/topics.json') as f:
        topics = json.load(f)

    reddit = configure_reddit_api()
    
    for topic in topics:
        comments = fetch_comments_for_topic(topic, reddit)
        save_comments_to_file(comments, f'data/{topic.replace(" ", "_")}_comments.csv')
        print(f"Saved comments for topic '{topic}' to data/{topic.replace(' ', '_')}_comments.csv")

if __name__ == '__main__':
    main()
