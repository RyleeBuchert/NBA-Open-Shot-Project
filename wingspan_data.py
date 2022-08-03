import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_wingspan(player_id):
    # Scrape html from url
    url = f"http://nbasavant.com/player.php?player_id={player_id}"
    soup = BeautifulSoup(requests.get(url).content, 'html5lib')
    
    # Extract and return wingspan from data
    try:
        player_data = soup.find_all("div", {"id": "boxes"})
        player_text = player_data[0].find("br").next
        wingspan = float(player_text.split('Wingspan: ', 1)[1][:5])
        return(wingspan)
    except:
        return('NA')

def add_wingspan(row):
    return get_wingspan(row['CLOSEST_DEFENDER_PLAYER_ID'])

shot_data = pd.read_csv('shot_data.csv')
# shot_data['def_wingspan'] = get_wingspan(shot_data['CLOSEST_DEFENDER_PLAYER_ID'])
# print(get_wingspan(shot_data.loc[0]['CLOSEST_DEFENDER_PLAYER_ID']))

shot_data['closest_def_wingspan'] = shot_data.apply(lambda row: get_wingspan(row['closest_defender_id']), axis=1)
shot_data.to_csv('shot_data2.csv')