import googleapiclient.discovery
import googleapiclient.errors

DEFAULT_MAX_RESULTS = 50


def gen_resources(res, **list_params):
    print("Generating resources.")
    if "maxResults" not in list_params.keys():
        list_params["maxResults"] = DEFAULT_MAX_RESULTS

    next_page_token = None
    while True:
        if next_page_token:
            list_params["pageToken"] = next_page_token

        request = res().list(**list_params)
        # print("\t\tRequest made successfully.")
        response = request.execute()
        # print(f"\t\tRaw response: {response}")

        data = response["items"]
        print(f"\tRetrieved {len(data)}")

        yield data

        if "nextPageToken" in response.keys():
            next_page_token = response["nextPageToken"]
        else:
            print("\tReached last page.")
            break

    return None


def gen_resources_for_ids(res, res_ids, **list_params):
    print("Generating resources for ids.")
    total = len(res_ids)
    res_counter = 0

    if "maxResults" not in list_params.keys():
        list_params["maxResults"] = DEFAULT_MAX_RESULTS
        max_results = DEFAULT_MAX_RESULTS
    else:
        max_results = list_params["maxResults"]

    _res_ids = res_ids.copy()

    while len(_res_ids) > 0:
        request_ids = []
        for _ in range(max_results):
            request_ids.append(_res_ids.pop(0))

            if len(_res_ids) == 0:
                break

        print(f"\tRequesting {res_counter}-{res_counter + len(request_ids)} of {total}.")

        list_params["id"] = ",".join(request_ids)

        request = res().list(**list_params)
        response = request.execute()
        yield response["items"]

        res_counter += max_results

    print("\tFinished requesting resources.")
    return None


class YouTube:
    def __init__(self, api_key):
        api_service_name = "youtube"
        api_version = "v3"

        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=api_key)

    def get_pitems_for_pid(self, pid):
        print(f"Requesting playlist items for {pid}.")

        data = []

        for items in gen_resources(
                self.youtube.playlistItems,
                part="contentDetails",
                playlistId=pid):
            data += items

        return data

    def get_videos_for_pitems(self, pitems):
        print("Requesting videos for playlist items.")

        vids = [pitem["contentDetails"]["videoId"] for pitem in pitems]
        data = []

        for items in gen_resources_for_ids(
                self.youtube.videos,
                vids,
                part="snippet,statistics"):
            data += items

        return data

    def gen_comment_threads_for_videos(self, videos):
        print("Requesting comment threads for videos.")

        for video in videos:
            threads = self.get_comment_threads_for_video(video["id"])

            yield threads

        return None

    def get_comment_threads_for_video(self, video_id):
        print(f"Getting threads for {video_id}")

        # Get all the threads for the video (paginated).
        threads = []
        for items in gen_resources(
                self.youtube.commentThreads,
                part="snippet",
                videoId=video_id,
                textFormat="plainText",
                maxResults=100):  # Allows up to 100 at a time.
            threads += items
            pass

        for thread in threads:
            # print(thread)
            # Then get the top-level comments' replies (paginated).
            if thread["snippet"]["totalReplyCount"] > 0:
                top_level_comment = thread["snippet"]["topLevelComment"]

                print(f"\tGetting replies for {thread['id']}")
                replies = []
                for items in gen_resources(
                        self.youtube.comments,
                        part="snippet",
                        parentId=top_level_comment["id"],
                        textFormat="plainText",
                        maxResults=100):  # Allows up to 100 at a time.
                    replies += items

                # And hydrate the thread with the retrieved comments.
                thread["replies"] = {
                    "comments": replies
                }

        return threads