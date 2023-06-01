#!/usr/bin/env python
# coding: utf-8

# ## Speech Recognition Exercise 
# 
# ### Author: Jesus Cantu Jr.
# ### Date: May 31, 2023
# 
# Speech recognition in machine learning refers to the task of automatically converting spoken language into written text. Machine learning techniques allow speech recognition systems to learn from data and adapt to various speech patterns, accents, and languages. The models are trained to capture acoustic and linguistic patterns in the data, enabling accurate recognition of spoken words and sentences. The modeling process generally entails: 
# 1. __Data Collection__: Large amounts of speech data are collected, usually in the form of audio recordings, along with their corresponding transcriptions or labels.
# 3. __Feature Extraction__: From the raw audio data, various acoustic features are extracted, such as mel-frequency cepstral coefficients (MFCCs), filter banks, or spectrograms. These features represent the characteristics of the speech signal that are relevant for recognition.
# 3. __Training Data Preparation__: The collected data is split into two parts: a training set and a validation set. The training set is used to train the machine learning model, while the validation set is used for model evaluation and hyperparameter tuning.
# 4. __Model Training__: Machine learning algorithms, such as deep neural networks (DNNs), recurrent neural networks (RNNs), or convolutional neural networks (CNNs), are trained on the extracted acoustic features and corresponding transcriptions. The model learns to map the input features to the target text labels.
# 5. __Model Evaluation and Refinement__: The trained model is evaluated on the validation set to assess its performance. Various metrics, such as word error rate (WER), are used to measure the accuracy of the transcriptions. The model is refined by adjusting its architecture, parameters, and training process based on the evaluation results.
# 6. __Inference__: Once the model is trained and evaluated, it can be used for speech recognition on new, unseen audio data. The model takes the acoustic features of the input speech and predicts the corresponding text transcription.
# 7. __Post-processing__: The output text may undergo additional post-processing steps, such as language modeling, spell-checking, or punctuation restoration, to improve the final transcription.

# In Python, there are several libraries and APIs available that we can use to perform speech recognition. One popular library is the __SpeechRecognition__ library, which provides a simple interface to access various speech recognition engines. Here's an example of how we can perform speech recognition using this library:

# In[140]:


# Import the library and create a recognizer object
import speech_recognition as sr
import time

def recognize_speech(audio_file):
    r = sr.Recognizer()

    # Load audio from a file or capture audio from a microphone
    if audio_file is None:
        with sr.Microphone() as source:
            print("Speak something...")
            audio = r.listen(source)
            recording_duration = len(audio.frame_data) / float(audio.sample_rate)
            print("Recording Duration: {:.2f} seconds".format(recording_duration))
    else:
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)

    try:
        # Recognize speech using the default engine
        text = r.recognize_google(audio)
        print("Speech Recognition Result:", text)
    except sr.UnknownValueError:
        print("Unable to recognize speech")
    except sr.RequestError as e:
        print("Error: {0}".format(e))

# Example usage
audio_file = None  # Set to 'None' to capture audio from the microphone, otherwise use 'path/to/audio/file.wav'
recognize_speech(audio_file)


# In the above example, the __recognize_google__ method is used to perform speech recognition using __Google's Web Speech API__. However, we can also use other speech recognition engines such as __Sphinx__ or __Wit.ai__ by specifying the appropriate recognizer method (e.g., recognize_sphinx or recognize_wit).
# 
# Note that to use the __recognize_google__ method, we'll need an internet connection as it sends the audio data to Google's servers for processing. For offline speech recognition, we can use the __recognize_sphinx__ method, which utilizes the CMU Sphinx engine.
# 
# Pros of using Google's API for speech-to-text translation:
# 
# - __Accuracy__: Google's speech recognition technology is known for its high accuracy. It utilizes advanced machine learning algorithms and large datasets to deliver reliable and precise transcriptions.
# - __Language support__: Google's API supports a wide range of languages, allowing you to transcribe audio in different languages and dialects. This makes it a versatile choice for multilingual applications.
# - __Continuous improvements__: Google continually invests in improving its speech recognition technology. They frequently update their models and algorithms to enhance accuracy and add new features, ensuring you benefit from ongoing advancements.
# - __Ease of use__: Google provides comprehensive documentation and client libraries for various programming languages, including Python. This simplifies the integration process and makes it easier to incorporate speech recognition into your applications.
# - __Scalability__: Google Cloud Speech-to-Text API is designed to handle large volumes of audio data and can scale to meet your needs. It provides robust infrastructure to process and transcribe audio in real-time or batch mode.

# Cons of using Google's API for speech-to-text translation:
# 
# - __Cost__: Google's API usage comes at a cost. While there is a free tier with limitations, extensive usage or processing large amounts of audio data may incur charges. It's essential to consider the pricing structure and estimate the potential costs based on your usage requirements.
# - __Internet dependency__: Using Google's API for speech recognition requires an internet connection. If your application needs to work offline or in environments with limited internet access, this can be a limitation.
# - __Privacy and data handling__: Transcribing audio using Google's API means your audio data is sent to Google's servers for processing. Depending on your data privacy requirements, you may need to consider the implications of sharing sensitive or confidential audio content.
# - __Reliance on third-party service__: Integrating with Google's API means relying on their service availability and performance. If there are any disruptions or issues with the API, it may impact your application's functionality.
# - __Customization limitations__: While Google's API offers a range of features and customization options, it may not cover all specialized use cases. If your application requires highly specific domain-specific vocabulary or unique requirements, you may need to explore other alternatives or consider building a custom speech recognition model.
# 
# It's important to evaluate these factors based on your specific project requirements, budget, data privacy considerations, and the trade-offs you are willing to make before deciding on a specific speech recognition engine. For this example, we will continue to utilize Google's API as it allows for the easy implementation of more advanced techniques for speech recognition, such as language models, noise filtering, and speaker diarization. But before that let's create functions that will allow us to better capture and save audio files; these will serve as the data for our analysis. 

# ### Record Audio Files

# In[144]:


import pyaudio
import wave
import time
import threading
from datetime import datetime

def save_audio_from_microphone(output_folder, sample_rate):
    print("Press Enter to start recording...")
    input()

    print("Recording will start in:")
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)

    print()
    print("Recording started. Speak now...")
    print()
    start_time = time.time()

    # Create a stop event
    stop_event = threading.Event()

    def stop_recording():
        # Set the stop event when the user presses Enter again
        input("Press Enter again to stop recording...")
        print()
        stop_event.set()

    # Start recording audio from the default microphone in a separate thread
    recording_thread = threading.Thread(target = record_audio, args = (output_folder, sample_rate, start_time, stop_event))
    recording_thread.start()

    stop_recording()

    # Wait for the recording thread to finish
    recording_thread.join()

def record_audio(output_folder, sample_rate, start_time, stop_event):
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open audio stream
    stream = audio.open(format = pyaudio.paInt16, # Specifies the format of the audio data, in this case, pyaudio.paInt16 represents 16-bit signed integer format.
                        channels = 1, # Specifies the number of audio channels to record, in this case, 1 for mono audio.
                        rate = sample_rate, # Specifies the sample rate of the audio stream, which is set to sample_rate variable.
                        input = True, # Sets the audio stream for input (recording) mode.
                        frames_per_buffer = 1024) # Specifies the number of audio frames to read at a time, which is set to 1024.

    frames = [] # This line initializes an empty list called frames. This list will be used to store the audio frames captured from the microphone. Each audio frame contains a chunk of audio data.

    # Record audio until the stop event is set
    while not stop_event.is_set():
        data = stream.read(1024)
        frames.append(data)

    print("Recording finished.")
    print()

    # Stop the stream and close the audio stream
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Calculate the duration of the recording
    end_time = time.time()
    duration = end_time - start_time

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") # Note, we utilize current timestamp to name our recordings!!
    file_name = f"recording_{timestamp}.wav"

    # Save the recorded audio as a WAV file
    file_path = os.path.join(output_folder, file_name)
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wf.setframerate(sample_rate)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Audio saved as '{file_name}'.")


# This code allows you to record audio from the microphone and save it as a WAV file. It prompts the user to start the recording and displays a countdown. The audio is recorded in a separate thread until the user presses Enter again to stop it. The duration of the recording is calculated, and the recorded audio is saved as a WAV file in the specified output directory.
# 
# Note, the parameter __sample_rate__ in the __save_audio_from_microphone__ function controls the sample rate at which the audio is captured. The sample rate refers to the number of samples (audio data points) captured per second during the recording. It is measured in Hertz (Hz). A higher sample rate provides a more accurate representation of the audio waveform but also results in larger file sizes. Common sample rates include 44100 Hz (CD quality), 48000 Hz (DVD quality), and 16000 Hz (standard for speech recognition). You can adjust the __sample_rate__ parameter to match your desired audio quality and storage constraints.
# 

# In[145]:


# Example usage
output_folder = '/Users/Jesse/Desktop/Speech_Recognition_Exercise/Recordings'
sample_rate = 16000  # Audio sample rate in hertz
save_audio_from_microphone(output_folder, sample_rate)


# ### Upload & Convert Audio Files

# We might wish to upload some of our own audio files locally for analysis. The __SpeechRecognition__ library supports various audio formats, but it has certain requirements for optimal performance. The library can work with audio files in WAV, AIFF, FLAC, or MP3 formats. However, it is recommended to use 16-bit WAV files with a sample rate of 16 kHz for the best accuracy and performance.
# 
# If our audio files are in a different format, such as MP3, we can use a library like pydub to convert them to the required format before performing speech recognition. Here's an example code snippet that demonstrates how to convert an MP3 file to a WAV file using pydub:

# In[55]:


import os
from pydub import AudioSegment

def convert_mp3_to_wav(mp3_file):
    wav_file = os.path.splitext(mp3_file)[0] + '.wav'  # Generate the WAV file name
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format = 'wav')
    return wav_file

# Example usage
mp3_file = '/Users/Jesse/Desktop/Speech_Recognition_Exercise/Recordings/small_talk_everyday_english.mp3' # 'path/to/input/file.mp3'
mp3_file_name = os.path.basename(mp3_file)

wav_file = convert_mp3_to_wav(mp3_file) # Note, new WAV file will be saved under the same directory as the MP3 file! 
wav_file_name = os.path.basename(wav_file)
print(f"Converted MP3 file '{mp3_file_name}' to WAV: '{wav_file_name}'.")


# By converting the audio files to the recommended format, we can ensure better compatibility and accuracy when using the __SpeechRecognition__ library. In most cases, when using the __SpeechRecognition__, you do not need to know the sample rate of each audio file explicitly. The library is designed to automatically detect the sample rate of the audio files during the speech recognition process.
# 
# However, it's worth noting that if we have specific knowledge about the sample rate or other properties of the audio file, we can provide that information as part of the configuration options when using this library or other speech recognition engines. This can help in cases where the automatic detection may not be accurate or when dealing with unique audio file formats. Below is an example of how to figure out the sample rate in Hz of a specific audio file.

# In[60]:


import soundfile as sf

def measure_sample_rate(audio_file):
    with sf.SoundFile(audio_file, "r") as sound_file:
        sample_rate = sound_file.samplerate
    return sample_rate

# Example usage
audio_file = "/Users/Jesse/Desktop/Speech_Recognition_Exercise/Recordings/small_talk_everyday_english.wav"
file_name = os.path.basename(audio_file)
sample_rate = measure_sample_rate(audio_file)
print(f"Audio file: '{file_name}'")
print(f"Sample rate: {sample_rate} Hz")


# The __Google Cloud Speech-to-Text API__, which we will utilize later, requires single-channel (mono) audio. The number of channels in an audio file indicates the number of audio streams present, with mono representing a single channel and stereo representing two channels. The choice of mono or stereo depends on the recording setup, audio source, and intended use of the audio.
# 
# The number of channels is important because it affects how audio is perceived and processed. For example, when performing speech recognition or audio processing tasks, it is often desirable to have mono audio as input to ensure compatibility and consistent analysis. If the input audio has more than one channel, it may need to be converted to mono for certain applications. Here is how we can find how many channels a specific audio file might contain.

# In[61]:


import wave

def get_audio_channels(audio_file):
    with wave.open(audio_file, 'rb') as wav:
        num_channels = wav.getnchannels()
    return num_channels

# Example usage
audio_file = '/Users/Jesse/Desktop/Speech_Recognition_Exercise/Recordings/small_talk_everyday_english.wav'
file_name = os.path.basename(audio_file)
num_channels = get_audio_channels(audio_file)
print(f"Audio file: '{file_name}'")
print(f"Number of channels: {num_channels}")


# To resolve this issue, we can convert the audio file to a single-channel format before passing it to the API like so:

# In[62]:


from pydub import AudioSegment
import os

def convert_to_mono(audio_file):
    output_file = os.path.splitext(audio_file)[0] + '_mono.wav'
    audio = AudioSegment.from_wav(audio_file)
    audio = audio.set_channels(1)  # Convert to mono
    audio.export(output_file, format = 'wav')
    return output_file 

# Example usage
audio_file = '/Users/Jesse/Desktop/Speech_Recognition_Exercise/Recordings/small_talk_everyday_english.wav'
file_input = os.path.basename(audio_file)

output_file = convert_to_mono(audio_file) # Note, new WAV file will be saved under the same directory as the old file
file_output = os.path.basename(output_file)
print(f"Audio file '{file_input}' converted to mono: '{file_output}'.")


# ### Transcribe Audio Files

# We will move on to transcribing some of the recordings by utilizing the __SpeechRecognition__ library which offers the following capabilities:
# 
# 1. __Microphone Input__: It allows you to capture audio input directly from a microphone. You can start and stop recording audio using the Microphone class provided by the library.
# 2. __Audio File Input__: You can process speech recognition on pre-recorded audio files by providing the file path to the library. It supports various audio file formats such as WAV, MP3, FLAC, and more.
# 3. __Multiple Recognition Engines__: SpeechRecognition supports multiple recognition engines, allowing you to choose the one that suits your requirements. It currently supports the following engines:
#    - Google Web Speech API (requires an internet connection)
#    - Google Cloud Speech API (requires API credentials and an internet connection)
#    - CMU Sphinx (offline, requires installation of pocketsphinx library)
#    - Microsoft Bing Voice Recognition (requires an internet connection and API key)
#    - Houndify API (requires an internet connection and API credentials)
#    - IBM Speech to Text (requires an internet connection and IBM Cloud credentials)
#    - Wit.ai API (requires an internet connection and Wit.ai credentials)
# 4. __Transcription Results__: Once the speech recognition is performed, you can obtain the transcriptions in text format. The library provides methods to retrieve the transcriptions, confidence scores, and other information from the recognized audio.
# 5. __Language Support__: The library supports multiple languages for speech recognition. You can specify the language code corresponding to the spoken language in the configuration.
# 4. __Error Handling__: SpeechRecognition provides error handling mechanisms to handle any exceptions or errors that may occur during the speech recognition process.
# 
# The code below provides a basic speech recognition functionality with the ability to process multiple audio files and save the transcriptions for further analysis or use.

# In[63]:


import os
import speech_recognition as sr

def transcribe_audio(audio_file):
    # Initialize the recognizer
    r = sr.Recognizer()

    # Load audio file
    with sr.AudioFile(audio_file) as source:
        # Read the audio data from the file
        audio = r.record(source)

        # Perform speech recognition
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from speech recognition service: {e}")

# Specify the directory containing the audio files
audio_directory = '/Users/Jesse/Desktop/Speech_Recognition_Exercise/Recordings' # /path/to/audio/files

# Specify the directory to save the transcriptions
output_directory = '/Users/Jesse/Desktop/Speech_Recognition_Exercise/Transcriptions' # /path/to/transcriptions

# List all the files in the directory
audio_files = os.listdir(audio_directory)

# Filter the files to keep only the audio files (e.g., WAV, MP3, etc.)
audio_files = [f for f in audio_files if f.endswith(('.wav'))] # Note, we are limiting the format to WAV files only


# Print the available audio files
print("Available audio files:")
for i, file in enumerate(audio_files):
    print(f"{i + 1}. {file}")

# Prompt the user to choose the files to transcribe
print()
selection = input("Enter the file numbers (separated by commas) then click Enter to transcribe: ")
print()

# Split the user's selection into individual file numbers
selected_files = selection.split(",")

# Transcribe the selected files
for file_num in selected_files:
    try:
        file_index = int(file_num.strip()) - 1
        if file_index >= 0 and file_index < len(audio_files):
            audio_file = os.path.join(audio_directory, audio_files[file_index])
            print(f"Transcribing: {audio_file}")
            transcription = transcribe_audio(audio_file)
            print("Transcription:")
            print(transcription)
            print()

            # Save the transcription as a text file
            base_name = os.path.splitext(audio_files[file_index])[0]
            output_file = os.path.join(output_directory, f"{base_name}.txt")
            with open(output_file, 'w') as f:
                f.write(transcription)
            print(f"Transcription saved as: {output_file}")
            print()
        else:
            print(f"Invalid file number: {file_num}")
    except ValueError:
        print(f"Invalid file number: {file_num}")


# 
# The provided code allows the user to select audio files from a directory and transcribe them. The script utilizes the __recognize_google__ method for speech recognition. After transcribing each selected file, the script prints the transcription to the console. It also saves the transcriptions as text files with the same name as the audio files in a specified output directory. 
# This is to ensure we keep track of our data as it moves down the pipeline and why utilizing a unique and dynamic naming convention, like a timestamp, initially (when creating the audio files) is very important. 
# 
# However, as tou can see, the provided code does not explicitly handle punctuation in the transcriptions. The __recognize_google__ method from the __SpeechRecognition__ library does not include punctuation by default. It focuses on converting spoken words into text without including punctuation marks such as periods or commas. If you want to include punctuation in the transcriptions, you would need to modify the code to either use a different speech recognition API that supports punctuation or implement post-processing steps to add punctuation marks based on the recognized words and context.
# 
# We will move on to working with __Google Cloud Speech API__, which requires API credentials. The __Google Cloud Speech-to-Text API__ provides advanced speech recognition capabilities, including the ability to recognize and include punctuation marks in the transcriptions. We may also want to be able to translate numeric information into text for further natural language processing (NLP) analysis, as well as distinguish the number of users and their lines (i.e, diarization) to count the number of conversational turns, for example, and this can be all done through the __Google Cloud Speech API__.

# Note, if you want to listen to the audio file and compare it it to transcription above run the following: 

# In[83]:


import os
from IPython.display import Audio

def list_audio_files(directory):
    audio_files = []
    for file in os.listdir(directory):
        if file.endswith(".wav"): # Note, we are limiting the format to WAV files only
            audio_files.append(file)
    return audio_files

def select_files(audio_files):
    selected_files = []
    print("Available audio files:")
    for i, file in enumerate(audio_files):
        print(f"{i + 1}. {file}")
    while True:
        print()
        selection = input("Select the audio file to play (enter the number) then press Enter: ")
        try:
            selected_index = int(selection) - 1
            if selected_index >= 0 and selected_index < len(audio_files):
                selected_file = audio_files[selected_index]
                selected_files.append(selected_file)
                break
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid selection. Please try again.")
    return selected_files

def play_audio_file(directory, audio_file):
    audio_path = os.path.join(directory, audio_file)
    return Audio(audio_path, autoplay = True, normalize = False)

def main():
    directory = "/Users/Jesse/Desktop/Speech_Recognition_Exercise/Recordings" 
    audio_files = list_audio_files(directory)
    selected_files = select_files(audio_files)
    print()
    print(f'Currently Playing: {", ".join(selected_files)}')
    for audio_file in selected_files:
        audio = play_audio_file(directory, audio_file)
        display(audio)

if __name__ == "__main__":
    main()


# ### Setting up Google Cloud Services 

# To use the __Google Cloud Speech-to-Text API__, you need to set up a Google Cloud project, enable the __Speech-to-Text API__, and obtain the necessary credentials (API key or service account key).

# To access Google Cloud services and obtain credentials, you can follow these steps:
# 
# 1.  Go to the Google Cloud Console: https://console.cloud.google.com/
# 2. Create a new project or select an existing project.
# 3. Enable the necessary APIs for the services you want to use (e.g., Google Cloud Storage, Speech-to-Text API).
# 4. Set up authentication by creating service account credentials:
#    - In the Cloud Console, navigate to "IAM & Admin" -> "Service Accounts" section.
#    - Click on "Create Service Account" and provide a name and optional description.
#    - Assign the required roles to the service account based on the services you want to access.
#    - Choose a key type (JSON is recommended) and click "Create".
#    - The JSON key file will be downloaded to your local machine.
# 
# For detailed instructions, you can refer to the following Google Cloud documentation on managing service account keys:
#   - Authentication Overview: https://cloud.google.com/docs/authentication
#   - Creating and Managing Service Account Keys: https://cloud.google.com/iam/docs/creating-managing-service-account-keys

# Note, to set up the credentials for the __Google Cloud Speech-to-Text API__ as an environment variable in your Jupyter Notebook, you can use the __os.environ__ dictionary. Here's an example of how you can do it:
# 
# 1. Obtain the service account key JSON file for your Google Cloud project that has access to the Speech-to-Text API. Make sure you have downloaded the key file to your local machine!
# 2. In your Jupyter Notebook, add the following code to set the GOOGLE_APPLICATION_CREDENTIALS environment variable to the path of your service account key JSON file:

# In[64]:


import os

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/path/to/service_account_key.json'

# Remember to keep the downloaded JSON key file secure and not share it publicly, 
# as it grants access to your Google Cloud resources!!!


# 3. After setting the environment variable, you can use the Google Cloud Speech-to-Text API in your notebook without explicitly specifying the credentials. The API client libraries will automatically look for the GOOGLE_APPLICATION_CREDENTIALS environment variable to authenticate the requests. 

# ### Transcribe Audio Files with Punctuation

# In[86]:


import os
#import logging
import soundfile as sf
from google.cloud import storage
from google.cloud import speech
from num2words import num2words

# Disable debug messages from google.auth
logging.getLogger('google.auth').setLevel(logging.WARNING)

# Disable debug messages from google-api-core
logging.getLogger('google.api_core').setLevel(logging.WARNING)

# Disable debug messages from urllib3
logging.getLogger('urllib3').setLevel(logging.WARNING)

def upload_audio_to_gcs(local_file, gcs_bucket, gcs_filename):
    file_name = os.path.basename(local_file)
    print(f"Uploading {file_name} to GCS Bucket: {gcs_bucket}...")
    print()
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_filename)

    if blob.exists():
        print(f"File {gcs_filename} already exists. Skipping upload.")
    else:
        blob.upload_from_filename(local_file)
        print(f"File {gcs_filename} uploaded successfully.")

    return f"gs://{gcs_bucket}/{gcs_filename}"

def transcribe_audio(gcs_uri, convert_numeric_to_text = True, sample_rate = None):
    print(f"Transcribing with punctuation...")
    print()
    client = speech.SpeechClient()

    # Configure the audio settings
    audio = speech.RecognitionAudio(uri = gcs_uri)
    config = speech.RecognitionConfig(
        encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = sample_rate,
        language_code = "en-US",
        enable_automatic_punctuation = True,
        enable_word_time_offsets = True, # Enable word-level time offsets
        diarization_config = speech.SpeakerDiarizationConfig(
            enable_speaker_diarization = False # Set to True to enable speaker diarization
        ),
    )

    # Perform the asynchronous transcription
    operation = client.long_running_recognize(config = config, audio = audio)
    response = operation.result()

    # Extract the transcriptions and convert numeric values to text if enabled
    transcriptions = []
    for result in response.results:
        alternative = result.alternatives[0]
        words = []
        for word_info in alternative.words:
            word = word_info.word
            if convert_numeric_to_text and word.isdigit():
                # Convert numeric value to text
                if int(word) < 10:
                    word = num2words(int(word))
                else:
                    word = num2words(int(word), lang = 'en')
            words.append(word)
        transcriptions.append(" ".join(words))

    return " ".join(transcriptions)

def save_transcription(transcription, text_filename):
    with open(text_filename, "w") as f:
        f.write(transcription)

def list_audio_files(directory):
    audio_files = []
    for file in os.listdir(directory):
        if file.endswith(".wav"):
            audio_files.append(file)
    return audio_files

def select_files(audio_files):
    selected_files = []
    print("Available audio files:")
    for i, file in enumerate(audio_files):
        print(f"{i + 1}. {file}")
    while True:
        print()
        selection = input("Select the files to upload (separated by commas): ")
        try:
            selected_indexes = [int(index.strip()) - 1 for index in selection.split(",")]
            selected_files = [audio_files[index] for index in selected_indexes]
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")
    return selected_files

def measure_sample_rate(local_file):
    with sf.SoundFile(local_file, "r") as sound_file:
        sample_rate = sound_file.samplerate
    return sample_rate

def main():
    directory = "/Users/Jesse/Desktop/Speech_Recognition_Exercise/Recordings" # /path/to/audio/files
    gcs_bucket = "sample-voice-recordings" # your-gcs-bucket
    gcs_folder = "audio_files" # your-gcs-bucket-folder
    text_folder = "/Users/Jesse/Desktop/Speech_Recognition_Exercise/Transcriptions/WithPunctuation" # /path/to/transcriptions

    audio_files = list_audio_files(directory)
    selected_files = select_files(audio_files)

    for audio_file in selected_files:
        local_file = os.path.join(directory, audio_file)
        gcs_filename = os.path.join(gcs_folder, audio_file)
        gcs_uri = upload_audio_to_gcs(local_file, gcs_bucket, gcs_filename)
        sample_rate = measure_sample_rate(local_file)
        transcription = transcribe_audio(gcs_uri, convert_numeric_to_text = True, sample_rate = sample_rate) # Set the flag to True or False for numeric conversion to text
        text_filename = os.path.join(text_folder, audio_file.replace(".wav", ".txt"))
        save_transcription(transcription, text_filename)
        print(f"Transcription saved for {audio_file}")
        print("Transcription:")
        print(transcription)

if __name__ == "__main__":
    main()


# The code above transcribes audio files with punctuation using the __Google Cloud Speech-to-Text API__. It includes functions for uploading audio files to Google Cloud Storage, performing transcription, and saving transcriptions to text files. Note that the code requires appropriate credentials and access to Google Cloud services.
# 
# Here's a more detailed breakdown of what the code does:
# 
# 1. It imports the necessary modules and sets the log levels to enable/disable debug messages.
# 2. The __upload_audio_to_gcs__ function takes a local audio file, Google Cloud Storage bucket, and filename as input. It uploads the audio file to the specified bucket in Google Cloud Storage (GCS). Saving the data in the GCS bucket is needed to utilize the API. 
# 3. The __transcribe_audio__ function takes a GCS URI (i.e., Uniform Resource Identifier), a flag for converting numeric values to text, and a sample rate as input. It uses the Speech-to-Text API to perform asynchronous audio transcription and returns the transcriptions as a string.
# 4. The __save_transcription__ function takes a transcription string and a text filename as input. It saves the transcription to a text file.
# 5. The __list_audio_files__ function takes a directory path as input and returns a list of audio files in that directory.
# 6. The __select_files__ function takes a list of audio files as input and prompts the user to select the files they want to transcribe.
# 7. The __measure_sample_rate__ function determines the sample rate of an audio file by accessing its samplerate attribute. It returns the sample rate value in hertz.
# 8. The __main__ function is the main entry point of the script. It defines the directory where the audio files are located, the GCS bucket and folder names, and the directory where the transcriptions will be saved. It lists the audio files, prompts the user to select the files they want to transcribe, and then iterates over the selected files. For each file, it uploads the audio to GCS, transcribes the audio, saves the transcription to a text file, and prints the transcription.
# 9. Finally, the script calls the __main__ function if it is executed directly.
# 
# 

# ## Diarization
# 
# Diarization is a process in automatic speech recognition (ASR) and audio processing that involves segmenting an audio recording into distinct sections corresponding to different speakers. The goal of diarization is to determine "who spoke when" in a given audio recording. Diarization techniques analyze the audio signal to identify speaker turns, which are portions of the audio where a single speaker is actively speaking. The process typically involves several steps, including speaker segmentation, speaker clustering, and speaker labeling.
# 
# The __Google Cloud Speech-to-Text API__ provides support for diarization and can be enabled by configuring the __diarization_config__ parameter in the __RecognitionConfig__ object when making a transcription request. Here are the key aspects of how the Google API handles diarization:
# 
# 1. __Speaker diarization__: The API can automatically detect and label different speakers in the audio based on their voice characteristics. This allows the API to provide separate transcriptions for each speaker.
# 2. __Speaker count__: You can specify the expected number of speakers in the audio using the min_speaker_count and max_speaker_count parameters in the diarization_config. By setting these values, you provide a hint to the API about the expected number of speakers. If the number of speakers is unknown or variable, you can set min_speaker_count to 1 and omit max_speaker_count.
# 3. __Speaker labels__: When diarization is enabled, the API provides additional information in the transcription response, including the start and end times for each spoken word and the corresponding speaker label. The speaker label allows you to associate each word with the specific speaker who spoke it.
# 
# By leveraging diarization, we can obtain transcriptions that are segmented by speaker, which can be useful in scenarios such as conference calls, interviews, or multi-speaker recordings. To add speaker labels to the transcription of the audio files, we can modify the __transcribe_audio__ function and update the transcription extraction process like so:

# In[93]:


import os
#import logging
import soundfile as sf
from google.cloud import storage
from google.cloud import speech
from num2words import num2words

# Disable debug messages from google.auth
logging.getLogger('google.auth').setLevel(logging.WARNING)

# Disable debug messages from google-api-core
logging.getLogger('google.api_core').setLevel(logging.WARNING)

# Disable debug messages from urllib3
logging.getLogger('urllib3').setLevel(logging.WARNING)

def upload_audio_to_gcs(local_file, gcs_bucket, gcs_filename):
    file_name = os.path.basename(local_file)
    print(f"Uploading {file_name} to GCS Bucket: {gcs_bucket}...")
    print()
    client = storage.Client()
    bucket = client.bucket(gcs_bucket)
    blob = bucket.blob(gcs_filename)

    if blob.exists():
        print(f"File {gcs_filename} already exists. Skipping upload.")
    else:
        blob.upload_from_filename(local_file)
        print(f"File {gcs_filename} uploaded successfully.")

    return f"gs://{gcs_bucket}/{gcs_filename}"

def transcribe_audio(gcs_uri, convert_numeric_to_text = True, sample_rate = None,
                     enable_diarization = False, min_num_speaker = None, max_num_speaker = None): # as default, diarization won't be enabled
                
    print(f"Transcribing with punctuation and diarization...")
    print()
    client = speech.SpeechClient()

    # Configure the audio settings
    audio = speech.RecognitionAudio(uri = gcs_uri)
    config = speech.RecognitionConfig(
        encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz = sample_rate,
        language_code = "en-US",
        enable_automatic_punctuation = True,
        enable_word_time_offsets = True, 
        diarization_config = speech.SpeakerDiarizationConfig(
            enable_speaker_diarization = enable_diarization,
            min_speaker_count = min_num_speaker,
            max_speaker_count = max_num_speaker,
        ),
    )

    # Perform the asynchronous transcription
    operation = client.long_running_recognize(config = config, audio = audio)
    response = operation.result()

    # Extract the transcriptions with speaker labels
    transcriptions = []
    for result in response.results:
        alternative = result.alternatives[0]
        words = []
        for word_info in alternative.words:
            word = word_info.word
            if convert_numeric_to_text and word.isdigit():
                # Convert numeric value to text
                if int(word) < 10:
                    word = num2words(int(word))
                else:
                    word = num2words(int(word), lang = 'en')
            words.append(word)
        speaker_label = result.alternatives[0].words[0].speaker_tag
        transcriptions.append({"transcript": " ".join(words), "speaker_label": speaker_label})

    return transcriptions

def save_transcription(transcriptions, text_filename):
    with open(text_filename, "w") as f:
        for transcription in transcriptions:
            f.write(f"Speaker {transcription['speaker_label']}: {transcription['transcript']}\n")

def list_audio_files(directory):
    audio_files = []
    for file in os.listdir(directory):
        if file.endswith(".wav"):
            audio_files.append(file)
    return audio_files

def select_files(audio_files):
    selected_files = []
    print("Available audio files:")
    for i, file in enumerate(audio_files):
        print(f"{i + 1}. {file}")
    while True:
        print()
        selection = input("Select the files to upload (separated by commas): ")
        try:
            selected_indexes = [int(index.strip()) - 1 for index in selection.split(",")]
            selected_files = [audio_files[index] for index in selected_indexes]
            break
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")
    return selected_files

def measure_sample_rate(local_file):
    with sf.SoundFile(local_file, "r") as sound_file:
        sample_rate = sound_file.samplerate
    return sample_rate

def main():
    directory = "/Users/Jesse/Desktop/Speech_Recognition_Exercise/Recordings"  
    gcs_bucket = "sample-voice-recordings"  
    gcs_folder = "audio_files"  
    text_folder = "/Users/Jesse/Desktop/Speech_Recognition_Exercise/Transcriptions/WithDiarization"  

    audio_files = list_audio_files(directory)
    selected_files = select_files(audio_files)

    for audio_file in selected_files:
        local_file = os.path.join(directory, audio_file)
        gcs_filename = os.path.join(gcs_folder, audio_file)
        gcs_uri = upload_audio_to_gcs(local_file, gcs_bucket, gcs_filename)
        sample_rate = measure_sample_rate(local_file)
        transcriptions = transcribe_audio(gcs_uri, convert_numeric_to_text = True, sample_rate = sample_rate,
                                          enable_diarization = True, min_num_speaker = 1, max_num_speaker = 2) # Set to True to enable speaker diarization & specify speaker count 
        text_filename = os.path.join(text_folder, audio_file.replace(".wav", ".txt"))
        save_transcription(transcriptions, text_filename)
        print(f"Transcription saved for {audio_file}")
        print("Transcription:")
        for transcription in transcriptions:
            print(f"Speaker {transcription['speaker_label']}: {transcription['transcript']}")

if __name__ == "__main__":
    main()


# In the updated code:
# 
# - The __transcribe_audio__ function now returns a list of dictionaries, where each dictionary contains the transcript and corresponding speaker label.
# - The __save_transcription__ function has been modified to handle the list of transcriptions and save them with speaker labels in the text file.
# - The __main__ function has been updated to print each transcription with its corresponding speaker label.
# 
# Note, however, that although lines are separated by speaker, the dialogue is the same for both Speaker 0 and Speaker 1. Why is the model inaccurate?
# 
# __Google Cloud Speech-to-Text API__ offers built-in speaker diarization functionality. This means that we can perform speaker diarization without having to train a model ourselves. The API leverages pre-trained models and algorithms to automatically identify and differentiate speakers in the audio.
# 
# By enabling the speaker diarization flag (__enable_speaker_diarization__ = True) in the __transcribe_audio__ function and setting the appropriate values for __min_num_speaker__ and __max_num_speaker__, we can utilize the pre-trained speaker diarization capabilities of the API. However, it is important to note that while pre-trained models can be effective in many cases, the accuracy of diarization can vary depending on factors such as audio quality, speaker characteristics, background noise, etc.

# ## Model Optimization
# 
# Google offers ways to optimize the Speech-to-Text API using advanced techniques such as speaker diarization neural networks and speaker adaptation. These techniques can help improve the accuracy and efficiency of the transcription process. A few of the optimization options provided by Google are:
# 
# 1. __Speaker Diarization Neural Networks__: Google Cloud Speech-to-Text offers speaker diarization capabilities based on neural networks. Speaker diarization neural networks can automatically distinguish and identify individual speakers in an audio recording. This allows you to obtain more accurate speaker labels and transcriptions. By leveraging neural networks, the diarization process can be optimized to handle a wide range of audio conditions and speaker variations.
# 2. __Speaker Adaptation__: Google Cloud Speech-to-Text also provides speaker adaptation techniques. Speaker adaptation allows you to fine-tune the speech recognition models to better recognize the speech patterns and characteristics of specific speakers. By providing additional training data from specific speakers, you can enhance the accuracy and performance of the transcription for those individuals.
# 
# These optimization techniques require additional setup and configuration, and they may have associated costs and limitations. You can refer to the Google Cloud Speech-to-Text documentation for more information on how to implement these optimization methods by going to https://cloud.google.com/speech-to-text/docs. 

# ## Data Analysis with Spark

# Spark is a powerful distributed computing framework that can be used for large-scale data processing and analysis, including speech recognition tasks. By leveraging the distributed computing capabilities of Spark, we can efficiently process and analyze large volumes of audio data for speech recognition purposes. Here's an outline of how Spark can be utilized for speech recognition analysis:
# 
# 1. __Data Ingestion__: Load the audio data into Spark by reading audio files from storage systems like Hadoop Distributed File System (HDFS), Amazon S3, or Google Cloud Storage. Spark provides APIs to read and process various file formats, including audio files.
# 2. __Data Preprocessing__: Perform necessary preprocessing steps on the audio data, such as resampling, normalization, noise removal, or other transformations. Spark's distributed processing capabilities allow you to parallelize these preprocessing tasks across a cluster of machines.
# 3. __Feature Extraction__: Extract relevant features from the audio data, such as mel-frequency cepstral coefficients (MFCCs), spectrograms, or other acoustic features. These features serve as inputs to the speech recognition algorithms. Spark can distribute the feature extraction process across the cluster to accelerate the computation.
# 4. __Speech Recognition__: Apply speech recognition algorithms to convert the audio data into text. This involves training acoustic models, language models, and using decoding techniques like Hidden Markov Models (HMMs), deep neural networks (DNNs), or sequence-to-sequence models. Spark's distributed processing capabilities can be leveraged to parallelize the recognition process and scale it across multiple nodes.
# 5. __Post-processing and Analysis__: Perform post-processing steps on the transcriptions generated by the speech recognition system. This can involve tasks like punctuation restoration, spell-checking, language model integration, or other analysis specific to your application. Spark enables distributed data manipulation and analysis, allowing you to efficiently process and analyze the transcriptions.
# 6. __Result Aggregation and Visualization__: Collect and aggregate the results of the speech recognition analysis. Spark can help consolidate the outputs from distributed computations and generate meaningful insights. You can leverage Spark's integration with data visualization libraries like Matplotlib or Plotly to visualize the analysis results.
# 
# By utilizing Spark's distributed computing capabilities, we can process large volumes of audio data in parallel, significantly reducing the overall processing time and enabling efficient speech recognition analysis at scale. In the example below, we will utilize Spark to count the number of unique words in each of our transcripts. Word counts plays a crucial role in assessing accuracy, optimizing our language models, evaluating transcriptions, and enabling further analysis and processing of speech recognition outputs, such as the number of unique words spoken durning a conversation and the total number of conversational turns.

# In[5]:


import os
import logging
import pandas as pd
from pyspark import SparkContext
import string

def count_word_occurrences(text_file):
    # Create a SparkContext
    sc = SparkContext(appName = "WordCount")

    # Read the text file and split it into words
    lines = sc.textFile(text_file)
    words = lines.flatMap(lambda line: line.split(" "))

    # Remove punctuations from the words
    translator = str.maketrans("", "", string.punctuation)
    words = words.map(lambda word: word.translate(translator))

    # Convert words to lowercase
    words = words.map(lambda word: word.lower())

    # Map each word to a tuple (word, 1) for counting
    word_counts = words.map(lambda word: (word, 1))

    # Count the occurrences of each word
    word_counts = word_counts.reduceByKey(lambda a, b: a + b)

    # Collect the results into a dictionary
    word_count_dict = word_counts.collectAsMap()

    # Stop the SparkContext
    sc.stop()

    return word_count_dict

# Specify the paths to the transcriptions folder and the output directory for CSV files
transcriptions_folder = "/Users/Jesse/Desktop/Speech_Recognition_Exercise/Transcriptions"
output_directory = "/Users/Jesse/Desktop/Speech_Recognition_Exercise/Transcriptions/WordCount"

# Create a DataFrame to store the word counts
columns = ["Word", "Count", "Transcription"]
df_list = []

# Process each transcription file and count word occurrences
for file_name in os.listdir(transcriptions_folder):
    if file_name.endswith(".txt"):
        file_path = os.path.join(transcriptions_folder, file_name)
        word_counts = count_word_occurrences(file_path)

        # Create a DataFrame for the current transcription
        transcription_df = pd.DataFrame(word_counts.items(), columns = ["Word", "Count"])
        transcription_df["Transcription"] = file_name

        # Append the transcription's word counts to the list
        df_list.append(transcription_df)

        # Save the word counts as a separate CSV file in the output directory for each transcription
        csv_file = file_name.replace(".txt", ".csv")
        csv_path = os.path.join(output_directory, csv_file)
        transcription_df.to_csv(csv_path, index = False)

# Concatenate all DataFrames in the list
df = pd.concat(df_list, ignore_index = True)

# Save the main DataFrame as a CSV file
df.to_csv(os.path.join(output_directory, "word_counts_all_transcripts.csv"), index = False)


# In[6]:


df.head(10)


# In[7]:


df.tail(10)


# The code above utilizes Spark to count word occurrences in multiple transcription files and saves the results as CSV files. It performs the following steps:
# 
# 1. Creates a SparkContext and reads the text file, splitting it into words.
# 2. Removes punctuation and converts words to lowercase.
# 3. Maps each word to a tuple (word, 1) for counting.
# 4. Reduces by key to count the occurrences of each word.
# 5. Collects the results into a dictionary, saves word count DataFrames as CSV files, and concatenates them into a single DataFrame   before saving it as "word_counts.csv".
# 
# As you can infer, having the transcription name include a timestamp can allow us to track changes in speech patterns over time. This can be incredibly useful for future analysis, specially if the data can be systematically collected, processed, and stored in a database, data warehouse, or data lake through a cloud computing service provider. 
# 
# Futhermore, as simple as the word count code may now be, we can update it to do much more, such as calculating the total number of conversational turns and the total number of words spoken during a conversation: 

# In[8]:


import os
import pandas as pd
from pyspark import SparkContext
import string

def count_word_occurrences(text_file):
    # Create a SparkContext
    sc = SparkContext(appName="WordCount")

    # Read the text file and split it into lines
    lines = sc.textFile(text_file)

    # Filter out lines starting with "Speaker"
    speaker_lines = lines.filter(lambda line: line.startswith("Speaker"))

    # Get the distinct speakers
    speakers = speaker_lines.map(lambda line: line.split(":")[0]).distinct()

    # Count the number of conversational turns
    conversational_turns = speakers.count()

    # Count the total number of different lines
    total_lines = lines.distinct().count()

    # Split the lines into words and remove punctuation
    words = lines.flatMap(lambda line: line.split())
    words = words.map(lambda word: word.translate(str.maketrans("", "", string.punctuation)))

    # Convert words to lowercase
    words = words.map(lambda word: word.lower())

    # Map each word to a tuple (word, speaker) for counting
    word_speaker_counts = words.map(lambda word: (word, 1))

    # Count the occurrences of each word by speaker
    word_speaker_counts = word_speaker_counts.reduceByKey(lambda a, b: a + b)

    # Count the total number of words spoken
    total_words_spoken = words.count()

    # Collect the results into dictionaries
    word_speaker_count_dict = word_speaker_counts.collectAsMap()

    # Stop the SparkContext
    sc.stop()

    return word_speaker_count_dict, conversational_turns, total_words_spoken, total_lines


# Specify the paths to the transcriptions folder and the output directory for CSV files
transcriptions_folder = "/Users/Jesse/Desktop/Speech_Recognition_Exercise/Transcriptions/WithDiarization"
output_directory = "/Users/Jesse/Desktop/Speech_Recognition_Exercise/Transcriptions/WordCount/ConversationalTurns"

# Create a DataFrame to store the word counts
columns = ["Transcription", "Word", "Count", "Total Conversational Turns", "Total Words Spoken", "Total Lines"]
df_list = []

# Process each transcription file and count word occurrences
for file_name in os.listdir(transcriptions_folder):
    if file_name.endswith(".txt"):
        file_path = os.path.join(transcriptions_folder, file_name)
        word_counts, conversational_turns, total_words_spoken, total_lines = count_word_occurrences(file_path)

        # Create a DataFrame for the current transcription
        transcription_df = pd.DataFrame(word_counts.items(), columns=["Word", "Count"])
        transcription_df["Transcription"] = file_name.replace(".txt", "")
        transcription_df["Total Conversational Turns"] = conversational_turns
        transcription_df["Total Words Spoken"] = total_words_spoken
        transcription_df["Total Lines"] = total_lines

        # Append the transcription's word counts to the list
        df_list.append(transcription_df)

        # Save the word counts as a separate CSV file in the output directory for each transcription
        csv_file = file_name.replace(".txt", ".csv")
        csv_path = os.path.join(output_directory, csv_file)
        transcription_df.to_csv(csv_path, index=False)

# Concatenate all DataFrames in the list
df = pd.concat(df_list, ignore_index=True)

# Save the main DataFrame as a CSV file
df.to_csv(os.path.join(output_directory, "word_counts_conversational_turns_all_transcripts.csv"), index = False)


# In[9]:


df.head()


# In[10]:


df.tail()


# We can update the code above even further to utilize the speaker labels and get some more fine-grind statistics for individual speakers. 

# In[13]:


import os
import pandas as pd
from pyspark import SparkContext
import string

def count_word_occurrences(text_file):
    # Create a SparkContext
    sc = SparkContext(appName = "WordCount")

    # Read the text file and split it into lines
    lines = sc.textFile(text_file)

    # Extract speaker lines and their corresponding text
    speaker_lines = lines.filter(lambda line: line.startswith("Speaker"))
    speakers = speaker_lines.map(lambda line: line.split(":")[0].split(" ")[1]).distinct().collect()

    # Initialize dictionaries to store speaker statistics
    speaker_word_counts = {}
    speaker_conversational_turns = {}
    speaker_total_lines = {}
    speaker_total_words = {}
    speaker_unique_words = {}

    for speaker in speakers:
        # Filter lines for the current speaker
        speaker_lines = lines.filter(lambda line: line.startswith(f"Speaker {speaker}:"))

        # Get the speaker's text
        speaker_text = speaker_lines.map(lambda line: line.split(":")[1].strip())

        # Count the number of conversational turns for the speaker
        conversational_turns = speaker_lines.count()
        speaker_conversational_turns[speaker] = conversational_turns

        # Count the total number of different lines for the speaker
        total_lines = speaker_lines.distinct().count()
        speaker_total_lines[speaker] = total_lines

        # Split the speaker text into words and remove punctuation
        words = speaker_text.flatMap(lambda line: line.split())
        words = words.map(lambda word: word.translate(str.maketrans("", "", string.punctuation)))

        # Convert words to lowercase
        words = words.map(lambda word: word.lower())

        # Count the occurrences of each word for the speaker
        word_counts = words.countByValue()
        speaker_word_counts[speaker] = word_counts

        # Calculate total words and unique words for the speaker
        total_words = words.count()
        unique_words = len(word_counts)
        speaker_total_words[speaker] = total_words
        speaker_unique_words[speaker] = unique_words

    # Stop the SparkContext
    sc.stop()

    return (
        speaker_word_counts,
        speaker_conversational_turns,
        speaker_total_lines,
        speaker_total_words,
        speaker_unique_words,
    )

# Specify the paths to the transcriptions folder and the output directory for CSV files
transcriptions_folder = "/Users/Jesse/Desktop/Speech_Recognition_Exercise/Transcriptions/WithDiarization"
output_directory = "/Users/Jesse/Desktop/Speech_Recognition_Exercise/Transcriptions/WordCount/SpeakerStatistics"

# Calculate speaker statistics and store in a list
statistics_list = []

for file_name in os.listdir(transcriptions_folder):
    if file_name.endswith(".txt"):
        file_path = os.path.join(transcriptions_folder, file_name)
        word_counts, conversational_turns, total_lines, total_words, unique_words = count_word_occurrences(file_path)

        # Store the speaker statistics
        speaker_stats = {}
        for speaker in word_counts:
            speaker_stats[speaker] = {
                "Total Words": total_words[speaker],
                "Unique Words": unique_words[speaker],
                "Conversational Turns": conversational_turns[speaker],
                "Total Lines": total_lines[speaker],
            }

        # Create a DataFrame for speaker statistics
        df_speaker_stats = pd.DataFrame.from_dict(speaker_stats, orient="index")

        # Add a speaker_label column
        df_speaker_stats["Speaker_Label"] = df_speaker_stats.index

        # Reorder the columns
        df_speaker_stats = df_speaker_stats[
            ["Speaker_Label", "Total Words", "Unique Words", "Conversational Turns", "Total Lines"]
        ]

        # Add the transcription column with the file name
        df_speaker_stats["Transcription"] = file_name

        # Append to the statistics list
        statistics_list.append(df_speaker_stats)

        # Save the speaker statistics as a CSV file for each transcription
        csv_file = file_name.replace(".txt", ".csv")
        csv_path = os.path.join(output_directory, csv_file)
        df_speaker_stats.to_csv(csv_path, index = False)

# Concatenate all DataFrames in the statistics list
df_merged = pd.concat(statistics_list, ignore_index = True)

# Save the merged DataFrame as a CSV file
merged_csv_path = os.path.join(output_directory, "speaker_statistics_all_transcripts.csv")
df_merged.to_csv(merged_csv_path, index = False)


# In[14]:


df_merged.head()


# Transcription for 'small_talk_everyday_english_mono.wav':
# 
# - __Speaker 0__: So what's new Mark, how is your new job going? To be honest, I can't complain. I really love the company that I am working for.
# - __Speaker 0__: My coworkers are all really friendly and helpful. They really help me feel welcome.
# - __Speaker 0__: It's a really energetic and fun atmosphere.
# - __Speaker 0__: My boss is hilarious, and he's really flexible. Really
# - __Speaker 0__: How so?
# - __Speaker 0__: He allows me to come in when I want and make my own hours.
# - __Speaker 0__: I can also leave early. If I start early, there is no real dress code either. I can wear jeans and a t-shirt if I want I can even wear shorts in the summer. Wow it sounds really cool. I can't stand wearing a suit every day which do you prefer working late or finishing early? I prefer finishing early. I really enjoyed the morning.
# - __Speaker 0__: I love getting up early and going for a run. There's nothing like watching the sunrise while drinking my morning coffee.
# - __Speaker 0__: Really. I am opposite. I love sleeping in.
# - __Speaker 0__: I am most Alert in the evenings. I'm a real night owl.
# - __Speaker 0__: Well, you know what, they say, the early bird catches the worm, you know, you could be right?
# - __Speaker 0__: Maybe I will try to go to bed a little earlier tonight.
# - __Speaker 1__: So what's new Mark, how is your new job going? To be honest, I can't complain. I really love the company that I am working for. My coworkers are all really friendly and helpful. They really help me feel welcome. It's a really energetic and fun atmosphere. My boss is hilarious, and he's really flexible. Really How so? He allows me to come in when I want and make my own hours. I can also leave early. If I start early, there is no real dress code either. I can wear jeans and a t-shirt if I want I can even wear shorts in the summer. Wow it sounds really cool. I can't stand wearing a suit every day which do you prefer working late or finishing early? I prefer finishing early. I really enjoyed the morning. I love getting up early and going for a run. There's nothing like watching the sunrise while drinking my morning coffee. Really. I am opposite. I love sleeping in. I am most Alert in the evenings. I'm a real night owl. Well, you know what, they say, the early bird catches the worm, you know, you could be right? Maybe I will try to go to bed a little earlier tonight.

# Recall that our current model innacurately tags speaker labels, as such the number of conversational turns is incorrect, as well as the number of unique and total words spoken by each individual. However, once our model is trained and optimized, the code above will allow us to retreive those speaker statistics accurately, enabling us to continue our speech recognition endevours, including the use of more advanced tools like NLP for speech-to-text data analysis.  

# In[ ]:




