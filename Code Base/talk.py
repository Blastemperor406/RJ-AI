import ollama
import elevenlabs

client = elevenlabs.client.ElevenLabs(api_key='sk_f12ce640d451b07ddfc80aa92c08b961e7c520746d74ff14')


def talk(choice,content):

    if choice==1:
        prompt='News articles have been played. Provide a paragraph of commentary on the following news article.give your opinions.Urge the users to reach out with opinions.'
        content="News articles:" +". ".join(content)
    elif choice==2:
        prompt='Some songs have been played. Provide a paragraph of commentary summing up the played songs. Give us fun facts/opinions on the songs. Urge the users to reach out with opinions.'
        content="Songs:" +", ".join(content)
    elif choice==0:
        prompt='You are opening the radio show in the morning. Start with a greeting. Your task is to summarize weather report and tell how the weather will be. Give your opinion on it. Urge the users to reach out with opinions.'
        content="Current weather is :" +content[0]+" forecasted weather is :"+content[1]

    response = ollama.chat(model='hostllama', messages=[{'role': 'system', 'content': 'You are a radio host. Your job is to interactively speak to the audience.'},{'role': 'assistant', 'content':prompt} ,{'role': 'user', 'content': content}])
    k=response['message']['content']
    #audio=client.generate(text=k, voice="Paul")
    #elevenlabs.save(audio, "output.mp3")
    print(response['message']['content'])

#talk(2," [('Bad Romance', 'Lady Gaga'), ('stressed out', 'Twenty-one Pilots'), ('Happier', 'Marshmello')]")


    
