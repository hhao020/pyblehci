#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@fn ble_parser.py

@author Stephen Finucane, 2013-2014
@email  stephenfinucane@hotmail.com

@about Version of simple-demo.py that formats the output to the
        terminal.
"""

from __future__ import print_function

import collections

from pyblehci import BLEBuilder
from pyblehci import BLEParser


def pretty(hex_string, seperator=None):
    """
    Prettify a hex string.

    >>> pretty("\x01\x02\x03\xff")
    '01 02 03 FF'
    """
    hex_string = hex_string.encode('hex')
    out = ''

    for i in range(len(hex_string)):
        if not i % 2:
            out = out + seperator
        out = out + hex_string[i].capitalize()

    return out


def print_ordered_dict(dictionary):
    result = ""
    for key in dictionary:
        if dictionary[key]:
            #convert e.g. "data_len" -> "Data Len"
            title = ' '.join(key.split("_")).title()
            if isinstance(dictionary[key], list):
                for idx2, _ in enumerate(dictionary[key]):
                    result += "{0} ({1})\n".format(title, idx2)
                    result += print_ordered_dict(dictionary[key][idx2])
            elif isinstance(dictionary[key], type(collections.OrderedDict())):
                result += '{0}\n{1}'.format(title, print_ordered_dict(
                    dictionary[key]))
            else:
                result += "{0:15}\t: {1}\n\t\t  ({2})\n".format(
                    title, pretty(dictionary[key][0], ':'), dictionary[key][1])
        else:
            result += "{0:15}\t: None".format(key)
    return result


def print_output((packet, dictionary)):
    result = print_ordered_dict(dictionary)
    result += 'Dump:\n{0}\n'.format(pretty(packet))
    return result


def test_builder():
    ble_builder = BLEBuilder()
    print(print_output(ble_builder._build_command("fe00")))
    print(print_output(ble_builder._build_command("fe31", param_id="\x15")))
    print(print_output(ble_builder._build_command("fe04", mode="\x03")))
    print(print_output(ble_builder._build_command(
        "fe09", peer_addr="\x57\x6A\xE4\x31\x18\x00")))
    print(print_output(ble_builder._build_command(
        "fd8a", conn_handle="\x00\x00", handle="\x27\x00")))
    print(print_output(ble_builder._build_command(
        "fe0a", conn_handle="\x00\x00")))

def test_parser():
    ble_parser = BLEParser()
    print(print_output(ble_parser._split_response(
        "\x04\xFF\x2C\x00\x06\x00\x06\x30\x85\x31\x18\x00\x1B\x00\x04\x00\x00\x00\x00\x00\x00\x00\x00\x09\x09\x09\x09\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x09\x09\x09\x09\x00\x00")))
    print(print_output(ble_parser._split_response(
        "\x04\xFF\x08\x7F\x06\x00\x31\xFE\x02\xD0\x07")))
    print(print_output(ble_parser._split_response(
        "\x04\xFF\x0C\x01\x06\x00\x01\x00\x00\x57\x6A\xE4\x31\x18\x00")))
    print(print_output(ble_parser._split_response(
        "\x04\xFF\x14\x01\x06\x00\x01\x00\x00\x57\x6A\xE4\x31\x18\x00\x11\x11\x11\x11\x11\x11\x11\x11")))
    print(print_output(ble_parser._split_response(
        "\x04\xFF\x07\x01\x06\x00\x00")))


if __name__ == "__main__":
    test_builder()
    test_parser()
