import pandas as pd
import re

player_stats = pd.read_csv(r"NBA players stats.csv")
player_salaries = pd.read_csv(r"NBA salaries 1985-2018.csv")

df1 = pd.DataFrame(player_stats)
df2 = pd.DataFrame(player_salaries)

merged_df = pd.merge(df1, df2, on="player_id")

def extract_weight(weight):
    try:
        cleaned_weight = weight.replace("lb", "").strip()
        return float(cleaned_weight)
    except ValueError:
        return None
    
def convert_height(height):
    try:
        feet, inches = map(int, height.split('-'))
        return feet * 12 + inches
    except ValueError:
        return None
    
def convert_shoots(shoots):
    return 1 if shoots.lower() == 'left' else 2

def convert_draft(draft_pick, draft_round):
    combined_draft = draft_round.astype(str) + draft_pick.astype(str)

    draft_num = combined_draft.apply(
        lambda x: int(re.findall(r'\d+', x)[0])* 100 + int(re.findall(r'\d+', x)[1]) 
        if re.findall(r'\d+', x) else 400
    )
    return draft_num

merged_df['weight'] = merged_df['weight'].apply(extract_weight)
merged_df['height'] = merged_df['height'].apply(convert_height)
merged_df['shoots'] = merged_df['shoots'].apply(convert_shoots)
merged_df['combined_draft'] = convert_draft(merged_df['draft_pick'], merged_df['draft_round'])

master_data = (
    merged_df.groupby("player_id")
    .agg(
        {
            "name": "first",
            "salary": "mean",
            "player_id": "first",
            "birthPlace": "first",
            "career_AST": "first",
            "career_FG%": "first",
            "career_FG3%": "first",
            "career_FT%": "first",
            "career_G": "first",
            "career_PER": "first",
            "career_PTS": "first",
            "shoots": "first",
            "weight": "first",
            "season_start": "first",
            "season_end": "last",
            "team": "first",
            "career_TRB": "first",
            "career_WS": "first",
            "career_eFG%": "first",
            "college": "first",
            "combined_draft":"first",
            "draft_team": "first",
            "draft_year": "first",
            "height": "first",
            "highSchool": "first",
            "position": "first",
        }
    )
)

master_data.to_csv('master_data.csv', index=False)
