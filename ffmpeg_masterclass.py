#!/usr/bin/env python3
"""
FFmpeg Masterclass - A comprehensive guide to using FFmpeg with Python

This program demonstrates:
1. Using ffmpeg via subprocess (CLI commands)
2. Using ffmpeg-python library (Pythonic wrapper)
3. Video/audio manipulation, conversion, filtering, streaming, and more

Requirements:
    pip install ffmpeg-python pillow numpy

    Also requires ffmpeg installed on your system:
    - Ubuntu/Debian: sudo apt install ffmpeg
    - macOS: brew install ffmpeg
    - Windows: Download from ffmpeg.org
"""

import subprocess
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import ffmpeg
except ImportError:
    print("Please install ffmpeg-python: pip install ffmpeg-python")
    sys.exit(1)


class FFmpegMasterclass:
    """
    Comprehensive FFmpeg learning tool demonstrating various operations
    """

    def __init__(self, output_dir: str = "./ffmpeg_output"):
        """Initialize with output directory for generated files"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        print(f"Output directory: {self.output_dir.absolute()}\n")

    # ============================================================================
    # SECTION 1: FFmpeg CLI via Subprocess
    # ============================================================================

    def demo_cli_basic_conversion(self, input_file: str):
        """
        Demo 1: Basic video conversion using subprocess
        Shows how to call ffmpeg CLI directly from Python
        """
        print("=" * 80)
        print("DEMO 1: Basic CLI Conversion (MP4 to WebM)")
        print("=" * 80)

        output_file = self.output_dir / "converted_basic.webm"

        # Build ffmpeg command as a list
        cmd = [
            "ffmpeg",
            "-i",
            input_file,  # Input file
            "-c:v",
            "libvpx-vp9",  # Video codec
            "-c:a",
            "libopus",  # Audio codec
            "-b:v",
            "1M",  # Video bitrate
            "-b:a",
            "128k",  # Audio bitrate
            "-y",  # Overwrite output
            str(output_file),
        ]

        print(f"Command: {' '.join(cmd)}\n")

        try:
            # Run with output capture
            result = subprocess.run(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
            )

            if result.returncode == 0:
                print(f"✓ Success! Output: {output_file}")
            else:
                print(f"✗ Error: {result.stderr}")

        except FileNotFoundError:
            print("✗ ffmpeg not found! Please install ffmpeg first.")
        except Exception as e:
            print(f"✗ Error: {e}")

        print()

    def demo_cli_with_filters(self, input_file: str):
        """
        Demo 2: Apply video filters using CLI
        Demonstrates complex filter chains
        """
        print("=" * 80)
        print("DEMO 2: CLI with Complex Filters")
        print("=" * 80)

        output_file = self.output_dir / "filtered_cli.mp4"

        # Complex filter: scale, add text overlay, adjust colors
        filter_complex = (
            "[0:v]scale=1280:720,"
            "drawtext=text='FFmpeg Demo':fontsize=48:fontcolor=white:"
            "x=(w-text_w)/2:y=50:box=1:boxcolor=black@0.5:boxborderw=5,"
            "eq=contrast=1.2:brightness=0.1[v]"
        )

        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-filter_complex",
            filter_complex,
            "-map",
            "[v]",  # Map filtered video
            "-map",
            "0:a?",  # Map audio if exists
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "23",
            "-c:a",
            "aac",
            "-y",
            str(output_file),
        ]

        print("Filter chain:")
        print("  1. Scale to 1280x720")
        print("  2. Add text overlay with box")
        print("  3. Adjust contrast and brightness")
        print(f"\nCommand: {' '.join(cmd)}\n")

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Success! Output: {output_file}\n")
        except subprocess.CalledProcessError as e:
            print(f"✗ Error: {e.stderr.decode()}\n")
        except FileNotFoundError:
            print("✗ ffmpeg not found!\n")

    def demo_cli_extract_audio(self, input_file: str):
        """
        Demo 3: Extract audio track from video
        """
        print("=" * 80)
        print("DEMO 3: Extract Audio Track")
        print("=" * 80)

        output_file = self.output_dir / "extracted_audio.mp3"

        cmd = [
            "ffmpeg",
            "-i",
            input_file,
            "-vn",  # No video
            "-acodec",
            "libmp3lame",
            "-q:a",
            "2",  # Quality (0-9, lower is better)
            "-y",
            str(output_file),
        ]

        print(f"Command: {' '.join(cmd)}\n")

        try:
            subprocess.run(cmd, check=True, capture_output=True)
            print(f"✓ Success! Output: {output_file}\n")
        except Exception as e:
            print(f"✗ Error: {e}\n")

    # ============================================================================
    # SECTION 2: FFmpeg-Python Library (Pythonic Approach)
    # ============================================================================

    def demo_ffmpeg_python_basic(self, input_file: str):
        """
        Demo 4: Basic conversion using ffmpeg-python library
        Shows the Pythonic way to use ffmpeg
        """
        print("=" * 80)
        print("DEMO 4: FFmpeg-Python Basic Conversion")
        print("=" * 80)

        output_file = self.output_dir / "converted_python.mp4"

        try:
            # Chain ffmpeg operations in a Pythonic way
            stream = (
                ffmpeg.input(input_file)
                .output(
                    str(output_file),
                    vcodec="libx264",
                    acodec="aac",
                    video_bitrate="2M",
                    audio_bitrate="192k",
                    preset="medium",
                )
                .overwrite_output()
            )

            # View the generated command
            print("Generated FFmpeg command:")
            print(" ".join(ffmpeg.compile(stream)))
            print()

            # Execute
            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"✓ Success! Output: {output_file}\n")

        except ffmpeg.Error as e:
            print(f"✗ FFmpeg error: {e.stderr.decode()}\n")

    def demo_ffmpeg_python_probe(self, input_file: str):
        """
        Demo 5: Probe video metadata
        Extract detailed information about media files
        """
        print("=" * 80)
        print("DEMO 5: Probe Video Metadata")
        print("=" * 80)

        try:
            probe = ffmpeg.probe(input_file)

            # Video stream info
            video_stream = next(
                (s for s in probe["streams"] if s["codec_type"] == "video"), None
            )

            # Audio stream info
            audio_stream = next(
                (s for s in probe["streams"] if s["codec_type"] == "audio"), None
            )

            print("File Information:")
            print(f"  Format: {probe['format']['format_long_name']}")
            print(f"  Duration: {float(probe['format']['duration']):.2f} seconds")
            print(f"  Size: {int(probe['format']['size']) / 1024 / 1024:.2f} MB")
            print(f"  Bitrate: {int(probe['format']['bit_rate']) / 1000:.0f} kbps")

            if video_stream:
                print("\nVideo Stream:")
                print(f"  Codec: {video_stream['codec_name']}")
                print(f"  Resolution: {video_stream['width']}x{video_stream['height']}")
                print(f"  FPS: {eval(video_stream.get('r_frame_rate', '0/1')):.2f}")
                print(f"  Pixel Format: {video_stream.get('pix_fmt', 'N/A')}")

            if audio_stream:
                print("\nAudio Stream:")
                print(f"  Codec: {audio_stream['codec_name']}")
                print(f"  Sample Rate: {audio_stream['sample_rate']} Hz")
                print(f"  Channels: {audio_stream['channels']}")
                print(
                    f"  Bitrate: {int(audio_stream.get('bit_rate', 0)) / 1000:.0f} kbps"
                )

            print()

        except ffmpeg.Error as e:
            print(f"✗ Error probing file: {e.stderr.decode()}\n")

    def demo_ffmpeg_python_filters(self, input_file: str):
        """
        Demo 6: Apply multiple filters using ffmpeg-python
        Shows filter chaining
        """
        print("=" * 80)
        print("DEMO 6: FFmpeg-Python Filter Chain")
        print("=" * 80)

        output_file = self.output_dir / "filtered_python.mp4"

        try:
            stream = (
                ffmpeg.input(input_file)
                .filter("scale", 1280, 720)  # Resize
                .filter("fps", fps=30)  # Set framerate
                .filter("eq", contrast=1.1, brightness=0.05)  # Color adjustment
                .filter("hue", h=10)  # Hue shift
                .output(str(output_file), vcodec="libx264", crf=23, acodec="aac")
                .overwrite_output()
            )

            print("Applied filters:")
            print("  1. Scale to 1280x720")
            print("  2. Set framerate to 30fps")
            print("  3. Adjust contrast and brightness")
            print("  4. Shift hue")
            print()

            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"✓ Success! Output: {output_file}\n")

        except ffmpeg.Error as e:
            print(f"✗ Error: {e.stderr.decode()}\n")

    def demo_ffmpeg_python_trim(
        self, input_file: str, start: float = 5, duration: float = 10
    ):
        """
        Demo 7: Trim video to specific duration
        """
        print("=" * 80)
        print("DEMO 7: Trim Video")
        print("=" * 80)

        output_file = self.output_dir / "trimmed.mp4"

        try:
            stream = (
                ffmpeg.input(
                    input_file, ss=start, t=duration
                )  # Start time and duration
                .output(
                    str(output_file),
                    vcodec="copy",  # Copy codec (no re-encoding)
                    acodec="copy",
                )
                .overwrite_output()
            )

            print(f"Trimming from {start}s for {duration}s duration")
            print("Using stream copy (no re-encoding)\n")

            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"✓ Success! Output: {output_file}\n")

        except ffmpeg.Error as e:
            print(f"✗ Error: {e.stderr.decode()}\n")

    def demo_ffmpeg_python_concat(self, input_files: List[str]):
        """
        Demo 8: Concatenate multiple videos
        """
        print("=" * 80)
        print("DEMO 8: Concatenate Videos")
        print("=" * 80)

        output_file = self.output_dir / "concatenated.mp4"

        try:
            # Create input streams
            inputs = [ffmpeg.input(f) for f in input_files]

            # Concatenate
            stream = (
                ffmpeg.concat(
                    *inputs, v=1, a=1
                )  # v=1: 1 video stream, a=1: 1 audio stream
                .output(str(output_file), vcodec="libx264", acodec="aac")
                .overwrite_output()
            )

            print(f"Concatenating {len(input_files)} videos\n")

            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"✓ Success! Output: {output_file}\n")

        except ffmpeg.Error as e:
            print(f"✗ Error: {e.stderr.decode()}\n")

    def demo_ffmpeg_python_overlay(self, base_video: str, overlay_video: str):
        """
        Demo 9: Overlay one video on top of another (Picture-in-Picture)
        """
        print("=" * 80)
        print("DEMO 9: Video Overlay (Picture-in-Picture)")
        print("=" * 80)

        output_file = self.output_dir / "overlay.mp4"

        try:
            base = ffmpeg.input(base_video)
            overlay = ffmpeg.input(overlay_video)

            # Scale overlay to 25% size and position in bottom-right corner
            stream = (
                ffmpeg.filter(
                    [base, overlay.filter("scale", "iw/4", "ih/4")],
                    "overlay",
                    x="W-w-10",
                    y="H-h-10",
                )
                .output(str(output_file), vcodec="libx264", acodec="aac")
                .overwrite_output()
            )

            print("Creating picture-in-picture effect")
            print("  - Overlay scaled to 25%")
            print("  - Positioned in bottom-right corner\n")

            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"✓ Success! Output: {output_file}\n")

        except ffmpeg.Error as e:
            print(f"✗ Error: {e.stderr.decode()}\n")

    # ============================================================================
    # SECTION 3: Advanced Operations
    # ============================================================================

    def demo_extract_frames(self, input_file: str, fps: int = 1):
        """
        Demo 10: Extract frames as images
        """
        print("=" * 80)
        print("DEMO 10: Extract Frames as Images")
        print("=" * 80)

        frames_dir = self.output_dir / "frames"
        frames_dir.mkdir(exist_ok=True)
        output_pattern = frames_dir / "frame_%04d.png"

        try:
            stream = (
                ffmpeg.input(input_file)
                .filter("fps", fps=fps)
                .output(str(output_pattern), format="image2", vcodec="png")
                .overwrite_output()
            )

            print(f"Extracting {fps} frame(s) per second\n")

            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"✓ Success! Frames saved to: {frames_dir}\n")

        except ffmpeg.Error as e:
            print(f"✗ Error: {e.stderr.decode()}\n")

    def demo_create_video_from_images(self, image_pattern: str, fps: int = 30):
        """
        Demo 11: Create video from image sequence
        """
        print("=" * 80)
        print("DEMO 11: Create Video from Images")
        print("=" * 80)

        output_file = self.output_dir / "from_images.mp4"

        try:
            stream = (
                ffmpeg.input(image_pattern, pattern_type="glob", framerate=fps)
                .output(str(output_file), vcodec="libx264", pix_fmt="yuv420p", crf=20)
                .overwrite_output()
            )

            print(f"Creating video from images at {fps} fps\n")

            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"✓ Success! Output: {output_file}\n")

        except ffmpeg.Error as e:
            print(f"✗ Error: {e.stderr.decode()}\n")

    def demo_add_audio_to_video(self, video_file: str, audio_file: str):
        """
        Demo 12: Replace or add audio track to video
        """
        print("=" * 80)
        print("DEMO 12: Add/Replace Audio Track")
        print("=" * 80)

        output_file = self.output_dir / "with_audio.mp4"

        try:
            video = ffmpeg.input(video_file)
            audio = ffmpeg.input(audio_file)

            stream = ffmpeg.output(
                video.video,  # Take video from first input
                audio.audio,  # Take audio from second input
                str(output_file),
                vcodec="copy",
                acodec="aac",
                shortest=None,  # End when shortest stream ends
            ).overwrite_output()

            print("Replacing audio track\n")

            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"✓ Success! Output: {output_file}\n")

        except ffmpeg.Error as e:
            print(f"✗ Error: {e.stderr.decode()}\n")

    def demo_create_gif(self, input_file: str, start: float = 0, duration: float = 5):
        """
        Demo 13: Create optimized GIF from video
        """
        print("=" * 80)
        print("DEMO 13: Create Optimized GIF")
        print("=" * 80)

        output_file = self.output_dir / "output.gif"

        try:
            # Two-pass approach for better quality GIF
            stream = (
                ffmpeg.input(input_file, ss=start, t=duration)
                .filter("fps", fps=10)
                .filter("scale", 480, -1)  # Width 480, height auto
                .output(str(output_file), format="gif")
                .overwrite_output()
            )

            print(f"Creating GIF from {start}s for {duration}s")
            print("  - 10 fps")
            print("  - Width: 480px\n")

            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"✓ Success! Output: {output_file}\n")

        except ffmpeg.Error as e:
            print(f"✗ Error: {e.stderr.decode()}\n")

    def demo_streaming_hls(self, input_file: str):
        """
        Demo 14: Create HLS streaming segments
        """
        print("=" * 80)
        print("DEMO 14: Create HLS Streaming Segments")
        print("=" * 80)

        hls_dir = self.output_dir / "hls"
        hls_dir.mkdir(exist_ok=True)
        playlist = hls_dir / "playlist.m3u8"

        try:
            stream = (
                ffmpeg.input(input_file)
                .output(
                    str(playlist),
                    format="hls",
                    start_number=0,
                    hls_time=10,  # 10 second segments
                    hls_list_size=0,  # Include all segments
                    vcodec="libx264",
                    acodec="aac",
                )
                .overwrite_output()
            )

            print("Creating HLS segments")
            print("  - 10 second segments")
            print("  - H.264 video, AAC audio\n")

            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"✓ Success! Playlist: {playlist}\n")

        except ffmpeg.Error as e:
            print(f"✗ Error: {e.stderr.decode()}\n")

    def demo_watermark(self, input_file: str, watermark_image: str):
        """
        Demo 15: Add watermark to video
        """
        print("=" * 80)
        print("DEMO 15: Add Watermark")
        print("=" * 80)

        output_file = self.output_dir / "watermarked.mp4"

        try:
            video = ffmpeg.input(input_file)
            watermark = ffmpeg.input(watermark_image)

            stream = (
                ffmpeg.filter([video, watermark], "overlay", x="W-w-10", y="10")
                .output(str(output_file), vcodec="libx264", acodec="copy")
                .overwrite_output()
            )

            print("Adding watermark to top-right corner\n")

            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"✓ Success! Output: {output_file}\n")

        except ffmpeg.Error as e:
            print(f"✗ Error: {e.stderr.decode()}\n")

    def demo_audio_visualization(self, audio_file: str):
        """
        Demo 16: Create audio waveform visualization
        """
        print("=" * 80)
        print("DEMO 16: Audio Waveform Visualization")
        print("=" * 80)

        output_file = self.output_dir / "audio_viz.mp4"

        try:
            stream = (
                ffmpeg.input(audio_file)
                .filter("showwaves", s="1280x720", mode="line", colors="blue")
                .output(
                    str(output_file), vcodec="libx264", pix_fmt="yuv420p", acodec="aac"
                )
                .overwrite_output()
            )

            print("Creating waveform visualization\n")

            ffmpeg.run(stream, capture_stdout=True, capture_stderr=True)
            print(f"✓ Success! Output: {output_file}\n")

        except ffmpeg.Error as e:
            print(f"✗ Error: {e.stderr.decode()}\n")

    # ============================================================================
    # Utility Methods
    # ============================================================================

    def get_video_info(self, input_file: str) -> Dict:
        """Get comprehensive video information"""
        try:
            probe = ffmpeg.probe(input_file)
            return {
                "format": probe["format"],
                "video_streams": [
                    s for s in probe["streams"] if s["codec_type"] == "video"
                ],
                "audio_streams": [
                    s for s in probe["streams"] if s["codec_type"] == "audio"
                ],
                "subtitle_streams": [
                    s for s in probe["streams"] if s["codec_type"] == "subtitle"
                ],
            }
        except ffmpeg.Error as e:
            print(f"Error getting video info: {e.stderr.decode()}")
            return {}

    def check_ffmpeg_installed(self) -> bool:
        """Check if ffmpeg is installed and accessible"""
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"], capture_output=True, text=True
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False


def main():
    """
    Main function to demonstrate FFmpeg usage
    """
    print("\n" + "=" * 80)
    print(" " * 25 + "FFmpeg Masterclass")
    print("=" * 80 + "\n")

    # Initialize
    masterclass = FFmpegMasterclass()

    # Check if ffmpeg is installed
    if not masterclass.check_ffmpeg_installed():
        print("⚠ FFmpeg is not installed or not in PATH!")
        print("\nInstallation instructions:")
        print("  Ubuntu/Debian: sudo apt install ffmpeg")
        print("  macOS: brew install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        return

    print("✓ FFmpeg is installed and ready!\n")

    # You need to provide your own video file to test these demos
    # For demonstration purposes, we'll show how to use each method

    print("USAGE EXAMPLES:")
    print("-" * 80)
    print()
    print("# Basic conversion")
    print("masterclass.demo_cli_basic_conversion('input.mp4')")
    print()
    print("# Apply filters")
    print("masterclass.demo_cli_with_filters('input.mp4')")
    print()
    print("# Extract audio")
    print("masterclass.demo_cli_extract_audio('input.mp4')")
    print()
    print("# Using ffmpeg-python library")
    print("masterclass.demo_ffmpeg_python_basic('input.mp4')")
    print()
    print("# Probe video metadata")
    print("masterclass.demo_ffmpeg_python_probe('input.mp4')")
    print()
    print("# Apply filter chain")
    print("masterclass.demo_ffmpeg_python_filters('input.mp4')")
    print()
    print("# Trim video")
    print("masterclass.demo_ffmpeg_python_trim('input.mp4', start=5, duration=10)")
    print()
    print("# Concatenate videos")
    print("masterclass.demo_ffmpeg_python_concat(['vid1.mp4', 'vid2.mp4'])")
    print()
    print("# Picture-in-picture overlay")
    print("masterclass.demo_ffmpeg_python_overlay('base.mp4', 'overlay.mp4')")
    print()
    print("# Extract frames")
    print("masterclass.demo_extract_frames('input.mp4', fps=1)")
    print()
    print("# Create video from images")
    print("masterclass.demo_create_video_from_images('frames/*.png', fps=30)")
    print()
    print("# Add/replace audio")
    print("masterclass.demo_add_audio_to_video('video.mp4', 'audio.mp3')")
    print()
    print("# Create GIF")
    print("masterclass.demo_create_gif('input.mp4', start=10, duration=5)")
    print()
    print("# Create HLS streaming segments")
    print("masterclass.demo_streaming_hls('input.mp4')")
    print()
    print("# Add watermark")
    print("masterclass.demo_watermark('input.mp4', 'logo.png')")
    print()
    print("# Audio visualization")
    print("masterclass.demo_audio_visualization('audio.mp3')")
    print()
    print("=" * 80)
    print("\nTo run these demos, provide your own video files and uncomment")
    print("the desired demo calls in the main() function.")
    print()
    print("All outputs will be saved to: ./ffmpeg_output/")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
