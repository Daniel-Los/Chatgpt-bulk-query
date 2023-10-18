import read_variables_from_instructions
from begrippenlijst import begrippenlijst
from text_miner import Text_Miner
import os
from read_variables_from_instructions import read_instructions
import sys
import load_instructions
import subprocess

#TODO: sometimes server is overloaded, then flings your request. Would be great to segment this

def main():

    def main_loop(folder_path, prompt_input, mode, output_folder, project_name, word_formatting, api_key_path):
        '''' The main loop '''
        print('Starting')


        x = Text_Miner(folder_path = folder_path,
                       prompt_input = prompt,
                       mode = mode,
                       output_folder = output_folder,
                       project_name = project_name,
                       word_formatting = bool(word_formatting),
                       api_key_path = api_key_path)

        x.get_structure()
        x.read_files()

        x.estimate_costs
        # x.agree()
        x.accord = True

        if x.accord == True:
            x.AI_interact()
            x.write_to_file(x.outputdict, formatting = word_formatting)
            return x

    project_name, folder_path, test_run, prompt_input, output_folder, word_formatting, api_key_path = sys.argv

    folder_path = folder_path
    prompt_input = prompt_input
    test_run_bool = bool(test_run)
    prompt = prompt_input
    output_folder = output_folder
    word_formatting = bool(word_formatting)
    api_key_path = api_key_path
    mode = ''

    # TODO: clean up all the code
    prompts = None
    project_names = None

    if not prompts:
        prompts = [prompt, ]
    if not project_names:
        project_names = [project_name, ]

        # this was an experiment with multiple prompts for themes.

        # prompts = [
        #     "Samenwerking. Geef mij alle passages terug uit de bijgevoegde tekst over gemeente Hoorn met betrekking tot samenwerking. Deze samenvatting moet het schrijven van een woonvisie ondersteunen. Gebruik kopjes om de tekst te structureren: 'Bestaande samenwerkingen en partnerschappen in Hoorn,' 'Samenwerking met zorgaanbieders, woningbouwcorporaties en zorgverzekeraars,' en 'Doel van de samenwerking in het bieden van goede zorg en ondersteuning.' Antwoord in het Nederlands. Vermijd vaagheden en wees extra duidelijk. Leg in de stukjes precies uit wat er vermeld is over de onderwerpen. Als er niets over het thema wordt vermeld, antwoord dan met [].",
        #     "Participatie. Geef mij alle passages terug uit de bijgevoegde tekst over gemeente Hoorn met betrekking tot participatie. Deze samenvatting moet het schrijven van een woonvisie ondersteunen. Gebruik kopjes om de tekst te structureren: 'Betrekking van inwoners bij plannen rondom wonen en zorg,' 'Inspraak en besluitvorming door de gemeente,' en 'Maatregelen om rekening te houden met de betrokkenheid van inwoners.' Antwoord in het Nederlands. Vermijd vaagheden en wees extra duidelijk. Leg in de stukjes precies uit wat er vermeld is over de onderwerpen. Als er niets over het thema wordt vermeld, antwoord dan met [].",
        #     "Leefomgeving. Geef mij alle passages terug uit de bijgevoegde tekst over gemeente Hoorn met betrekking tot de leefomgeving. Deze samenvatting moet het schrijven van een woonvisie ondersteunen. Gebruik kopjes om de tekst te structureren: 'Ontwerp van de fysieke woonomgeving,' 'Voorzieningenniveau en leefbaarheid,' en 'Bevordering van welzijn en sociale interactie.' Antwoord in het Nederlands. Vermijd vaagheden en wees extra duidelijk. Leg in de stukjes precies uit wat er vermeld is over de onderwerpen. Als er niets over het thema wordt vermeld, antwoord dan met [].",
        #     "Demografie. Geef mij alle passages terug uit de bijgevoegde tekst over gemeente Hoorn met betrekking tot demografie. Deze samenvatting moet het schrijven van een woonvisie ondersteunen. Gebruik kopjes om de tekst te structureren: 'Bevolkingsopbouw en -ontwikkeling in Hoorn,' 'Doelgroepen en kwetsbare inwoners,' en 'Bevolkingsprognose voor de gemeente.' Antwoord in het Nederlands. Vermijd vaagheden en wees extra duidelijk. Leg in de stukjes precies uit wat er vermeld is over de onderwerpen. Als er niets over het thema wordt vermeld, antwoord dan met [].",
        #     "Woningmarkt. Geef mij alle passages terug uit de bijgevoegde tekst over gemeente Hoorn met betrekking tot de woningmarkt. Deze samenvatting moet het schrijven van een woonvisie ondersteunen. Gebruik kopjes om de tekst te structureren: 'Aanbod en vraag naar passende woningen,' 'Diverse woonvormen en woningvoorraad,' en 'Transformatie en nieuwbouwontwikkelingen.' Antwoord in het Nederlands. Vermijd vaagheden en wees extra duidelijk. Leg in de stukjes precies uit wat er vermeld is over de onderwerpen. Als er niets over het thema wordt vermeld, antwoord dan met [].",
        #     "Zorgbehoefte. Geef mij alle passages terug uit de bijgevoegde tekst over gemeente Hoorn met betrekking tot zorgbehoefte. Deze samenvatting moet het schrijven van een woonvisie ondersteunen. Gebruik kopjes om de tekst te structureren: 'Verschillende zorgvormen en -aanbod in Hoorn,' 'Organisatie van zorgverlening en verblijfsvormen,' en 'Rol van intramurale en extramurale zorg.' Antwoord in het Nederlands. Vermijd vaagheden en wees extra duidelijk. Leg in de stukjes precies uit wat er vermeld is over de onderwerpen. Als er niets over het thema wordt vermeld, antwoord dan met [].",
        #
        # ]
        # project_names = [
        #     'Samenwerking',
        #     'Participatie',
        #     'Leefomgeving',
        #     'Demografie',
        #     'Woningmarkt',
        #     'Zorgbehoefte',
        # ]

    # converting string to bool
    sub_folders = [name for name in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, name))]

    print(sub_folders)
    if test_run_bool:
        test_mode = 'Testing'
        try:
            to_do = sub_folders[0]  # Can also be a list if you want less
        except:
            raise Exception('Documents must be in a folder to group them')

    else:
        test_mode = 'Running'
        to_do = sub_folders
    print(f'Loading: {sub_folders if not to_do else to_do}')

    for index, prompt in enumerate(prompts):  # Can use multiple prompts
        project_name = project_names[index]  # if there are multiple project names. #todo: add this to interface
        for name in sub_folders:  # This code iterates through all documents in the root
            if name in to_do:
                # TODO: add a thing that tokenises everything first and calculates cost estimate
                print(f'Processing: {name}')
                try:

                    x = main_loop(
                        mode = mode,
                        folder_path=str(fr"{project_root}\{name}"),
                        project_name=project_name,
                        output_folder=output_folder,
                        prompt_input=prompt,
                        word_formatting=word_formatting,
                        api_key_path = api_key_path
                    )

                except Exception as e:
                    raise Exception(f'An error occurred with {name}: {e}')
                    continue

        endstring = f'\n{test_mode} project "{project_name}" is done'
        print(endstring)
        subprocess.run(['explorer', output_folder])

if __name__ == "__main__":

    project_name = 'name'
    project_root = folder_path = r'C:\Users\d.los\PycharmProjects\documentsearch\test documenten'
    prompt_input = 'prompt input'
    test_run = 'True'
    prompt = 'prompt_input'
    output_folder = r'C:\Users\d.los\PycharmProjects\documentsearch\output'
    word_formatting = 'True'
    api_key_path = 'api_key.txt'

    sys.argv = [project_name, folder_path, test_run, prompt_input, output_folder, word_formatting, api_key_path]
    # print(sys.argv)
    main()



