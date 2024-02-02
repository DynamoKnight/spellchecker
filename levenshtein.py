'''
Nakul Kumar
Period 1
Spell Checker Project
'''
# Find an Implementation of Levenshtein Distance on the internet.
# You should do this TWO ways:
# 1) python code 
# 2) import a module
try:
    import Levenshtein
except ImportError:
    print("The 'python-Levenshtein' module is not installed. Installing it now...")
    try:
        from pip import main as pipmain
    except ImportError:
        from pip._internal import main as pipmain

    pipmain(['install', 'python-Levenshtein'])
    import Levenshtein

def levenshtein_distance(s1, s2):
    # Find internet code to return the distance between s1 & s2
    # Source: https://stackoverflow.com/a/24172422
    m=len(s1)+1
    n=len(s2)+1
    tbl = {}
    for i in range(m): tbl[i,0]=i
    for j in range(n): tbl[0,j]=j
    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i-1] == s2[j-1] else 1
            tbl[i,j] = min(tbl[i, j-1]+1, tbl[i-1, j]+1, tbl[i-1, j-1]+cost)
    return tbl[i,j]

def lev_distance(s1, s2):
    # This is a wrapper method that calls the module's implementation
    return Levenshtein.distance(s1, s2)