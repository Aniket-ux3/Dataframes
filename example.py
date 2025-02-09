import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the data
df = pd.read_csv(r"C:\Users\anike\OneDrive\Desktop\matches.csv")

# 1. Team Performance Over Seasons
# Create a list of all teams
all_teams = pd.concat([df['team1'], df['team2']]).unique()

# Prepare DataFrame for team performance
performance = []
for season in df['season'].unique():
    season_df = df[df['season'] == season]
    for team in all_teams:
        total_matches = len(season_df[(season_df['team1'] == team) | (season_df['team2'] == team)])
        if total_matches == 0:
            continue
        wins = len(season_df[season_df['winner'] == team])
        win_percent = (wins / total_matches) * 100
        performance.append({
            'Season': season,
            'Team': team,
            'Wins': wins,
            'Total Matches': total_matches,
            'Win Percentage': win_percent
        })

performance_df = pd.DataFrame(performance)

# Visualization for Team Performance
plt.figure(figsize=(12,8))
sns.barplot(x='Season', y='Win Percentage', hue='Team', data=performance_df, ci=None)
plt.title('Team Win Percentage Across Seasons')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

# 2. Player Statistics (Simplified - Player of Match Counts)
player_of_match = df['player_of_match'].value_counts().reset_index()
player_of_match.columns = ['Player', 'Awards']
print("Top 10 Players with Most 'Player of Match' Awards:")
print(player_of_match.head(10))

# 3. Match Outcome Trends
# Home Advantage (assuming city = home venue)
df['home_team'] = df.apply(lambda x: x['team1'] if x['venue'].split(',')[0].strip() in x['team1'] else x['team2'], axis=1)
df['home_win'] = df['winner'] == df['home_team']
home_win_rate = df['home_win'].mean()

# Toss Impact
df['toss_win_game'] = df['toss_winner'] == df['winner']
toss_win_ratio = df['toss_win_game'].mean()

print(f"\nHome Win Rate: {home_win_rate:.2%}")
print(f"Toss Winner Match Win Rate: {toss_win_ratio:.2%}")

# 4. Visualizations
# Histogram of Win Margins
plt.figure(figsize=(10,6))
sns.histplot(df['win_by_runs'], bins=20, kde=True)
plt.title('Distribution of Win Margins by Runs')
plt.show()

# Scatter Plot: Toss Decision vs Win
plt.figure(figsize=(10,6))
sns.scatterplot(x='toss_decision', y='win_by_runs', data=df)
plt.title('Toss Decision vs Win Margin')
plt.show()

# Box Plot of Win Percentages by Team
plt.figure(figsize=(15,8))
sns.boxplot(x='Team', y='Win Percentage', data=performance_df)
plt.xticks(rotation=90)
plt.title('Distribution of Win Percentages by Team')
plt.show()