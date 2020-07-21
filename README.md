# `save-supra`
A hodgepodge Python command-line application that uses the [YouTube Data API](https://developers.google.com/youtube/v3/docs)
to archive (primarily) comment data from SupraDarky's soon-to-be-terminated
"Best Video Game Music" YouTube channel.

In its current incarnation, the primary logic is focused around simply working
through all of the videos in the BVGM playlist. As it is using the official API,
this is limited by a daily quota of requests. However, the benefit is that the
data is fairly comprehensive.

**NOTE:** The BVGM videos are complete. There is data on some of the videos
unique to the other playlists, but no comments for those yet. If I can get a
little more data quota before the channel is taken down, I'll continue to scoop
up as much as I can.

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
