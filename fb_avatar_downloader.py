import pandas as pd
import requests
# friend_list = pd.read_json("output/friend_list.json")
# img_list = pd.read_json("output/img_list.json")
# df = pd.merge(img_list,friend_list)
# df.to_pickle('output/fb_avatar.pkl')
df = pd.read_pickle('output/fb_avatar.pkl')
df['url_id'] = df['to_url'].apply(lambda v:v.split('https://www.facebook.com/profile.php?id=')[1] if 'php?id=' in v else v.split('https://www.facebook.com/')[1])
print(df)
print(len(df))

for i in range(len(df)):
    # Send the request and retrieve image data
    folder = 'fb_avatar_image/'
    response = requests.get(df['img_src'].iloc[i])
    # Check if the request was successful
    if response.status_code == 200:
        with open(folder + df['url_id'].iloc[i]+".jpg", "wb") as file:
            file.write(response.content)
        print(str(i) + ":The picture has been successfully downloaded locally.")
    else:
        print("Unable to download the picture.")