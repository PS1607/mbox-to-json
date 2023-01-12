import pandas as pd
import mailbox
import argparse
import subprocess
import os


def getcharsets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    return charsets

def getBody(msg):
    while msg.is_multipart():
        msg=msg.get_payload()[0]
    t=msg.get_payload(decode=True)
    for charset in getcharsets(msg):
        t=t.decode(charset)
    return t

def main():
    parser = argparse.ArgumentParser(description = 'Converts MBOX file to JSON')
    parser.add_argument('filename', help = 'Input MBOX file path')
    parser.add_argument('-o', '--output', required = False, default = 'file.json',
                        help = 'Output JSON file path and name. Defaults to same location and name as input file.')
    parser.add_argument('-a', '--attachments',
                        action = 'store_true', help = 'Extracts Attachments from the MBOX.')

    args = parser.parse_args()

    if args.attachments:
        #Run extract.py
        subprocess.run('python src/extract.py -i ' + args.filename, shell = True)

    MBOX = args.filename
    mbox = mailbox.mbox(MBOX)

    mbox_dict = {}
    for i, msg in enumerate(mbox):
        mbox_dict[i] = {}
        for header in msg.keys():
            mbox_dict[i][header] = msg[header]
        try:
          mbox_dict[i]['Body'] = getBody(msg)
        except Exception as e:

          print("Error Occured at: ",i)
          print(e)
        else:
          continue

    df = pd.DataFrame.from_dict(mbox_dict, orient='index')
    df.to_json(args.output, orient = 'split', compression = 'infer', index = 'true')

if __name__ == "__main__":
    # calling the main function
    main()