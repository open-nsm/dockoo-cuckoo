import re
import json

# Parse file and return result
def parsefile( output_file ):

    # For now, just return the whole thing as 'results'
    d = {
        'result': 'results to come'
    }

    return json.dumps(d)

# Is there anything suspicious in the results?
def suspicious(output_file):
    suspicious_results = False

    return suspicious_results
