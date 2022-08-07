from turtle import position
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


def get_position(player_id):
    # Scrape html from url
    url = f"https://www.nba.com/player/{player_id}"
    soup = BeautifulSoup(requests.get(url).content, 'html5lib')

    # Extract and return position from data
    try:
        player_data = soup.find_all("p", {"class": "t11 md:t2"})
        player_text = player_data[0].contents[0].split('|')
        position = player_text[2].strip(" ")
        return(position)
    except:
        return('NA')


def get_height_position(player_id):
    # Scrape html from url
    url = f"https://www.nba.com/player/{player_id}"
    soup = BeautifulSoup(requests.get(url).content, 'html5lib')

    # Get height from data
    try:
        height_data = soup.find_all("p", {"class": "PlayerSummary_playerInfoValue__mSfou"})
        height_text = height_data[0].contents[0].split(' ')[0].split("\'")
        height = (int(height_text[0])*12) + int(height_text[1].replace("\"", ""))
    except:
        height = 'NA'

    # Get position from data
    try:
        position_data = soup.find_all("p", {"class": "t11 md:t2"})
        position_text = position_data[0].contents[0].split('|')
        position = position_text[2].strip(" ")
    except:
        position = 'NA'

    return (height, position)


if __name__ == "__main__":

    shot_data = pd.read_csv('shot_data.csv')

    shooter_list = shot_data.player_id.unique().tolist()
    defender_list = shot_data.closest_defender_id.unique().tolist()
    player_df = pd.DataFrame(set(shooter_list + defender_list)).rename(columns={0: 'player_id'})

    player_df['height'] = player_df.apply(lambda row: get_height_position(row['player_id'])[0], axis=1)
    player_df['position'] = player_df.apply(lambda row: get_height_position(row['player_id'])[1], axis=1)

    player_df.to_csv('player_info.csv')

    # shot_data['closest_def_height'] = shot_data.apply(lambda row: get_height(row['closest_defender_id']), axis=1)
    # shot_data['closest_def_wingspan'] = shot_data.apply(lambda row: get_wingspan(row['closest_defender_id']), axis=1)
    
    # shot_data.to_csv('shot_data2.csv')