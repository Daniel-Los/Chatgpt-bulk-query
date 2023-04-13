
from text_miner import Text_Miner
import interface
import pandas as pd
import cProfile

#TODO: sometimes server is overloaded, then flings your request. Would be great to segment this

if __name__ == "__main__":
    def main():
        # interface.MyProgramInterface.start()

        # categories = "Plaats elke maatregel in een van de volgende categorieen: Mobiliteit (verkeer), Mobiele werktuigen, Industrie, Houtstook van particuliere huishoudens, Binnenvaart en havens, Landbouw, Participatie van burgers en bedrijven, Monitoring, Hoogblootgestelde locaties en gevoelige groepen, Internationaal luchtbeleid of Geen van allen"
        #

        # mode = "Zoek naar maatregelen die te maken hebben met het verbeteren van luchtkwaliteit in deze tekst en vat ze samen in bullets"\
        #         "Als er niets in staat antwoord dan met: - Geen. " # "Plaats elke maatregel in een van de volgende categorieen: Mobiliteit (verkeer), Mobiele werktuigen, " \
        #        # "Industrie, Houtstook van particuliere huishoudens, Binnenvaart en havens, Landbouw, Participatie van burgers " \
        #        # "en bedrijven, Monitoring, Hoogblootgestelde locaties en gevoelige groepen, Internationaal luchtbeleid of " \
        #        # "Geen. Formatteer zoals volgt :" \
        #        #  "'maatregel' : [de tekst van de maatregel], 'thema' : [het geclassificeerde thema],",

        # mode =  'List all relevant sections that improve air quality in bulletpoints. \n If there are no methods, return "- $\n"'

        mode = 'Haal uit dit stuk tekst alle maatregelen die te maken hebben met Schone lucht. Plaats maatregelen kunnen in de categorieën: “Mobiliteit (verkeer), Mobiele werktuigen, Industrie, Houtstook van particuliere huishoudens, Binnenvaart en havens, Landbouw, Participatie van burgers en bedrijven, Monitoring, Hoogblootgestelde locaties en gevoelige groepen, Internationaal luchtbeleid of Geen van allen.” Geef het terug in csv met kolommen maatregel en categorie: '

        root = "test documenten"
        root = r'C:\Users\d.los\Berenschot\Provincie Noord-Brabant - 69559 - Provinciale SLA samenwerking - EvRe\2. Documenten en data\Analysedocumenten\Zundert'

        x = Text_Miner(root = root ,mode = mode)
        # x.get_languages()
        print('Structuur opzetten')
        x.get_structure()
        print(x.doclist.keys())
        x.read_files()
        print('Kosten inschatten')
        # x.estimate_costs()

        # x.AI_interact()

        # x.write_to_file()

        # x.agree()
        x.accord = True
        if x.accord == True:
            x.AI_interact()

            # x.AI.summarize(x.outputdict)

            x.AI.generate_text_with_prompt(mode= 'vat deze tekst samen', prompt=x.outputdict)

            x.write_to_doc()
            # f = pd.read_json('[' + str(x.AI.categorized) + ']')
            # f.to_excel('output/' + x.name + '_categorized.xlsx')

        # x.agree()
        # if x.accord == True:
        #     x.AI_interact()
        # x.write_to_file()

    # p = cProfile.run(main())
    main()



