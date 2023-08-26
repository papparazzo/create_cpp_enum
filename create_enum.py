"""
  Project:    create_cpp_enum
 
  Copyright (C) 2023 Stefan Paproth <pappi-@gmx.de>
 
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU Affero General Public License as
  published by the Free Software Foundation, either version 3 of the
  License, or (at your option) any later version.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
  GNU Affero General Public License for more details.
 
  You should have received a copy of the GNU Affero General Public License
  along with this program. If not, see <https://www.gnu.org/licenses/agpl.txt>.
"""

import sys
import datetime
import argparse
import re


def strip(string):
    first_index = -1
    match = re.search(r'[^A-Za-z0-9_]', string)
    if match:
        first_index = match.start()

    if first_index == -1:
        return string

    return string[:first_index]


parser = argparse.ArgumentParser(description='creates a c++ enum')
parser.add_argument('-n', '--name', dest='name', help='enum name', required=True)

args = parser.parse_args()

items = []

for line in sys.stdin:
    items.append(line.strip(' \n'))

print(f"""/*
 *  Project:    moba-lib-msghandling
 * 
 *  Copyright (C) {datetime.date.today().year} Stefan Paproth <pappi-@gmx.de>
 * 
 *  This program is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU Affero General Public License as
 *  published by the Free Software Foundation, either version 3 of the
 *  License, or (at your option) any later version.
 * 
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 *  GNU Affero General Public License for more details.
 * 
 *  You should have received a copy of the GNU Affero General Public License
 *  along with this program. If not, see <https://www.gnu.org/licenses/agpl.txt>.
 * 
 */
 
#pragma once

#include <moba-common/exception.h>
""")

print(f'enum class {args.name} {{')

for i in items:
    if i == '':
        print()
        continue
    print(f'    {i}')

print('};')
print()

print(f'inline {args.name} stringTo{args.name}Enum(const std::string &s) {{')
for i in items:
    i = strip(i)
    if i == '':
        continue

    print(f'    if(s == "{i}") {{')
    print(f'        return {args.name}::{i};')
    print('    }')

print(f'    throw moba::UnsupportedOperationException{{"{args.name}: invalid value given"}};')
print('}')
print()
print(f'inline std::string {args.name[0].lower()}{args.name[1:]}EnumToString({args.name} s) {{')
print('    switch(s) {')
for i in items:
    i = strip(i)
    if i == '':
        continue

    print(f'        case {args.name}::{i}:')
    print(f'            return "{i}";')
    print()

print('        default:')
print(f'            throw moba::UnsupportedOperationException{{"{args.name}: invalid value given"}};')
print('    }')
print('}')
