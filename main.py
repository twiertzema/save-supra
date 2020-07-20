# -*- coding: utf-8 -*-

import json
import os
import sys
from time import sleep
from typing import Dict, List

from data_access import DataAccess
from youtube import YouTube

ROOT_DIR = os.getcwd()


def save_all_playlist_items(
    youtube: YouTube, playlist_ids: List[str], dry_run: bool = True
):
    for pid in playlist_ids:
        if not dry_run:
            data = youtube.get_pitems_for_pid(pid)

            with open(os.path.join(ROOT_DIR, "playlist_items", f"{pid}.json")) as f:
                f.write(json.dumps(data))

        sleep(0.5)


def save_all_videos(
    youtube: YouTube, playlist_item_dict: Dict[str, List], dry_run: bool = True
):
    for pid, pitems in playlist_item_dict.items():
        if not dry_run:
            data = youtube.get_videos_for_pitems(pitems)

            for video in data:
                with open(os.path.join(ROOT_DIR, "videos", f"{video['id']}.json")) as f:
                    f.write(json.dumps(video))

        sleep(0.5)


def save_threads(youtube: YouTube, da: DataAccess, from_vid: str, dry_run: bool = True):
    for video in da.gen_all_videos_in_order(from_vid):
        vid = video["id"]
        vtitle = video["snippet"]["title"]

        print()
        print(f"Processing {vtitle}...")
        if da.have_comments_for_video(vid):
            print(f'We\'ve already got comments for "{vtitle}".')
            print("Skipping...")
            continue

        if not dry_run:
            threads = youtube.get_comment_threads_for_video(vid)

            with open(
                os.path.join(ROOT_DIR, "db", "commentThreads", f"{vid}.json"), mode="w"
            ) as f:
                f.write(json.dumps(threads))
        else:
            print("\t(Dry run)")

        print(f'Threads for "{vtitle}" saved.')
        print()
        print("------------------------------------------------------------")

        # Give a little delay between batches.
        # - DOS paranoia.
        sleep(1)


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get the API key as a CLI arg.
    api_key = sys.argv[1]
    if not api_key:
        raise Exception("No API key provided.")

    # Get credentials and create an API client
    youtube = YouTube(api_key)

    # Do stuff.
    da = DataAccess()

    # current_vid = "lM28rfsHge0"
    # save_threads(youtube, da, from_vid=current_vid, dry_run=False)


if __name__ == "__main__":
    main()
