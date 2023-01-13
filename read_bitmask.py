#!/usr/bin/env python

#
# BSD 3-Clause License
#
# Copyright (c) 2018, Litrin Jiang
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# * Neither the name of the copyright holder nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

import optparse
import sys


class BitMask(int):

    def __str__(self):
        offset, step = 0, 0
        desc = []

        def fmt(curr_core, step):
            step -= 1
            if step == 0:
                return "%s" % (curr_core)
            if step == 1:
                return "%s,%s" % (curr_core - 1, curr_core)
            return "%s-%s" % (curr_core - step, curr_core)

        while offset <= self.bit_length():
            if 1 << offset & self:
                step += 1
            elif step > 0:
                desc.append(fmt(offset - 1, step))
                step = 0

            offset += 1

        return ",".join(desc)


def main():
    parser = optparse.OptionParser()
    parser.add_option("-x", "--hex", dest="hex", action="store_true",
                      default=True, help="HEX format input")

    parser.add_option("-o", "--oct", dest="oct", action="store_true",
                      default=False, help="OCT format input")

    parser.add_option("-d", "--dec", dest="dec", action="store_true",
                      default=False, help="DEC format input")

    parser.add_option("-b", "--bin", dest="binary", action="store_true",
                      default=False, help="DEC format input")

    (options, args) = parser.parse_args()

    raw_input = sys.stdin.readline()

    if options.dec:
        mask = BitMask(raw_input)
    elif options.oct:
        mask = BitMask(raw_input, 8)
    elif options.binary:
        mask = BitMask(raw_input, 2)
    else:
        mask = BitMask(raw_input, 16)

    return mask


if __name__ == "__main__":
    print(main())
