from flask import Flask, render_template, request
import requests
from collections import Counter

app = Flask(__name__)

def get_github_data(username):
    headers = {}  # Add GitHub token if available
    base_url = f'https://api.github.com/users/{username}'
    
    # Get basic profile info
    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        return None
        
    user_data = response.json()
    
    # Get repositories
    repos_response = requests.get(f'{base_url}/repos', headers=headers)
    repos = repos_response.json() if repos_response.status_code == 200 else []
    
    # Calculate language stats
    languages_counter = Counter()
    for repo in repos:
        if repo['language']:
            languages_counter[repo['language']] += 1
            
    total_langs = sum(languages_counter.values())
    languages = [
        {
            'name': lang,
            'percentage': round((count / total_langs) * 100, 1),
            'color': get_language_color(lang)
        }
        for lang, count in languages_counter.most_common(5)
    ]
    
    # Get contribution count (simplified)
    contributions = len(repos)  # In real app, you'd want to get actual contribution count
    
    # Calculate total stars
    stars = sum(repo['stargazers_count'] for repo in repos)
    
    return {
        'name': user_data['name'] or user_data['login'],
        'login': user_data['login'],
        'avatar_url': user_data['avatar_url'],
        'followers': user_data['followers'],
        'public_repos': user_data['public_repos'],
        'contributions': contributions,
        'stars': stars,
        'languages': languages
    }

def get_language_color(language):
    # Simplified color mapping - in real app, you'd want a complete mapping
    colors = {
        'Python': '#3572A5',
        'JavaScript': '#f1e05a',
        'Java': '#b07219',
        'TypeScript': '#2b7489',
        'Ruby': '#701516'
    }
    return colors.get(language, '#6e7681')

@app.route('/', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        username1 = request.form.get('username1')
        username2 = request.form.get('username2')
        
        profile1 = get_github_data(username1)
        profile2 = get_github_data(username2)
        
        if not profile1 and not profile2:
            return render_template('index1.html', error="Both users not found!")
        elif not profile1:
            return render_template('index1.html', error=f"User '{username1}' not found!")
        elif not profile2:
            return render_template('index1.html', error=f"User '{username2}' not found!")
            
        # Determine winner based on total metrics
        score1 = (profile1['followers'] + profile1['stars'] + 
                 profile1['contributions'] + profile1['public_repos'])
        score2 = (profile2['followers'] + profile2['stars'] + 
                 profile2['contributions'] + profile2['public_repos'])
        
        profile1['winner'] = score1 >= score2
        profile2['winner'] = score2 > score1
        
        return render_template('index1.html', profiles=[profile1, profile2])
        
    return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)
