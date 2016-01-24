#!/usr/bin/env python
class IPList():

    def __init__(self, upborder = 254):
        self._upborder = upborder
        self.iplist = [{'start': 1, 'end': upborder}]

    def getnext(self):
        if self.iplist == []:
            return None
        first_tup = self.iplist[0]
        if first_tup['start'] == first_tup['end']:
            self.iplist.pop(0)
            return first_tup['start']
        first_tup = self.iplist[0]
        self.iplist[0] = {'start': first_tup['start'] + 1, 'end': first_tup['end']}
        return first_tup['start']

    def get(self, num):
        if num > self._upborder:
            return None
        new_list = []
        find = False
        for tup in self.iplist:
            new_tup = self._change_tuple(num, tup)
            if new_tup[0]:
                find = True
            if not new_tup[1]:
                continue
            new_list.extend(new_tup[1])
        self.iplist = new_list[:]
        if find:
            return num
        return None
    
    def _change_tuple(self, num, tup):
        find = False
        if num not in range(tup['start'], tup['end']+1):
            return ( find, [tup] )
        find = True
        if tup['end'] == tup['start']:
            return ( find, None ) 
        if num == tup['start']:
            return ( find, [{'start': tup['start'] + 1, 'end': tup['end']}] )
        if num == tup['end']:
            return ( find, [{'start': tup['start'], 'end': tup['end'] - 1}] )
        return ( find, [{'start': tup['start'], 'end': num-1}, {'start': num+1, 'end': tup['end']}] )

    def __str__(self):
        return str(self.iplist)
    
    def set_border(self, border):
        last_tup = self.iplist[-1]
        if last_tup['start'] > border:
            return False
        self._upborder = border
        self.iplist[-1] = {'start': last_tup['start'], 'end': border}
        return True

    def release(self, num):
        insert_num = {'start': num, 'end': num}
        filled_list = []
        for elem in self.iplist:
            try:
                prev_end = filled_list[-1]['end']
            except:
                prev_end = 0
            next_start = elem['start']
            if num in range(prev_end + 1, next_start):
                filled_list.extend([insert_num])
            filled_list.extend([elem])
        if num <= self._upborder and num > self.iplist[-1]['end']:
            filled_list.extend([insert_num])
        if len(self.iplist) == len(filled_list):
            return False
        defrag_list = []
        defrag_list.extend([filled_list.pop(0)])
        for key in filled_list:
            if defrag_list[-1]['end'] == (key['start'] - 1):
                defrag_list[-1]['end'] = key['end']
            else:
                defrag_list.extend([key])
        self.iplist = defrag_list[:]
        return True

ipl = IPList()
print ipl
print ipl.get(100)
print ipl
print ipl.getnext()
print ipl
print ipl.getnext()
print ipl
print ipl.get(3)
print ipl
print ipl.get(99)
print ipl

print ipl.get(99)
print ipl
print ipl.get(300)
print ipl
print ipl.get(5)
print ipl
print ipl.get(4)
print ipl
print ipl.get(230)
print ipl
print ipl.set_border(240)
print ipl
print ipl.set_border(230)
print ipl
print ipl.set_border(231)
print ipl
print ipl.get(231)
print ipl
print '==========='
print ipl.release(230)
print ipl
