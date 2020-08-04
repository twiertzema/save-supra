# `save-supra`
## Overview
A hodgepodge Python command-line application that used the [YouTube Data API](https://developers.google.com/youtube/v3/docs)
to archive video information and  comment data from SupraDarky's old "Best Video
Game Music" YouTube channel.

The primary logic was focused around simply working through all of the videos in
the BVGM playlist. Since it used the official API, this was limited by a daily
quota of requests. However, the benefit was that the data was fairly comprehensive.

Unfortunately, this does not include the video and comment information for videos
that had to be marked as private (or the ones that were de-listed). As such,
there are some small holes in the BVGM sequence.

### Prioritized BVGM
The data for the BVGM playlist is complete, but there is no comment
data for the videos in the other playlists from the channel; I ran out of quota
before I was able to get those.

### Timeframe of Data
Since the data was collected over the course of a few days, comments that were
made very close to the channel's termination (especially on the earlier videos)
are not included.

The following table should help illustrate when the data was collected to give
you an idea of how current the respective comment data.

| BVGM Range  | Date Collected |
|:-----------:|:--------------:|
| 1 - ~450    | 2020-07-19     |
| ~450 - 1497 | 2020-07-20     |
| 1497 - end  | 2020-07-21     |

## The Data
```
db/  <- Archived data (JSON)
  commentThreads/      <- Comprehensive comment threads for every BVGM video.
  playlist_items/      <- Data tying playlists and videos together.
  playlists/           <- Information on the all the channels' playlists.
  videos/              <- Information on all the BVGM videos (and a few more).
  bvgm_video_ids.json  <- All video IDs conveniently ordered from BVGM.
  channel.json         <- Basic channel information.

exports/  <- Dumping ground for nicely formatted stuff. Not much of use now.
```
