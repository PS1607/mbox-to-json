import errno
import mailbox
import os
import pathlib  # since Python 3.4
import re
import traceback
from email.header import decode_header
from alive_progress import alive_bar
import argparse
import sys


def parse_options(args=[]):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input', default='all.mbox', help='Input file')
    parser.add_argument('-o', '--output', default='attachments/', help='Output folder')
    parser.add_argument('--no-inline-images', action='store_true')
    parser.add_argument('--start',
                        type=message_id_type, default=0,
                        help='On which message to start')
    parser.add_argument('--stop',
                        type=message_id_type, default=100000000000,
                        help='On which message to stop, not included')
    return parser.parse_args(args)


def message_id_type(arg):
    try:
        i = int(arg)
    except ValueError as e:
        raise argparse.ArgumentTypeError(str(e))
    if i < 0:
        raise argparse.ArgumentTypeError("Must be greater than or equal 0.")
    return i


class Extractor:
    def __init__(self, options):
        self.__total = 0
        self.__failed = 0

        self.options = options

        assert os.path.isfile(options.input)
        self.mbox = mailbox.mbox(options.input)

        if not os.path.exists(options.output):
            os.makedirs(options.output)

        self.inline_image_folder = os.path.join(options.output, 'inline_images/')
        if (not options.no_inline_images) and (not os.path.exists(self.inline_image_folder)):
            os.makedirs(self.inline_image_folder)

    def increment_total(self):
        self.__total += 1

    def increment_failed(self):
        self.__failed += 1

    def get_total(self):
        return self.__total

    def get_failed(self):
        return self.__failed


def to_file_path(save_to, name):
    return os.path.join(save_to, name)


def get_extension(name):
    extension = pathlib.Path(name).suffix
    return extension if len(extension) <= 20 else ''


def resolve_name_conflicts(save_to, name, file_paths, attachment_number):
    file_path = to_file_path(save_to, name)

    START = 1
    iteration_number = START

    while os.path.normcase(file_path) in file_paths:
        extension = get_extension(name)
        iteration = '' if iteration_number <= START else ' (%s)' % iteration_number
        new_name = '%s attachment %s%s%s' % (name, attachment_number, iteration, extension)
        file_path = to_file_path(save_to, new_name)
        iteration_number += 1

    file_paths.append(os.path.normcase(file_path))
    return file_path


# Whitespaces: tab, carriage return, newline, vertical tab, form feed.
FORBIDDEN_WHITESPACE_IN_FILENAMES = re.compile('[\t\r\n\v\f]+')
OTHER_FORBIDDEN_FN_CHARACTERS = re.compile('[/\\\\\\?%\\*:\\|"<>\0]')


def filter_fn_characters(s):
    result = re.sub(FORBIDDEN_WHITESPACE_IN_FILENAMES, ' ', s)
    result = re.sub(OTHER_FORBIDDEN_FN_CHARACTERS, '_', result)
    return result


def decode_filename(part, fallback_filename, mid):
    if part.get_filename() is None:
        print('Filename is none: %s %s.' % (mid, fallback_filename))
        return fallback_filename
    else:
        decoded_name = decode_header(part.get_filename())

        if isinstance(decoded_name[0][0], str):
            return decoded_name[0][0]
        else:
            try:
                name_encoding = decoded_name[0][1]
                return decoded_name[0][0].decode(name_encoding)
            except:
                print('Could not decode %s %s attachment name.' % (mid, fallback_filename))
                return fallback_filename


def write_to_disk(part, file_path):
    with open(file_path, 'wb') as f:
        f.write(part.get_payload(decode=True))


def save(extractor, mid, part, attachments_counter, inline_image=False):
    extractor.increment_total()

    try:
        if inline_image:
            attachments_counter['inline_image'] += 1
            attachment_number_string = 'ii' + str(attachments_counter['inline_image'])
            destination_folder = extractor.inline_image_folder
        else:
            attachments_counter['value'] += 1
            attachment_number_string = str(attachments_counter['value'])
            destination_folder = extractor.options.output

        filename = decode_filename(part, attachment_number_string, mid)
        filename = filter_fn_characters(filename)
        filename = '%s %s' % (mid, filename)

        previous_file_paths = attachments_counter['file_paths']

        try:
            write_to_disk(part, resolve_name_conflicts(
                destination_folder, filename,
                previous_file_paths,
                attachment_number_string))
        except OSError as e:
            if e.errno == errno.ENAMETOOLONG:
                short_name = '%s %s%s' % (mid, attachment_number_string, get_extension(filename))
                write_to_disk(part, resolve_name_conflicts(
                    destination_folder, short_name,
                    previous_file_paths,
                    attachment_number_string))
            else:
                raise
    except:
        traceback.print_exc()
        extractor.increment_failed()


def check_part(extractor, mid, part, attachments_counter):
    mime_type = part.get_content_type()
    if part.is_multipart():
        for p in part.get_payload():
            check_part(extractor, mid, p, attachments_counter)
    elif (part.get_content_disposition() == 'attachment') \
            or ((part.get_content_disposition() != 'inline') and (part.get_filename() is not None)):
        save(extractor, mid, part, attachments_counter)
    elif (mime_type.startswith('application/') and not mime_type == 'application/javascript') \
            or mime_type.startswith('model/') \
            or mime_type.startswith('audio/') \
            or mime_type.startswith('video/'):
        message_id_content_type = 'Message id = %s, Content-type = %s.' % (mid, mime_type)
        if part.get_content_disposition() == 'inline':
            print('Extracting inline part... ' + message_id_content_type)
        else:
            print('Other Content-disposition... ' + message_id_content_type)
        save(extractor, mid, part, attachments_counter)
    elif (not extractor.options.no_inline_images) and mime_type.startswith('image/'):
        save(extractor, mid, part, attachments_counter, True)


def process_message(extractor, mid):
    msg = extractor.mbox.get_message(mid)
    if msg.is_multipart():
        attachments_counter = {
            'value': 0,
            'inline_image': 0,
            'file_paths': []
        }
        for part in msg.get_payload():
            check_part(extractor, mid, part, attachments_counter)


def extract_mbox_file(options):
    extractor = Extractor(options)
    message_count = extractor.mbox.__len__()
    print()
    print('Extracting Attachments...')
    with alive_bar(message_count) as bar:
        for i in range(options.start, options.stop):
            try:
                process_message(extractor, i)
            except KeyError:
                print('The whole mbox file was processed.')
                break
            bar()

    print()
    print('Total files:  %s' % extractor.get_total())
    print('Failed:       %s' % extractor.get_failed())
    print()
    print('Your files are available in the folder "mbox-to-json/attachments"')
    print()


if __name__ == "__main__":
    extract_mbox_file(parse_options(sys.argv[1:]))
