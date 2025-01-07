# geosolver
Geoguessr assistant to solve rounds based on voice commands.

## How to install

source venv/bin/activate
pip -r requirements.txt

Export or create a `.env` file with the following content:

```
OPEN_API_KEY=your_api_key
```

$ python main.py 2> /dev/null

## How it works

The program listens to voice commands and uses the Google Cloud Speech-to-Text API to transcribe them.
It accepts two commands:
* "take photo" - takes a screenshot of the current geoguessr round.
* "location" - use all the screenshots taken to solve the round with an OpenAI API call. The result is spoken out loud and a browser is open with the exact location on a map.
* "exit" - exits the program.
