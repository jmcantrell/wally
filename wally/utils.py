import hashlib

def matches_any(x, patterns): #{{{1
    """Test whether 'x' matches any pattern in 'patterns'"""
    for p in patterns:
        if p.search(x): return True
    return False

def matches_all(x, patterns): #{{{1
    """Test whether 'x' matches all patterns in 'patterns'"""
    for p in patterns:
        if not p.search(x): return False
    return True

def split_list(l, delim): #{{{1
    tokens = []
    acc = []
    for elm in l:
        if elm == delim:
            tokens.append(acc)
            acc = []
            continue
        acc.append(elm)
    tokens.append(acc)
    return tokens

def md5sum(value): #{{{1
    md5 = hashlib.md5()
    md5.update(value)
    return md5.hexdigest()

def uniqify(seq, key=None): #{{{1
    if key is None:
        def key(x): return x
    seen = {}
    result = []
    for item in seq:
        marker = key(item)
        if marker not in seen:
            seen[marker] = 1
            result.append(item)
    return result
