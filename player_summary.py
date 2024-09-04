from bs4 import BeautifulSoup
import requests
import pandas as pd
import fotmob_scrapping as fs

def get_players_summary_helper(player_soup, players_summary_map, name):
    stats = player_soup.find_all('div', class_ = 'css-1kkujsn-StatBox e1ahduwc6')
    for stat in stats:
        stat_key = stat.find('span', class_ = 'css-1m9s03m-StatTitle e1ahduwc4').text
        stat_value = stat.find('div', class_ = 'css-170fd60-StatValue e1ahduwc5')
        if stat_value != None:
            stat_value.find('span').text
            players_summary_map[name][stat_key] = stat_value.find('span').text

def get_players_summary(player_links):
    players_summary_map = {}
    for link in player_links:
        html_text = requests.get(link).text
        player_soup = BeautifulSoup(html_text, 'lxml')
        name = fs.get_player_name(player_soup)
        players_summary_map[name] = {}
        # Get all stats for each player
        get_players_summary_helper(player_soup, players_summary_map, name)
        
    return players_summary_map

html_text = requests.get('https://www.fotmob.com/teams/5800/squad/venezuela/').text
soup = BeautifulSoup(html_text, 'lxml')
player_boxes = soup.find_all('div', class_ = 'css-10a1gry-SquadTilesWrapper e1kl3u1z2')
player_links = fs.get_player_links(player_boxes)
players_summary_map = get_players_summary(player_links)


print(players_summary_map)