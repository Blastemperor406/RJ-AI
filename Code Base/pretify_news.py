import os
from groq import Groq

def news_data(data):
    result = []
    sentiment = 0
    count = 0
    client = Groq(
    api_key="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",
)
    if data:
        for article in data['news']:
            sentiment += article['sentiment']
            count +=1
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are given a the text from a news article. Generate a summary(within 80 words) of the news text provided to look like today's headlines. You should summarize and highlight the key points from the article. The tone should be informative and neutral, suitable for a radio audience such that there are no additional audio and videos. Do not include any introductory phrases or extra words like 'Here's a summary' or 'In today's news. Only write the main content of the summary in an informative, neutral tone."
                    },
                    {
                        "role": "user", 
                        "content": f"Here are the news article in the form of an array\n{article['text']}"
                    }
                ],
                model="llama-3.1-8b-instant",
            )
            result.append(response.choices[0].message.content)
        
        return result,sentiment/count
        