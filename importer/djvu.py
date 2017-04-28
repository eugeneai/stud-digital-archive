from __future__ import print_function

import os
import sys

import djvu.decode
import codecs


class Context(djvu.decode.Context):

    def handle_message(self, message):
        if isinstance(message, djvu.decode.ErrorMessage):
            print(message, file=sys.stderr)
            # Exceptions in handle_message() are ignored, so sys.exit()
            # wouldn't work here.
            os._exit(1)

    def process(self, path, assexpr=False):
        document = self.new_document(djvu.decode.FileURI(path))
        document.decoding_job.wait()
        for page in document.pages:
            page.get_info()
            # print_text(page.text.sexpr)
            if assexpr:
                yield page.text.sexpr
            else:
                yield from self.interp(page.text.sexpr)

    def get_text(self, sexpr, level=0):
        if level > 0:
            yield ' ' * (2 * level - 1)
        if isinstance(sexpr, djvu.sexpr.ListExpression):
            if len(sexpr) == 0:
                return
            yield (str(sexpr[0].value), [s.value for s in sexpr[1:]])
            for child in sexpr:
                yield from self.get_text(child, level + 1)
        else:
            yield (sexpr)

    def interp_args(self, symb, args):
        for arg in args:
            yield from self.interp(arg)

    def interp(self, sexpr):
        if not sexpr:
            return
        symb = str(sexpr[0].value)
        # print(help(symb))

        x1 = sexpr[1]
        y1 = sexpr[2]
        x2 = sexpr[3]
        y2 = sexpr[4]
        args = sexpr[5:]

        if symb in ["page", "para", "line"]:
            yield symb, None
            yield from self.interp_args(symb, args)
        elif symb == "word":
            a = (args[0].bytes).decode("utf8")
            yield symb, a


def main():
    if len(sys.argv) != 2:
        print(
            'Usage: {prog} <djvu-file>'.format(prog=sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    context = Context()
    context.process(sys.argv[1])

# if __name__ == '__main__':
#    main()