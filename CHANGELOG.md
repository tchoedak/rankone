# Change Log

Please log all key deployments here. They include all major changes and customizations to the project.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [1.1.6] - 2020-09-30
### Added
- Added a `.version` command to report what version of the bot is live on discord.

### [1.1.5] - 2020-09-30
### Added
- Added match win probability report to the match added message.
- Added more possible losers to the command `.elo_loser`

### [1.1.4] - 2020-09-22
### Added
- Added a new command `.elo_losers` to report players with the lowest elos.

### [1.1.3] - 2020-09-22
### Added
- Added a new command `.elo_loser` to report lowest elo player.

### [1.1.2] - 2020-09-22
### Added
- Added a MatchManager to handle match added and match updated events.
- Added type hints to the codebase and simplified heavy functions into simple ones.

### [1.1.1] - 2020-09-21
### Changed
- The bot new reacts to any recognized match message with an emoji :crossed_swords: to help players identify them visually.

### [1.1.0] - 2020-09-20
### Added
- Added new algorithm for calculating elo ratings using [TrueSkill](http://trueskill.org)

### Changed
- Updated bot to start using trueskill algorithm to adjust player elo ratings.

### [1.0.2] - 2020-09-19
### Changed
- Updated all reports to display `display_name`s instead of discord member name.
- Updated `.myelo` to create a player record with default elo if player does not exist.

### [1.0.1] - 2020-09-18
### Changed
- Updated matches to only be recorded and monitored for game modes that are configured in `config.MONITORED_GAME_MODES`.
- Updated `.myelo` command to report a more helpful message when a player doesn't exist in the database.

### [1.0.0] - 2020-09-18
### Added
- Initial release of rankone bot for RU discord community.
