import re
import sys


def parse_line(line: str) -> str:
    if (match := re.match(r'.item\[(?P<name>\w*?)\]\s*(?P<ja>.*?)\s*\\\\\s*\((?P<en>.*?)\)', line)):
        data = dict(
            name=match.group('name'),
            ja=match.group('ja').replace('\\jablank', '・・・ ・・・ ・・・'),
            en=match.group('en')
        )
        return f'''
        <p class="dialogue">
            <span class="speaker">{data["name"]}</span>
            <span class="japanese">{data["ja"]}</span> <br/>
            <span class="english">{data["en"]}</span>
        </p>'''
    elif line.strip() == '':
        return ''
    elif line.startswith('\\SD'):
        direction = re.fullmatch(r'\\SD{(.*)?}', line).group(1)
        return f'''<p class="stage-direction">{direction}</p>\n'''
    elif line.startswith('\\vskip'):
        return '&nbsp;\n'
    else:
        return f'''
        <!-- UNHANDLED TEXT! -->
        <p>
            {line}
        </p>
        '''


def main(block: str):
    with open('html-output.html', 'w+') as f:
        for line in block.splitlines():
            f.write(parse_line(line))


if __name__ == '__main__':
    block = sys.stdin.read()
    main(block)


# \item[VAYNE] \jablank 君は、だれ？ \\ (......Who are you?)
# \item[SULPHER] 名前を聞いているのか？・・・サルファ、だ。 \\ (Do you mean my name? ...It's Sulpher.)
# \item[VAYNE] サルファ・・・君も、一人ぼっちなの？ \\ (Sulpher ... Are you all alone, too?)
# \item[SULPHER] ・・・ああ。お前とおなじだ。 \\ (... Yes, just like you.)
# \item[VAYNE] そっか・・・一緒にはいてもいいかな？ \\ (I see ... Can I stay with you?)
# \item[SULPHER] ・・・そうだな・それも思くない。\\ (... Sure. That's not a bad idea.)
# \item[VAYNE] ありがと。えっと、僕は・・・ \\ (Thank you. Um, I'm ...)
# \item[SULPHER] ヴェイン、だ。あいつがそう読んでいた \\ (Vayne. That's what he called you.)
# \item[VAYNE] ヴェイン・・・僕の、名前・・・ \\ (Vayne ... is my name ...)
