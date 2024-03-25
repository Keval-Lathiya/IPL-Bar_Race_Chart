import requests
from bs4 import BeautifulSoup
import os

headers = {
    'User-Agent': 'Chrome/58.0.3029.110'
}

# List of IPL teams
teams = [
    'Gujarat Titans', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Punjab Kings', 'Mumbai Indians',
    'Lucknow Super Giants', 'Sunrisers Hyderabad', 'Delhi Capitals', 'Kolkata Knight Riders', 'Chennai Super Kings',
    'Rising Pune Supergiant', 'Gujarat Lions', 'Pune Warriors', 'Deccan Chargers',
    'Kochi Tuskers Kerala'
]

# Base URL for Wikipedia pages
base_url = "https://en.wikipedia.org/wiki/"

# Directory to save the logos
logos_dir = "Logo"
os.makedirs(logos_dir, exist_ok=True)

for team in teams:
    # Replace spaces with underscores for the URL
    team_url = base_url + team.replace(" ", "_")
    
    # Fetch the team's Wikipedia page with a user-agent
    response = requests.get(team_url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        logo_image_meta = soup.find("meta", property="og:image")
        
        if logo_image_meta:
            logo_url = logo_image_meta["content"]
            print(f"Downloading {team} logo from: {logo_url}")
            
            logo_response = requests.get(logo_url, headers=headers)
            if logo_response.status_code == 200:
                # Adding the path where the logo will be saved
                logo_path = os.path.join(logos_dir, f"{team}.png")
                
                with open(logo_path, 'wb') as f:
                    f.write(logo_response.content)
                print(f"Saved {team} logo to {logo_path}")
            else:
                print(f"Failed to download logo for {team}. Status code: {logo_response.status_code}")
        else:
            print(f"Logo URL not found for {team}.")
    else:
        print(f"Failed to fetch page for {team}. Status code: {response.status_code}")
