# Status Codes used in the bot

## Match Status Codes
These codes are stored in the database, to distinguish active from inactive matches and store winners

### 1x Series: Active Matches
- 10: Challenge has been issued, but not accepted
- 11: Current turn is the challenger's
- 12: Current turn is the challenged's

### 2x Series: Finished Matches
- 20: Challenge declined
- 21: Challenger win
- 22: Challenged win
- 23: Draw for reasons other than timeout
- 24: Match ended by timeout

## Mancala Move Status Codes
These codes are used internally by the mancala logic to determine the outcome of specific moves

### 1x series: Success

### 2x series: Error