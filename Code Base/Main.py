
from news import news #charitha, yet to do.
from playsound import playsound
from music import music # not needed (playing songs functions) 
from recommender import recommend_songs # done (string formatting concatination)
from talk import talk # done (yippeee)
from programme import programme # done (format)
from weather import weather #done
from data import load_songs_data #done
songs_df = load_songs_data("music_data.csv")  #done (maybe a new dataset)
import json

today_programme = programme() #done
print(today_programme)

from data import load_songs_data
news_snippet,sentiment=news(today_programme.count("News")) #done 

weather_today=weather()
tw=json.loads(weather_today[0])
temp=tw[0].get('temperature_2m')
prec=tw[0].get('precipitation')
cloud=tw[0].get('cloud_cover')
recommendations = recommend_songs(songs_df, sentiment, temp, prec, cloud, today_programme.count("song")*3) #done
m_pointer=0
n_pointer=0
def showrunner(programme):
    global m_pointer
    global n_pointer
    for i in range(len(programme)):
        if programme[i]=="News":
            playsound("./nt.mp3")
            print(news_snippet[n_pointer:n_pointer+2])
            n_pointer=n_pointer+2
        elif programme[i]=="song":
            playsound("./mt.mp3")
            print(recommendations[m_pointer:m_pointer+5])
            m_pointer+=5
        elif programme[i]=="Talk":
            playsound("./rt.mp3")
            if i==0:
                talk(0,weather_today)
            elif programme[i-1]=="News":
                talk(1,news_snippet[n_pointer-2:n_pointer])
            elif programme[i-1]=="song":
                talk(2,recommendations[m_pointer-5:m_pointer]) 
showrunner(today_programme)

