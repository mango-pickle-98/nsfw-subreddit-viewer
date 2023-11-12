import pandas as pd
import requests
import json
import streamlit as st

data = pd.read_csv("/home/phani/Desktop/New Folder/nsfw_sr.csv")['sr'].unique()

# Create two columns
col1, col2 = st.columns(2)

# Display DataFrame in the first column
col1.dataframe(data)

# Display input box in the second column
sub_reddit_name = col2.text_input("Enter subreddit name:")
col2.text("Example: dankmememes for r/dankmemes")
refresh = col2.button("🔄")
fav = col2.button("❤️")

if sub_reddit_name == "":
    pass
if refresh or sub_reddit_name != "":
    try:
        response = requests.get(f'https://meme-api.com/gimme/{sub_reddit_name}/50')

        if response.status_code == 200:
            content = response.content.decode('utf-8')
            data = json.loads(content)
            urls = []
            for post in data['memes']:
                urls.append(post['url'])
            # Create a new set of columns for each image
            for i in range(0, len(urls), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(urls):
                        cols[j].image(urls[i + j])
        else:
            st.warning("Failed to retrieve data. Check if the subreddit exists.")
    except:
        with open("nvm.txt", "a") as f:
            f.write(str(data))
        st.warning("Enter a valid subreddit name!")

if fav:
    if sub_reddit_name == "":
        col2.warning("Enter a subreddit name!")

    else:
        col2.text(f"r/{sub_reddit_name} - Added to favourites.")