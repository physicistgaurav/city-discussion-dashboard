import praw
import json
from datetime import datetime, timedelta
import re
import os

def configure_reddit_api():
    reddit = praw.Reddit(
        client_id= os.getenv('REDDIT_CLIENT_ID'),
        client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
        user_agent=os.getenv('REDDIT_USER_AGENT')
    )
    return reddit

def extract_keywords(title):
    words = re.findall(r'\w+', title.lower())
    stopwords = {'the', 'of', 'in', 'and', 'on', 'for', 'as', 'its'}
    keywords = [word for word in words if word not in stopwords]
    
    return ' '.join(keywords)

def fetch_comments_for_topic(topic, reddit, subreddits=['worldnews', 'news', 'geopolitics'], limit=5, max_age_days=30):
    comments_data = []
    current_time = datetime.now()
    max_age = timedelta(days=max_age_days)
    
    search_query = extract_keywords(topic)

    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        
        for submission in subreddit.search(search_query, sort='new', limit=limit):
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
