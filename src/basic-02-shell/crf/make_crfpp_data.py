#!/usr/bin/env python
# coding: utf-8

# In[20]:

import sys
import os
import codecs
import optparse


def make_crf_data(input_file, output_file):
    with codecs.open(input_file, 'r', 'utf-8') as f:
        with codecs.open(output_file, 'w', 'utf-8') as outf:
            arr = f.readlines()
            i = 0
            for a in arr:
                i += 1
                a = a.strip()
                if a == "":
                    continue
                words = a.split()
                words = words
                if len(words) == 0:
                    continue
                tags = ["S"] * len(words)
                # pos = 0
                # print(words)
                w = [ix.rsplit('/', 1)[0] for ix in words]
                t = [ix.rsplit('/', 1)[1] for ix in words]
                # tags_unique = list(set(t))
                # pos = 0
                # wp = w[pos]
                # tp = t[pos]
                # print(tags_unique)
                for p in range(0, len(w)):
                    if p < len(w) - 1:
                        if t[p] == t[p + 1] and \
                            (p == 0 or p > 0 and
                             t[p - 1] != t[p]):
                            tags[p] = "B"
                            for sp in range(p + 1, len(w)):
                                if t[p] == t[sp]:
                                    if sp >= len(w) - 1 or t[sp + 1] != t[sp]:
                                        tags[sp] = "E"
                                        break
                                    tags[sp] = "I"
                # for p in range(0,len(w)):
                    # print(w[p],'\t',t[p],'\t',tags[p])
                for p in range(0, len(w)):
                    # outf.write(("%s\t%s\t%s\n") % (w[p], t[p], tags[p]))
                    if t[p] == "FSEP":
                       continue
                    outf.write(("%s %s %s\n") % (w[p], t[p], tags[p]+"_"+t[p]))
                outf.write("\n")


if __name__ == '__main__':
    parser = optparse.OptionParser()
    input_file = os.path.join(os.getcwd(), "input.data")
    output_file = os.path.join(os.getcwd(), "output.data")
    parser.add_option('-i', '--input', 
                      help="input file", default=input_file)
    parser.add_option('-o', '--output', 
                      help="output file", default=output_file)
    options, args = parser.parse_args()

    make_crf_data(options.input, options.output)
