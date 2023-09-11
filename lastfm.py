import os
import requests
import pandas as pd

def send_request(url: str) -> pd.DataFrame:
    response = requests.get(top_albums_req)
    data = response.json()
    albums = data.get("topalbums", {}).get("album", [])
    df = pd.DataFrame(albums)

    # Flatten nested dictionaries
    df["artist_name"] = df["artist"].apply(lambda x: x["name"])

    # Drop columns
    df = df.drop(["artist", "image", "url", "mbid", "@attr"], axis=1)

    return df


def select_time_period():
    valid_periods = ["overall", "7day", "1month", "3month", "6month", "12month"]

    while True:
        print("Choose a time period:")
        for i, period in enumerate(valid_periods, start=1):
            print(f"{i}. {period}")

        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(valid_periods):
                return valid_periods[choice - 1]
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def select_depth():
    scale_options = ["shallow", "moderate", "deep"]
    scale_values = [10, 50, 150]

    while True:
        print("Choose the depth of recommendations:")
        for i, scale in enumerate(scale_options, start=1):
            print(f"{i}. {scale}")

        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(scale_options):
                selected_scale = scale_options[choice - 1]
                selected_value = scale_values[choice - 1]
                return selected_scale, selected_value
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")



period = select_time_period()
depth = select_depth()
api_key = os.environ.get("lastfm_api_key")
username = "danimann02"

base_url = "http://ws.audioscrobbler.com"
top_albums_req = base_url + "/2.0/?method=user.gettopalbums&user=" + username + "&period=" + period + "&limit=500&api_key=" + api_key + "&format=json"

top_albums = send_request(top_albums_req)


print(top_albums)

