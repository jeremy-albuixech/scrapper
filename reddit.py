from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort
import praw
from praw.models import MoreComments
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from gmusicapi import Mobileclient
from uuid import getnode as getmac
from scrapper.google_config import g_music
import os

import re

reddit_app_id     = os.getenv("SCRAPPER_REDDIT_ID")
reddit_app_secret = os.getenv("SCRAPPER_REDDIT_SECRET")
reddit = praw.Reddit(user_agent="Comment Extraction",
                     client_id=reddit_app_id, client_secret=reddit_app_secret)

client = language.LanguageServiceClient()

bp = Blueprint("reddit", __name__)


@bp.route("/", methods=("GET", "POST"))
def index():
    song_match_regexp = r"^(.*)\s(by|-)\s(\w+)(.*)"
    """Scrape a reddit post."""
    if request.method == "POST":
        url = request.form["url"]
        playlist = request.form["playlist"]
        error = None
        

        if not url:
            error = "URL is required."
        if not playlist:
            playlist = "Songs from Reddit " + url
        if error is not None:
            flash(error)
        else:
            print("Parsing the following URL: " + url)            
            
            song_ids = []
            submission = reddit.submission(url=url)
            songs = []
            submission.comment_sort = "top"
            submission.comments.replace_more(limit=1)
            exclude_words = ["SONG", "COMMENT", "ICON", "COMMENTS", "SONGS", "ICONS"]
            print("Fetching top comments")
            for top_level_comment in submission.comments:
                # We only want short-ish replies as we're looking for songs and not meta or chatter
                if len(top_level_comment.body) < 90:   
                    cleaned_comment = clean(top_level_comment.body)
                    if re.match(song_match_regexp, cleaned_comment, re.IGNORECASE):
                        song_match = re.match(song_match_regexp, cleaned_comment)
                        songs.append(song_match.group(1))
                    else:
                        print("Extracting entities")
                        document = types.Document(
                            content=cleaned_comment,
                            type=enums.Document.Type.PLAIN_TEXT)                    
                        # Extract entities of the comments
                        entities = client.analyze_entities(document=document).entities
                        # If the entity is a work of art, append it to the list.
                        for entity in entities:   
                            # entity type number 5 is WORK_OF_ART              
                            if entity.type == 5 and entity.name.upper() not in exclude_words:
                                songs.append(entity.name)
            print("Matching songs with Google play music")
            for song in songs:        
                search_result = g_music.search(song, max_results=20)    
                if("song_hits" in search_result):
                    if len(search_result["song_hits"]) > 0:
                        song_id = search_result["song_hits"][0]["track"]["storeId"]; 
                        song_ids.append(song_id)           
            
            print("Creating playist: " + playlist)
            playist_id = g_music.create_playlist(playlist, "", True)
            print("adding songs to playlist" + playist_id )
            g_music.add_songs_to_playlist(playist_id, song_ids)          
        return render_template("reddit/index.html", posts=songs, google_auth = g_music.is_authenticated())

    return render_template("reddit/index.html", google_auth = g_music.is_authenticated())

def clean(comment):
    comment = re.sub(r'https?:\/\/.*[\r\n]*', '', comment, flags=re.MULTILINE)
    comment = comment.replace("[", "").replace("(", "").replace("]", "").replace(")", "")
    return comment

