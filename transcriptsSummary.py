# Filename: process_transcript.py

import re
import os

# Import the get_transcript function from your existing script
from transcriptsDownload import get_transcript

def split_transcript(transcript, max_chunk_size=10000):
    # Split the transcript into sentences using regular expressions
    sentences = re.split(r'(?<=[.!?]) +', transcript)
    chunks = []
    current_chunk = ''
    for sentence in sentences:
        # Check if adding the next sentence exceeds the max chunk size
        
        if len(current_chunk) + len(sentence) + 1 <= max_chunk_size:
            current_chunk += sentence + ' '
        else:
            # If the current chunk is not empty, add it to the list of chunks
            if current_chunk:
                chunks.append(current_chunk.strip())
            # Start a new chunk with the current sentence
            current_chunk = sentence + ' '
    # Add the last chunk if it's not empty
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def main():
    video_id = 'i11fFciD9zQ'  # Replace with your YouTube video ID

    # Get the transcript using your existing function
    transcript = get_transcript(video_id)
    if not transcript:
        print("Failed to retrieve transcript.")
        return

    # Split the transcript into chunks
    chunks = split_transcript(transcript, max_chunk_size=5000)
    print(f"Transcript split into {len(chunks)} chunks.")

    # Optional: Save chunks to files or process them further
    # For demonstration, we'll just print the length of each chunk
    for i, chunk in enumerate(chunks, 1):
        print(f"Chunk {i} length: {len(chunk)} characters")
        print(chunk)

    # If you want to process the chunks further (e.g., send to OpenAI API), you can do so here

if __name__ == "__main__":
    main()
