#For Python3+

DEEPL_API_KEY = ''

import deepl
import srt

translator = deepl.Translator(deepl.RequestsAdapter(DEEPL_API_KEY))

def translate_section(text):
    target_lang_deepl = deepl.TargetLang.English_US
    translated_text = translator.translate(
        text,
        target_lang=target_lang_deepl
    )
    return translated_text

def parse_srt(file_name):
    srt_text = ''
    with open(file_name, 'r') as f:
        srt_text = f.read()
    srt_data = srt.parse(srt_text)
    return list(srt_data)

def parse_subtitle_line(srt_line_data):
    if '<font ' in srt_line_data:
        srt_line_data = srt_line_data.split('">')[1].split('</')[0]
    return srt_line_data

def main():
    srt_data = parse_srt('subs.srt')
    srt_data_copy = list(srt_data)
    for index, sub_data in enumerate(srt_data_copy):
        raw_text = parse_subtitle_line(sub_data.content)
        translated_text = translate_section(raw_text)
        srt_data[index].content = translated_text
        print('[Section {}] {} --> {}'.format(index + 1, raw_text, translated_text))
    srt_file_data = srt.compose(srt_data)
    with open('subs-processed.srt', 'w') as f:
        f.write(srt_file_data)

if __name__ == '__main__':
    main()
