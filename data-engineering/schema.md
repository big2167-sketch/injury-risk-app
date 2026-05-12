# Data Schema

## Main Table: tracking_sample.csv

| Column | Type | Description |
|---|---|---|
| gameId | Integer | Unique game identifier |
| playId | Integer | Unique play identifier |
| nflId | Float/Integer | Unique player identifier |
| displayName | Text | Player name |
| s | Float | Speed in yards per second |
| a | Float | Acceleration |
| speed_mph | Float | Converted player speed in miles per hour |
| speed_category | Category | Low, moderate, high, or sprint speed |
| accel_category | Category | Low, moderate, or high acceleration |
| movement_intensity | Float | Speed in mph multiplied by acceleration |
| risk_category | Category | Normal, elevated, or high-risk proxy |

## Data Model
This project uses a simplified single-table model for the demo app. Additional datasets such as weather, field surface, and injury reports can be joined later using `gameId`, `playId`, or player identifiers.
