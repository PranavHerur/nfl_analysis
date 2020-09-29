import pandas as pd
import matplotlib.pyplot as plt


def fg_scoring(row):
	if row.field_goal_attempt == 1:
		if fg_result_check(row) == 0:
			return -1

		if row.kick_distance >= 50:
			return 5
		elif row.kick_distance >= 40:
			return 4
		elif row.kick_distance >= 0:
			return 3

	return 0


def xp_result_check(row):
	return 1.0 if "good" == row.extra_point_result else 0


def fg_result_check(row):
	return 1.0 if "made" == row.field_goal_result else 0


def xp_scoring(row):
	if row.extra_point_attempt == 1:
		return -1 + (2 * xp_result_check(row))
	return 0


def kicker_scoring(row):
	return fg_scoring(row) + xp_scoring(row)


def scatter(season_df, x, y):
	plt.scatter(data=season_df, x=x, y=y, zorder=3)
	for label, a, b in zip(season_df.index, season_df[x], season_df[y]):
		plt.annotate(str(label), xy=(a, b), picker=5, fontsize=8, zorder=4)
	plt.show()
	plt.close()


def add_columns(df):
	df['ff_pts'] = df.apply(lambda row: kicker_scoring(row), axis=1)
	df['fg_pts'] = df.apply(lambda row: fg_scoring(row), axis=1)
	df['xp_pts'] = df.apply(lambda row: xp_scoring(row), axis=1)
	df['kick_attempt'] = df.apply(lambda row: row.extra_point_attempt + row.field_goal_attempt, axis=1)
	df["extra_point_result"] = df.apply(lambda r: xp_result_check(r), axis=1)
	df["field_goal_result"] = df.apply(lambda r: fg_result_check(r), axis=1)
	df['kick_result'] = df.apply(lambda row: row.extra_point_result + row.field_goal_result, axis=1)
	return df


def main():
	df = pd.read_csv('E:/nfl_data/nflfastR-data/data/play_by_play_2020.csv.gz', low_memory=False)
	df = df[(df.field_goal_attempt == 1) | (df.extra_point_attempt == 1)]
	df = add_columns(df)

	season_df = df.groupby(['kicker_player_name', 'posteam']).sum(numeric_only=True)
	cols = [
		"ff_pts", "kick_result", "kick_attempt",
		"fg_pts", "field_goal_result", "field_goal_attempt",
		'xp_pts', "extra_point_result", "extra_point_attempt"]
	season_df = season_df[cols]
	season_df["fg_ratio"] = season_df.apply(lambda r: round(r.field_goal_attempt / r.kick_attempt, 2), axis=1)
	season_df["fg_acc"] = season_df.apply(lambda r: round(r.field_goal_result / r.field_goal_attempt, 2), axis=1)
	season_df["xp_acc"] = season_df.apply(lambda r: round(r.extra_point_result / r.extra_point_attempt, 2), axis=1)
	print(season_df.sort_values(by="ff_pts", ascending=False).head(12).to_string())

	scatter(season_df, "kick_attempt", "ff_pts")
	scatter(season_df, "field_goal_attempt", "fg_pts")


if __name__ == '__main__':
	main()
