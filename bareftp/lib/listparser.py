from __future__ import division
from lib.ftpfile import FtpFile
import sys
from datetime import datetime, timedelta


def parse_list_unix(list):
    files = []

    now = datetime.now()
    current_year = now.year

    for line in list:
        if line.startswith('total') or line.strip() == '':
            continue

        fields = get_fields(line)

        # field position
        idx = 0
        permissions = fields[idx]

        _is_dir = permissions.startswith('d')
        _is_link = permissions.startswith('l')

        idx += 1
        linkcount = 0
        if fields[idx][0].isdigit():
            try:
                linkcount = int(fields[idx])
            except:
                pass
        elif fields[idx][0] == '-':
            idx += 1

        # user and group
        idx += 1
        user = fields[idx]
        idx += 1
        group = fields[idx]

        # size
        idx += 1
        size = 0
        sizestr = fields[idx]
        # rearrange fields for listings without user
        if not sizestr[0].isdigit() and group[0].isdigit():
            sizestr = group
            group = user
            user = ''
        else:
            idx += 1

        if sys.version[0] == '3':
            size = int(sizestr)
        else:
            size = long(sizestr)

        lastmodified = None
        if fields[idx][0].isdigit():
            idx += 1

        datetimepos = idx
        timestr = fields[idx]
        idx += 1
        timestr += fields[idx]
        idx += 1
        timestr += fields[idx]

        try:
            if timestr.find(':') > 0:
                timestr += str(current_year)
                lastmodified = datetime.strptime(timestr, '%b%d%H:%M%Y')
            else:
                lastmodified = datetime.strptime(timestr, '%b%d%Y')

            if lastmodified > timedelta(days=2) + now:
                lastmodified = lastmodified + timedelta(weeks=-52)
        except:
            print timestr
            lastmodified = ''

        name = ''
        linkedname = ''
        pos = 0
        ok = True

        for i in range(datetimepos, datetimepos + 3):
            pos = line.find(fields[i], pos)
            if pos < 0:
                ok = False
                break
            else:
                pos += len(fields[i])
        if ok:
            remainder = line[pos:]
            if not _is_link:
                name = remainder
            else:
                pos = remainder.find('->')
                if pos <= 0:
                    name = remainder
                else:
                    name = remainder[0:pos].strip()
                    if pos + 2 < len(remainder):
                        linkedname = remainder[pos+2:].strip()

        f = FtpFile()
        f.isdir = _is_dir
        f.islink = _is_link
        #f.filename = unicode(name.strip())
        f.filename = name.strip()
        f.linkdest = linkedname
        if sys.version[0] == '3':
            f.size = int(size)
        else:
            f.size = long(size)
        f.lastmodified = lastmodified
        f.owner = user
        f.group = group
        f.permissions = permissions
        files.append(f)

    return files


def parse_list_mlsd(list):
    pass


def parse_list_win(list):
    files = []

    for line in list:
        if line.strip() == '':
            continue

        fields = get_fields(line)

        lastmodified = datetime.strptime(fields[0] + " " + fields[1], '%m-%d-%y %I:%M%p')
        _isdir = False
        _size = 0
        if fields[2].upper() == "<DIR>":
            _isdir = True
        else:
            _size = int(fields[2])

        ok = True
        pos = 0
        for i in range(pos, 3):
            pos = line.find(fields[i], pos)
            if pos < 0:
                ok = False
                break
            else:
                pos += len(fields[i])
        if ok:
            f = FtpFile()
            f.isdir = _isdir
            f.islink = False
            f.filename = line[pos:].strip()
            f.linkdest = ''
            if sys.version[0] == '3':
                f.size = int(_size)
            else:
                f.size = long(_size)
            f.lastmodified = lastmodified
            f.owner = ''
            f.group = ''
            f.permissions = ''
            files.append(f)

    return files


def parse_list(list):
    if list is None:
        return None

    teststr = ''
    for line in list:
        if line is not '':
            teststr = line
            break

    if teststr.startswith('-') or teststr.startswith('d') or teststr.startswith('l') or teststr.startswith('total'):
        return parse_list_unix(list)
    elif teststr.startswith('type='):
        return parse_list_mlsd(list)
    else:
        return parse_list_win(list)


def get_fields(line):
    fields = []
    field = []
    for c in line:
        if not c == ' ':
            field.append(c)
        else:
            if len(field) > 0:
                fields.append(''.join(field))
                field = []
    if len(field) > 0:
        fields.append(''.join(field))
    return fields

