import os

def api_import(path_to_txt_file):
    #
    # # get the hostname of the computer
    # hostname = os.environ['COMPUTERNAME'] if os.name == 'nt' else os.uname().nodename
    #
    # # check which computer you're working on
    # if hostname == 'BT11833':
    #     api_key_file = r"C:\Users\d.los\OneDrive\Bureaublad\Coding\api keys\openai key berenschot.txt"
    # elif hostname == 'computer2':
    #     api_key_file = r"C:\Users\danie\OneDrive\Bureaublad\Coding\api keys\chatgpt openai key.txt"
    # elif hostname == 'BT11557':
    #     api_key_file = r"C:\Users\r.looijenga\OneDrive - Berenschot\Bureaublad\OpenAI_API_key.txt"
    # else:
    #     # handle the case where the script is running on an unrecognized computer
    #     raise ValueError('Unrecognized computer: {}'.format(hostname))
    #
    # # read the API key from the appropriate file
    # with open(api_key_file, 'r') as f:
    #     api_key = f.read().strip()
    # api_key = os.environ['OPENAI_API_KEY']

    with open(path_to_txt_file, 'r') as f:
        api_key = f.read().strip()

    # api_key = os.environ['OPENAI_API_KEY']

    return api_key

if __name__ == '__main__':
    key = api_import()
    print(key)