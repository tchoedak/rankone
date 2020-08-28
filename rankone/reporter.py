import random


def get_report(players):
	report = ', '.join(
		[f'{player.name}: {random.randint(900, 1700)}' for player in players]
	)
	return report