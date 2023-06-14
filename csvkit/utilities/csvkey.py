#!/usr/bin/env python

import sys
from konlpy.tag import Twitter
from csvkit.cleanup import RowChecker
from csvkit.cli import CSVKitUtility
import agate

class CSVKeyword(CSVKitUtility):
    description = 'Extract keywords from a text column in a CSV file.'

    def add_arguments(self):
        self.argparser.add_argument(
            '-c', '--column', dest='column',
            help='The column of the CSV file to extract keywords from.')

    def main(self):
        if self.additional_input_expected():
            sys.stderr.write('No input file or piped data provided. Waiting for standard input:\n')

        reader = agate.csv.reader(self.skip_lines(), **self.reader_kwargs)

        # Get the index of the column to extract keywords from
        header = next(reader)
        column_index = header.index(self.args.column)

        twit = Twitter()

        for row in reader:
            text = row[column_index]
            keywords = self.keyword_extractor(twit, text)
            print(keywords)

    @staticmethod
    def keyword_extractor(tagger, text):
        tokens = tagger.phrases(text)
        tokens = [token for token in tokens if len(token) > 1]  # 한 글자인 단어는 제외
        count_dict = [(token, text.count(token)) for token in tokens]
        ranked_words = sorted(count_dict, key=lambda x: x[1], reverse=True)[:10]
        return [keyword for keyword, freq in ranked_words]


def launch_new_instance():
    utility = CSVKeyword()
    utility.run()


if __name__ == '__main__':
    launch_new_instance()