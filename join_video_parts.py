from pathlib import Path

VIDEO_PATH = Path('videos')


def write_solid_video(video_dir: Path):
    with open(f'{video_dir.name}.ts', 'wb') as video_file:
        for child in video_dir.iterdir():
            with open(child, 'rb') as video_part:
                video_file.write(video_part.read())


for video_dir in VIDEO_PATH.iterdir():
    write_solid_video(video_dir)
