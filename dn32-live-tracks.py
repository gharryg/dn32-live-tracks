import argparse
import os
import uuid
import sys
import subprocess
import shutil
import atexit


def main():
    parser = argparse.ArgumentParser(description='A tool to extract only what you want from (potentially many) multichannel WAV files.')
    parser.add_argument('-c', '--channels', nargs='+', help='List of channels to extract. Channels should be in the format "CHANNEL_NUMBER:CHANNEL_NAME" with each channel seperated by a space.')
    parser.add_argument('-f', '--files', nargs='+', required=True, help='The multichannel WAV files in sequential order.')
    parser.add_argument('-l', '--list', help='Text file that contains a list of channels. Channels should be in the format "CHANNEL_NUMBER:CHANNEL_NAME" with each channel seperated by a newline.')
    parser.add_argument('-o', '--output', default='Tracks', help='Output directory to create for final tracks. Default: ./Tracks')
    args = parser.parse_args()

    if not args.channels and not args.list:
        print('You must provide a list of channels for me to extract! (--channels XOR --list)')
        sys.exit(1)
    if args.channels and args.list:
        print('I cannot handle both --channels and --list. Please use just one.')
        sys.exit(1)

    # Make output directory.
    output_directory = args.output
    print('Output directory: %s' % output_directory)
    if not os.path.isdir(output_directory):
        os.mkdir(output_directory)
        # Escape spaces for future use in ffmpeg command.
        output_directory = output_directory.replace(' ', '\\ ')
    else:
        # We'll just play is safe and not proceed if something is already there.
        print('Output directory already exists! Exiting.')
        sys.exit(1)

    files = args.files
    print('Multichannel files: %s' % files)

    # If we have multiple files, make a tempoary directory to store each segment of a channel.
    if len(files) > 1:
        tmp_directory = '/tmp/dn32-live-tracks-%s' % uuid.uuid1()
        os.mkdir(tmp_directory)
        print('Temporary directory: %s' % tmp_directory)
        # Make sure we delete our temporary directory no matter how we exit.
        atexit.register(shutil.rmtree, tmp_directory)

    if args.list:
        with open(args.list) as f:
            channels_raw = f.read().splitlines()
    else:
        channels_raw = args.channels

    channels = []
    for channel in channels_raw:
        index, name = channel.split(':')
        # We need to use zero-based indexing for channel numbers.
        index = int(index) - 1
        # Escape spaces for ffmpeg command.
        channels.append((index, name.replace(' ', '\\ ')))
    print('Channels: %s' % channels)

    # Find out where ffmpeg lives.
    ffmpeg_path = shutil.which('ffmpeg')
    print('ffmpeg path: %s' % ffmpeg_path)

    # ffmpeg -i 00000001.WAV -map_channel 0.0.0 Kick.wav -map_chanel 0.0.1 Snare.wav ...
    # Seperate all the channels.
    file_count = 0
    for file in files:
        cmd = '%s -i %s' % (ffmpeg_path, file)
        for channel in channels:
            index = channel[0]
            name = channel[1]
            if len(files) > 1:
                cmd += ' -map_channel 0.0.%s %s/%s.%s.wav' % (index, tmp_directory, name, file_count)
            else:
                cmd += ' -map_channel 0.0.%s %s/%s.wav' % (index, output_directory, name)
        print('Cmd: %s' % cmd)
        subprocess.run(cmd, shell=True)
        file_count += 1

    if len(files) > 1:
        # ffmpeg -f concat -safe 0 -i files.txt -c copy Kick.wav
        # Merge individual channel files.
        for channel in channels:
            index = channel[0]
            name = channel[1]
            with open('%s/files.txt' % tmp_directory, 'w') as f:
                for i in range(file_count):
                    f.write('file %s/%s.%s.wav\n' % (tmp_directory, name, i))
            cmd = '%s -f concat -safe 0 -i %s/files.txt -c copy %s/%s.wav' % (ffmpeg_path, tmp_directory, output_directory, name)
            print('Cmd: %s' % cmd)
            subprocess.run(cmd, shell=True)


if __name__ == '__main__':
    main()
