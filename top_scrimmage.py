import pandas as pd

from constants import scrimmage_cols
from top_players_utils import chart, add_columns
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def scrimmage(df):
	# start rushing analysis
	df['scrimmage_player_name'] = df.apply(lambda r: r.receiver_player_name if r.rusher_player_name is np.nan else r.rusher_player_name, axis=1)
	rush_df = df.groupby(['scrimmage_player_name', 'posteam']).sum(numeric_only=True)
	rush_df['ff_pts'] = rush_df.apply(lambda r: r.complete_pass * 0.5 + r['yards_gained'] * 0.1 + r.rush_touchdown * 6 - r.fumble * 2, axis=1)

	rush_df["touches"] = rush_df.apply(lambda r: r.pass_attempt * 1 + r.rush_attempt + 1, axis=1)
	rush_df = rush_df[scrimmage_cols]
	print(rush_df.describe().to_string())

	def kde():
		sns.kdeplot(rush_df['touches'], label="touches")
		plt.legend(loc="best")
		plt.show()
		plt.close()

		sns.kdeplot(rush_df['ff_pts'], label="ff_pts")
		plt.legend(loc="best")
		plt.show()
		plt.close()

	kde()
	# rush_df = rush_df[rush_df.rush_attempt > rush_df.rush_attempt.quantile(0.75)]

	print(rush_df.sort_values(by=['ff_pts'], ascending=False).head(10).to_string())
	chart(rush_df.reset_index(), "touches", "ff_pts", label_name="scrimmage_player_name")
	chart(rush_df.reset_index(), "rush_attempt", "ff_pts", label_name="scrimmage_player_name")
	chart(rush_df.reset_index(), "rush_attempt", "yards_gained", label_name="scrimmage_player_name")
	chart(rush_df.reset_index(), "yards_gained", "rush_touchdown", label_name="scrimmage_player_name")
	chart(rush_df.reset_index(), "yards_gained", "ff_pts", label_name="scrimmage_player_name")
	chart(rush_df.reset_index(), "assist_tackle", "ff_pts", label_name="scrimmage_player_name")
	chart(rush_df.reset_index(), "solo_tackle", "ff_pts", label_name="scrimmage_player_name")
	chart(rush_df.reset_index(), "no_tackle", "ff_pts", label_name="scrimmage_player_name")


if __name__ == '__main__':
	df = pd.read_csv('E:/nfl_data/nflfastR-data/data/play_by_play_2020.csv.gz', low_memory=False)
	df: pd.DataFrame = add_columns(df)

	print(df.head().to_string())
	scrimmage(df)
