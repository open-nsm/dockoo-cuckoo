import re
import json

# Parse file and return result
def parsefile( output_file ):

    result_str = ""
    infile = open(output_file, "r")
    for line in infile:
        result_str = result_str + line

    # For now, just return the whole thing as 'results'
    d = {
        'result': result_str
    }

    return json.dumps(d)

# Is there anything suspicious in the results?
def suspicious(output_file):
    suspicious_results = False
    mode_IAT = False
    result_str = ""

    infile = open(output_file, "r")
    for line in infile:
        result_str = result_str + line
        if re.match("(.*)SUSPICIOUS(.*)", line):
            suspicious_results = True
        if re.match("Suspicious IAT alerts(.*)", line):
            mode_IAT = True
        if (mode_IAT):
            if re.match("(.*)\d+(.*)", line):
                suspicious_results = True
    return suspicious_results

