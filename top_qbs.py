import pandas as pd
from constants import receiving_cols
from top_players_utils import chart, add_columns


def passing(df):
	# start passing analysis
	season_df = df.groupby(['passer_player_name', 'posteam']).sum(numeric_only=True)
	season_df = season_df[receiving_cols]
	season_df["pass_attempt"] = season_df.apply(lambda r: r.complete_pass + r.incomplete_pass, axis=1)
	season_df['ff_pts'] = season_df.apply(lambda r: r['yards_gained'] * 0.04 + r.pass_touchdown * 4 - r.interception * 2 - r.fumble * 2, axis=1)
	season_df = season_df.sort_values(by="ff_pts", ascending=False).head(24)
	print(season_df[receiving_cols].describe().to_string())
	# print(season_df.head().to_string())
	print(season_df.sort_values(by=['pass_attempt'], ascending=False).head(10).to_string())
	chart(season_df.reset_index(), "pass_attempt", "ff_pts", label_name="passer_player_name")
	chart(season_df.reset_index(), "pass_attempt", "yards_gained", label_name="passer_player_name")
	chart(season_df.reset_index(), "pass_attempt", "air_yards", label_name="passer_player_name")
	chart(season_df.reset_index(), "pass_attempt", "yards_after_catch", label_name="passer_player_name")
	chart(season_df.reset_index(), "pass_attempt", "ff_pts", label_name="passer_player_name")
	chart(season_df.reset_index(), "complete_pass", "ff_pts", label_name="passer_player_name")
	chart(season_df.reset_index(), "yards_gained", "ff_pts", label_name="passer_player_name")


def rolling_epa(df):
	import matplotlib.pyplot as plt
	plt.style.use('fivethirtyeight')
	plt.figure(figsize=(15, 9))

	qbs = df['passer'].dropna().unique()

	labels = []
	rb_sum = df.loc[(df['passer'].isin(qbs)) & (df['epa'].notnull())]
	for team in qbs:
		temp_df = rb_sum.loc[(rb_sum['passer'] == team)]
		temp_df['rolling_epa'] = temp_df.epa.cumsum()
		temp_df.reset_index(inplace=True)
		plt.plot(temp_df['rolling_epa'], lw=2, label=temp_df['passer'].iloc[0], alpha=0.6)
		labels.append((team, len(temp_df.rolling_epa), temp_df.rolling_epa.iloc[-1]))

	for label, x, y in labels:
		plt.annotate(str(label), xy=(x-1, y-1), picker=5, fontsize=8, zorder=4)

	plt.xlabel('Number of Plays')
	plt.ylabel('Cumulative EPA Added')
	plt.title("Data: nflfastR | Chart: @space_priest", fontsize=8)
	plt.suptitle('QB earned epa through 2020 Week 3\n', fontsize=24)

	plt.savefig("./figs/qb_epa.jpg")
	plt.show()
	plt.close()


if __name__ == '__main__':
	df = pd.read_csv('E:/nfl_data/nflfastR-data/data/play_by_play_2020.csv.gz', low_memory=False)
	df: pd.DataFrame = add_columns(df)

	print(df.head().to_string())
	# passing(df)
	rolling_epa(df)