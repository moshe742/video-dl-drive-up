#!/usr/bin/env python

import argparse
import pickle
import os.path

import youtube_dl
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload
from youtube_dl import DateRange

CLIENT_SECRETS_FILE = 'credentials.json'
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'

SCOPES = [
    'https://www.googleapis.com/auth/drive',
]


def get_authenticated_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(host='localhost', port=8080,
                                          authorization_prompt_message='Please visit this url: {url}',
                                          success_message='The auth flow is complete; you may close this window.',
                                          open_browser=True)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return build(API_SERVICE_NAME, API_VERSION, credentials=creds)


class DownloadLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)


def finished_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('-s', '--start-date')
    parser.add_argument('-e', '--end-date')

    args = parser.parse_args()
    start_date = None
    end_date = None
    if args.start_date:
        start_date = args.start_date
    if args.end_date:
        end_date = args.end_date

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'logger': DownloadLogger(),
        'progress_hooks': [finished_hook],
        'writeinfojson': True,
        'writedescription': True,
    }

    if start_date or end_date:
        ydl_opts.update({'date_range': DateRange(args.start_date, args.end_date)})
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.url])

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    files_dir = os.path.abspath(os.path.dirname(__file__))
    for f in os.listdir(files_dir):
        if f.endswith('mp4'):
            file_metadata = {
                'name': f,
                'mimeType': 'video/mp4',
            }
            media = MediaFileUpload(f, mimetype='video/mp4', resumable=True)
            service.files().create(body=file_metadata, media_body=media,
                                   fields='id').execute()


if __name__ == '__main__':
    main()
