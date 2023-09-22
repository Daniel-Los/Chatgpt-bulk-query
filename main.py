from begrippenlijst import begrippenlijst
from text_miner import Text_Miner
import os
from read_variables_from_instructions import read_instructions

#TODO: sometimes server is overloaded, then flings your request. Would be great to segment this

if __name__ == "__main__":
    def main(root, project_name, output_folder, prompt):
        # interface.MyProgramInterface.start()

        # categories = "Plaats elke maatregel in een van de volgende categorieen: Mobiliteit (verkeer), Mobiele werktuigen, Industrie, Houtstook van particuliere huishoudens, Binnenvaart en havens, Landbouw, Participatie van burgers en bedrijven, Monitoring, Hoogblootgestelde locaties en gevoelige groepen, Internationaal luchtbeleid of Geen van allen"
        #

        # mode = "Zoek naar maatregelen die te maken hebben met het verbeteren van luchtkwaliteit in deze tekst en vat ze
        # samen in bullets"\ "Als er niets in staat antwoord dan met: - Geen. " # "Plaats elke maatregel in een van de
        # volgende categorieen: Mobiliteit (verkeer), Mobiele werktuigen, " \ # "Industrie, Houtstook van particuliere
        # huishoudens, Binnenvaart en havens, Landbouw, Participatie van burgers " \ # "en bedrijven, Monitoring,
        # Hoogblootgestelde locaties en gevoelige groepen, Internationaal luchtbeleid of " \ # "Geen. Formatteer zoals
        # volgt :" \ #  "'maatregel' : [de tekst van de maatregel], 'thema' : [het geclassificeerde thema],",

        # mode = "Identificeer en categoriseer alle maatregelen die betrekking hebben op het verbeteren van de
        # luchtkwaliteit in de volgende tekst. Geef voor elke maatregel een duidelijke uitleg waarom deze bijdraagt aan
        # een betere luchtkwaliteit. Gebruik heldere en beknopte taal, specifieke termen en voorbeelden waar nodig om te
        # helpen begrijpen waar u naar verwijst. Zorg voor voldoende context zodat de lezer de maatregel kan begrijpen.
        # Test de prompt en verfijn deze indien nodig totdat u de gewenste resultaten krijgt. Categoriseer elke maatregel
        # in een van de volgende categorieën: Mobiliteit (verkeer), Mobiele werktuigen, Industrie, Houtstook van
        # particuliere huishoudens, Binnenvaart en havens, Landbouw, Participatie van burgers en bedrijven, Monitoring,
        # Hoogblootgestelde locaties en gevoelige groepen, Internationaal luchtbeleid of Geen van allen."

        # prompt = str("Geef een samenvatting van deze tekst voor iemand die geinteresserd is in luchtkwaliteit. "
        #            "Noem alle relevante maatregelen die in de tekst staan zijn en waarom deze te "
        #            "maken hebben met luchtkwaliteit. Gebruik duidelijke en taal, specifieke termen en beleidsprogramma's"
        #            "Geef voldoende context en zorg dat er zo min mogelijk informatie verloren gaat."
        #            " Geef het antwoord in het Nederlands. ")
        #
        # prompt = str("Je bent onderzoeker die een analyse moet maken van stukken tekst."
        #            "Zoek in het volgende stuk tekst de zinnen die direct te maken hebben met doeltreffendheid en doelmatigheid van genoemde maatregelen. "
        #            "Het kan voorkomen dat de woorden doeltreffendhed en doelmatigheid uitwisselbaar worden gebruikt met effectiviteit en efficientie. "
        #            "Wij willen weten of er in het document iets staat over doeltreffendheid en doelmatigheid, maar ook "
        #            "op welke maatregelen dat van toepassing is. Het moet mogelijk zijn om dit terug te leiden naar de bron."
        #            "Plaats genoemde maatregelen tussen [] haakjes."
        #            )

       # "Categoriseer elk citaat in een "
       # "van de volgende categorieën: Mobiliteit (verkeer), Mobiele machines, Industrie, Houtverbranding in particuliere "
       # "huishoudens, Binnenvaart en havens, Landbouw, Participatie van burgers en bedrijven, Monitoring, "
       # "Locaties met hoge blootstelling en kwetsbare groepen, Internationaal luchtbeleid, of Geen.\n")

        # mode =str("Citeer of quote alle acties die relevant zijn voor de luchtkwaliteit in de tekst na deze prompt. "
        # "Geef een duidelijke uitleg voor alle maatregelen waarom deze te maken heeft met luchtkwaliteit. Gebruik "
        # "duidelijke en taal, specifieke termen en voorbeelden waar nodig om te helpen begrijpen waar je naar "
        # "verwijst. Geef voldoende context zodat de lezer de maatregel kan begrijpen. Test je prompt en verfijn het indien nodig "
        # "totdat je de gewenste resultaten krijgt. Vertaal het antwoord in het Nederlands. Categoriseer elk citaat in een "
        # "van de volgende categorieën: Mobiliteit (verkeer), Mobiele machines, Industrie, Houtverbranding in particuliere "
        # "huishoudens, Binnenvaart en havens, Landbouw, Participatie van burgers en bedrijven, Monitoring, "
        # "Locaties met hoge blootstelling en kwetsbare groepen, Internationaal luchtbeleid, of Geen.\n")

        # root = "test documenten"
        # root = r'C:\Users\d.los\Berenschot\Provincie Noord-Brabant - 69559 - Provinciale SLA samenwerking - EvRe\2. Documenten en data\Analysedocumenten\Zundert'
        # root = r'C:\Users\d.los\Berenschot\Provincie Noord-Brabant - 69559 - Provinciale SLA samenwerking - EvRe\2. Documenten en data\Analysedocumenten\Bergen op Zoom'

        x = Text_Miner(root = root ,
                       mode = prompt,
                       output_folder = output_folder,
                       project_name = project_name)
        # x.get_languages()
        print('Structuur opzetten')
        x.get_structure()
        # print(x.doclist.keys())
        x.read_files()
        print('Kosten inschatten')
        x.estimate_costs()
        # x.agree()
        x.accord = True

        if x.accord == True:
            x.AI_interact()

            x.write_to_file(x.outputdict, formatting = False)
            return x
        #     summarized_output = x.AI.bulletize(x.outputdict)
        #     x.write_to_file(summarized_output, extra='_samengevoegd')

if __name__ == "__main__":
    #TODO: clean up all the code

    # instruction_file = r"C:\Users\d.los\OneDrive - Berenschot\Bureaublad\instructie_voorjaarsnota.txt"
    instruction_file = r"C:\Users\d.los\PycharmProjects\documentsearch\instruction_voorjaarsnota.txt"
    variables = read_instructions(instruction_file)
    project_root = variables['root']
    prompt = variables['prompt']
    project_name = variables['project_name']
    output_folder = variables['output_folder']

    sub_folders = [name for name in os.listdir(project_root) if os.path.isdir(os.path.join(project_root, name))]

    to_do = False# ['Voorschoten'] #['Leiden'] # Can also be a list if you want less
    # to_do = ['Laarbeek']
    print(f'Loading: {sub_folders if not to_do else to_do}')
    maps_and_files = [i for i in os.walk(project_root)]

    ## This code can be used to find a list of used documents
    # print(sub_folders.index(to_do))
    # print(maps_and_files[sub_folders.index(to_do)+1])

    # terms = begrippenlijst()
    # terms = ["Aanbod",]
    for name in sub_folders:
    # This code iterates through all documents in the root
        if to_do:
            if name in to_do:
                print(f'Processing: {name}')
                try:
                    # for term in terms:
                    # print(f'Doing {terms} now')
                    x = main(
                        root=str(fr"{project_root}\{name}"),
                        project_name = project_name,
                        output_folder = output_folder,
                        # prompt = f"Benoem uit dit stuk tekst de volgende termen, of afgeleiden van de term: '{terms}'." + prompt
                        prompt = prompt
                    )

                except Exception as e:
                    print(f'An error occurred with {name}')
                    print(e)
                    continue
        else:
            try:
                # for term in terms:
                # print(f'Doing {terms} now')
                x = main(
                    root=str(fr"{project_root}\{name}"),
                    project_name=project_name,
                    output_folder=output_folder,
                    # prompt = f"Benoem uit dit stuk tekst de volgende termen, of afgeleiden van de term: '{terms}'." + prompt
                    prompt=prompt
                )

            except Exception as e:
                print(f'An error occurred with {name}')
                print(e)
                continue

    print('done')



