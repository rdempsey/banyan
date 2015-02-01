# Feature: Tweet Alerts

## Goals

  * Receive verbal and visual alerts when someone mentions me in a tweet
  * Receive verbal and visual alerts when FCPS (fcpsnews) delays or cancels school
  * Receive verbal and visual alerts when Metro Rail (metrorailinfo) announces delays on the Orange Line
  * Receive verbal and visual alerts when Metro Bus (Metrobusinfo) announces delays on my bus route (23A/23T)

## Acceptance Criteria

  * All Alerts
    * Only alert me to new tweets during hours that I'm awake
    * If a new tweet comes in while I'm asleep, wait until I'm awake to tell/show me
    * Show the associated tweet in a Chrome tab
  * Mentions
    * Do not alert me when a tweet of mine has been retweeted; only show direct mentions
  * FCPS
    * Ignore all tweets that do not apply to schools being delayed or closed
  * Metro Rail & Metro Bus
    * Ignore all tweets that do not apply to my metro or bus line