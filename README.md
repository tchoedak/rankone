# RankOne Bot
A discord bot that works with your pugbot!

# Integration with Pugbot
As long as pugbot's match messages syntax do not change, this bot will continue to recognize matches and record matches, players, and win/losses. If that syntax does change, an update to rankone.parser is required.

# Configuration
This bot requires `DISCORD_GUILD` and `DISCORD_TOKEN` environment variables to be set.

# How It Works
On channels that the bot is configured to monitor, any matches that start with:
`Teams have been selected:` will be read and any players mentioned within next to `red team` will be considered as red team players. Likewise for `blue team` players. A match is created based on this message.

```
Teams have been selected:
red team: @tenz @MYTHIC
blue team: @monty @°Vapor°
```

Once the match has been completed, a 🔵 reaction emoji placed on the message will allow the bot to register that blue team players won the match and award them elo while taking away elo from red players. Likewise a 🔴 reaction emoji will award red team players elo.


# Commmands

## General commands

### .myelo
Get your current elo

### .elo @discordmember1 @discordmember2 @...
Get elo of `discordmember` and `discordmember2`

### .elo_leaders
Get the elo leaderboard

### .elo_loser
Get the biggest loserr

### .version
Get the current version of the bot running

## Admin commands

### .reset_elo
Reset elo to the default elo for all registered players

### .reset_db
Reset the entire database back to the starting point

### .backup_db <id>
Backup the database to a file named `<id>`. If `<id>` is not given, one is generated.

### .restore_db <id>
Restore an existing db from a backup id of `<id>`
