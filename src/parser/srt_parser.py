import re


def parse_srt(file_path: str) -> list[dict[str, int | str]]:
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    blocks = content.strip().split('\n\n')
    subtitles = []
    for block in blocks:
        lines = block.split('\n')
        index = int(lines[0])
        timecode = lines[1]
        text = ' '.join(lines[2:])
        start_time, end_time = parse_timecode(timecode)
        subtitles.append({
          'index': index,
          'start_time': start_time,
          'end_time': end_time,
          'text': text
        })
    return subtitles


def parse_timecode(timecode):
    start, end = timecode.split(' --> ')
    return start, end
