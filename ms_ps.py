# -*- mode: python; coding: utf-8; -*-

# ms_ps.py - simulate coalescent with partial-selfing with Hudson's ms.

# Copyright (C) 2012 Seiji Kumagai

# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice (including the next
# paragraph) shall be included in all copies or substantial portions of the
# Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import os
import sys
from subprocess import call
from scipy.stats import binom

MSPATH="./msdir/ms"

def is_exe(fpath):
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

def which(program):
    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def run_ms(args):
    program = 'ms'
    if which('ms') is None:
        if is_exe(MSPATH) is None:
            sys.exit(1)
        else:
            program = MSPATH

    command = [program]
    command.extend(args)
    if int(args[0]) > 1:
        call(command)

def adjust_args(args):
    idx = args.index('-S')
    s = float(args[idx + 1])
    p = s / (2.0 - s)
    del args[idx:idx+2]


    # Adjust demographic parameters (Nordborg & Donnelly (1997) and
    # Nordborg (2000))

    # mutation rate: \theta_eff = \theta * (2 - s) / s
    if '-t' in args:
        idx = args.index('-t')
        args[idx+1] = str(float(args[idx+1]) * (2.0 - s) / 2.0)

    # recombination: \rho_eff = \rho * (1 - s)
    if '-r' in args:
        idx = args.index('-r')
        args[idx+1] = str(float(args[idx+1]) * (1.0 - s))

    if '-I' in args:
        idx = args.index('-I')
        npops = int(args[idx + 1])
        start = idx + 2
        stop = start + npops
        for n in range(start, stop):
                # binom(int(
            args[n] = str(int(args[n]) -
                          binom.rvs(int(args[n+npops]), p))
        args[0] = str(sum([int(i) for i in args[start:stop]]))

        start += npops
        stop += npops
        del args[start:stop]
    else:
        args[0] = str(int(args[0]) -
                      binom.rvs(int(args[2]), p))
        del args[2]

    return args



if __name__ == '__main__':

    args = sys.argv[1:]

    if '-S' in args:
        # 'Partial selfing is present in a model'
        run_ms(adjust_args(args))
    else:
        # No partial-selfing.  Use ms as-is.
        run_ms(args)
