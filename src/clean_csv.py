#!/usr/bin/python
# -*- coding: UTF-8 -*-
import io
import sys

utf8_with_bom = b'\xef\xbb\xbf'
target_path = '/var/tmp/'


def get_output_file_name(input_file_name):
    """
    Get output file full path & name via input file
    :param input_file_name: input file
    :return: output file full path & name
    """
    f_ls = input_file_name.split('/')
    rtn = f_ls[len(f_ls) - 1]

    return target_path + rtn


def get_file_handle(f_name):
    """
    Open file in default way
    :param f_name: file name
    :return: file handle
    """
    return io.open(f_name, 'r')


def get_file_handle_in_binary(f_name):
    """
    Open file in binary
    :param f_name: file name
    :return: file handle
    """
    return io.open(f_name, 'rb')


def replace(line_val, seq):
    """
    Replace special characters
    :param line_val: line as string
    :param seq: sequence number
    :return: changed value
    """
    # replace TAB to ','
    rtn = line_val.replace('\t', ',')
    # remove line break
    rtn = rtn.replace('\r\n', '')
    rtn = rtn.replace('\n', '')
    # verify if there is a 'NULL' or 'ZZ' row
    _tmp_lst = rtn.split(',')
    for _tmp in _tmp_lst:
        _tmp = _tmp.strip().upper()
        if 'NULL' == _tmp or 'ZZ' == _tmp:
            # print('[warning] Find empty line, remove it')
            rtn = None
            break

    if rtn is not None:
        _tmp_lst.append(str(seq))
        rtn = ','.join(_tmp_lst)
        rtn = rtn + '\n'

    return rtn


file_name_in = sys.argv[1]
file_name_out = get_output_file_name(file_name_in)

line_in = get_file_handle_in_binary(file_name_in)
line_out = io.open(file_name_out, 'w', encoding='utf-8', newline='\n')

# verify whether the file is encoded as 'utf8 bom'
is_utf8_with_bom = line_in.read(3) == utf8_with_bom

if is_utf8_with_bom:

    line_in.close()
    line_in = get_file_handle_in_binary(file_name_in)

    is_header = True
    seq = 0

    for l in line_in.readlines():
        if is_header:
            is_header = False
            # remove "BOM" tag
            l = l[3:]

        seq = seq + 1
        line_to_write = replace(l.decode('utf-8'), seq=seq)
        if line_to_write is not None:
            line_out.write(line_to_write)

else:
    line_in.close()
    line_in = get_file_handle(file_name_in)

    seq = 0
    for l in line_in.readlines():
        seq = seq + 1
        line_to_write = replace(l, seq=seq)
        if line_to_write is not None:
            line_out.write(line_to_write)
