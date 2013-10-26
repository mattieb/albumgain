#!/usr/bin/env python
#
# Copyright (c) 2010 Matt Behrens.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import fnmatch, getopt, re, os, sys

import ape2id3

filetypes = {
        'mp3': ('*.mp3', ['mp3gain', '-k']),
        'ogg': ('*.ogg', ['vorbisgain', '-f', '-a'])
        }

opts, args = getopt.getopt(sys.argv[1:], 'gdt:')
filetype = None
dry_run = False
show_groups = False
for o, a in opts:
    if o == '-d':
        dry_run = True
    if o == '-g':
        show_groups = True
    if o == '-t':
        filetype = filetypes[a]
if filetype is None:
    raise SyntaxError, 'must specify filetype with -t'

disc_strip = re.compile(r'(.+) \((.+ )?disc( .+)?\)')
part_strip = re.compile(r'(.+), Part ')
vol_strip = re.compile(r'(.+), Volume ')

groups = {}
for top in args:
    for dirpath, dirnames, filenames in os.walk(top):
        group = [os.path.join(dirpath, filename) for filename
                    in fnmatch.filter(filenames, filetype[0])]
        if group:
            m = disc_strip.match(dirpath)
            if m:
                groupname = m.group(1)
            else:
                m = part_strip.match(dirpath)
                if m:
                    groupname = m.group(1)
                else:
                    m = vol_strip.match(dirpath)
                    if m:
                        groupname = m.group(1)
                    else:
                        groupname = dirpath
            groups[groupname] = groups.get(groupname, []) + group

apelog = ape2id3.Logger(3, sys.argv[0])
ape2id3 = ape2id3.Ape2Id3(apelog, force=True, id3v23=True)

for groupname, group in groups.items():
    if dry_run:
        sys.stderr.write("==> %r\n" % (filetype[1] + group))
    elif show_groups:
        sys.stderr.write(groupname + '\n')
    else:
        if os.spawnvp(os.P_WAIT, filetype[1][0], filetype[1] + group):
            sys.exit(1)
        if filetype[0] == '*.mp3':
            for filename in group:
                ape2id3.copy_replaygain_tags(filename)

# ex:et:sw=4:ts=4
