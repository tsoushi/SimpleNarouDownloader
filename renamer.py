import os
import re
import logging

logger = logging.getLogger(__name__)

def rename(files, numonly=False):
    logger.debug('リネームを開始します')
    files = [[os.path.abspath(i), int(re.search(r'.+?-([0-9]+?)\.txt', os.path.basename(i)).group(1))] for i in files]
    no_length = len(str(max(files, key=lambda i:i[1])[1]))

    for file, no in files:
        newname = str(no).rjust(no_length, '0')+'.txt'
        if not numonly:
            newname = re.search(r'(.+?-)[0-9]+?\.txt', os.path.basename(file)).group(1) + newname
        logger.debug('rename : {} >>> {}'.format(os.path.basename(file), newname))
        os.rename(file, os.path.dirname(file)+os.sep+newname)
    logger.debug('リネームが完了しました')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='*', help='リネームするファイル')
    parser.add_argument('--numonly', '-n', action='store_true', help='数字のみのファイル名にする')
    parser.add_argument('--debug', '-d', action='store_true', help='ログを表示する')
    args = parser.parse_args()

    LOGLEVEL = logging.WARNING
    if args.debug:
        LOGLEVEL = logging.DEBUG
    logger.setLevel(LOGLEVEL)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(LOGLEVEL)
    streamHandler.setFormatter(logging.Formatter('%(levelname)s - %(name)s - %(message)s'))
    logger.addHandler(streamHandler)

    rename(args.input, args.numonly)
