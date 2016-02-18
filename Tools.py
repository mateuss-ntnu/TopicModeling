import os
import errno
import re


def count_articles(path):
    f = open(path)
    line = f.readline()
    count = 0
    while line:
        # assume there's one document per line, tokens separated by whitespace
        # yield dictionary.doc2bow(line.lower().split())
        start_line_pattern = re.compile("<doc.*>")
        # endlinePattern = re.compile("</doc>")
        if start_line_pattern.match(line):
            count += 1
    f.close()
    return count


def count_article_hierarcy(paths_list):
    for path in paths_list:
        f = open(path)
        line = f.readline()
        count = 0
        while line:
            # assume there's one document per line, tokens separated by whitespace
            # yield dictionary.doc2bow(line.lower().split())
            start_line_pattern = re.compile("<doc.*>")
            # endlinePattern = re.compile("</doc>")
            if start_line_pattern.match(line):
                count += 1
        f.close()
        return count


def create_folder_if_not_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise
