# Data Dictionary

## s
Original speed value from NFL tracking data, measured in yards per second.

## a
Acceleration value from NFL tracking data.

## speed_mph
Speed converted from yards per second to miles per hour using:

speed_mph = s × 2.045

## speed_category
Categorizes speed into:
- Low: 0–5 mph
- Moderate: 5–12 mph
- High: 12–18 mph
- Sprint: 18–25 mph

## accel_category
Categorizes acceleration into:
- Low: 0–1
- Moderate: 1–2.5
- High: 2.5+

## movement_intensity
A created feature calculated as:

movement_intensity = speed_mph × acceleration

This combines how fast a player is moving with how quickly their movement is changing.

## risk_category
A proxy risk category based on movement intensity:
- Normal: Bottom 75%
- Elevated: 75th–90th percentile
- High Risk Proxy: Top 10%
