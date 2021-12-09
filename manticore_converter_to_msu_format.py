#!/usr/bin/env python3
import os

def convert_to_msu(file_path=''):
    print('Start convertation to MSU format!')
    if not os.path.isfile(file_path):
        print(file_path, " file read ERROR!")
        return -1

    with open(file_path, 'r') as fin_file:
        lines_list = fin_file.readlines()

    events_dict = dict()
    print(' Input file ', file_path, ' reading ...')
    for line in lines_list:
        split_line = line.split()
        if len(split_line) > 0:
            if split_line[0] == "Event_number":
                ev_id = split_line[1]
                events_dict[ev_id] = list()
            else:
                events_dict[ev_id].append(split_line)

    print(' Converting and writing to the file ', file_path, '...')
    with open(file_path+'.msu', 'w') as out_file:
        for ev_id, clrs_list in events_dict.items():
            clrs_num = len(events_dict[ev_id])
            out_file.write('{}{}\n'.format(' '*(3-len(str(clrs_num))),clrs_num))
            for clr in clrs_list:
                clr_id = clr[0]
                clr_time = clr[1]
                clr_amps = clr[2:]
                out_file.write("{}{}{}{}   {}\n".format(' '*(2-len(clr_id)), \
                                int(clr_id)+1, ' '*(11-len(ev_id)), ev_id, clr_time))
                counter = 0
                out_file.write('   ')
                for i in range(0, len(clr_amps), 2):
                    amp = int(float(clr_amps[i]))
                    chanel_id = int(clr_amps[i+1])
                    if chanel_id == 0:
                        out_file.write('{}  0   '.format(amp))
                        out_file.write('-11  1   ')
                    else:
                        out_file.write('451  0   ')
                        out_file.write('{}  1   '.format(amp))
                    counter += 4
                    if counter % 16 == 0:
                        out_file.write('\n')
                        if counter < 8*16:
                            out_file.write('   ')
    print('End convertation to MSU format: from ', file_path,\
          ' to ', file_path+'.m'\
         )
    return 0
