import streamlit as st
from googleapiclient.discovery import build
from key import youtube_api_key,gemini_api_key
import google.generativeai as genai

#web framework
st.title(":orange[OpenChat]")
user_prompt = st.chat_input("Enter your prompt ")

#Initializing the gemini
import os 
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel("gemini-1.5-flash")
if user_prompt:
    response = model.generate_content(user_prompt)
    assistant_response=response.text

    #Integrating youtube inks using youtube data api
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    video_search_response = youtube.search().list(
    part="snippet",
    q=user_prompt,
    type="video",
    order="relevance"
    ).execute()
    videos_list=[]
    for item in video_search_response['items']:
        video_id = item['id']['videoId']
        videos_list.append(video_id)

    #session_state is used to show the conversation history for that session
    if "history" not in st.session_state:
        st.session_state.history=[]
    st.session_state.history.append([user_prompt,assistant_response,videos_list])
    print(st.session_state.history)
    
    for prompt,response,video in st.session_state.history:
        user_message=st.chat_message("User")
        user_message.write(prompt)
        assistant_message = st.chat_message('Assistant')
        assistant_message.write(response)
        assistant_message.write("Here are few videos from youtube based on your search.")
    
        for url in range(0,5):
            assistant_message.video(f"https://www.youtube.com/watch?v={video[url]}")
                

    

    