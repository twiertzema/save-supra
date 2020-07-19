import json
import os
import sys

import data_access

ROOT_DIR = os.getcwd()
DB_DIR = os.path.join(ROOT_DIR, "db")
EXPORT_DIR = os.path.join(ROOT_DIR, "export")


def export_video_ids_tsv():
    videos = data_access.get_all_videos(sort=True)

    with open(f"{EXPORT_DIR}\\vids.tsv", mode="w", encoding="utf-8") as f:
        f.write(f"video_id\tvideo_title\n")

        for video in videos:
            vtitle = video["snippet"]["title"]
            f.write(f"{video['id']}\t{vtitle}\n")


def export_video_ids_json():
    videos = data_access.get_all_videos(sort=True)

    vids = [video["id"] for video in videos]

    with open(f"{EXPORT_DIR}\\video_ids.txt", mode="w") as f:
        f.write(json.dumps(vids, indent=2))


if __name__ == "__main__":
    # export_video_ids_tsv()
    export_video_ids_json()
