import googleapiclient.discovery
import pandas as pd

# YouTube API key
API_KEY = "YOUR_API_KEY"

def get_youtube_service():
    return googleapiclient.discovery.build("youtube", "v3", developerKey=API_KEY)

def get_channel_details(channel_id):
    youtube = get_youtube_service()
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()

    data = response["items"][0]
    details = {
        "Channel Name": data["snippet"]["title"],
        "Subscribers": data["statistics"].get("subscriberCount"),
        "Total Views": data["statistics"].get("viewCount"),
        "Total Videos": data["statistics"].get("videoCount")
    }
    return details

def get_channel_videos(channel_id):
    youtube = get_youtube_service()
    videos = []
    
    request = youtube.search().list(
        part="snippet",
        channelId=channel_id,
        maxResults=20,
        type="video"
    )
    response = request.execute()

    for item in response["items"]:
        videos.append({
            "Video Title": item["snippet"]["title"],
            "Video ID": item["id"]["videoId"]
        })
    
    return pd.DataFrame(videos)


# Example Usage
if __name__ == "__main__":
    channel_id = "UCYO_jab_esuFRV4b17AJtAw"   # Example channel
    print("Channel Details:")
    print(get_channel_details(channel_id))
    
    print("\nVideo List:")
    print(get_channel_videos(channel_id))
