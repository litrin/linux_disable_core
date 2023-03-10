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

if sys.platform != "linux":
    raise OSError("This tool is for Linux only")

ONLINE_FILE = r"/sys/devices/system/cpu/cpu%d/online"
SIBLING_FILE = "/sys/devices/system/cpu/cpu%d/topology/thread_siblings_list"
enable = '1'
disable = '0'


class CPUcores(int):

    @staticmethod
    def from_bit(b):
        return CPUcores(b, 2)

    @staticmethod
    def from_hex(h):
        return CPUcores(h, 16)

    @staticmethod
    def from_desc(core_desc):
        cores = 0
        begin, end = -1, -1
        tmp = 0

        def set_mask(b, e):
            src = 0
            if b == -1:
                b = e
            if b > e:
                b, e = e, b
            for i in range(b, e + 1):
                src = src | (1 << i)
            return src

        for s in core_desc:
            c = ord(s)
            if 47 < c and 58 > c:
                tmp = tmp * 10 + c - 48
                continue

            end = tmp
            if begin == -1:
                begin = tmp

            if c != 45:
                cores |= set_mask(begin, end)
                begin = -1

            tmp = 0

        cores |= set_mask(begin, tmp)
        return CPUcores(cores)

    def __str__(self):
        core_id, step = 0, 0
        desc = []

        def fmt(curr_core, step):
            step -= 1
            if step == 0:
                return "%s" % (curr_core)
            if step == 1:
                return "%s,%s" % (curr_core - 1, curr_core)
            return "%s-%s" % (curr_core - step, curr_core)

        while core_id <= self.bit_length():
            if 1 << core_id & self:
                step += 1
            elif step > 0:
                desc.append(fmt(core_id - 1, step))
                step = 0

            core_id += 1

        return ",".join(desc)

    def __iter__(self):
        core_id = 0
        while core_id <= self.bit_length():
            if 1 << core_id & self:
                yield core_id
            core_id += 1

    def __len__(self):
        tmp, length = self, 0
        while tmp > 0:
            length += 1
            tmp &= (tmp - 1)

        return length

    def all_cores(self):
        return ",".join(map(str, self))


def set_online(core_id, online=enable):
    filename = ONLINE_FILE % core_id
    try:
        fd = open(filename, "w")
        fd.write(online)
        fd.close()
        return True
    except:
        raise OSError("CPU#%d cannot be accessed!" % core_id)


def get_siblings(core_id):
    filename = SIBLING_FILE % core_id
    fd = open(filename, "r")
    sibling_content = fd.readline()

    return map(int, sibling_content.split(","))


def main():
    parser = optparse.OptionParser()
    parser.add_option("-e", "--enable", dest="enable", action="store",
                      type="string", help="input core set for enabling")

    parser.add_option("-d", "--disable", dest="disable", action="store",
                      type="string", help="input core set for disabling")

    (options, args) = parser.parse_args()

    if options.enable is not None:
        core_set = CPUcores.from_desc(options.enable)
        online = enable
    elif options.disable is not None:
        core_set = CPUcores.from_desc(options.disable)
        online = disable
    else:
        exit(0)

    for core in core_set:
        set_online(core, online)

    exit(0)


if __name__ == "__main__":
    main()
