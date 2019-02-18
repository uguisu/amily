import io

utf8_with_bom = b'\xef\xbb\xbf'

# file_name_in = 'iris.csv'
file_name_in = 'iris_with_bom.csv'
file_name_out = 'iris_result.csv'

line_in = io.open(file_name_in, 'rb')
line_out = io.open(file_name_out, 'w', encoding='utf-8', newline='\n')

# verify whether the file is encoded as 'utf8 bom'
is_utf8_with_bom = line_in.read(3) == utf8_with_bom

if is_utf8_with_bom:
    print('detecting bom')

    line_in.close()
    line_in = io.open(file_name_in, 'rb')

    is_header = True

    for l in line_in.readlines():
        if is_header:
            is_header = False
            # remove "BOM" tag
            l = l[3:]

        line_out.write(l.decode('utf-8').replace('\r\n', '\n'))

else:
    print('without bom')

    line_in.close()
    line_in = io.open(file_name_in, 'r')

    for l in line_in.readlines():
        line_out.write(l)
