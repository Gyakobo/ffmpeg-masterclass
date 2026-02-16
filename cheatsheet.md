# FFmpeg Quick Reference Cheat Sheet

## Basic Syntax
```bash
ffmpeg [global_options] {[input_options] -i input_url} ... {[output_options] -i output_url} ...
``` 

## File Information
```bash
# Get detailed file info
ffmpeg -i video.mp4
ffprobe video.mp4
ffprobe -show_format -show_streams video.mp4

# JSON output
ffprobe -v quiet -print_format json -show_format -show_streams video.mp4
```

### Basic Conversions
```bash
ffmpeg -i input.avi output.mp4
ffmpeg -i input.mp4 output.webm
ffmpeg -i input.mov output.mkv
```

### Change Video Codec
```bash
# H.264
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4

# H.265 (better compression)
ffmpeg -i input.mp4 -c:v libx265 -crf 28 output.mp4

# VP9 (WebM)
ffmpeg -i input.mp4 -c:v libvpx-vp9 -b:v 2M ouput.webm
```

### Change Audio Codec
```bash
ffmpeg -i input.mp4 -c:v copy -c:a aac output.mp4
ffmpeg -i input.mp4 -c:v copy -c:a libmp3lame -q:a 2 output.mp4
```

### Extract Audio
```bash
ffmpeg -i video.mp4 -vn -c:a copy audio.m4a
ffmpeg -i video.mp4 -vn -c:a libmp3lame -q:a 0 audio.mp3
```

### Extract Video (no audio)
```bash
ffmpeg -i input.mp4 -an -c:v copy output.mp4
```

## Trimming & Cutting

### Cut Segment
```bash
# From 00:00:30 for 15 seconds
ffmpeg -i input.mp4 -ss 00:00:30 -t 15 -c copy output.mp4

# From 00:01:00 to 00:02:30
ffmpeg -i input.mp4 -ss 00:01:00 -to 00:02:30 -c copy output.mp4

# Fast seek (less accurate but faster)
ffmpeg -ss 00:00:30 -i input.mp4 -t 15 -c copy output.mp4
```

### Split into Segments
```bash
# Split into 10 seconds segments
ffmpeg -i input.mp4 -c copy -f segment -segment_time 10 output%03d.mp4
```

## Resizing & Scaling

### Resize to Specific Dimensions
```bash
#1920x1080
ffmpeg -i input.mp4 -vf scale=1920:1080 output.mp4

# Keep aspect ratio, set width ot 1280
ffmpeg -i input.mp4 -vf scale=1280:-1 output.mp4

#Keep aspect ratio, set height to 720
ffmpeg -i input.mp4 -vf scale=-1:720 output.mp4
```

### Resize by Percentage
```bash
# 50% size
ffmpeg -i input.mp4 -vf scale=iw/2:ih/2 output.mp4
```

### Common Resolutions
```bash
# 4k
ffmpeg -i input.mp4 -vf scale=3840:2160 output.mp4

# 1080p
ffmpeg -i input.mp4 -vf scale=1920:1080 output.mp4

# 720p
ffmpeg -i input.mp4 -vf scale=1280:720 output.mp4

# 480p
ffmpeg -i input.mp4 -vf scale=854:480 output.mp4
```

## Quality Control

### Constant Quality (CRF)
```bash
# 0 = lossless, 51 = worst quality
# 18 - 28 recommended range
ffmpeg -i input.mp4 -c:v libx264 -crf 23 output.mp4
```

### Bitrate
```bash
# Video bitrate
ffmpeg -i input.mp4 -b:v 2M output.mp4

# Audio bitrate
ffmpeg -i input.mp4 -b:a 192k output.mp4

# Both
ffmpeg -i input.mp4 -b:v 2M -b:a 192k output.mp4
```

### Preset (speed/quality tradeoff)
```bash
# Slower = better compression
ffmpeg -i input.mp4 -c:v libx264 -preset slow -crf 23 output.mp4

# Options: ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow
```

## Frame Rate

### Change Frame Rate
```bash 
# 30 fps
ffmpeg -i input.mp4 -r 30 output.mp4

# Using filter
ffmpeg -i input.mp4 -vf fps=30 output.mp4
```

### Extract Frames as Images
```bash
# All frame
ffmpeg -i input.mp4 frame%04d.png

# 1 frame per second
ffmpeg -i input.mp4 -vf fps=1 frame%04d.png

# Every 10th frame
ffmpeg -i input.mp4 -vf "select='not(mod(n,10))'" -vsync 0 frame%04d.png
```

### Create Video from Images
```bash
# From numbered sequence
ffmpeg -framerate 30 -i frame%04d.png -c:v libx264 output.mp4

# From glob pattern
ffmpeg -framerate 30 -pattern_type glob -i '*.png' output.mp4
``` 

## Rotation & Flipping

### Rotate
```bash
# 90° clockwise
ffmpeg -i input.mp4 -vf "tranpose=1" output.mp4

# 90° counter-clockwise
ffmpeg -i input.mp4 -vf "transpose=2" output.mp4

# 180° counter-clockwise
ffmpeg -i input.mp4 -vf "transpose=2,transpose=2" output.mp4
```

### Flip
```bash
# Horizontal flip
ffmpeg -i input.mp4 -vf hflip output.mp4

# Vertical flip
ffmpeg -i input.mp4 -vf vflip output.mp4
```

## Cropping

### Crop Syntax
```bash
# crop=width:height:x:y
ffmpeg -i input.mp4 -vf "crop=640:480:200:100" output.mp4

# Center crop to 16:9
ffmpeg -i input.mp4 -vf "crop=ih*16/9:ih" output.mp4

# Auto-detect crop area
ffmpeg -i input.mp4 -vf cropdetect -f null -
```

## Concatenation

### Method 1: Concat Demuxer (same codec)
```bash
# Create list file
echo "file 'video1.mp4'" > list.txt
echo "file 'video2.mp4'" >> list.txt
echo "file 'video3.mp4'" >> list.txt

# Concatenate
ffmpeg -f concat -safe 0 -i list.txt -c copy output.mp4
```

### Method 2: Concat Filter (different codecs)
```bash
ffmpeg -i video1.mp4 -i video2.mp4 -video3.mp4 \
  -filter_complex "[0:v][0:a][1:v][1:a][2:v][2:a]concat=n=3:v=1:a=1[v][a]" \
  -mpa "[v]" -map "[a]" output.mp4
```

## Overlays

### Picture-in-Picture
```bash
# Overlay in top-right corner
ffmpeg -i base.mp4 -i overlay.mp4 \
  -filter_complex "[1:v]scale=iw/4:ih/4[pip];[0:v][pip]overlay=W-w-10:10" \
  output.mp4
```

### Watermark
```bash
ffmpeg -i video.mp4 -i logo.png \
  -filter_complex "overlay=W-w-10:H-h-10" \ 
  output.mp4
```

### Side-by-Side
```bash
ffmpeg -i left.mp4 -i right.mp4 \
  -filter_complex "[0:v][1:v]hstack" \
  output.mp4
```

### Grid Layout (2x2)
```bash
ffmpeg -i v1.mp4 -i v2.mp4 -i v3.mp4 -i m4.mp4 \
  -filter_complex "[0:v][1:v][2:v][3:v]xstack=inputs=4:layout=0_0|w0_0|0_h0|w0_h0" \
  output.mp4 
```

## Text & Subtitles

### Add Text Overlay
```bash
# Simple text
ffmpeg -i input.mp4 -vf \
   "drawtext=text='Hello World':fontsize=24:fontcolor=white:x=10:y=10" \
   output.mp4

# Centered text
ffmpeg -i input.mp4 -vf \
   "drawtext=text='Hello':fontsize=48:fontcolor=white:x=(w-text_w)/2:y=(h-text_h)/2" \
   output.mp4

# With background box
ffmpeg -i input.mp4 -vf \
   "drawtext=text='Title':fontsize=48:fontcolor=white:box=1:boxcolor=black@0.5:x=10:y=10" \
   output.mp4
```

### Burn Subtitles
```bash
ffmpeg -i video.mp4 -vf "subtitles=sub.srt" output.mp4
```

## Audio

### Change Volume
```bash
# Double volume 
ffmpeg -i input.mp4 -af "volume=2.0" output.mp4

# Half volume
ffmpeg -i input.mp4 -af "volume=0.5" output.mp4

# Increase by 10dB
ffmpeg -i input.mp4 -af "volume=10dB" output.mp4
```

### Normalize Audio
```bash
ffmpeg -i input.mp4 -af loudnorm output.mp4
```

### Fade In/Out
```bash
# Audio fade in (first 3 seconds)
ffmpeg -i input.mp4 -af "afade=in:st=0:d=3" output.mp4

# Audio fade out (last 3 seconds)
ffmpeg -i input.mp4 -af "afade=out:st=27:d=3" output.mp4

# Video fade in
ffmpeg -i input.mp4 -vf "fade=in:0:30" output.mp4

# Video fade out
ffmpeg -i input.mp4 -vf "fade=out:150:30" output.mp4
```

### Mix Audio
```bash
# Add background music
ffmpeg -i video.mp4 -i music.mp3 \
   -filter_complex "[0:a][1:a]amix=inputs=2:duration=first" \
   -c:v copy output.mp4
```

## Speed & Slow Motion

### Video Speed
```bash
# 2x speed
ffmpeg -i input.mp4 -filter:v "setpts=0.5*PTS" output.mp4


# 0.5x speed (slow motion)
ffmpeg -i input.mp4 -filter:v "setpts=2.0*PTS" output.mp4
```

### Audio Speed (without pitch change)
```bash
# 2x speed
ffmpeg -i input.mp4 -filter:a "atempo=2.0" output.mp4

# 0.5x speed
ffmpeg -i input.mp4 -filter:a "atempo=0.5" output.mp4

# For speed > 2x, chain filters
ffmpeg -i input.mp4 -filter:a "atempo=2.0,atempo=2.0" output.mp4 # 4x
```

### Video + Audio Speed
```bash
ffmpeg -i input.mp4 \
   -filter_complex "[0:v]setpts=0.5*PTS[v];[0:a]atempo=2.0[a]" \
   -map "[v]" -map "[a]" output.mp4
```

## GIF Creation

### Basic GIF
```bash
ffmpeg -i input.mp4 -vf "fps=10,scale=320:-1" output.gif
```

### High Quality GIF
```bash
# Generate palette
ffmpeg -i input.mp4 -vf "fps=10,scale=480:-1:flag=lanczos,palettegen" palette.png

# Use palette
ffmpeg -i input.mp4 -i palette.png \
   -filter_complex "fps=10,scale=480:-1:flags=lanczos[x];[x][1:v]paletteuse" \
   output.gif
```

## Streaming

### HLS (HTTP Live Streaming)
```bash
ffmpeg -i input.mp4 \
   -codec: copy \
   -start_number 0 \
   -hls_time 10 \
   -hls_list_size 0 \
   -f hls \
   playlist.m3u8
```

### DASH
```bash
ffmpeg -i input.mp4 \
   -c copy \
   -f dash \
   -seg_duration 10 \
   manifest.mpd
```

