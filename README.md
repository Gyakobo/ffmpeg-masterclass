# FFmpeg Masterclass - Complete Learning Guide

This is a comprehensive Python program designed to teach you FFmpeg through practical examples, covering both CLI usage and the Python ffmpeg-python library.

## Installation

### 1. Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Extract and add to PATH

### 2. Install Python Dependencies

```bash
pip install ffmpeg-python pillow numpy
```

## Quick Start

```python
from ffmpeg_masterclass import FFmpegMasterclass

# Initialize
mc = FFmpegMasterclass(output_dir="./my_output")

# Run demos with your video files
mc.demo_cli_basic_conversion('my_video.mp4')
mc.demo_ffmpeg_python_probe('my_video.mp4')
mc.demo_create_gif('my_video.mp4', start=10, duration=5)
```

## What You'll Learn

### Section 1: FFmpeg CLI via Subprocess
- **Demo 1-3**: Direct CLI command execution from Python
- Learn how to construct ffmpeg commands programmatically
- Understand input/output options, codecs, and bitrates

### Section 2: FFmpeg-Python Library
- **Demo 4-9**: Pythonic approach to ffmpeg
- Method chaining and filter application
- Probing media metadata
- Video concatenation and overlays

### Section 3: Advanced Operations
- **Demo 10-16**: Professional video processing techniques
- Frame extraction and video creation from images
- HLS streaming preparation
- Audio visualization
- Watermarking

## FFmpeg Core Concepts

### 1. Basic Command Structure
```bash
ffmpeg [global_options] [input_options] -i input_file [output_options] output_file
```

### 2. Common Codecs

**Video Codecs:**
- `libx264` - H.264 (most compatible)
- `libx265` - H.265/HEVC (better compression)
- `libvpx-vp9` - VP9 (WebM)
- `libaom-av1` - AV1 (future-proof)

**Audio Codecs:**
- `aac` - AAC (most compatible)
- `libmp3lame` - MP3
- `libopus` - Opus (high quality)
- `flac` - FLAC (lossless)

### 3. Quality Control

**CRF (Constant Rate Factor):**
- Range: 0-51 (lower = better quality)
- Recommended: 18-28
- Example: `-crf 23`

**Bitrate:**
- Video: `-b:v 2M` (2 Mbps)
- Audio: `-b:a 192k` (192 kbps)

**Presets (encoding speed):**
- `ultrafast`, `superfast`, `veryfast`, `faster`, `fast`
- `medium` (default)
- `slow`, `slower`, `veryslow`

## Essential FFmpeg Filters

### Video Filters

```bash
# Scaling
-vf "scale=1280:720"              # Fixed size
-vf "scale=1280:-1"               # Auto height
-vf "scale=-1:720"                # Auto width
-vf "scale=iw/2:ih/2"             # Half size

# Cropping
-vf "crop=w:h:x:y"                # Custom crop
-vf "crop=1280:720:0:0"           # From top-left

# Rotation
-vf "rotate=90*PI/180"            # Rotate 90°
-vf "transpose=1"                 # Rotate 90° clockwise
-vf "transpose=2"                 # Rotate 90° counter-clockwise
-vf "hflip"                       # Horizontal flip
-vf "vflip"                       # Vertical flip

# Color Adjustment
-vf "eq=contrast=1.5:brightness=0.1"
-vf "hue=h=30:s=1.5"
-vf "colorbalance=rs=0.5:gs=0.2:bs=-0.3"

# Blur & Sharpen
-vf "boxblur=5:1"                 # Blur
-vf "unsharp=5:5:1.0:5:5:0.0"     # Sharpen

# Stabilization
-vf "deshake"
-vf "vidstabdetect"               # Step 1 of 2-pass stabilization
-vf "vidstabtransform"            # Step 2 of 2-pass stabilization

# Fade Effects
-vf "fade=in:0:30"                # Fade in, 30 frames
-vf "fade=out:150:30"             # Fade out at frame 150

# Text Overlay
-vf "drawtext=text='Hello':fontsize=24:fontcolor=white:x=10:y=10"
-vf "drawtext=textfile=subs.txt:fontsize=24:fontcolor=white"

# Framerate
-vf "fps=30"                      # Set to 30 fps
-vf "fps=fps=24000/1001"          # NTSC framerate
```

### Audio Filters

```bash
# Volume
-af "volume=2.0"                  # Double volume
-af "volume=0.5"                  # Half volume
-af "volume=10dB"                 # Increase by 10dB

# Normalization
-af "loudnorm"                    # EBU R128 normalization
-af "dynaudnorm"                  # Dynamic audio normalization

# Fade
-af "afade=in:st=0:d=2"          # Fade in, 2 seconds
-af "afade=out:st=10:d=3"        # Fade out at 10s, 3 sec duration

# Equalization
-af "equalizer=f=1000:width_type=h:width=200:g=10"

# Tempo (without pitch change)
-af "atempo=1.5"                  # 1.5x speed
-af "atempo=0.75"                 # 0.75x speed

# Remove silence
-af "silenceremove=start_periods=1:stop_periods=1:detection=peak"
```

### Complex Filter Chains

```bash
# Combine multiple filters
-vf "scale=1280:720,eq=contrast=1.2,unsharp=5:5:1.0"

# Multiple inputs/outputs
-filter_complex "[0:v]scale=1280:720[v1];[1:v]scale=640:480[v2];[v1][v2]hstack"

# Picture-in-picture
-filter_complex "[1:v]scale=iw/4:ih/4[pip];[0:v][pip]overlay=W-w-10:H-h-10"

# Side-by-side comparison
-filter_complex "[0:v][1:v]hstack"

# Grid layout (2x2)
-filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0"
```

## Common Use Cases

### 1. Convert Video Format
```python
# Using ffmpeg-python
import ffmpeg
ffmpeg.input('input.avi').output('output.mp4').run()
```

```bash
# Using CLI
ffmpeg -i input.avi output.mp4
```

### 2. Compress Video
```python
# High compression
ffmpeg.input('large.mp4').output(
    'compressed.mp4',
    vcodec='libx264',
    crf=28,
    preset='slow'
).run()
```

### 3. Extract Segment
```python
# From 30s to 45s (15s duration)
ffmpeg.input('input.mp4', ss=30, t=15).output(
    'segment.mp4',
    codec='copy'  # No re-encoding
).run()
```

### 4. Create Thumbnail
```python
# Extract frame at 10 seconds
ffmpeg.input('video.mp4', ss=10).output(
    'thumb.jpg',
    vframes=1
).run()
```

### 5. Add Subtitles
```bash
ffmpeg -i video.mp4 -vf "subtitles=subs.srt" output.mp4
```

### 6. Merge Video and Audio
```python
video = ffmpeg.input('video_only.mp4')
audio = ffmpeg.input('audio_only.mp3')
ffmpeg.output(video.video, audio.audio, 'merged.mp4').run()
```

### 7. Screen Recording to GIF
```python
ffmpeg.input('recording.mp4').filter('fps', fps=10).filter(
    'scale', 720, -1
).output('demo.gif').run()
```

### 8. Batch Convert
```python
from pathlib import Path
import ffmpeg

for video in Path('.').glob('*.avi'):
    output = video.with_suffix('.mp4')
    ffmpeg.input(str(video)).output(
        str(output),
        vcodec='libx264',
        crf=23
    ).run()
```

## Performance Tips

### 1. Use Stream Copy When Possible
```bash
# No re-encoding (fastest)
ffmpeg -i input.mp4 -ss 10 -t 30 -c copy output.mp4
```

### 2. Hardware Acceleration

**NVIDIA GPU:**
```bash
ffmpeg -hwaccel cuda -i input.mp4 -c:v h264_nvenc output.mp4
```

**Intel Quick Sync:**
```bash
ffmpeg -hwaccel qsv -i input.mp4 -c:v h264_qsv output.mp4
```

**Apple VideoToolbox:**
```bash
ffmpeg -i input.mp4 -c:v h264_videotoolbox output.mp4
```

### 3. Multi-threading
```bash
ffmpeg -i input.mp4 -threads 8 output.mp4
```

### 4. Two-pass Encoding (better quality)
```bash
# Pass 1
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 1 -f null /dev/null

# Pass 2
ffmpeg -i input.mp4 -c:v libx264 -b:v 2M -pass 2 output.mp4
```

## Troubleshooting

### Check Supported Formats
```bash
ffmpeg -formats          # List formats
ffmpeg -codecs          # List codecs
ffmpeg -encoders        # List encoders
ffmpeg -decoders        # List decoders
ffmpeg -filters         # List filters
```

### Debug Information
```bash
ffmpeg -i input.mp4     # Show file info without converting
ffprobe input.mp4       # Detailed media information
```

### Common Errors

**"Unknown encoder"**
- Your ffmpeg build doesn't include that encoder
- Install a full build or use alternative codec

**"Invalid data found"**
- File is corrupted
- Use `-err_detect ignore_err` to try anyway

**"Cannot find a matching stream"**
- Specify stream mapping: `-map 0:v -map 0:a`

## Additional Resources

### Official Documentation
- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [FFmpeg Wiki](https://trac.ffmpeg.org/wiki)
- [FFmpeg-python Documentation](https://github.com/kkroening/ffmpeg-python)

### Learning Materials
- [FFmpeg Filters Documentation](https://ffmpeg.org/ffmpeg-filters.html)
- [FFmpeg Cookbook](https://github.com/leandromoreira/ffmpeg-libav-tutorial)

### Community
- [FFmpeg Users Mailing List](https://ffmpeg.org/contact.html#MailingLists)
- [Stack Overflow - FFmpeg](https://stackoverflow.com/questions/tagged/ffmpeg)

## License

This educational material is provided as-is for learning purposes. FFmpeg itself is licensed under LGPL/GPL.

## Contributing

Feel free to add more examples and demos! The goal is to create the most comprehensive FFmpeg learning resource.