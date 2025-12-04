import os
import pandas as pd
import mailbox
import argparse
import subprocess
import logging
import sys
import json
import gc
import multiprocessing as mp
from functools import partial
from alive_progress import alive_bar
from charset_normalizer import from_bytes  # Import charset-normalizer for encoding detection
from email.header import decode_header

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('mbox_to_json.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)


def getBody(msg, max_payload_mb=10, max_body_part_mb=1, max_depth=50):
    """Extracts the body from the email, handling different encodings and errors."""
    body_parts = []
    max_payload_bytes = max_payload_mb * 1000000
    max_body_part_bytes = max_body_part_mb * 1000000
    
    def extract_text_parts(part, depth=0):
        """Recursively extract text parts from multipart messages."""
        if depth > max_depth:
            logger.warning(f"Maximum recursion depth reached ({max_depth}). Truncating email parsing.")
            return
        
        if part.is_multipart():
            try:
                payload = part.get_payload()
                if payload:
                    for subpart in payload:
                        extract_text_parts(subpart, depth + 1)
            except (TypeError, AttributeError) as e:
                logger.warning(f"Error processing multipart payload at depth {depth}: {e}")
        else:
            content_type = part.get_content_type()
            # Extract text/plain and text/html parts
            if content_type in ['text/plain', 'text/html']:
                try:
                    raw_payload = part.get_payload(decode=True)
                    if raw_payload:
                        decoded_body = decode_payload(raw_payload)
                        if decoded_body:
                            # Limit body part size to prevent memory issues
                            if len(decoded_body) > max_body_part_bytes:
                                decoded_body = decoded_body[:max_body_part_bytes] + f"\n[TRUNCATED - Content too large (>{max_body_part_mb}MB)]"
                            body_parts.append(f"[{content_type}]: {decoded_body}")
                except Exception as e:
                    logger.warning(f"Error extracting text part: {e}")
    
    def decode_payload(raw_payload):
        """Helper function to decode payload with proper encoding detection."""
        if raw_payload is None:
            return ""
        
        # Limit payload size to prevent memory issues
        if len(raw_payload) > max_payload_bytes:
            logger.warning(f"Payload too large ({len(raw_payload)} bytes), truncating to {max_payload_mb}MB")
            raw_payload = raw_payload[:max_payload_bytes]
        
        # Attempt to detect encoding using charset-normalizer
        try:
            result = from_bytes(raw_payload)
            detected_encoding = result.best().encoding if result.best() else None
        except Exception as e:
            logger.warning(f"Encoding detection failed: {e}")
            detected_encoding = None
        
        if detected_encoding:
            try:
                return raw_payload.decode(detected_encoding, errors='replace')
            except (UnicodeDecodeError, TypeError) as e:
                logger.warning(f"Failed to decode with {detected_encoding}, error: {e}")
                return raw_payload.decode('utf-8', errors='replace')
        else:
            return raw_payload.decode('utf-8', errors='replace')
    
    # Handle both multipart and single part messages
    try:
        if msg.is_multipart():
            extract_text_parts(msg)
            return "\n\n".join(body_parts) if body_parts else ""
        else:
            # Single part message
            raw_payload = msg.get_payload(decode=True)
            if raw_payload is None:
                logger.warning(f"No payload for message {msg}")
                return ""
            return decode_payload(raw_payload)
    except RecursionError:
        logger.error("Maximum recursion depth exceeded while parsing email body")
        return "[ERROR: Email structure too complex to parse]"
    except MemoryError:
        logger.error("Out of memory while parsing email body")
        return "[ERROR: Email too large to parse]"
    except Exception as e:
        logger.error(f"Unexpected error parsing email body: {e}")
        return "[ERROR: Failed to parse email body]"


def extract_attachments_info(msg, message_id):
    """Extract attachment information without saving files."""
    attachments = []
    
    def process_part(part):
        if part.is_multipart():
            for subpart in part.get_payload():
                process_part(subpart)
        else:
            # Check if this part is an attachment
            content_disposition = part.get_content_disposition()
            content_type = part.get_content_type()
            filename = part.get_filename()
            
            is_attachment = False
            
            # Determine if this is an attachment
            if content_disposition == 'attachment':
                is_attachment = True
            elif filename is not None and content_disposition != 'inline':
                is_attachment = True
            elif (content_type.startswith('application/') and content_type != 'application/javascript') \
                    or content_type.startswith('model/') \
                    or content_type.startswith('audio/') \
                    or content_type.startswith('video/'):
                is_attachment = True
            
            if is_attachment and filename:
                # Decode filename if needed
                try:
                    decoded_name = decode_header(filename)
                    if isinstance(decoded_name[0][0], bytes):
                        name_encoding = decoded_name[0][1] or 'utf-8'
                        filename = decoded_name[0][0].decode(name_encoding)
                    else:
                        filename = decoded_name[0][0]
                except:
                    # Keep original filename if decoding fails
                    pass
                
                # Get file size
                try:
                    payload = part.get_payload(decode=True)
                    file_size = len(payload) if payload else 0
                except:
                    file_size = 0
                
                attachment_info = {
                    'filename': filename,
                    'content_type': content_type,
                    'content_disposition': content_disposition,
                    'size_bytes': file_size,
                    'message_id': message_id
                }
                attachments.append(attachment_info)
    
    if msg.is_multipart():
        process_part(msg)
    
    return attachments


def process_message_worker(args_tuple):
    """Worker function to process a single message in parallel."""
    msg_data, msg_index, extract_attachments, skip_metadata, max_payload_mb, max_body_part_mb, max_depth = args_tuple
    
    try:
        # Recreate message object from string data
        import email
        msg = email.message_from_string(msg_data)
        
        result = {"index": msg_index}
        
        # Extract headers with MIME decoding
        for header in msg.keys():
            raw_header_value = msg[header]
            decoded_header_value = decode_mime_header(raw_header_value)
            result[header] = decoded_header_value
        
        # Extract body
        result["Body"] = getBody(msg, max_payload_mb, max_body_part_mb, max_depth)
        
        # Extract attachments if needed
        if extract_attachments and not skip_metadata:
            attachments = extract_attachments_info(msg, msg_index)
            result["Attachments"] = attachments
            result["Attachment_Count"] = len(attachments)
            
            # Add metadata to attachments
            for att in attachments:
                att["source_message_index"] = msg_index
                att["extracted_with"] = "mbox-to-json v2.0.0"
        else:
            result["Attachments"] = []
            result["Attachment_Count"] = 0
            
        return result
        
    except Exception as e:
        logger.error(f"Error processing message {msg_index}: {e}")
        return {
            "index": msg_index,
            "Body": "",
            "Attachments": [],
            "Attachment_Count": 0,
            "Error": str(e)
        }


def decode_mime_header(header_value):
    """Decode MIME-encoded email headers."""
    if not header_value:
        return header_value
    
    try:
        decoded_parts = decode_header(header_value)
        decoded_string = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                if encoding:
                    try:
                        decoded_string += part.decode(encoding, errors='replace')
                    except (UnicodeDecodeError, LookupError):
                        # Fallback to utf-8 if encoding fails
                        decoded_string += part.decode('utf-8', errors='replace')
                else:
                    # No encoding specified, try utf-8
                    decoded_string += part.decode('utf-8', errors='replace')
            else:
                # Already a string
                decoded_string += part
        
        return decoded_string
    except (ValueError, TypeError) as e:
        logger.warning(f"Failed to decode MIME header '{header_value[:50]}...': {e}")
        return header_value  # Return original if decoding fails


def sanitize_string(value):
    """Sanitize the string to avoid potential encoding issues."""
    if isinstance(value, str):
        return value.replace('\x00', '')  # Remove null byte
    return value


def split_dataframe(df, num_splits):
    """Splits the DataFrame into a given number of parts."""
    chunk_size = max(1, len(df) // num_splits)  # Ensure at least 1 row per chunk
    chunks = []
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size].copy()  # Use copy to free memory
        chunks.append(chunk)
    return chunks


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
    parser.add_argument(
        "--skip-attachment-metadata",
        action="store_true",
        help="Skip attachment metadata tagging when using -a flag (extract files but don't add metadata to JSON/CSV)",
    )
    parser.add_argument(
        "--max-payload-size",
        type=int,
        default=10,
        help="Maximum email payload size in MB (default: 10MB)",
    )
    parser.add_argument(
        "--max-body-part-size",
        type=int,
        default=1,
        help="Maximum body part size in MB (default: 1MB)",
    )
    parser.add_argument(
        "--max-recursion-depth",
        type=int,
        default=50,
        help="Maximum recursion depth for nested emails (default: 50)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="Number of messages processed before memory cleanup (default: 1000)"
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of parallel workers for processing (default: 1, max: CPU cores)"
    )
    parser.add_argument(
        "--enable-parallel",
        action="store_true",
        help="Force enable parallel processing regardless of file size or message count"
    )

    args = parser.parse_args()
    
    # Input validation
    if not os.path.exists(args.filename):
        logger.error(f"Input file does not exist: {args.filename}")
        sys.exit(1)
    
    if not os.path.isfile(args.filename):
        logger.error(f"Input path is not a file: {args.filename}")
        sys.exit(1)
    
    # Check if input file is readable
    try:
        with open(args.filename, 'rb') as test_file:
            test_file.read(1)
    except PermissionError:
        logger.error(f"Permission denied reading file: {args.filename}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Cannot read input file {args.filename}: {e}")
        sys.exit(1)
    
    if args.output is None:
        if args.csv:
            args.output = os.path.splitext(args.filename)[0] + '.csv'
        else:
            args.output = os.path.splitext(args.filename)[0] + '.json'
    
    # Check if output directory exists and is writable
    output_dir = os.path.dirname(os.path.abspath(args.output))
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            logger.info(f"Created output directory: {output_dir}")
        except Exception as e:
            logger.error(f"Cannot create output directory {output_dir}: {e}")
            sys.exit(1)
    
    if not os.access(output_dir, os.W_OK):
        logger.error(f"Output directory is not writable: {output_dir}")
        sys.exit(1)
    
    # Validate arguments
    if args.split < 1:
        logger.error("Split value must be greater than 0")
        sys.exit(1)
    
    if args.max_payload_size < 1:
        logger.error("Max payload size must be at least 1MB")
        sys.exit(1)
        
    if args.max_body_part_size < 1:
        logger.error("Max body part size must be at least 1MB")
        sys.exit(1)
        
    if args.max_recursion_depth < 1:
        logger.error("Max recursion depth must be at least 1")
        sys.exit(1)
        
    if args.batch_size < 1:
        logger.error("Batch size must be at least 1")
        sys.exit(1)

    if args.attachments:
        # Run extract.py safely without shell=True
        output_directory = os.path.join(os.path.dirname(args.output), 'attachments', '')
        extract_script = os.path.join(os.path.dirname(__file__), "extract.py")
        
        try:
            # Use subprocess.run with a list of arguments instead of shell=True
            result = subprocess.run([
                sys.executable, extract_script, 
                "-i", args.filename, 
                "-o", output_directory
            ], capture_output=True, text=True, check=True)
            logger.info("Attachment extraction completed successfully")
        except subprocess.CalledProcessError as e:
            logger.error(f"Error extracting attachments: {e}")
            logger.error(f"Output: {e.stdout}")
            logger.error(f"Error: {e.stderr}")
        except FileNotFoundError:
            logger.error(f"Extract script not found: {extract_script}")
            return

    logger.info('Initializing MBOX processing...')
    MBOX = args.filename
    
    try:
        mbox = mailbox.mbox(MBOX)
        msg_count = mbox.__len__()
        logger.info(f"Found {msg_count} messages in MBOX file")
        
        if msg_count == 0:
            logger.warning("MBOX file contains no messages")
            return
            
    except Exception as e:
        logger.error(f"Failed to open MBOX file {MBOX}: {e}")
        sys.exit(1)

    mbox_dict = {}
    all_attachments = []  # Track all attachments across messages
    
    # Get file size for logging
    file_size_mb = os.path.getsize(args.filename) / (1024 * 1024)
    
    # Determine if parallel processing should be used
    use_parallel = (
        args.workers > 1 and 
        (
            args.enable_parallel or 
            (msg_count >= 1000 and file_size_mb >= 200.0)
        )
    )
    
    # Log the decision with detailed reasoning
    if args.workers > 1:
        if use_parallel:
            if args.enable_parallel:
                logger.info(f"Parallel processing force-enabled: {file_size_mb:.1f}MB, {msg_count} messages")
            else:
                logger.info(f"File qualifies for parallel processing: {file_size_mb:.1f}MB, {msg_count} messages")
        else:
            reasons = []
            if msg_count < 1000:
                reasons.append(f"message count too low ({msg_count} < 1000)")
            if file_size_mb < 200.0:
                reasons.append(f"file size too small ({file_size_mb:.1f}MB < 200.0MB)")
            logger.info(f"Using serial processing: {', '.join(reasons)}. Use --enable-parallel to override.")
    
    # Determine number of workers
    max_workers = min(args.workers, mp.cpu_count(), msg_count) if use_parallel else 1
    
    if use_parallel:
        logger.info(f"Using parallel processing with {max_workers} workers for {msg_count} messages ({file_size_mb:.1f}MB file)")
        # Prepare message data for parallel processing
        message_data = []
        for i, msg in enumerate(mbox):
            msg_str = str(msg)  # Convert message to string for pickling
            message_data.append((
                msg_str, i, args.attachments, args.skip_attachment_metadata,
                args.max_payload_size, args.max_body_part_size, args.max_recursion_depth
            ))
        
        # Process in parallel using multiprocessing
        with mp.Pool(processes=max_workers) as pool:
            with alive_bar(msg_count) as bar:
                # Process messages in batches to manage memory
                batch_size = args.batch_size
                for batch_start in range(0, len(message_data), batch_size):
                    batch_end = min(batch_start + batch_size, len(message_data))
                    batch_data = message_data[batch_start:batch_end]
                    
                    # Process batch in parallel
                    batch_results = pool.map(process_message_worker, batch_data)
                    
                    # Collect results
                    for result in batch_results:
                        msg_idx = result.pop("index")
                        mbox_dict[msg_idx] = result
                        
                        # Collect attachments
                        if "Attachments" in result and result["Attachments"]:
                            all_attachments.extend(result["Attachments"])
                        
                        bar()
                    
                    # Memory cleanup after each batch
                    gc.collect()
                    logger.info(f"Completed batch {batch_start//batch_size + 1}/{(len(message_data) + batch_size - 1)//batch_size}")
    
    else:
        # Serial processing for small files or when parallel processing is disabled
        logger.info(f"Using serial processing for {msg_count} messages ({file_size_mb:.1f}MB file)")
        process_batch_size = args.batch_size
        
        with alive_bar(msg_count) as bar:
            for i, msg in enumerate(mbox):
                mbox_dict[i] = {}
                bar()
                
                # Memory cleanup every batch
                if i > 0 and i % process_batch_size == 0:
                    gc.collect()  # Force garbage collection
                    logger.info(f"Processed {i} messages, running garbage collection")
                
                for header in msg.keys():
                    # Decode MIME-encoded headers
                    raw_header_value = msg[header]
                    decoded_header_value = decode_mime_header(raw_header_value)
                    mbox_dict[i][header] = decoded_header_value
                try:
                    mbox_dict[i]["Body"] = getBody(
                        msg, 
                        max_payload_mb=args.max_payload_size,
                        max_body_part_mb=args.max_body_part_size,
                        max_depth=args.max_recursion_depth
                    )
                    
                    # Extract attachment information only if attachments flag is used and not skipping metadata
                    if args.attachments and not args.skip_attachment_metadata:
                        attachments = extract_attachments_info(msg, i)
                        mbox_dict[i]["Attachments"] = attachments
                        mbox_dict[i]["Attachment_Count"] = len(attachments)
                        
                        # Add to global attachment list with message reference
                        for att in attachments:
                            att["source_message_index"] = i
                            att["extracted_with"] = "mbox-to-json v2.0.0"
                            all_attachments.append(att)
                        
                except Exception as e:
                    logger.error(f"Error occurred at message {i}: {e}")
                    mbox_dict[i]["Body"] = ""  # Set empty body on error
                    if args.attachments and not args.skip_attachment_metadata:
                        mbox_dict[i]["Attachments"] = []
                        mbox_dict[i]["Attachment_Count"] = 0

    # Convert mbox_dict to DataFrame
    df = pd.DataFrame.from_dict(mbox_dict, orient="index")

    # Sanitize the DataFrame values - apply to all elements
    try:
        # Use map() for element-wise application on the entire DataFrame
        for col in df.columns:
            df[col] = df[col].apply(lambda x: sanitize_string(x) if isinstance(x, str) else x)
        logger.info("DataFrame sanitization completed")
    except Exception as e:
        logger.error(f"Error during DataFrame sanitization: {e}")
        # Continue without sanitization if it fails

    # Split DataFrame if needed
    if args.split > 1:
        df_chunks = split_dataframe(df, args.split)
        for idx, chunk in enumerate(df_chunks):
            chunk_output = f"{os.path.splitext(args.output)[0]}_part{idx + 1}{os.path.splitext(args.output)[1]}"
            try:
                if args.csv:
                    chunk.to_csv(chunk_output, index=False)
                else:
                    chunk.to_json(chunk_output, orient="records", index=False, force_ascii=False)
                logger.info(f"Saved: {chunk_output}")
            except Exception as e:
                logger.error(f"Failed to save chunk {idx + 1}: {e}")
        
        # Save attachments manifest for split files
        if all_attachments and args.attachments and not args.skip_attachment_metadata:
            attachments_file = f"{os.path.splitext(args.output)[0]}_attachments_manifest.json"
            try:
                with open(attachments_file, 'w', encoding='utf-8') as f:
                    json.dump(all_attachments, f, indent=2, ensure_ascii=False)
                logger.info(f"Saved attachments manifest: {attachments_file}")
            except Exception as e:
                logger.error(f"Failed to save attachments manifest: {e}")
                
    else:
        # Save to the appropriate output format
        try:
            if args.csv:
                df.to_csv(args.output, index=False)
            else:
                df.to_json(args.output, orient="records", index=False, force_ascii=False)
            logger.info(f"Successfully saved output to: {args.output}")
            
            # Save separate attachments manifest
            if all_attachments and args.attachments and not args.skip_attachment_metadata:
                attachments_file = f"{os.path.splitext(args.output)[0]}_attachments_manifest.json"
                try:
                    with open(attachments_file, 'w', encoding='utf-8') as f:
                        json.dump(all_attachments, f, indent=2, ensure_ascii=False)
                    logger.info(f"Saved attachments manifest: {attachments_file}")
                except Exception as e:
                    logger.error(f"Failed to save attachments manifest: {e}")
                    
        except Exception as e:
            logger.error(f"Failed to save output file {args.output}: {e}")
            sys.exit(1)


if __name__ == "__main__":
    # Set multiprocessing start method for cross-platform compatibility
    if sys.platform == 'win32':
        mp.set_start_method('spawn', force=True)
    # Calling the main function
    main()