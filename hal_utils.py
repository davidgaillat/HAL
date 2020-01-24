import re

def grep_from_to_year(leaves, startpos):
    year_intervals = []
    while True:
        _, start, _, end, startpos = grep_leaves(
            leaves, '#IN#*NUM[]*(#TO#|Conj[])*NUM[]', startpos)
        if start and end:
            year_intervals.append((start, end))
        else:
            break
    return year_intervals

def grep_in_year(leaves, startpos):
    years = []           
    while True:
        _, year, startpos = grep_leaves(leaves, '#IN#*NUM[]', startpos)
        if year:
            years.append(year) 
        else:
            break
    return years

def grep_in_country(leaves, startpos, all_countries):
    countries = []
    while True:
        _, name, startpos = grep_leaves(leaves, '#IN#*N[]', startpos)
        if name in all_countries:
            countries.append(name)
        elif not name:
            break
    return countries

def stringify(l):        
    return ','.join(["'" + x + "'" for x in l])         

# syntax of regex: 'Det[]*N[]*V[]' or 'Det[]*(N[]|V[])*V[]' 
def grep_leaves(leaves, regex, startpos = 0):
    i = 0
    r = regex.split('*')
    c = 0
    result = [None for i in range(len(r)+1)]
    i = startpos
    while i < len(leaves):
        if c == len(r):
            break
        leave = leaves[i]
        match, can_skip = _leave_matches(leave, r[c])
        if match:
            result[c] = leave[1]
            c += 1
        elif can_skip and c < len(r) - 1:
            match, _ = _leave_matches(leave, r[c+1])
            if match:
                result[c+1] = leave[1]
                c += 2
        i += 1
    result[-1] = i
    return result            

def _leave_matches(leave, r):
    if leave[0] == r or leave[1] == r:
        return (True, False)
    else:
        pattern1 = re.compile(r'\((.+)\|(.+)\)')
        for (first, second) in re.findall(pattern1, r):
            if leave[0] == first or leave[1] == first or leave[0] == second or leave[1] == second:
                return (True, False)        
        pattern2 = re.compile(r'\((.+)\)')
        for optional in re.findall(pattern2, r):
            if leave[0] == optional or leave[1] == optional:
                return (True, True)
            else:
                return (False, True)
    return (False, False)

if __name__ == '__main__':
    pass
