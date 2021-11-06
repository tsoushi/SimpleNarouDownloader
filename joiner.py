import os
import logging

logger = logging.getLogger(__name__)

def join(files, out, enc='utf-8'):
    logger.debug('結合を開始します')
    files = [os.path.abspath(i) for i in files]
    logger.debug('openning file to write : {}'.format(out))
    with open(out, 'w', encoding=enc) as f_out:
        for file in files:
            with open(file, encoding=enc) as f_in:
                logger.debug('reading file : {}'.format(file))
                f_out.write(f_in.read())
    logger.debug('file is closed')
    logger.debug('結合が完了しました')

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('input', nargs='*', help='まとめる')
    parser.add_argument('--out', '-o', default='out.txt', type=os.path.abspath, help='出力ファイル名')
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

    files = sorted(args.input, key=lambda i:os.path.basename(i))
    join(files, out=args.out)
