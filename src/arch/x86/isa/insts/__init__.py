# Copyright (c) 2007 The Hewlett-Packard Development Company
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# Authors: Gabe Black
import importlib

categories = ["romutil",
              "general_purpose",
              "simd128",
              "simd64",
              "system",
              "x87"]
microcode = '''
# X86 microcode
'''
for category in categories:
    cat = importlib.import_module('.' + category, package=__name__)
    microcode += cat.microcode