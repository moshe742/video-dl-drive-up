# video-dl-drive-up
Project to download videos from the web and upload to your drive

## setup docker
One can use docker to use this script with

    $ docker build -t image_name .
    $ docker run -it image_name bash
## usage
The script is very simple, one run the script with

    $ python main.py youtube_link
The command above will download the videos in the link above. If you want
to limit the download by date you can use either start date (-s), end date (-e)
or both.

Take notice that the date format is the one used by youtube-dl, it must be
4 digits year, followed by 2 digits month, and 2 digits day.

    $ python main.py youtube_link -s 20200101 -e 20210131