from marcds.importer.expert import DataPageRecognizer
from marcds.importer import djvu


class NoIssueDataException(Exception):
    pass


class DJVUtoMARC(object):
    """Recognize issue data in a DJVU file.
    """

    def __init__(self, filename):
        self.filename = filename
        self.context = djvu.Context()
        self.document = self.context.document(filename)

    def issue_data(self, noexc=True):
        r = DataPageRecognizer(
            self.filename, context=self.context, document=self.document)
        r.reset()
        r.run()
        if r.issue_data is None:
            if noexc:
                return None
            else:
                raise NoIssueDataException()

        idata = r.issue_data
        self.isbn = r.isbn
        page = idata["page"]

        for p in self.context.by_sexpr(sexprs=["page"],
                                       document=self.document,
                                       # start=page,
                                       # end=page + 1
                                       start=page,
                                       end=page + 2
                                       ):
            start, end = idata["start"], idata["end"]
            #print(p[1], start, end)
            lines = p[1].split("\n")[start:end + 1]
            # print("\n".join(lines))
            self.lines = lines
            self.issue_data

        return True

    def query_with_isbn(self, services=None, format=None):
        from isbnlib import meta
        from isbnlib.registry import bibformatters
        if self.isbn is None:
            raise ValueError("no isbn recognized")

        if services is None:
            services = ("default",)

        rc = {}
        if format is None:
            def formatter(x):
                return x
        else:
            formatter = bibformatters[format]

        for serv in services:
            data = meta(self.isbn)
            if data is not None:
                rc[serv] = formatter(data)

        return rc
