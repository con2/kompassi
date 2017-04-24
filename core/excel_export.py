import io

import xlsxwriter


class XlsxWriter(object):
    """
    An almost csv.writer compatible wrapper for XlsxWriter. Horribly inefficient.

    Must .close() to get the data actually written. Use getattr(writer, 'must_close', False)
    to distinguish from an actual csv.writer.
    """

    def __init__(self, output_stream):
        self.row = 0
        self.output_stream = output_stream
        self.buf = io.BytesIO()
        self.workbook = xlsxwriter.Workbook(self.buf)
        self.worksheet = self.workbook.add_worksheet()
        self.must_close = True

    def writerow(self, row):
        for col, value in enumerate(row):
            if isinstance(value, str):
                # Workaround to avoid corner case bug that triggers (when all of the following)
                # - value starts with http:// (write interprets it as URL)
                # - value is longer than 255 chars
                # - value contains characters with ordinal not in range(0, 128)
                self.worksheet.write_string(self.row, col, value)
            else:
                self.worksheet.write(self.row, col, value)

        self.row += 1

    def close(self):
        self.workbook.close()
        self.buf.seek(0)
        self.output_stream.write(self.buf.read())
        self.buf.close()
