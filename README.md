# Project description
The application is intended to download videos from Netology website (Kinescope player). It logs in 
to the page where the video is available, secludes the video file to a separate window, then runs the 
video and periodically winds it forward. Meanwhile, the requests sent by Kinescope are detected and recorded.
Later the app uses those requests to receive video and audio chunks to join them to a solid playable file.  
Though the program is designed specifically for Netology, it's composition allows to use certain elements
of the program to download other videos published at Kinescope. More details on various ways to use the app
are stated below.

# Program composition and set up
### main.py
This is the entry point to the program. It puts the algorythm together and leads the process.

### config.py
The configuration file that is to be manually edited in order set up all necessary details to run the 
app:
- URL -  Link to Netology video file. Nothing specific, just the page, where you can play the video.
- EMAIL - Netology authorization e-mail
- PASS_PATH - Path (and filename) to store the Netology password. The app asks for the password once, at first launch.
- OUTPUT - Path (and filename) for the output video file.
- LINKS_LOG - Path (and filename) to store the links from detected requests
- FFMPEG_LOG - The output video is put together with ffmpeg program. This is the compilation report.
- STEP - This parameter sets up the forward winding step (how many times the right arrow key is pressed).
It winds 5 seconds forward with each press.
- DURATION - The overall duration of winding/detecting process in seconds. 

Set up the STEP and DURATION parameters in accordance with video duration experimentally. For example, a 
2 hours video is best downloaded with the following params: DURATION: 150, STEP: 200.  
Specific values to be set depend on the server's configuration (max chunk size, for instance) and may vary for
different videos. In order to keep the app functional with a wide range of videos, it was decided to leave
the params open for edit. Feel free to test what is best for your needs.  

If the resulting video lacks sound or video fragments, that means that some requests failed to be detected. To fix this, reduce the STEP and 
increase the DURATION. If the video is short and small in size, there is no need to wait for too long, and
the DURATION may be shortened.

### kinescrapper
This is a package that performs the links detection and downloading. It operates the playback and winding as well.
It has three major functions: 'scrape', 'download', 'merge_files' that split the process to stages. Functions
can be called independently in an order required for your needs.  
The package also contains the UnDetChrome class that is used to operate the browser.  

The package can be used independently of the rest of the program to download any video material hosted by 
Kinescope. In order to do so, a specific URL starting with "https://kinescope.io/..." needs to be fed to the scrape function.
This link must lead directly to the video without any extra content. It can be found using dev tools on the original video webpage.  
The remaining function parameters correspond to the constants from config.py, so you may want to return
to config.py description and study their definitions.

# Requirements
The application is based on the Undetected Chrome Driver (which uses Selenium). It needs 'requests' module to be
installed as well. Python requirements are specified in requirements.txt.   
Ffmpeg needs to be installed to put the video together.  
Functioning Netology account, login and password must be possessed.  

# Legal notes: 
All Netology materials are right protected, and it's use beyond personal educational needs is prohibited. So are, 
supposedly, most of the videos from Kinescope.  
This program was designed for educational purposes only and must never be used in illegal acts. Ensure to study the 
legal aspects of the actions you plan to undertake with and its potential consequences.

# Updates notes:
`09/07/2023` Now the script ensures that the same chunk would not be downloaded twice, by saving each one to a set, and checking if it isn't there before downloading.


