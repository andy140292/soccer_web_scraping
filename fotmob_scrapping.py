from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_player_links(player_boxes):
    player_links = []
    for player_box in player_boxes:
        for link in player_box.find_all('a'):
            player_links.append('https://www.fotmob.com' + link.get('href'))
    return player_links

def get_minutes_playes(player_soup, players_stats_map, player_name):
    players_stats_map[player_name] = {}
    minutes_played_parent = player_soup.find('div', class_ = 'css-1lp5pdv-SeasonPerformanceSubtitle e1uibvo111')
    if minutes_played_parent is not None:
        minutes_played = minutes_played_parent.find_all('span')
        players_stats_map[player_name]['Minutes played'] = minutes_played[1].text
        
def get_players_stats_helper(player_soup, players_stats_map, name):
    stats = player_soup.find_all('div', class_ = 'css-1v73fp6-StatItemCSS e1uibvo10')
    for stat in stats:
        stat_key = stat.find('div', class_ = 'css-2duihq-StatTitle e1uibvo11').text
        stat_value = stat.find('div', class_ = 'css-jb6lgd-StatValue e1uibvo12').find('span').text
        players_stats_map[name][stat_key] = stat_value
        
def get_player_name(player_soup):
    name = player_soup.find('h1', class_ = 'css-zt63wq-PlayerNameCSS e3s3byw1')  
    if name is not None:
        return name.text
    return ""
    
def get_players_stats(player_links):
    players_stats_map = {}
    for link in player_links:
        html_text = requests.get(link).text
        player_soup = BeautifulSoup(html_text, 'lxml')
        name = get_player_name(player_soup)
        
        # Add minutes played to the players stats map
        get_minutes_playes(player_soup, players_stats_map, name)
        
        # Get all stats for each player
        get_players_stats_helper(player_soup, players_stats_map, name)
        
    return players_stats_map

html_text = requests.get('https://www.fotmob.com/teams/5800/squad/venezuela/').text
soup = BeautifulSoup(html_text, 'lxml')
player_boxes = soup.find_all('div', class_ = 'css-10a1gry-SquadTilesWrapper e1kl3u1z2')
player_links = get_player_links(player_boxes)
# print(player_links)
players_stats_map = get_players_stats(player_links)

# df = pd.DataFrame(players_stats_map)
# print(df['Yangel Herrera'])
# print(players_stats_map)