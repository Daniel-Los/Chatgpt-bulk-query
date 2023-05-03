
from text_miner import Text_Miner
import interface
import pandas as pd
import cProfile

#TODO: sometimes server is overloaded, then flings your request. Would be great to segment this

if __name__ == "__main__":
    def main(root):
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

        mode = str("Geef een samenvatting van deze tekst voor iemand die geinteresserd is in luchtkwaliteit. "
                   "Noem alle relevante maatregelen die in de tekst staan zijn en waarom deze te "
                   "maken hebben met luchtkwaliteit. Gebruik duidelijke en taal, specifieke termen en beleidsprogramma's"
                   "Geef voldoende context en zorg dat er zo min mogelijk informatie verloren gaat."
                   " Geef het antwoord in het Nederlands. "
                   )
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


        x = Text_Miner(root = root ,mode = mode)
        # x.get_languages()
        print('Structuur opzetten')
        x.get_structure()
        # print(x.doclist.keys())
        x.read_files()
        print('Kosten inschatten')
        x.estimate_costs()
        # x.agree()
        x.accord = True
        x = x
        if x.accord == True:
            x.AI_interact()
            x.write_to_file(x.outputdict)
            summarized_output = x.AI.summarize(x.outputdict)

            # newdict = {}
            # for key, item in x.outputdict.items():
            #     summ_output = x.AI.generate_text_with_prompt(mode= 'vat deze tekst samen', prompt=item)
            #     newdict.setdefault(key, [])
            #     newdict[key].append(summ_output)
            # x.outputdict = newdict

            x.write_to_file(summarized_output, extra='_samengevoegd')
            # f = pd.read_json('[' + str(x.AI.categorized) + ']')
            # f.to_excel('output/' + x.name + '_categorized.xlsx')
            print('\nDone')
        # x.agree()
        # if x.accord == True:
        #     x.AI_interact()
        # x.write_to_file()

    # p = cProfile.run(main())
    import os
    rootroot = r'C:\Users\d.los\Berenschot\Provincie Noord-Brabant - 69559 - Provinciale SLA samenwerking - EvRe\2. Documenten en data\Analysedocumenten'

    folder = r'C:\Users\d.los\Berenschot\Provincie Noord-Brabant - 69559 - Provinciale SLA samenwerking - EvRe\2. Documenten en data\Analysedocumenten'
    sub_folders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
    to_do = ['Waalre', 'Woensdrecht', 'Loon op Zand', 'Drimmelen', 'Asten', 'Gilze-Rijen', 'Geldrop-Mierlo', 'Zundert']
    maps_and_files = [i for i in os.walk(folder)]
    # for name in sub_folders:
    #     if name in to_do:
    #
    #         print(f'Processing: {name}')
    #         try:
    #
    #             main(root = str(fr"{rootroot}\{name}"))
    #         except Exception as e:
    #             print(f'An error occured with {name}')
    #             print(e)
    #             continue
    #
    # print('done')


