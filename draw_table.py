import sys
import pickle
from PyQt4 import QtCore, QtGui
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import ImageFormatter
from pygments.styles import get_style_by_name


def get_image_name(count):
    return 'snippet%s.png' % (count)


def render_source_images(data):
    count = 0
    for snippet, setup, _, _ in data:
        fname = get_image_name(count)
        f = open(fname, 'wb')
        lexer = PythonLexer()
        style = get_style_by_name('emacs')
        formatter = ImageFormatter(line_numbers=False,
            font_name='Source Code Pro', font_size=14, style=style)
        if setup == 'pass':
            code = snippet
        else:
            code = '# Setup code\n%s\n# Code being measured\n%s' % (setup, snippet)
        highlight(code, lexer, formatter, outfile=f)
        f.close()
        count += 1


# Data presentation
def draw_table(data, filename, line_width=1):
    """ Save timing data as a table in png format

    Parameters
    ----------
    data : sequence of sequence
        Each entry is (snippet, setup, t, timerep(t))
    filename : string
        Name of file to save table
    line_width : integer
        Width of line drawn between different entries in the
        table
    """
    app = QtGui.QApplication(sys.argv)
    img_names = [get_image_name(idx) for idx in xrange(len(data))]
    f_pixmaps = [QtGui.QPixmap(img_name) for img_name in img_names]
    pmap_height = sum([pmap.height() for pmap in f_pixmaps])
    height = pmap_height + line_width * len(f_pixmaps)
    col_zero_width = max([pixmap.width() for pixmap in f_pixmaps])
    width = col_zero_width + 125
    pixmap = QtGui.QPixmap(width, height)
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
    font = QtGui.QFont("Source Code Pro", 12, QtGui.QFont.Normal);
    painter.setFont(font)
    painter.setBrush(QtGui.QColor(255, 255, 255))
    painter.fillRect(0, 0, width, height, QtGui.QColor(255, 255, 255))
    pen = QtGui.QPen(QtGui.QColor(0, 0, 0), line_width, QtCore.Qt.SolidLine)
    painter.setPen(pen)
    y = 0
    count = 0
    text_margin = 5
    for entry in data:
        fname = get_image_name(count)
        f_pixmap = QtGui.QPixmap(fname)
        painter.drawPixmap(0, y, f_pixmap)
        text_height = int(y + (f_pixmaps[count].height() / 2.0))
        painter.fillRect(col_zero_width, y, 300, f_pixmaps[count].height(),
            QtGui.QColor(245, 255, 245))
        painter.drawText(col_zero_width + text_margin, text_height, entry[-1])
        y += f_pixmap.height()
        if y > 0:
            painter.drawLine(0, y, width, y)
        y += line_width
        count += 1
    pixmap.save(filename)
    painter.end()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print sys.argv
        print 'Usage: python draw_table.py data_filename output.png'
    else:
        data_fname, png_fname = sys.argv[1], sys.argv[2]
        f = open(data_fname, 'rb')
        data = pickle.load(f)
        f.close()
        render_source_images(data)
        draw_table(data, png_fname)