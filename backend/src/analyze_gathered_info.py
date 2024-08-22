import os
import json
import requests

def call_openrouter_api(prompt):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        },
        data=json.dumps({
            "model": "mistralai/mistral-7b-instruct:free",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        })
    )
    return response.json()['choices'][0]['message']['content'].strip()

# Function to summarize the overall discussion
def summarize_discussion(discussions):
    combined_text = " ".join(discussions)
    prompt = (
        "Summarize the following discussions in 2-3 sentences, focusing on the main highlights and key concerns: "
        f"{combined_text}"
    )
    return call_openrouter_api(prompt)

# Function to analyze the sentiment of the discussion
def analyze_sentiment(discussions):
    combined_text = " ".join(discussions)
    prompt = (
        "Analyze the sentiment of the following discussions in one sentence. Indicate whether it is positive, negative, or neutral: "
        f"{combined_text}"
    )
    return call_openrouter_api(prompt)

# Function to identify actionable needs from the discussion
def identify_actionable_needs(discussions):
    combined_text = " ".join(discussions)
    prompt = (
        "Identify actionable needs from the following discussions in a list of 2-3 key points: "
        f"{combined_text}"
    )
    return call_openrouter_api(prompt)

# Function to identify actionable needs from the discussion
def getAnalyzedReport(discussions):
    summary = summarize_discussion(discussions)
    sentiment = analyze_sentiment(discussions)
    actionable_needs = identify_actionable_needs(discussions)
    return summary, sentiment, actionable_needs

# Function to save the analysis results to a JSON file
def save_analysis_to_json(topic, summary, sentiment, actionable_needs):
    result = {
        "topic": topic,
        "summary": summary,
        "sentiment": sentiment,
        "actionable_needs": actionable_needs
    }

    filename = f'data/analysis/{topic.replace(" ", "_")}_analysis.json'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(result, f, indent=4)

def main():
    with open('data/topics.json') as f:
        topics = json.load(f)

    for topic in topics:
        filename = f'data/reddit/{topic.replace(" ", "_")}_comments.csv'
        
        if os.path.exists(filename):
            with open(filename) as f:
                discussions = [comment['CommentBody'] for comment in json.load(f)]
            
            # Perform the analyses
            summary,sentiment, actionable_needs = getAnalyzedReport(discussions)
            
            # Save the results
            save_analysis_to_json(topic, summary, sentiment, actionable_needs)
            print(f"Analysis saved for topic '{topic}'")
        else:
            print(f"File not found: {filename}")

if __name__ == '__main__':
    main()
