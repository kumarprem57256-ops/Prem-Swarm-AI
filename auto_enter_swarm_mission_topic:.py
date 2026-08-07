import os
import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd

def get_swarm_mission_topics():
    url = "https://en.wikipedia.org/wiki/List_of_spacecraft_by_orbit"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    topics = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/wiki/') and 'spacecraft' in href:
            topic = href.split('/')[-1]
            topics.append(topic)
    return topics

def get_swarm_mission_info(topic):
    url = f"https://en.wikipedia.org/wiki/{topic}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    info = {}
    for paragraph in soup.find_all('p'):
        text = paragraph.get_text()
        if 'Enter' in text and 'Swarm' in text:
            info['description'] = text
            break
    return info

def save_swarm_mission_info(topics):
    for topic in topics:
        info = get_swarm_mission_info(topic)
        if info:
            with open(f"{topic}.txt", 'w') as f:
                f.write(info['description'])

def main():
    topics = get_swarm_mission_topics()
    save_swarm_mission_info(topics)

if __name__ == "__main__":
    main()