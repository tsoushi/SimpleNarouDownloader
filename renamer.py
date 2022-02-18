import os
import re
import logging

logger = logging.getLogger(__name__)

def rename(files, numonly=False, match=None):
    logger.info('リネームを開始します')
    if match:
        logger.debug('以下のパスは正規表現フィルターによって除外されます')
        filteredFiles = []
        for file in files:
            if re.search(match, file):
                filteredFiles.append(file)
            else:
                logger.debug('{}'.format(file))
        files = filteredFiles
        
    files = [[os.path.abspath(i), int(re.search(r'.+?-([0-9]+?)\.txt', os.path.basename(i)).group(1))] for i in files]
    no_length = len(str(max(files, key=lambda i:i[1])[1]))

    logger.info('リネーム中 : {} ファイル'.format(len(files)))
    for file, no in files:
        newname = str(no).rjust(no_length, '0')+'.txt'
        if not numonly:
            newname = re.search(r'(.+?-)[0-9]+?\.txt', os.path.basename(file)).group(1) + newname
        logger.debug('rename : {} >>> {}'.format(os.path.basename(file), newname))
        os.rename(file, os.path.dirname(file)+os.sep+newname)
    logger.info('リネームが完了しました')

def rename_dir(dirname, numonly=False, match=None):
    dirabs = os.path.abspath(dirname)
    logger.info('ディレクトリからファイルを選択します : {}'.format(dirabs))

    files = [dirabs + os.sep + i for i in os.listdir(dirabs)]
    logger.debug('選択したファイル : {}'.format('\n'.join(files)))
    rename(files, numonly=numonly, match=match)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', nargs='*', help='リネームするファイル')
    parser.add_argument('--dir', '-d', type=str, help='リネームするファイルが入ったディレクトリ')
    parser.add_argument('--match', '-m', type=str, help='ファイルを正規表現でフィルタリングします')
    parser.add_argument('--numonly', '-n', action='store_true', help='数字のみのファイル名にする')
    parser.add_argument('--debug', '-de', action='store_true', help='ログを表示する')
    args = parser.parse_args()

    LOGLEVEL = logging.WARNING
    if args.debug:
        LOGLEVEL = logging.DEBUG
    logger.setLevel(LOGLEVEL)
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(LOGLEVEL)
    streamHandler.setFormatter(logging.Formatter('%(levelname)s - %(name)s - %(message)s'))
    logger.addHandler(streamHandler)

    if args.input:
        rename(args.input, args.numonly, match=args.match)
    elif args.dir:
        rename_dir(args.dir, args.numonly, match=args.match)
    else:
        print('ファイルまたはディレクトリが指定されていません')
