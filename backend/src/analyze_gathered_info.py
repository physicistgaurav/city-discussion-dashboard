import os
import json
import requests

# microsoft/phi-3-mini-128k-instruct:free
# google/gemma-7b-it:free

def call_openrouter_api(prompt, top_p = 1, temperature = 0, frequency_penalty = 0, presence_penalty =0):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        data=json.dumps({
            "model": "microsoft/phi-3-mini-128k-instruct:free",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "top_p": top_p,
            "temperature": temperature,   
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
        })
    )
    return response.json()['choices'][0]['message']['content'].strip()

# Function to summarize the overall discussion
def summarize_discussion(discussions):
    combined_text = " ".join(discussions)
    prompt = (
        "Summarize the key themes, arguments, or points from the following discussion in 2-3 sentences. Focus only on relevant and on-topic information while ignoring unrelated or humorous remarks. For example, if the discussion is about a logistics challenge, prioritize comments that discuss the challenge itself, such as 'It was difficult to transport due to narrow roads.' Ignore off-topic comments like jokes ('This reminds me of a scene from a movie!') or pop culture references ('This looks like something from Fast & Furious.'). Here's the discussion: "
        f"{combined_text}"
    )
    return call_openrouter_api(prompt,top_p=0.9, temperature=0.5 , frequency_penalty=0, presence_penalty= 0)

# Function to analyze the sentiment of the discussion
def analyze_sentiment(discussions):
    combined_text = " ".join(discussions)
    prompt = (
        "Analyze the sentiment of the following discussion, classifying it as positive, neutral, or negative. Focus on comments relevant to the primary topic, and provide a brief reasoning for your classification. For example, if the discussion is generally supportive, like 'This process was well executed,' the sentiment is positive. Exclude any irrelevant jokes ('This sounds like a comedy sketch') or unrelated cultural references ('This could be in a superhero movie'). Here's the discussion: "
        f"{combined_text}"
    )
    return call_openrouter_api(prompt, top_p=1, temperature=0,frequency_penalty=0, presence_penalty=0)

# Function to identify actionable needs from the discussion
def identify_actionable_needs(discussions):
    combined_text = " ".join(discussions)
    prompt = (
        "Review the following discussion and identify any actionable needs, concerns, or relevant suggestions. Focus on comments directly related to the topic and that point out issues or recommendations, such as 'The equipment should be tested more thoroughly next time.' Ignore irrelevant or humorous comments like jokes ('Someone should turn this into a meme!') or unrelated pop culture references ('This is straight out of a sci-fi movie.'). Here's the discussion: "
        f"{combined_text}"
    )
    return call_openrouter_api(prompt, top_p=0.9, temperature=0.2, frequency_penalty=0.5, presence_penalty=0.5)

# Function to get summary, sentiment and actionable needs
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
                comments = json.load(f)
                discussions = [f"Main News Topic: {comment['newsTopic']} | Reddit-Post on this news: {comment['PostTitle']} | Comment on this post by people: {comment['CommentBody']}" for comment in comments]
            
            # Perform the analyses
            summary,sentiment, actionable_needs = getAnalyzedReport(discussions)
            
            # Save the results
            save_analysis_to_json(topic, summary, sentiment, actionable_needs)
            print(f"Analysis saved for topic '{topic}'")
        else:
            print(f"File not found: {filename}")

if __name__ == '__main__':
    main()
