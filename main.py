from _codecs import encode
import requests
import xml.etree.ElementTree as ET

__author__ = 'andriy.matkivskiy'
__url_template__ = 'http://mymemory.translated.net/api/get?q={0}&langpair={1}|{2}'

# Required to increase translated word limit up to 10000 words/day. Paste any valid email.
__test_mail__ = ''


def main():
    tree = ET.parse('strings.xml')
    root = tree.getroot()

    for child in root:
        translated = translate(child.text)

        print 'Attr: ', child.attrib['name'], ', raw value: ', child.text, ", translated : ", translated

        child.text = translated

    save_to_file(root)

    pass


def save_to_file(root):
    text_file = open("strings_out.xml", "w")
    text_file.write(ET.tostring(root))
    text_file.close()
    pass


def translate(word):
    r = requests.get(build_url(word, 'da', 'en'))

    return r.json()['responseData']['translatedText']


def build_url(word, input_lang, output_lang):
    url = __url_template__.format(encode(word, 'utf-8'), input_lang, output_lang)

    if len(__test_mail__) > 0:
        url += '&de=' + __test_mail__

    return url


if __name__ == "__main__":
    main()
