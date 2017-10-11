from threading import Thread, BoundedSemaphore
from argparse import ArgumentParser
import shutil
import os.path


def copy(path_from, path_to, end_path):
    if os.path.isfile(path_from):
        shutil.copy(path_from, path_to)
    elif os.path.isdir(path_from):
        shutil.copytree(path_from, path_to + "/" + end_path)


def move(path_from, path_to):
    shutil.move(path_from, path_to)


def get_path_dir(path):
    directory = path.split("/")
    directory[-1] = directory[0]
    path_dir = '/'.join(directory)
    return path_dir


def my_mask(path_dir, mask):
    mass_path_mask = []
    for root, dirs, files in os.walk(path_dir):
        for name in files:
            if name.find(mask[1:]) >= 0:
                if root[-1] == '/':
                    mass_path_mask.append(str(root)+str(name))
                else:
                    mass_path_mask.append(str(root)+'/'+str(name))
    return mass_path_mask


def run(operation, path_from, path_to, semaphore, end_path):

    semaphore.acquire()

    if operation == 'copy':
        copy(path_from, path_to, end_path)

    elif operation == 'move':
        move(path_from, path_to)

    semaphore.release()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--operation',
                        choices=['move', 'copy'],
                        required=True,
                        help="choose operation mode (move, copy)")
    parser.add_argument('--from',
                        type=str,
                        required=True,
                        help="path of source")
    parser.add_argument('--to',
                        type=str,
                        required=True,
                        help="path of destination")
    parser.add_argument('--threads',
                        type=int,
                        default=1,
                        help="an integer for the number of threads")

    args = parser.parse_args("--operation move --from /home/pasha/Документы/test/file1.txt \
                             --to /home/pasha/Документы/test1 --threads 2".split())
    dict_args = vars(args)

    semaphore = BoundedSemaphore(value=dict_args['threads'])
    end_path = dict_args['from'].split("/")[-1]

    if dict_args['from'].find('*.') >= 0:
        path = get_path_dir(dict_args['from'])
        files = my_mask(path, end_path)
    else:
        files = [dict_args['from']]

    for file in files:
        Thread(target=run, args=(dict_args['operation'], file, dict_args['to'], semaphore, end_path)).start()
