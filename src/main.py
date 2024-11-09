import os
import pandas as pd
import mailbox
import argparse
import subprocess
from alive_progress import alive_bar
from charset_normalizer import from_bytes  # Import charset-normalizer for encoding detection


def getcharsets(msg):
    """Extracts the charsets from the email headers."""
    charsets = set({})
    for c in msg.get_charsets() or []:  # Ensure we don't iterate over None
        if c is not None:
            charsets.update([c])
    return charsets


def getBody(msg):
    """Extracts the body from the email, handling different encodings and errors."""
    while msg.is_multipart():
        msg = msg.get_payload()[0]
    raw_payload = msg.get_payload(decode=True)

    if raw_payload is None:
        print(f"Warning: No payload for message {msg}")
        return ""  # If no payload, return an empty string

    # Attempt to detect encoding using charset-normalizer
    result = from_bytes(raw_payload)  # Detect encoding using charset-normalizer
    detected_encoding = result.best().encoding if result.best() else None  # Get the best encoding

    if detected_encoding:
        try:
            # Decode with the detected encoding
            return raw_payload.decode(detected_encoding, errors='replace')
        except (UnicodeDecodeError, TypeError) as e:
            print(f"Warning: Failed to decode with {detected_encoding}, error: {e}")
            return raw_payload.decode('utf-8', errors='replace')  # fallback to UTF-8
    else:
        # Fallback: Use UTF-8 decoding with 'replace' to handle invalid characters
        return raw_payload.decode('utf-8', errors='replace')


def sanitize_string(value):
    """Sanitize the string to avoid potential encoding issues."""
    if isinstance(value, str):
        return value.replace('\x00', '')  # Remove null byte
    return value


def split_dataframe(df, num_splits):
    """Splits the DataFrame into a given number of parts."""
    chunk_size = len(df) // num_splits
    return [df.iloc[i:i + chunk_size] for i in range(0, len(df), chunk_size)]


def main():
    parser = argparse.ArgumentParser(description="Converts MBOX file to JSON")
    parser.add_argument("filename", help="Input MBOX file path")
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        help="Output JSON file path and name. Defaults to same location and name as input file.",
    )
    parser.add_argument(
        "-a",
        "--attachments",
        action="store_true",
        help='Extracts Attachments from the MBOX. Stored to the same location as input file in a folder "attachments"',
    )
    parser.add_argument(
        "-c",
        "--csv",
        action="store_true",
        help="Saves as CSV instead of JSON. Defaults to same location and name as input file.",
    )
    parser.add_argument(
        "-s",
        "--split",
        type=int,
        default=1,
        help="Split the output into this many pieces (default: 1, no split)",
    )

    args = parser.parse_args()
    if args.output is None:
        if args.csv:
            args.output = os.path.splitext(args.filename)[0] + '.csv'
        else:
            args.output = os.path.splitext(args.filename)[0] + '.json'

    if args.attachments:
        # Run extract.py
        output_directory = os.path.join(os.path.dirname(args.output), 'attachments', '')
        extract = os.path.dirname(__file__) + "/extract.py"
        subprocess.run("python " + extract + " -i " + args.filename + " -o " + output_directory, shell=True)

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
                print(f"Error Occurred at message {i}: {e}")
            else:
                continue

    # Convert mbox_dict to DataFrame
    df = pd.DataFrame.from_dict(mbox_dict, orient="index")

    # Sanitize the DataFrame values using apply instead of applymap
    df = df.apply(lambda x: sanitize_string(x) if isinstance(x, str) else x)

    # Split DataFrame if needed
    if args.split > 1:
        df_chunks = split_dataframe(df, args.split)
        for idx, chunk in enumerate(df_chunks):
            chunk_output = f"{os.path.splitext(args.output)[0]}_part{idx + 1}{os.path.splitext(args.output)[1]}"
            if args.csv:
                chunk.to_csv(chunk_output, index=False)
            else:
                chunk.to_json(chunk_output, orient="records", index=False, force_ascii=False)
            print(f"Saved: {chunk_output}")
    else:
        # Save to the appropriate output format
        if args.csv:
            df.to_csv(args.output, index=False)
        else:
            df.to_json(args.output, orient="records", index=False, force_ascii=False)


if __name__ == "__main__":
    # Calling the main function
    main()