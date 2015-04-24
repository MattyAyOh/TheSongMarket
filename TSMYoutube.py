#!/usr/bin/python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

DEVELOPER_KEY = "AIzaSyDEPD8BKY8vBN7HWF2mIkBVWLX3JwwuC2Q"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def youtube_search(options):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.search().list(
    q=options["q"],
    part="id,snippet",
    maxResults=options["max_results"]
  ).execute()

  videos = []

  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("<title>%s</title> <date>%s</date> <id>%s</id>)" % (search_result["snippet"]["title"],
        search_result["snippet"]["publishedAt"], search_result["id"]["videoId"]))

  return "\n".join(videos)

def youtube_statistics(videoIDs):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  search_response = youtube.videos().list(
    id=videoIDs,
    part="statistics",
    maxResults=5
  ).execute()

  videos = []

  for search_result in search_response.get("items", []):
    if search_result["kind"] == "youtube#video":
      videos.append("<views>%s</views> <date>%s</date> <id>%s</id>)" % (search_result["statistics"]["viewCount"],
        search_result["statistics"]["likeCount"], search_result["statistics"]["dislikeCount"]))

  return "\n".join(videos)
