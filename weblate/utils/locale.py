# -*- coding: utf-8 -*-
#
# Copyright © 2012 - 2019 Michal Čihař <michal@cihar.com>
#
# This file is part of Weblate <https://weblate.org/>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from __future__ import absolute_import

from locale import setlocale, getlocale, LC_ALL, Error
from contextlib import contextmanager


@contextmanager
def c_locale():
    """Context to execute something in C locale."""
    locales = [
        ('C', 'UTF-8'),
        ('en_US', 'UTF-8'),
        '',
    ]
    try:
        currlocale = getlocale()
        print('Orig locale {}'.format(currlocale))
        if currlocale[0]:
            locales.insert(0, currlocale)
    except Error:
        pass
    setlocale(LC_ALL, 'C')
    print('Locale reset to C')
    yield
    for currlocale in locales:
        try:
            setlocale(LC_ALL, currlocale)
        except Error:
            continue
        if getlocale()[0]:
            print('Reverted locale to {}'.format(getlocale()))
            break