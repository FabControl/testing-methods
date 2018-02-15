from ast import literal_eval

def evaluate(input):
    """
    Evaluates a given input string and outputs either an int, float, list or tuple.
    :param input:
    :return:
    """
    try:
        output = literal_eval(input)
    except:
        output = input

    if output == "":
        return None
    else:
        return output