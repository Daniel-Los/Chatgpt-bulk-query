
from text_miner import Text_Miner
import interface

if __name__ == "__main__":

    # interface.MyProgramInterface.start()

    # mode = "Zoek naar maatregelen die te maken hebben met het verbeteren van luchtkwaliteit in deze tekst en vat ze samen in bullets"\
    #         "Als er niets in staat antwoord dan met: - Geen. "
    #        # "Plaats elke maatregel in een van de volgende categorieen: Mobiliteit (verkeer), Mobiele werktuigen, " \
    #        # "Industrie, Houtstook van particuliere huishoudens, Binnenvaart en havens, Landbouw, Participatie van burgers " \
    #        # "en bedrijven, Monitoring, Hoogblootgestelde locaties en gevoelige groepen, Internationaal luchtbeleid of " \
    #        # "Geen. Formatteer zoals volgt :" \
    #        #  "'maatregel' : [de tekst van de maatregel], 'thema' : [het geclassificeerde thema],",
    mode =  'List all relevant methods to improve air quality in bullets: \n If there are no methods, return "- null\n"'

    root = "test documenten"

    x = Text_Miner(root = root ,mode = mode)
    # x.get_languages()
    x.get_structure()
    print(x.doclist.keys())
    x.read_files()
    x.estimate_costs()

    # x.AI_interact()

    # x.write_to_file()

    x.agree()
    if x.accord == True:
        x.AI_interact()
        x.write_to_file()
    # x.agree()
    # if x.accord == True:
    #     x.AI_interact()
    # x.write_to_file()



    print(x.outputdict)
