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

    return suspicious_results
