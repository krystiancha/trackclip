# trackclip
Annotate videos by adding an automatically moving frame with a label.

![trackclip](docs/demo.gif)

## Requirements
```text
numpy
opencv-contrib-python
```

## Getting Trackclip

```bash
git clone https://github.com/protecto/trackclip.git
cd trackclip
python -m trackclip --help
```

## Usage
```text
usage: python -m trackclip [-h] [-l LABEL] [-c CODEC] [-o OUTPUT] [-p] input

Annotate videos by adding an automatically moving frame with a label. Hotkeys:
ESC -- close and save; SPACE -- pause/unpause; LEFT ARROW -- preview at 2x
speed; RIGHT ARROW -- preview at x/2 speed;

positional arguments:
  input                 Input filename, can be a video device (ex.
                        /dev/video0)

optional arguments:
  -h, --help            show this help message and exit
  -l LABEL, --label LABEL
                        A label that will appear near the tracking box
  -c CODEC, --codec CODEC
                        Four-letter codec name
  -o OUTPUT, --output OUTPUT
                        The name of the output file
  -p, --pause           Don't start playing the video right ahead (press SPACE
                        to unpause)

```

