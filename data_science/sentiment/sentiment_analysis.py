import string


def sentiment_analysis(msg):
    msg_tokens = tokenize_msg(msg)
    return msg_tokens


def tokenize_msg(msg):
    for c in string.punctuation:
        if c != "'":
            msg = msg.replace(c, " ")
    msg_tokens = msg.split(" ")
    msg_tokens = [c for c in msg_tokens if c not in [" ", ""]]
    return msg_tokens


def analyze_tokens(tokens):
    pass