
from text_miner import Text_Miner

if __name__ == "__main__":
    x = Text_Miner()
    # x.get_languages()
    x.get_structure()
    print(x.doclist.keys())
    x.read_files()
    x.estimate_costs()

    x.agree()
    if x.accord == True:
        x.AI_interact()
    x.write_to_file()


    print(x.outputdict)
