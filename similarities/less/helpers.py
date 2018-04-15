




# Code written by: Mohammad Alsalkini





from nltk.tokenize import sent_tokenize


def lines(a, b):
    """Return lines in both a and b"""

    # splitting the lines
    line_a = set(a.split('\n'))
    line_b = set(b.split('\n'))
    list1 = []
    # comparing two lines
    for element1 in line_a:
        for element2 in line_b:
            if element2 == element1:
                list1.append(element2)
    return list1


def sentences(a, b):
    """Return sentences in both a and b"""
    # splitting the sentences
    sentence_a = set(sent_tokenize(a))
    sentence_b = set(sent_tokenize(b))
    list1 = []
    # comparing two sentences
    for sentence1 in sentence_a:
        for sentence2 in sentence_b:
            if sentence2 == sentence1:
                list1.append(sentence2)
    return list1


def substrings(a, b, n):
    """Return substrings of length n in both a and b"""
    length_a = len(a)
    length_b = len(b)
    sub_a = []
    sub_b = []
    for i in range(length_a - n + 1):
        j = n + i
        sub_a.append(a[i:j])
        sub_a = set(sub_a)
        sub_a = list(sub_a)
    for i in range(length_b - n + 1):
        j = n + i
        sub_b.append(b[i:j])
        sub_b = set(sub_b)
        sub_b = list(sub_b)
    list1 = []
    for sub1 in sub_a:
        for sub2 in sub_b:
            if sub2 == sub1:
                list1.append(sub2)
    return list1