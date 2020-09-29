import pandas as pd
from constants import receiving_cols
from top_players_utils import chart, add_columns



def passing_def(df):
	season_df = df.query("play_type == 'pass'").groupby(['defteam']).sum(numeric_only=True)
	season_df = season_df[receiving_cols]
	# season_df = season_df[season_df.pass_attempt > season_df.pass_attempt.quantile(0.55)]
	print(season_df[receiving_cols].describe().to_string())

	# print(season_df.head().to_string())
	print(season_df.sort_values(by=['pass_attempt'], ascending=False).head(10).to_string())
	print(season_df.sort_values(by=['ff_pts'], ascending=False).head(10).to_string())

	season_df["ff_pts/first_down_pass"] = season_df.apply(lambda r: r.ff_pts/r.first_down_pass if r.first_down_pass > 0 and r.ff_pts > 0 else 0, axis=1)
	season_df["ff_pts/pass_attempt"] = season_df.apply(lambda r: r.ff_pts/r.pass_attempt if r.pass_attempt > 0 and r.ff_pts > 0 else 0, axis=1)
	season_df["completion_pct"] = season_df.apply(lambda r: round((r.complete_pass/r.pass_attempt)*100, 2) if r.complete_pass > 0 and r.pass_attempt > 0 else 0, axis=1)
	season_df["conversion_pct"] = season_df.apply(lambda r: round((r.conversions/r.conversion_attempts)*100, 2) if r.conversions > 0 and r.conversion_attempts > 0 else 0, axis=1)
	# print(season_df.sort_values(by=['ff_pts/first_down_pass'], ascending=False).head().to_string())
	# print(season_df.sort_values(by=['ff_pts/pass_attempt'], ascending=False).head(10).to_string())
	chart(season_df.reset_index(), "pass_attempt", "ff_pts", label_name="defteam")
	chart(season_df.reset_index(), "complete_pass", "ff_pts", label_name="defteam")
	chart(season_df.reset_index(), "completion_pct", "ff_pts", label_name="defteam")
	chart(season_df.reset_index(), "conversion_pct", "ff_pts", label_name="defteam")
	chart(season_df.reset_index(), "yards_gained", "ff_pts", label_name="defteam")
	chart(season_df.reset_index(), "qb_hit", "ff_pts", label_name="defteam")
	chart(season_df.reset_index(), "sack", "ff_pts", label_name="defteam")
	chart(season_df.reset_index(), "conversion_attempts", "ff_pts", label_name="defteam")
	chart(season_df.reset_index(), "yards_gained", "touchdown", label_name="defteam")


if __name__ == '__main__':
	df = pd.read_csv('E:/nfl_data/nflfastR-data/data/play_by_play_2020.csv.gz', low_memory=False)
	df: pd.DataFrame = add_columns(df)

	print(df.head().to_string())
	passing_def(df)
