import torchaudio
import datetime
from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write
import logging
import os
import json

model = None
loaded_model_name = None


logging.basicConfig(level=logging.INFO) #WARNING, ERROR, and CRITICAL

#Choose Model
#model = MusicGen.get_pretrained('facebook/musicgen-melody')
#model = MusicGen.get_pretrained('facebook/musicgen-small')

model_name = 'facebook/musicgen-small'

def run(model_name='facebook/musicgen-small',descriptions=None, top_k=250, top_p=0, temperature=1, cfg_coef=6.0, duration=2):
    global model
    global loaded_model_name


    # Only load the model if the model_name has changed or if the model is not loaded yet
    if model is None or loaded_model_name != model_name:
        logging.info(f"Loading model {model_name}...")
        model = MusicGen.get_pretrained(model_name)
        loaded_model_name = model_name  # Update the currently loaded model's name
        logging.info("Model loaded successfully!")

    # Ensure necessary folders exist
    if not os.path.exists('output_cables'):
        os.makedirs('output_cables')

    if not os.path.exists('output_cables/json'):
        os.makedirs('output_cables/json')

    # set date_time for file name
    current_date_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    file_paths = []  # list to hold paths of generated audio files
    file_urls = []

    model.set_generation_params(
        top_k=top_k,
        top_p=top_p,
        temperature=temperature,
        cfg_coef=cfg_coef,
        duration=duration
    )

    # Log the parameters used for audio generation
    logging.info(f"Generating audio with parameters:")
    logging.info(f"Prompt: {descriptions}")
    logging.info(f"top_k: {top_k}")
    logging.info(f"top_p: {top_p}")
    logging.info(f"temperature: {temperature}")
    logging.info(f"cfg_coef: {cfg_coef}")
    logging.info(f"duration: {duration}")

    #wav = model.generate_unconditional(1, progress=True)    # generates n unconditional audio samples
    # seems to need to comment out Line 342 in musicgen.py...

    if descriptions is None:
        descriptions = ['Drum Beat']

    wav = model.generate(descriptions, progress=True)  # generates as many samples as in comma seperated descriptions

    #melody, sr = torchaudio.load('./assets/bach.mp3')
    # generates using the melody from the given audio and the provided descriptions.
    #wav = model.generate_with_chroma(descriptions, melody[None].expand(3, -1, -1), sr)

    format_type = "wav" #wav or mp3

    for idx, one_wav in enumerate(wav):
        file_name_without_dir = f'{current_date_time}_{idx}'
        file_path = os.path.join('output_cables', file_name_without_dir)  # Include directory in the path
        json_file_path = os.path.join('output_cables', 'json', file_name_without_dir + '.json')
        file_url = f"http://localhost:5001/{file_path}.{format_type}"  # Construct the URL

        audio_write( 
            file_path,
            one_wav.cpu(),
            format = format_type, 
            #mp3_rate = 192,
            sample_rate = model.sample_rate,
            normalize = True,
            strategy = "loudness", #clip, peak, rms, loudness
            loudness_headroom_db = 16,
            #peak_clip_headroom_db = 1.0,
            #rms_headroom_db = 18,
            loudness_compressor = True,
            log_clipping = True #only when strategy = loudness
            #make_parent_dir = True
            )

        file_urls.append(file_url)

        json_data = {
            "description": descriptions[idx] if idx < len(descriptions) else "N/A",
            "top_k": top_k,
            "top_p": top_p,
            "temperature": temperature,
            "cfg_coef": cfg_coef,
            "duration": duration,
            "model": model_name
        }
        
        with open(json_file_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

    return file_urls

# If you want to run this script independently as well, add this:
# it allows to rund runAudioGen() if one just calls 
if __name__ == "__main__":
    run()