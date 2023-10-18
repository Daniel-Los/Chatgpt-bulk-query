import read_variables_from_instructions
from begrippenlijst import begrippenlijst
from text_miner import Text_Miner
import os
from read_variables_from_instructions import read_instructions
import sys
import load_instructions
import subprocess

#TODO: sometimes server is overloaded, then flings your request. Would be great to segment this

def main(project_root, prompt_input, output_folder, project_name, word_formatting, api_key_path, test_run):

    def main_loop(project_root, prompt_input, output_folder, project_name, word_formatting, api_key_path, mode = ''):
        '''' The main loop '''
        print('Starting')
        mode = ''

        x = Text_Miner(project_root = project_root,
                       prompt_input = prompt_input,
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

    # project_root, prompt_input, output_folder, project_name, word_formatting, api_key_path, test_run = sys.argv

    project_root = project_root
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
                        project_root=str(fr"{project_root}\{name}"),
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


    # project_root = project_root = r'C:\Users\d.los\Downloads\coronaparagraven\analyse\coronaparagraven'
    project_root = r'C:\Users\d.los\Downloads\coronaparagraven\output'
    # prompt_input = 'Geef een samenvatting op hoofdlijnen op basis van de volgende tekst. Leg nadruk op de onderdelen die te maken hebben met het tegengaan van de nadelige gevolgen van covid 19.'
    vragen = [
        "Wat zijn de grootste uitdagingen voor studenten door corona",
        "Wat zijn de grootste uitdagingen voor de organisatie, docenten of het programma",
        "Wat is de voortgang op het thema Welzijn en sociale binding",
        "Welke acties worden uitgevoerd in het kader van welzijn, sociale binding, psychologische ondersteuning, begeleiding van studenten of psychische problemen ",
        "Wat is de voortgang op het thema Soepele in- en doorstroom",
        "Welke acties worden uitgevoerd in het kader van studievoortgang, extra begeleiding, extra lessen, examinering, uitval, studentsucces, stoppen, switchen of instroom\n",
        "Wat is de voortgang op het thema Ondersteuning en begeleiding op het gebied van stages\n",
        "Welke acties worden uitgevoerd in het kader van loopbaanbegeleiding, stage, BPV, werk, arbeidsmarkt, werkgevers, bedrijven of LOB \n"
        "Wat is de voortgang op het thema Lerarenopleidingen",
        "Wat is de voortgang op het thema Ondersteuning en begeleiding op het gebied van coschappen medische opleidingen",
        "Wat is de voortgang op het thema Aanpak jeugdwerkloosheid",
        "Welke acties worden uitgevoerd in het kader van aanpak jeugdwerkloosheid, gemeenten, arbeidsmarkt, baan, naar werk, werkgevers en bedrijven of werkcoaches",
        "Hoe zetten instellingen blended learning, hybride onderwijs, digitaal onderwijs, online examinering of digitale begeleiding in",
        "Zijn er wijzigingen of reallocaties geweest ten opzichte van het bestedingsplan",
        "Hoe is de medezeggenschap betrokken zoals de faculteitsraad, studentenraad, universiteitsraad, ondernemingsraad",
        "In hoeverre sluiten de activiteiten aan bij de behoefte van studenten",
        "Welke activiteiten worden genoemd die het best de doelgroepen hebben bereikt",
        # "Worden activiteiten gericht op specifieke doelgroepen van studenten",
        "Welke activiteiten hebben het meeste effect gehad volgens de tekst",
        "Met welke activiteiten zijn onderwijsinstellingen gestopt door corona",
        # "Bij welke activiteiten is het vaakst sprake van vertraging",
        "Wat voor personeel is ingehuurd met de middelen uit de coronaenveloppe",
        "Welke uitdagingen kwamen instellingen tegen bij het besteden van middelen uit de coronaenveloppe",
        "Op welke manier wordt de voortgang gemonitord",
        # "Redden de instellingen het om binnen de looptijd van het programma de middelen te besteden",
        "Wat heeft goed gewerkt en noemen de instellingen als succesvol of goed voorbeeld",
        "Welke verdere uitdagingen voor de toekomst worden in de tekst genoemd",
    ]

    for index, vraag in enumerate(vragen):
        prompt_input = 'Geef op basis van de onderstaande samenvattingen uitgebreid en zo goed mogelijk antwoord op de volgende vragen. Noem bij ieder antwoord de teksten waar je het op baseert. ' \
               'Het is belangrijk om te laten zien hoe je tot je antwoord bent gekomen. Baseer je alleen op de gegeven tekst. Geef aan uit welke stukken tekst je antwoord komt. \n' \
               'Hier is de vraag: \n' \
                f'{vraag}? \nHier volgt de tekst: \n'

        # prompt_input = "Maak een uitgebreide samenvatting rond de 50% lengte van deze tekst. Wees uitgebreid en zorg ervoor dat geen details wegvallen." \
        #                "Hier volgt de tekst: \n"
        test_run = False
        try:
            project_name = f'{vraag} {index+1}'
        except:
            project_name = f'Antwoord op vraag {index + 1}'
        output_folder = r'C:\Users\d.los\Downloads\coronaparagraven'
        word_formatting = 'True'
        api_key_path = 'api_key.txt'

        # sys.argv = [project_name, project_root, test_run, prompt_input, output_folder, word_formatting, api_key_path]
        # print(sys.argv)
        main(project_root, prompt_input, output_folder, project_name, word_formatting, api_key_path, test_run)



