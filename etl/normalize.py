from unicodedata import normalize as ucnorm, category


def normalize_token(text):
    """ Simplify a piece of text to generate a more canonical
    representation. This involves lowercasing, stripping trailing
    spaces, removing symbols, diacritical marks (umlauts) and
    converting all newlines etc. to single spaces.
    """
    if not isinstance(text, unicode):
        text = unicode(text)
    text = text.lower()
    decomposed = ucnorm('NFKD', text)
    filtered = []
    for char in decomposed:
        cat = category(char)
        if cat.startswith('C'):
            filtered.append(' ')
        elif cat.startswith('M'):
            # marks, such as umlauts
            continue
        elif cat.startswith('Z'):
            # newlines, non-breaking etc.
            filtered.append(' ')
        elif cat.startswith('S') or cat.startswith('P'):
            # symbols, such as currency
            continue
        else:
            filtered.append(char)
    text = u''.join(filtered)
    while '  ' in text:
        text = text.replace('  ', ' ')
    text = text.strip()
    return ucnorm('NFKC', text)


def normalize_text(text):
    """ This is vaguely stolen from:
    http://code.google.com/p/google-refine/wiki/ClusteringInDepth
    """
    text = text.strip().lower()
    text = normalize_token(text)
    tokens = text.split()
    tokens = sorted(set(tokens))
    return " ".join(tokens)
