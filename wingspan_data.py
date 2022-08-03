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


def get_height(player_id):
    # Scrape html from url
    url = f"https://www.nba.com/player/{player_id}"
    soup = BeautifulSoup(requests.get(url).content, 'html5lib')

    # Extract and return height from data
    try:
        player_data = soup.find_all("p", {"class": "PlayerSummary_playerInfoValue__mSfou"})
        player_text = player_data[0].contents[0].split(' ')[0].split("\'")
        height = (int(player_text[0])*12) + int(player_text[1].replace("\"", ""))
        return(height)
    except:
        return('NA')


if __name__ == "__main__":

    shot_data = pd.read_csv('shot_data.csv')

    shot_data['closest_def_height'] = shot_data.apply(lambda row: get_height(row['closest_defender_id']), axis=1)
    shot_data['closest_def_wingspan'] = shot_data.apply(lambda row: get_wingspan(row['closest_defender_id']), axis=1)
    
    shot_data.to_csv('shot_data2.csv')