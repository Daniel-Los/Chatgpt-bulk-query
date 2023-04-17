print('starting')
from text_miner import Text_Miner
import interface
import pandas as pd
import tiktoken
#TODO: sometimes server is overloaded, then flings your request. Would be great to segment this

if __name__ == "__main__":
    # interface.MyProgramInterface.start()

    # categories = "Plaats elke maatregel in een van de volgende categorieen: Mobiliteit (verkeer), Mobiele werktuigen, Industrie, Houtstook van particuliere huishoudens, Binnenvaart en havens, Landbouw, Participatie van burgers en bedrijven, Monitoring, Hoogblootgestelde locaties en gevoelige groepen, Internationaal luchtbeleid of Geen van allen"
    #

    # mode = "Zoek naar maatregelen die te maken hebben met het verbeteren van luchtkwaliteit in deze tekst en vat ze samen in bullets"\
    #         "Als er niets in staat antwoord dan met: - Geen. " # "Plaats elke maatregel in een van de volgende categorieen: Mobiliteit (verkeer), Mobiele werktuigen, " \
    #        # "Industrie, Houtstook van particuliere huishoudens, Binnenvaart en havens, Landbouw, Participatie van burgers " \
    #        # "en bedrijven, Monitoring, Hoogblootgestelde locaties en gevoelige groepen, Internationaal luchtbeleid of " \
    #        # "Geen. Formatteer zoals volgt :" \
    #        #  "'maatregel' : [de tekst van de maatregel], 'thema' : [het geclassificeerde thema],",
    mode =  'Quote all relevant sections that improve air quality in bulletpoints. \n If there are no methods, return "- $\n"'

    root = "test documenten"
    root = r'C:\Users\r.looijenga\Berenschot\Provincie Noord-Brabant - Analysedocumenten\Roosendaal'

    x = Text_Miner(root = root ,mode = mode)
    # x.get_languages()
    print('Structuur opzetten')
    x.get_structure()
    print(x.doclist.keys())
    x.read_files()
    print('Kosten inschatten')
    x.estimate_costs()

    # x.AI_interact()

    # x.write_to_file()

    x.agree()
    if x.accord == True:
        x.AI_interact()

        x.AI.summarize(x.outputdict)
        x.write_to_file()
        f = pd.read_json('[' + str(x.AI.categorized) + ']')
        f.to_excel('output/' + x.name + '_categorized.xlsx')

    # x.agree()
    # if x.accord == True:
    #     x.AI_interact()
    # x.write_to_file()
