# `save-supra`
A hodgepodge Python command-line application that uses the [YouTube Data API](https://developers.google.com/youtube/v3/docs)
to archive (primarily) comment data from SupraDarky's soon-to-be-terminated
"Best Video Game Music" YouTube channel.

In its current incarnation, the primary logic is focused around simply working
through all of the videos in the BVGM playlist. As it is using the official API,
this is limited by a daily quota of requests. However, the benefit is that the
data is fairly comprehensive.

**NOTE:** I am prioritizing the "Best VGM" playlist first. If, after getting
through all of those, I still have some spare quota, I will do a sweep through
the other playlists on the channel for videos that are unique to those playlists.

## The Data
```
db/  <- Archived data (JSON)
  commentThreads/      <- Comprehensive comment threads for every video.
  playlist_items/      <- Data tying playlists and videos together.
  playlists/           <- Information on the all the channels' playlists.
  videos/              <- Information on all the videos.
  bvgm_video_ids.json  <- All video IDs conveniently ordered from BVGM.
  channel.json         <- Basic channel information.

exports/  <- Dumping ground for nicely formatted stuff.
```
