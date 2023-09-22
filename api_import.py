import os

def api_import():

    # get the hostname of the computer
    hostname = os.environ['COMPUTERNAME'] if os.name == 'nt' else os.uname().nodename

    # check which computer you're working on
    if hostname == 'BT11833':
        api_key_file = r"C:\Users\d.los\OneDrive - Berenschot\Bureaublad\chatgpt openai key.txt"
    elif hostname == 'computer2':
        api_key_file = r"C:\Users\danie\OneDrive\Bureaublad\Coding\api keys\openai key.txt"
    else:
        # handle the case where the script is running on an unrecognized computer
        raise ValueError('Unrecognized computer: {}'.format(hostname))

    # read the API key from the appropriate file

    with open(api_key_file, 'r') as f:
        api_key = f.read().strip()

    return api_key

if __name__ == '__main__':
    key = api_import()
    print(key == True)