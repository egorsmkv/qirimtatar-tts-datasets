import argparse
import json
import shutil
from os import makedirs
from os.path import exists
from glob import glob


def run(raw_files, save_to):
    # Create a folder if it doesn't exist
    if not exists(save_to):
        makedirs(save_to)
    
    new_meta_file = 'metadata.jsonl'

    # Read meta files
    for meta_file in glob(f'{raw_files}/*.json'):
        meta = json.loads(open(meta_file).read())

        ogg_file = meta_file.replace('.json', '.ogg')

        sample = meta['sample']

        new_meta = {
            'file': meta['file'],
            'orig_text_wo_stress': sample['orig_text_wo_stress'].replace('\u0301', ''),
            'orig_text': sample['orig_text'],
        }

        # create a meta file
        with open(f'{save_to}/{new_meta_file}', 'a') as f:
            f.write(json.dumps(new_meta) + "\n")

        # copy a file
        shutil.copyfile(ogg_file, f'{save_to}/{meta["file"]}')
    
    print('Finished')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Tool to prepare a TTS dataset"
    )
    parser.add_argument(
        "--raw_files", help="Path to the raw dataset exported from the Online Microphone", type=str, required=True
    )
    parser.add_argument(
        "--save_to", help="Path to the folder where we save data", type=str, required=True
    )
    args = parser.parse_args()

    run(args.raw_files, args.save_to)
