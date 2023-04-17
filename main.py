
from text_miner import Text_Miner
import interface
import pandas as pd
import cProfile

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

    # mode =  'List all relevant sections that improve air quality in bulletpoints. \n If there are no methods, return "- $\n"'

    # mode = 'Citeer uit het volgende stuk tekst alle passages met maatregelen die te maken hebben met het realiseren van betere' \
    #        ' luchtkwaliteit. Leg bij elke maatregel uit waarom het te maken heeft met schone lucht'
    # Plaats maatregelen kunnen in de categorieën: “Mobiliteit (verkeer), Mobiele werktuigen, Industrie, Houtstook '\
    # van particuliere huishoudens, Binnenvaart en havens, Landbouw, Participatie van burgers en bedrijven, Monitoring,'\
    # Hoogblootgestelde locaties en gevoelige groepen, Internationaal luchtbeleid of Geen van allen.”'

    mode = "Please identify and categorize all measures related to improving air quality in the following text. Please provide a clear explanation for each measure on why it contributes to better air quality. Please use clear and concise language, specific terms, and examples where needed to help understand what you are referring to. Please provide enough context for the reader to be able to understand the measure. Test your prompt and refine it as needed until you get the results you need. Translate the answer into Dutch. Categorize each measure into one of the following: Mobility (traffic), Mobile Machinery, Industry, Wood-burning in private households, Inland shipping and ports, Agriculture, Citizen and business participation, Monitoring, High-exposure locations and vulnerable groups, International air policy, or None."

    # root = "test documenten"
    # root = r'C:\Users\d.los\Berenschot\Provincie Noord-Brabant - 69559 - Provinciale SLA samenwerking - EvRe\2. Documenten en data\Analysedocumenten\Zundert'
    root = r'C:\Users\d.los\Berenschot\Provincie Noord-Brabant - 69559 - Provinciale SLA samenwerking - EvRe\2. Documenten en data\Analysedocumenten\Breda - Deelnemer'


    x = Text_Miner(root = root ,mode = mode)
    # x.get_languages()
    print('Structuur opzetten')
    x.get_structure()
    print(x.doclist.keys())
    x.read_files()
    print('Kosten inschatten')
    x.estimate_costs()
    x.agree()
    x.accord = True
    x = x
    if x.accord == True:
        x.AI_interact()

        summarized_output = x.AI.summarize(x.outputdict)

        # newdict = {}
        # for key, item in x.outputdict.items():
        #     summ_output = x.AI.generate_text_with_prompt(mode= 'vat deze tekst samen', prompt=item)
        #     newdict.setdefault(key, [])
        #     newdict[key].append(summ_output)
        # x.outputdict = newdict

        x.write_to_file(summarized_output)
        # f = pd.read_json('[' + str(x.AI.categorized) + ']')
        # f.to_excel('output/' + x.name + '_categorized.xlsx')
        print('\nDone')
    # x.agree()
    # if x.accord == True:
    #     x.AI_interact()
    # x.write_to_file()

# p = cProfile.run(main())




