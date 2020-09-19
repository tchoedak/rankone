# Change Log

Please log all key deployments here. They include all major changes and customizations to the project.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
