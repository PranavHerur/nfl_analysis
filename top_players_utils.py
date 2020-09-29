import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from numpy.polynomial.polynomial import polyfit
import bayesian_bootstrap.bootstrap as bb


def chart(df: pd.DataFrame, X, Y, label_name="Player", filter=True, include_quadrants=False):
	# Fit with polyfit
	if filter and len(df) > 32:
		df = df.sort_values(by=Y, ascending=False)[:50]
		# df = df[df[X] > df[X].mean() - df[X].std()/2][df[Y] > df[Y].mean() - df[Y].std()/2]

	b, m = polyfit(df[X], df[Y], 1)

	def dist(x):
		sns.distplot(x)
		plt.show()
		plt.close()
	# dist(df[X])

	def bootstrap():
		print(X, round(df[X].mean(), 2))
		player_bootstrap = bb.mean(df[X], n_replications=10000)
		ci_low, ci_hi = bb.highest_density_interval(player_bootstrap)
		print('low ci:', round(ci_low, 2), 'high ci:', round(ci_hi, 2))
		sns.distplot(player_bootstrap)
		plt.show()
		plt.close()

	plt.figure(figsize=(15, 9))
	# plt.figure()
	plt.scatter(df[X], df[Y], zorder=3)
	plt.title('{0}-{1}'.format(X, Y))
	plt.ylabel(Y)
	plt.xlabel(X)

	# label_df = df[df.Tm == 'BAL']
	for label, x, y in zip(df[label_name], df[X], df[Y]):
		plt.annotate(str(label), xy=(x, y), picker=5, fontsize=8, zorder=4)

	print('y = {0:.2f}x+{1:.3f}'.format(m, b))
	# print(msg)

	# https://stackoverflow.com/questions/24988448/how-to-draw-vertical-lines-on-a-given-plot-in-matplotlib
	plt.axvline(x=df[X].median(), color='orange', label="Median")
	plt.axhline(y=df[Y].median(), color='orange')
	plt.axvline(x=df[X].mean(), color='purple')
	plt.axhline(y=df[Y].mean(), color='purple', label='Mean')

	# Filling between line y3 and line y4
	# https://stackoverflow.com/questions/16417496/matplotlib-fill-between-multiple-lines
	# plt.fill(m*df[X]+b, df[X].median())
	x_line = np.arange(df[X].min()-df[X].std(), df[X].max()+df[X].std(), step=0.1)
	func_y = lambda x: m*x + b
	func_yu = lambda x: m*x + b + df[Y].std()/2
	func_yl = lambda x: m*x + b - df[Y].std()/2
	line = np.array(list(func_y(x) for x in x_line))
	upper_line = np.array(list(func_yu(x) for x in x_line))
	lower_line = np.array(list(func_yl(x) for x in x_line))


	# vertical asymptote to create "quadrants"
	asymptote = np.empty(len(x_line))
	# asymptote.fill(df[X].median())
	asymptote.fill(df[X].mean())

	# https://stackoverflow.com/questions/16917919/filling-above-below-matplotlib-line-plot

	# quadrant1
	plt.fill_between(x_line, line, df[Y].max() + df[Y].std(), where=x_line > asymptote, color='#baffbb', zorder=2)

	# q2
	# plt.fill_between(x_line, line, df[Y].min() - df[Y].std(), where=x_line > asymptote, color='darkgrey', zorder=2)
	plt.fill_between(x_line, line, 0, where=x_line > asymptote, color='darkgrey', zorder=2)

	# q3
	# plt.fill_between(x_line, df[Y].min()-df[Y].std(), line, where=x_line <= asymptote, color='#ffbaba', zorder=2)
	plt.fill_between(x_line, 0, line, where=x_line <= asymptote, color='#ffbaba', zorder=2)

	# q4
	plt.fill_between(x_line, line, df[Y].max() + df[Y].std(), where=x_line <= asymptote, color='lightblue', zorder=2)

	sns.regplot(data=df, x=X, y=Y, ci=False, scatter_kws={"s": 50})
	plt.xlim((df[X].min() - df[X].std() / 2, df[X].max() + df[X].std() / 2))
	plt.ylim([0, df[Y].max()+df[Y].std()])

	plt.plot(x_line, upper_line, 'r--', label='margin')
	plt.plot(x_line, lower_line, 'r--')

	if include_quadrants:
		plt.axvline(x=df[X].quantile(q=0.25), color='black')
		plt.axhline(y=df[Y].quantile(q=0.25), color='black', label='25%')
		plt.axvline(x=df[X].quantile(q=0.75), color='white', label='75%')
		plt.axhline(y=df[Y].quantile(q=0.75), color='white')

	plt.legend(loc="best")
	plt.text(df[X].min() - df[X].std() / 2, -df[Y].std()/2, 'source:nflfastR   author:@space_priest', fontsize=10)
	plt.show()

	# plt.savefig(fname='stats/figs/ff/{0}'.format(X, Y), dpi=100)
	# plt.savefig(fname='C:/Users/pherur/Documents/sumnews/client/resources/{0}-{1}'.format(X, Y), dpi=100)
	# plt.show()
	plt.close()


def add_columns(df):
	df['missed_air_yards'] = df.apply(lambda r: 0 if r.incomplete_pass == 0 else r.air_yards, axis=1)
	df['air_yards'] = df.apply(lambda r: 0 if r.complete_pass == 0 else r.air_yards, axis=1)
	df['ff_pts'] = df.apply(
		lambda r: r.complete_pass * 0.5 + r['yards_gained'] * 0.1 + r.pass_touchdown * 6 - r.fumble * 2, axis=1)
	df['third_down_attempts'] = df.apply(lambda r: r.third_down_converted + r.third_down_failed, axis=1)
	df['fourth_down_attempts'] = df.apply(lambda r: r.fourth_down_converted + r.fourth_down_failed, axis=1)
	df['conversion_attempts'] = df.apply(lambda r: r.third_down_attempts + r.fourth_down_attempts, axis=1)
	df['conversions'] = df.apply(lambda r: r.third_down_converted + r.fourth_down_converted, axis=1)
	df['no_tackle'] = df.apply(lambda r: r.rush_attempt - r.solo_tackle - r.assist_tackle, axis=1)
	return df

