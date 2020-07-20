import json
import os
import sys
from typing import Optional

from data_access import DataAccess


class Export:
    def __init__(self, root_dir: Optional[str] = None):
        self.root_dir = root_dir or os.getcwd()
        self.export_dir = os.path.join(self.root_dir, "export")

    def export_video_ids_tsv(self):
        da = DataAccess()
        videos = da.get_all_videos(sort=True)
        with open(
            os.path.join(self.export_dir, "vids.tsv"), mode="w", encoding="utf-8"
        ) as f:
            f.write(f"video_id\tvideo_title\n")

            for video in videos:
                vtitle = video["snippet"]["title"]
                f.write(f"{video['id']}\t{vtitle}\n")

    def export_video_ids_json(self):
        da = DataAccess()
        videos = da.get_all_videos(sort=True)

        vids = [video["id"] for video in videos]

        with open(os.path.join(self.export_dir, "video_ids.txt"), mode="w") as f:
            f.write(json.dumps(vids, indent=2))


if __name__ == "__main__":
    export = Export()
    export.export_video_ids_tsv()
    export.export_video_ids_json()
