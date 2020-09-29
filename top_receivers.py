import pandas as pd
from constants import receiving_cols
from top_players_utils import chart, add_columns
import seaborn as sns
import matplotlib.pyplot as plt


def receiving(df):
	season_df = df.groupby(['receiver_player_name', 'posteam']).sum(numeric_only=True)
	season_df = season_df[receiving_cols]
	print(season_df[receiving_cols].describe().to_string())

	# print(season_df.head().to_string())
	print(season_df.sort_values(by=['pass_attempt'], ascending=False).head(10).to_string())
	print(season_df.sort_values(by=['ff_pts'], ascending=False).head(10).to_string())

	season_df["ff_pts/first_down_pass"] = season_df.apply(lambda r: r.ff_pts/r.first_down_pass if r.first_down_pass > 0 and r.ff_pts > 0 else 0, axis=1)
	season_df["ff_pts/pass_attempt"] = season_df.apply(lambda r: r.ff_pts/r.pass_attempt if r.pass_attempt > 0 and r.ff_pts > 0 else 0, axis=1)
	chart(season_df.reset_index(), "pass_attempt", "ff_pts", label_name="receiver_player_name")
	chart(season_df.reset_index(), "complete_pass", "ff_pts", label_name="receiver_player_name")
	chart(season_df.reset_index(), "yards_gained", "ff_pts", label_name="receiver_player_name")
	chart(season_df.reset_index(), "qb_hit", "ff_pts", label_name="receiver_player_name")
	chart(season_df.reset_index(), "conversion_attempts", "ff_pts", label_name="receiver_player_name")
	chart(season_df.reset_index(), "yards_gained", "touchdown", label_name="receiver_player_name")


def create_receiver_charts(df, value='ff_pts'):
	passes = df[df["play_type"] == 'pass']
	names = df.groupby(['receiver_player_name', 'posteam'])\
		.sum(numeric_only=True).sort_values(by=['ff_pts'], ascending=False).head(10).index

	for name in names:
		print(name)
		draw_receiver_charts(passes, *name, value)
		# break


def draw_receiver_charts(passes, player, team, value):
	df = passes[passes.receiver_player_name == player]
	pivot_df = pd.pivot_table(df, index=['pass_length'], columns=['pass_location'], values=value, aggfunc=sum).fillna(0)
	print(pivot_df.head())

	sns.heatmap(pivot_df, linewidth=0.5, xticklabels=True, yticklabels=True, annot=True, fmt='.0f', cmap="coolwarm")
	plt.xlabel("pass location")
	plt.ylabel("total fantasy points (0.5 ppr)")

	plt.title('{0}-{1}'.format(player, team))
	plt.savefig(fname='figs/{0}-{1}.jpg'.format(player, team), dpi=100)
	# plt.show()
	plt.close()


def qb_eff_per_team(df, team="JAX"):
	dchark = df[df.posteam == team]\
		.groupby(['receiver_player_name', 'passer_player_name'])\
		.sum(numeric_only=True)[receiving_cols]\
		.sort_values(by="ff_pts", ascending=False)

	print(dchark.to_string())
	sns.catplot(x="receiver_player_name", y="ff_pts", hue="passer_player_name", data=dchark.reset_index(), height=6, kind="bar", palette="muted")
	plt.show()


if __name__ == '__main__':
	df = pd.read_csv('E:/nfl_data/nflfastR-data/data/play_by_play_2020.csv.gz', compression='gzip', low_memory=False)
	df: pd.DataFrame = add_columns(df)

	print(df.head().to_string())
	# create_receiver_charts(df)

	receiving(df)

	qb_eff_per_team(df, "JAX")
