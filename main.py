import read_variables_from_instructions
from begrippenlijst import begrippenlijst
from text_miner import Text_Miner
import os
from read_variables_from_instructions import read_instructions
import sys
import load_instructions
import subprocess

#TODO: sometimes server is overloaded, then flings your request. Would be great to segment this

if __name__ == "__main__":

    def main(folder_path, project_name, prompt_input, output_folder, word_formatting):
        root = folder_path
        prompt = prompt_input
        test_run_bool = test_run
        prompt = prompt_input
        output_folder = output_folder
        word_formatting = word_formatting

        x = Text_Miner(root = root ,
                       mode = prompt,
                       output_folder = output_folder,
                       project_name = project_name,
                       word_formatting = word_formatting)

        x.get_structure()
        x.read_files()

        x.estimate_costs()
        # x.agree()
        x.accord = True

        if x.accord == True:
            x.AI_interact()
            x.write_to_file(x.outputdict, formatting = word_formatting)
            return x
        #     summarized_output = x.AI.bulletize(x.outputdict)
        #     x.write_to_file(summarized_output, extra='_samengevoegd')


if __name__ == "__main__":
    #TODO: clean up all the code

    #loading variables from the interface
    try:
        _, project_name, project_root, test_run, prompt, output_folder, word_formatting = sys.argv
    except:
        print('no vars found from interface')
        inst_file = r"C:\Users\d.los\OneDrive - Berenschot\Bureaublad\instructie_voorjaarsnota.txt"
        project_root, prompt, project_name, output_folder = read_variables_from_instructions.load_instructons(inst_file)
        test_run = word_formatting = True

    #converting string to bool
    test_run = bool(test_run)
    word_formatting = bool(word_formatting)

    sub_folders = [name for name in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, name))]

    if test_run:
        to_do = sub_folders[0]# ['Voorschoten'] #['Leiden'] # Can also be a list if you want less
    else:
        to_do = sub_folders

    print(f'Loading: {sub_folders if not to_do else to_do}')

    for name in sub_folders:
    # This code iterates through all documents in the root
        if name in to_do:
            #TODO: add a thing that tokenises everything first and calculates cost estimate
            print(f'Processing: {name}')
            try:
                # for term in terms:
                # print(f'Doing {terms} now')
                x = main(
                    folder_path=str(fr"{project_root}\{name}"),
                    project_name = project_name,
                    output_folder = output_folder,
                    # prompt = f"Benoem uit dit stuk tekst de volgende termen, of afgeleiden van de term: '{terms}'." + prompt
                    prompt_input = prompt,
                    word_formatting = word_formatting
                )

            except Exception as e:
                print(f'An error occurred with {name}')
                print(e)
                continue

    # Alert the user the processing is done
    if test_run:
        test = 'Testing'
    else:
        test = 'Running'
    endstring = f'\n{test} project "{project_name}" is done'
    print(endstring)
    subprocess.run(['explorer', output_folder])


