import argparse
import re
import logging
import sys
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define IOC regular expressions
IP_REGEX = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
URL_REGEX = r'(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+'
# The TLD class is A-Za-z on purpose: [A-Z|a-z] would also match a literal
# pipe character, so an address with a | in its final part passed as valid.
EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
MD5_REGEX = r'\b[0-9a-fA-F]{32}\b'
SHA1_REGEX = r'\b[0-9a-fA-F]{40}\b'
SHA256_REGEX = r'\b[0-9a-fA-F]{64}\b'
DOMAIN_REGEX = r'\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}\b'
# What this set does not see at all: IPv6 addresses, defanged text of
# the hxxp or dot-bracket kind that reports actually circulate, and
# hashes longer than 64 characters. The URL pattern also has no scheme
# requirement, so a plain file name with an extension reads as a URL.
# I extract what is written in standard form and say so, rather than
# guessing at every obfuscation a source might use.


def setup_argparse():
    """
    Sets up the argument parser for the command line interface.

    Returns:
        argparse.ArgumentParser: The argument parser object.
    """
    parser = argparse.ArgumentParser(description="Extracts Indicators of Compromise (IOCs) from text.")
    parser.add_argument("input", nargs="?", type=str, default="-",
                        help="Input file or '-' for stdin (default: stdin)")
    parser.add_argument("-o", "--output", type=str, help="Output file (CSV format)", required=False)
    parser.add_argument("-i", "--ioc-type", type=str, choices=['ip', 'url', 'email', 'md5', 'sha1', 'sha256', 'domain', 'all'],
                        default='all', help="Type of IOC to extract (default: all)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output (logging)")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all output except errors")

    return parser


def extract_iocs(text, ioc_type='all'):
    """
    Extracts IOCs from the given text based on the specified type.

    Args:
        text (str): The input text to analyze.
        ioc_type (str): The type of IOC to extract ('ip', 'url', 'email', 'md5', 'sha1', 'sha256', 'domain', 'all').

    Returns:
        dict: A dictionary containing lists of extracted IOCs for each type.
    """
    iocs = {
        'ip': [],
        'url': [],
        'email': [],
        'md5': [],
        'sha1': [],
        'sha256': [],
        'domain': []
    }

    # One string can legitimately appear under several types (an IP also
    # matches the URL and domain patterns). Dedup is within a type only;
    # dropping the cross type repeats would hide how the text reads.
    # sorted() because set order is hash dependent: two runs over the same
    # file should produce the same report, row for row.
    try:
        if ioc_type in ('ip', 'all'):
            iocs['ip'] = sorted(set(re.findall(IP_REGEX, text)))
        if ioc_type in ('url', 'all'):
            iocs['url'] = sorted(set(re.findall(URL_REGEX, text)))
        if ioc_type in ('email', 'all'):
            iocs['email'] = sorted(set(re.findall(EMAIL_REGEX, text)))
        # The word boundaries around the hash patterns are what stop
        # a SHA256 from also being reported as an MD5 and a SHA1: the
        # shorter pattern cannot end mid string because the next
        # character is still a hex digit, so no boundary exists there.
        if ioc_type in ('md5', 'all'):
            iocs['md5'] = sorted(set(re.findall(MD5_REGEX, text)))
        if ioc_type in ('sha1', 'all'):
            iocs['sha1'] = sorted(set(re.findall(SHA1_REGEX, text)))
        if ioc_type in ('sha256', 'all'):
            iocs['sha256'] = sorted(set(re.findall(SHA256_REGEX, text)))
        if ioc_type in ('domain', 'all'):
            iocs['domain'] = sorted(set(re.findall(DOMAIN_REGEX, text)))

    except Exception as e:
        logging.error(f"Error during IOC extraction: {e}")
        return None

    return iocs


def main():
    """
    Main function to drive the IOC extraction process.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    # Configure logging based on verbosity
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled.")
    elif args.quiet:
        logging.getLogger().setLevel(logging.ERROR)

    try:
        # Read input from file or stdin
        if args.input == "-":
            logging.debug("Reading input from stdin.")
            input_text = sys.stdin.read()
        else:
            logging.debug(f"Reading input from file: {args.input}")
            try:
                with open(args.input, 'r', encoding='utf-8') as f:
                    input_text = f.read()
            except FileNotFoundError:
                logging.error(f"Error: Input file not found: {args.input}")
                sys.exit(1)
            except Exception as e:
                logging.error(f"Error reading input file: {e}")
                sys.exit(1)

        # Extract IOCs
        iocs = extract_iocs(input_text, args.ioc_type)

        if iocs is None:
            logging.error("IOC extraction failed.")
            sys.exit(1)

        # Prepare data for output
        data = []
        for ioc_type, ioc_list in iocs.items():
            for ioc in ioc_list:
                data.append({'ioc_type': ioc_type, 'ioc_value': ioc})

        df = pd.DataFrame(data)

        # With no finds, data is empty and this frame has no columns,
        # so the CSV form is an empty file with no header row and the
        # console form is the Empty DataFrame text. A reader cannot
        # tell that apart from a broken run by the output alone; the
        # exit code stays 0 either way.
        # Output results to file or stdout
        if args.output:
            try:
                df.to_csv(args.output, index=False)
                logging.info(f"IOCs written to: {args.output}")
            except Exception as e:
                logging.error(f"Error writing to output file: {e}")
                sys.exit(1)
        else:
            if not args.quiet:
                print(df.to_string())

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
