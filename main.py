# -*- coding: utf-8 -*-

import json
import os
import sys
from time import sleep

from data_access import DataAccess, BVGM_PLAYLIST_IDS
from youtube import YouTube

ROOT_DIR = os.getcwd()


def save_all_playlist_items(youtube, playlist_ids):
    for pid in playlist_ids:
        data = youtube.get_pitems_for_pid(pid)

        with open(os.path.join(ROOT_DIR, "playlist_items", f"{pid}.json")) as f:
            f.write(json.dumps(data))

        sleep(0.5)


def save_all_videos(youtube, playlist_item_dict):
    for pid, pitems in playlist_item_dict.items():
        data = youtube.get_videos_for_pitems(pitems)

        for video in data:
            with open(os.path.join(ROOT_DIR, "videos", f"{video['id']}.json")) as f:
                f.write(json.dumps(video))

        sleep(0.5)


def save_all_comment_threads(youtube, da, playlists):
    for playlist in playlists:
        pid = playlist["id"]
        ptitle = playlist["snippet"]["title"]

        print(f"Processing {ptitle}...")

        videos = da.get_videos_for_playlist(pid)

        for video in videos:
            vid = video["id"]
            vtitle = video["snippet"]["title"]

            print()
            print(f"Processing {vtitle}...")
            if da.have_comments_for_video(vid):
                print(f'We\'ve already got comments for "{vtitle}".')
                print("Skipping...")
                continue

            threads = youtube.get_comment_threads_for_video(vid)

            with open(
                os.path.join(ROOT_DIR, "db", "commentThreads", f"{vid}.json")
            ) as f:
                f.write(json.dumps(threads))

            print(f'Threads for "{vtitle}" saved.')

            # Give a little delay between batches.
            # - DOS paranoia.
            sleep(0.5)

        print(f"{ptitle} complete!")
        print()
        print("------------------------------------------------------------")
        print()

        # Nice long delay between playlists.
        sleep(2.0)


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get the AIP key as a CLI arg.
    api_key = sys.argv[1]
    if not api_key:
        raise Exception("No API key provided.")

    # Get credentials and create an API client
    youtube = YouTube(api_key)

    # Do stuff.
    da = DataAccess()
    current_playlist = 7
    playlists = da.get_playlists(BVGM_PLAYLIST_IDS[current_playlist:])
    playlists.sort(
        key=lambda playlist: int(playlist["snippet"]["title"].split(" ").pop())
    )

    save_all_comment_threads(youtube, da, playlists)


if __name__ == "__main__":
    main()
