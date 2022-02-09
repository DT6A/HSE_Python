import subprocess

from toughastgen import build_tree


def generate_table(data):
    return '\\begin{tabular}{' + 'c' * len(data[0]) + '}\n' + '\\\\'.join(
        map(lambda r: '&'.join(r), data)) + '\n\\end{tabular}\\\\\n' if all(
        map(lambda r: len(r) == len(data[0]), data)) else ''


def generate_image(img):
    return '\\includegraphics[width=\\textwidth]{' + img + '}\n'


def generate_latex(table, img):
    return '\\documentclass[a4paper, 12pt]{article}\n\\usepackage[utf8]{inputenc}\n\\usepackage[english]{' \
           'babel}\n\\usepackage{graphicx}\n\\begin{document}\n' + generate_table(table) + generate_image(img) + \
           '\\end{document}'


if __name__ == '__main__':
    build_tree()
    text = generate_latex([['hello', 'world', '!', 'kek'], ['this will be', 'a very long', 'string', 'kek' * 10]],
                          'artifacts/result.png')

    with open('artifacts/result.tex', 'w') as f:
        f.write(text)

    proc = subprocess.Popen(['pdflatex', '-output-directory=artifacts', 'artifacts/result.tex'])
    proc.communicate()

