# Timelinify

Timelineify is a web application that tracks your listens on Spotify, displays them to you in a timeline format and shows statistics for each track.

The app is currently not hosted on a live server, but this will be coming shortly so stay tuned!

## Running the App Locally

This app is a full-stack application, meaning that the frontend (React.js) and the backend (Flask) are separate and must be run simultanouesly.

After cloning this repository, install the dependencies. To install the frontend dependencies, navigate to the "client" directory and run

    $ npm install

To install the backend dependencies, navigate to the "server" directory and run

    $ pip install -r requirements.txt

### Acquiring your own Spotify Developer Credentials

To use the program, you must sign up as a Spotify Developer at (https://developer.spotify.com/dashboard). There, you can create an app and add the following URI to the "callback URIs" field:

  - http://localhost:5000/callback

You must then replace the "client_id" and "client_secret" in the .env file in the server directory with your own credentials.

Finally, navigate to the root directory and run

    $ npm start

Enjoy!
