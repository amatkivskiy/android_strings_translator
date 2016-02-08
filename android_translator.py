from _codecs import encode
import traceback
import xml.etree.ElementTree as ET
import argparse
import sys

try:
    import requests
except ImportError:
    raise ImportError('You should install \'requests\' dependency (pip install requests or easy_install requests) '
                      'library for this script to work')

__author__ = 'amatkivskiy'
__url_template__ = 'http://mymemory.translated.net/api/get?q={0}&langpair={1}|{2}'


def main(args):
    tree = ET.parse(args.input)
    root = tree.getroot()

    if args.verbose:
        print "Script arguments: " + str(args)

    for child in root:

        try:
            translated = translate(child.text, args.input_lang, args.output_lang, args.email)
        except:
            print 'Failed tp translate [' + child.attrib['name'] + '] because -> '
            traceback.print_exc(sys.exc_info()[0])
            continue

        if args.verbose:
            log(child, translated)

        child.text = translated

    save_to_file(root, args.output)

    pass


def save_to_file(root, output):
    text_file = open(output, "w")
    text_file.write(ET.tostring(root))
    text_file.close()

    pass


def log(child, translated):
    print child.attrib['name'], ': ', child.text, ' -> ', translated

    pass


def translate(word, input_lang, output_lang, email):
    r = requests.get(build_url(word, input_lang, output_lang, email))

    return r.json()['responseData']['translatedText']


def build_url(word, input_lang, output_lang, email):
    url = __url_template__.format(encode(word, 'utf-8'), input_lang, output_lang)

    if email is not None:
        url += '&de=' + email

    return url


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=""" This script automatically translates provided android string
        resource file into specified language. It uses http://mymemory.translated.net/doc/ API""")
    parser.add_argument('-i', '--input', help='Input file name', required=True)
    parser.add_argument('-o', '--output', help='Output file name', required=True)

    parser.add_argument('-il', '--input_lang', help='Input language. Use ISO standard names or RFC3066', required=True)
    parser.add_argument('-ol', '--output_lang', help='Output language. Use ISO standard names or RFC3066',
                        required=True)

    parser.add_argument('-e', '--email', help="""Valid email. Used when larger word limit required.
    For more information read : http://mymemory.translated.net/doc/usagelimits.php""", required=False)

    parser.add_argument('-v', '--verbose', help='Enable logging', required=False, action='store_true')

    main(parser.parse_args())
