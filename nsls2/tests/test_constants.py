# ######################################################################
# Copyright (c) 2014, Brookhaven Science Associates, Brookhaven        #
# National Laboratory. All rights reserved.                            #
#                                                                      #
# @author: Li Li (lili@bnl.gov)                                        #
# created on 08/19/2014                                                #
#                                                                      #
# Redistribution and use in source and binary forms, with or without   #
# modification, are permitted provided that the following conditions   #
# are met:                                                             #
#                                                                      #
# * Redistributions of source code must retain the above copyright     #
#   notice, this list of conditions and the following disclaimer.      #
#                                                                      #
# * Redistributions in binary form must reproduce the above copyright  #
#   notice this list of conditions and the following disclaimer in     #
#   the documentation and/or other materials provided with the         #
#   distribution.                                                      #
#                                                                      #
# * Neither the name of the Brookhaven Science Associates, Brookhaven  #
#   National Laboratory nor the names of its contributors may be used  #
#   to endorse or promote products derived from this software without  #
#   specific prior written permission.                                 #
#                                                                      #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS  #
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT    #
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS    #
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE       #
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,           #
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES   #
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR   #
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)   #
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,  #
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OTHERWISE) ARISING   #
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE   #
# POSSIBILITY OF SUCH DAMAGE.                                          #
########################################################################


from __future__ import (absolute_import, division,
                        unicode_literals, print_function)
import six
import numpy as np
from numpy.testing import assert_array_equal, assert_array_almost_equal
from nose.tools import assert_equal

from nsls2.constants import (Element, emission_line_search,
                             calibration_standards, HKL)
from nsls2.core import (q_to_d, d_to_q)


def test_element_data():
    """
    smoke test of all elements
    """

    data1 = []
    data2 = []

    name_list = []
    for i in range(100):
        e = Element(i+1)
        data1.append(e.cs(10)['Ka1'])
        name_list.append(e.name)

    for item in name_list:
        e = Element(item)
        data2.append(e.cs(10)['Ka1'])

    assert_array_equal(data1, data2)

    return


def test_element_finder():

    true_name = sorted(['Eu', 'Cu'])
    out = emission_line_search(8, 0.05, 10)
    found_name = sorted(list(six.iterkeys(out)))
    assert_equal(true_name, found_name)
    return


def smoke_test_powder_standard():
    name = 'Si'
    cal = calibration_standards[name]
    assert(name == cal.name)

    for d, hkl, q in cal:
        assert_array_almost_equal(d_to_q(d), q)
        assert_array_almost_equal(q_to_d(q), d)
        assert_array_equal(np.linalg.norm(hkl), hkl.length)

    assert_equal(str(cal), "Calibration standard: Si")
    assert_equal(len(cal), 11)


def test_hkl():
    a = HKL(1, 1, 1)
    b = HKL('1', '1', '1')
    c = HKL(h='1', k='1', l='1')
    d = HKL(1.5, 1.5, 1.75)
    assert_equal(a, b)
    assert_equal(a, c)
    assert_equal(a, d)