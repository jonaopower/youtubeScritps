import requests
import re
import json
import urllib3
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Suppress only the single InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)

# Disable SSL certificate verification globally
ssl._create_default_https_context = ssl._create_unverified_context

def get_transcript(video_id, lang='en'):
# def get_transcript(video_id):    
    url = f'https://www.youtube.com/watch?v={video_id}'

    # Use requests without SSL verification
    response = requests.get(url, verify=False)
    html = response.text

    def extract_json_object(text, start_index):
        # [Function remains unchanged]
        stack = []
        in_string = False
        escape = False
        i = start_index
        while i < len(text):
            c = text[i]
            if not in_string:
                if c == '{' or c == '[':
                    stack.append(c)
                elif c == '}' or c == ']':
                    if not stack:
                        return None
                    opening = stack.pop()
                    if (opening == '{' and c != '}') or (opening == '[' and c != ']'):
                        return None
                    if not stack:
                        # End of JSON object
                        return text[start_index:i+1]
                elif c == '"':
                    in_string = True
            else:
                if not escape and c == '"':
                    in_string = False
                elif c == '\\' and not escape:
                    escape = True
                else:
                    escape = False
            i += 1
        return None  # Could not find the end of JSON object

    def find_var(json_var, text):
        var_pattern = re.escape(json_var) + r'\s*=\s*'
        match = re.search(var_pattern, text)
        if match:
            start_index = match.end()
            json_str = extract_json_object(text, start_index)
            return json_str
        else:
            return None

    json_str = find_var('ytInitialPlayerResponse', html)
    if json_str:
        try:
            player_response = json.loads(json_str)
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
            return None
    else:
        print("Could not find ytInitialPlayerResponse")
        return None

    if 'captions' in player_response:
        caption_tracks = player_response['captions']['playerCaptionsTracklistRenderer']['captionTracks']
        # Find the caption track with the desired language code
        caption_track = None
        for caption in caption_tracks:
            if caption['languageCode'] == lang:
                caption_track = caption
                break
        if caption_track is None:
            # If desired language not found, use the first one
            print(f"Desired language '{lang}' not found, using default.")
            caption_track = caption_tracks[0]
        caption_url = caption_track['baseUrl']
        # Optionally, add format parameter
        caption_url += '&fmt=json3'
        # Use requests without SSL verification
        caption_response = requests.get(caption_url, verify=False)
        captions_text = caption_response.text
        captions_data = json.loads(captions_text)
        transcript = ''
        for event in captions_data['events']:
            if 'segs' in event:
                for seg in event['segs']:
                    transcript += seg.get('utf8', '')
            else:
                # This event may not have 'segs', skip it
                continue
            transcript += '\n'  # Add newline between captions
        return transcript
    else:
        print("No captions available for this video.")
        return None

# # Example usage:
# # video_id = 'YOUR_VIDEO_ID'  # Replace with your video ID
# # video_id = "i11fFciD9zQ"
# transcript = get_transcript(video_id)
# if transcript:
#     print("Transcript:")
#     print(transcript)
# else:
#     print("Could not retrieve transcript.")
