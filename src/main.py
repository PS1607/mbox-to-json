import pandas as pd
import mailbox
import argparse
import subprocess
from alive_progress import alive_bar


def getcharsets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    return charsets


def getBody(msg):
    while msg.is_multipart():
        msg = msg.get_payload()[0]
    t = msg.get_payload(decode=True)
    for charset in getcharsets(msg):
        t = t.decode(charset)
    return t


def main():
    parser = argparse.ArgumentParser(description="Converts MBOX file to JSON")
    parser.add_argument("filename", help="Input MBOX file path")
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        default="file.json",
        help="Output JSON file path and name. Defaults to same location and name as input file.",
    )
    parser.add_argument(
        "-a",
        "--attachments",
        action="store_true",
        help="Extracts Attachments from the MBOX.",
    )
    parser.add_argument(
        "-c",
        "--csv",
        action="save_as_CSV",
        help="Saves as CSV instead of JSON",
    )

    args = parser.parse_args()

    if args.attachments:
        # Run extract.py
        subprocess.run("python src/extract.py -i " + args.filename, shell=True)
        print()


    print('Initializing...')
    MBOX = args.filename
    mbox = mailbox.mbox(MBOX)
    msg_count = mbox.__len__()

    mbox_dict = {}
    with alive_bar(msg_count) as bar:
         for i, msg in enumerate(mbox):
            mbox_dict[i] = {}
            bar()
            for header in msg.keys():
                mbox_dict[i][header] = msg[header]
            try:
                mbox_dict[i]["Body"] = getBody(msg)
            except Exception as e:
                print("Error Occured at: ", i)
                print(e)
            else:
                continue

    df = pd.DataFrame.from_dict(mbox_dict, orient="index")

    if args.csv:
        df.to_csv(args.output, index="false")
    else:
        df.to_json(args.output, orient="records", index="false")


if __name__ == "__main__":
    # calling the main function
    main()
