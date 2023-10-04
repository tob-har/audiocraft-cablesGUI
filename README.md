THIS IS A CUSTOMIZED VERSION OF facebookresearch/audiocraft.<br>
It features a GUI created with [cables.gl](https://cables.gl).<br>

Tested and runs locally on ARM Mac (M1) using CPU for generation.<br>

## INSTALLATION

1. Clone this repository.
2. Follow the AudioCraft installation steps as described below.
3. Rename the root folder to "audiocraft-main-cablesUI"
4. Open terminal and:

```shell
cd audiocraft-main-cablesUI # make sure to have the correct and full path, e.g. /Users/peter.parker/Documents/audiocraft-main-cablesUI
./audiocables_start.sh # this starts up the necessary servers.

```

4.b. If an permission error occurs, change the permissions first, then proceed:
```shell

cd audiocraft-main-cablesUI
chmod +x audiocables_start.sh
chmod +x audiocables_kill.sh
```



5. When the terminal showed, that the flask server is running and finally the http.server is serving at localhost:8000, open then WebUI by opening localhost:8000 in a browser window.

## USAGE

1. In the Sidebar, select a model. If you select/use it the first time, it will be downloaded from hugginface. On Mac, the models will be stored under "/Users/peter.parker/.cache/huggingface/hub/" by default.
2. Type a prompt and set the values, hit generate. In the terminal, the counter should appear after a while to log the process. The generated files will be available in the newly created folder "output_cables".
3. Play back the last generated file, or all filles in the "output_cables" folder.
4. Done.

For infos about the values, see the MusicGen documentation.

## DISCALIMER

This project is shared as is. It is a highly customized version and way to use AudioCraft, and it was used to learn core concepts while creating it. 
I am happy for feedback, but for the reason given above, support will be very limited.

## ABOUT

Everyhthing is kept in it's original state so far... what I added:<br>
Audio generation is done by the generateaudio.py script.<br>
The GUI is created inside cables_audiocraftAPI4, and served via the python http.server.<br>
serverCables.py handles serving the necessay scripts and files, so the GUI can communicate via AJAX requests.<br>
audiocables_start.sh and audiocables_kills.sh only handly starting/killing the processes.<br>



---


# AudioCraft
![docs badge](https://github.com/facebookresearch/audiocraft/workflows/audiocraft_docs/badge.svg)
![linter badge](https://github.com/facebookresearch/audiocraft/workflows/audiocraft_linter/badge.svg)
![tests badge](https://github.com/facebookresearch/audiocraft/workflows/audiocraft_tests/badge.svg)

AudioCraft is a PyTorch library for deep learning research on audio generation. AudioCraft contains inference and training code
for two state-of-the-art AI generative models producing high-quality audio: AudioGen and MusicGen.


## Installation
AudioCraft requires Python 3.9, PyTorch 2.0.0. To install AudioCraft, you can run the following:

```shell
# Best to make sure you have torch installed first, in particular before installing xformers.
# Don't run this if you already have PyTorch installed.
pip install 'torch>=2.0'
# Then proceed to one of the following
pip install -U audiocraft  # stable release
pip install -U git+https://git@github.com/facebookresearch/audiocraft#egg=audiocraft  # bleeding edge
pip install -e .  # or if you cloned the repo locally (mandatory if you want to train).
```

We also recommend having `ffmpeg` installed, either through your system or Anaconda:
```bash
sudo apt-get install ffmpeg
# Or if you are using Anaconda or Miniconda
conda install 'ffmpeg<5' -c  conda-forge
```

## Models

At the moment, AudioCraft contains the training code and inference code for:
* [MusicGen](./docs/MUSICGEN.md): A state-of-the-art controllable text-to-music model.
* [AudioGen](./docs/AUDIOGEN.md): A state-of-the-art text-to-sound model.
* [EnCodec](./docs/ENCODEC.md): A state-of-the-art high fidelity neural audio codec.
* [Multi Band Diffusion](./docs/MBD.md): An EnCodec compatible decoder using diffusion.

## Training code

AudioCraft contains PyTorch components for deep learning research in audio and training pipelines for the developed models.
For a general introduction of AudioCraft design principles and instructions to develop your own training pipeline, refer to
the [AudioCraft training documentation](./docs/TRAINING.md).

For reproducing existing work and using the developed training pipelines, refer to the instructions for each specific model
that provides pointers to configuration, example grids and model/task-specific information and FAQ.


## API documentation

We provide some [API documentation](https://facebookresearch.github.io/audiocraft/api_docs/audiocraft/index.html) for AudioCraft.


## FAQ

#### Is the training code available?

Yes! We provide the training code for [EnCodec](./docs/ENCODEC.md), [MusicGen](./docs/MUSICGEN.md) and [Multi Band Diffusion](./docs/MBD.md).

#### Where are the models stored?

Hugging Face stored the model in a specific location, which can be overriden by setting the `AUDIOCRAFT_CACHE_DIR` environment variable.


## License
* The code in this repository is released under the MIT license as found in the [LICENSE file](LICENSE).
* The models weights in this repository are released under the CC-BY-NC 4.0 license as found in the [LICENSE_weights file](LICENSE_weights).


## Citation

For the general framework of AudioCraft, please cite the following.
```
@article{copet2023simple,
    title={Simple and Controllable Music Generation},
    author={Jade Copet and Felix Kreuk and Itai Gat and Tal Remez and David Kant and Gabriel Synnaeve and Yossi Adi and Alexandre Défossez},
    year={2023},
    journal={arXiv preprint arXiv:2306.05284},
}
```

When referring to a specific model, please cite as mentioned in the model specific README, e.g
[./docs/MUSICGEN.md](./docs/MUSICGEN.md), [./docs/AUDIOGEN.md](./docs/AUDIOGEN.md), etc.
