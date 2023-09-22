# -*- coding: utf-8 -*-


"""standard libraries"""
import pandas as pd
import os
import re
# for the unique matches (python does shallow copying by default)
import copy
import datetime

"""my own functions"""
# from _functies import extractPDF
from _functies import extract_TXT, extractDocx

import docx2txt

""" 
Class Doc, for all methods related to an individual document. The values matches
    and scores contain the actual results and are returned to the Folder class
The big advantage is the memory usage: only the data relevant for one document 
    at a time is saved in memory."""


class Doc():
    def __init__(self, path_to_doc, excel_categories, excel_pairs):
        # variables necessary for the analysis. self.cat are the words in the different categories. self.pairs is how the categories must be checked against each other
        self.cat = excel_categories
        self.pairs = excel_pairs
        # the raw self.text and self.sententenses
        self.text = docx2txt.process(path_to_doc)
        self.sentences = re.split(r' *[\.\?!][\'"\)\]]* *', self.text)
        # the empty variables to be filled during the use of the Doc class
        self.matches = {}
        self.scores = {}
        self.matching_subSets = {}
        self.voorkomen_themas = {}
        self.wordcount = {}

    def subSentence(self, index):
        # breaks self.sentences up in subset of three sentences at a time
        # this is a way to use the context of a sentence as well as the sentence itself
        try:
            subSet = " 1: " + self.sentences[index] + ". 2: " + self.sentences[index + 1] + ". 3: " + self.sentences[
                index + 2] + " | \n\n"
        except IndexError:
            try:
                subSet = " 1: " + self.sentences[index] + ". 2: " + self.sentences[index + 1] + " | \n\n"
            except IndexError:
                subSet = " 1: " + self.sentences[index] + " | \n\n "
        return subSet.lower()

    def wordCount(self):
        for word in self.cat.iloc[:]['Woordenlijst']:
            self.wordcount[word] = self.text.lower().count(word)
        # print(self.wordcount)
        return self.wordcount

    # the matches must be combined again because of the indexproblems (index from sentences is not the same as list_of_sentences)
    def match(self, pair_A, pair_B):
        # checks if the words of list_of_words appear in list_of_sentences voorkomt and returns a list of these (match_list)
        match_subSets = []
        index = 0

        # note that everything below happens on a senctence-level
        for sentence in self.sentences:
            # print(sentence)
            # the loop with the words from pair_A
            for word_a in pair_A:
                # the problems with the NaN came from unfiltered floats in the document.
                # This matched with the nan's already (and still) present in the categories file
                if type(word_a) == str and word_a.lower() in sentence.lower():  # and first_sentence
                    new_sentence = sentence + ' \n\n '
                    try:
                        self.voorkomen_themas[word_a] += new_sentence
                    except KeyError:
                        self.voorkomen_themas[word_a] = new_sentence

                    subSet = self.subSentence(index).lower()
                    # the loop with the words from pair_B, but only when pair a matches
                    for word_b in pair_B:
                        # the conditional of not being in the matchlist is deleted, beacause you want a point for every term that is in the subSet
                        if type(word_b) == str and word_b.lower() in subSet:
                            match_subSets.append(subSet)
                            try:
                                self.matches[word_a].append(str(word_b).lower())
                            except KeyError:
                                self.matches[word_a] = []
                                self.matches[word_a].append(str(word_b).lower())
                            try:
                                self.matching_subSets[word_a] += subSet
                            except KeyError:
                                self.matching_subSets[word_a] = subSet
            index += 1
        return match_subSets

    # the matches must be combined again because of the indexproblems (index from sentences is not the same as list_of_sentences)
    def match1(self, list_of_sentences, list_of_words):
        # checks if the words of list_of_words appear in list_of_sentences voorkomt and returns a list of these (match_list)
        match_list = []
        for sentence in list_of_sentences:
            for word in list_of_words:
                # the problems with the NaN came from unfiltered floats in the document.
                # This matched with the nan's already (and still) present in the categories file
                if type(word) == str and str(word).lower() in sentence and sentence not in match_list:
                    match_list.append(sentence)
                    new_sentence = sentence + ' \n\n '
                    try:
                        self.voorkomen_themas[word] += new_sentence
                    except KeyError:
                        self.voorkomen_themas[word] = new_sentence
        return match_list

    def match2(self, list_of_sentences, list_of_words, match_word=''):
        # checks if the words of list_of_words appear in list_of_sentences voorkomt and returns a list of these (match_list)
        # for simplicity's sake, the matching words are always registered
        match_list = []
        index = 0
        self.matches[match_word] = []
        self.matching_subSets[match_word] = ''
        for sentence in list_of_sentences:
            subSet = self.subSentence(index, list_of_sentences).lower()
            for word in list_of_words:
                # the conditional of not being in the matchlist is deleted, beacause you want a point for every term that is in the subSet
                if str(word).lower() in subSet and type(word) == str:
                    match_list.append(subSet)
                    self.matches[match_word].append(str(word).lower())
                    self.matching_subSets[match_word] += subSet
            index += 1
        return match_list

    def loop(self):
        # kijkt of de woorden van de eerste matchlist in sentences voorkomen en gooit deze in een nieuwe match_list.
        # De score wordt in lijst gegooid and added to self.scores
        for pair in range(0, self.total_pairs()):  # deze nog aanpassen
            pair_A = self.pairs.iloc[pair, 0]
            pair_B = self.pairs.iloc[pair, 1]
            # match_list = self.match1(self.sentences, self.cat[pair_A])
            # match_list = self.match2(match_list, self.cat[pair_B], match_word = pair_A)
            match_list = self.match(self.cat[pair_A], self.cat[pair_B])
            variable = pair_A + ' * ' + pair_B
            self.scores[variable] = len(match_list)

    def score_document(self):
        # fills the dictionary self.scores  with all the variables you want
        # this is done in order to provide for current and future linear dependencies in the analysis
        self.scores['num_words'] = len(self.text.split())
        self.scores['num_sentences'] = len(self.sentences)
        self.scores['words_per_sentence'] = int(self.scores['num_words'] / self.scores['num_sentences'])
        self.scores['title'] = self.sentences[0]

    def unique_matches(self):
        # returns a copy of self.matches containing only the unique matches
        uniques = copy.deepcopy(self.matches)
        for key in uniques:
            if len(uniques[key]) > 0:
                uniques[key] = set(uniques[key])
            else:
                uniques[key] = ''
        return uniques

    def total_pairs(self):
        # calculating the total number of pairs
        # consider to integrate this, it is only used once
        first_column_name = self.pairs.columns[0]
        return len(self.pairs[first_column_name])


""" 
Class Folder, for all methods related to the entire dataset (in this case a folder of documents)
    loops through all the documents in the particular forlder and creates Doc instances
    only the relevant data of these instances is saved  and used for analysis.
This class is a legacy from earlier analyses and might be redundant in the current setup.
    However, for the convenient data structure (multiple variables with appropriate scope) 
    and future expansion, I decided to keep it for now. """


class Folder():
    def __init__(self, path_categories, path_pairs, folder_of_files):
        self.folder = folder_of_files
        # extract the words in the different categories to self.cat and the pairs to match in self.pairs
        self.cat = pd.read_excel(path_categories)
        self.pairs = pd.read_excel(path_pairs)
        # empty df's to be filled later
        self.matches = pd.DataFrame()
        self.scores = pd.DataFrame()
        self.unique_matches = pd.DataFrame()
        self.subSets = pd.DataFrame()
        self.voorkomen_themas = pd.DataFrame()
        self.wordcounts = pd.DataFrame()

    def loop_folder(self):
        # loops throught the folder provided in the __init__. Checks if the files are pdf.
        # if so, it creates an instance of Doc, runs the necessary analyses and saves the results in the class variables
        print('\n---starting loop in ', self.folder, '---')
        scores = {}
        matches = {}
        unique_matches = {}
        subSets = {}
        voorkomen_themas = {}
        wordcounts = {}
        for root, directories, files in os.walk('./' + self.folder + '/'):
            for file in files:
                if file[-4:] == 'docx':
                    print('  ', file)
                    new_doc = Doc(root + file, self.cat, self.pairs)
                    new_doc.loop()
                    new_doc.score_document()

                    title = file.split('_')[0]
                    scores[title] = new_doc.scores
                    matches[title] = new_doc.matches
                    unique_matches[title] = new_doc.unique_matches()
                    subSets[title] = new_doc.matching_subSets
                    voorkomen_themas[title] = new_doc.voorkomen_themas
                    wordcounts[title] = new_doc.wordCount()
        self.scores = pd.DataFrame.from_dict(scores, orient='index')
        self.matches = pd.DataFrame.from_dict(matches, orient='index')
        self.unique_matches = pd.DataFrame.from_dict(unique_matches, orient='index')
        self.subSets = pd.DataFrame.from_dict(subSets, orient='index')
        self.voorkomen_themas = pd.DataFrame.from_dict(voorkomen_themas, orient='index')
        self.wordcounts = pd.DataFrame.from_dict(wordcounts, orient='index')
        print('---loop finished---\n')

    def create_excel(self, title='Uitkomsten analyse'):
        fullTitle = "{} - {}.xlsx".format(title, datetime.datetime.now().strftime("%Y%m%d %H%M"))
        # creating the excel and preparing format
        new_excel = pd.ExcelWriter(fullTitle, engine='xlsxwriter')
        workbook = new_excel.book
        format1 = workbook.add_format()
        format1.set_text_wrap()
        format1.set_align('top')

        # write the individual sheets from instance data with a loop and add formatting
        # a good todo is converting the error-sensitive solution with two lists to one dict
        dfs = [data.wordcounts, data.scores, data.matches, data.unique_matches, data.voorkomen_themas, data.subSets,
               data.cat, data.pairs]
        sheetnames = ['woordtelling', 'scores', 'matchwoorden', 'unieke matchwoorden', 'zinnen met themawoord',
                      '3 zinnen met match', 'thema- en matchwoorden', 'zoekcombinaties']
        for i, df in enumerate(dfs):
            df.to_excel(new_excel, sheet_name=sheetnames[i])
            worksheet = new_excel.sheets[sheetnames[i]]
            worksheet.set_column('B:Z', 40, format1)

        # always save the file
        new_excel.save()
        print("file {} finished".format(fullTitle))


"""Do the actual analysis and create the exce file from instance data"""
# when a new category is added, add it to zoektermen.xlsx and koppeling.xlsx
data = Folder('20220717 - AlleWoorden.xlsx', 'koppeling.xlsx', 'doc100.docx')
data.loop_folder()
data.create_excel(title='20220717 - analyse coalitieakkoorden')  # automatisch datum eraan

# BIN, all deleted methods, just in case I need them again

"""
    def word_count(self):
        return len(self.text.split())

    def sentence_count(self):
        return len(self.sentences)

    def totals_categories(self):
        return self.scores.sum().sort_values(axis=0, ascending=False)

    def totals_exclusion(self, list_to_exclude):
        # deze is gecheckt met behulp van: analysis.scores.loc['Jaarverslag 2015 3B Wonen']
        df_exclude = self.scores[self.scores.columns.difference(list_to_exclude)]
        return df_exclude.sum(axis = 1).sort_values(axis=0,ascending=False)

    def totals_inclusion(self, list_to_include):
        # deze is gecheckt met behulp van: analysis.scores.loc['Jaarverslag 2015 Mooiland']
        df_include = self.scores[list_to_include]
        return df_include.sum(axis = 1).sort_values(axis=0,ascending=False)

    def rank_scores(self, df):
        return df.rank(ascending=False)

    def rank_scores_asc(self, df):
        return df.rank(ascending=True)

    def std_series(self, series):
        return (series - series.mean()) / series.std(ddof=0)

    def ompoolen(self, series):
        return series * -1

    def correction(self, series, series_to_correct_with, factor):
        factor2 = (float(1) - float(factor))
        return (series * factor2 + series_to_correct_with * factor)

    def grand_total(self, raw = False):
        aanspreekbaarheid = self.totals_exclusion(['words_per_sentence', 'num_sentences', 'num_words'])
        governance = self.totals_inclusion(['vtw_gover_visie * be_rvc', 'vtw_gover_govCode * be_rvc'])
        leesbaarheid = self.totals_inclusion(['words_per_sentence'])
        woorden = self.totals_inclusion(['num_words'])
        if raw == False:

            woorden = self.ompoolen((woorden))
            correctie_factor = 0.25
            aanspreekbaarheid = self.correction((aanspreekbaarheid), woorden, correctie_factor)
            governance = self.correction((governance), woorden, correctie_factor)
            leesbaarheid = self.ompoolen((leesbaarheid))
            grand_total = (((aanspreekbaarheid + governance + leesbaarheid)) / 3)
        else:
            grand_total = (((aanspreekbaarheid + governance + leesbaarheid))/3)
        return pd.DataFrame({'Aanspreekbaarheid' : aanspreekbaarheid, 'Governance' : governance, 'Leesbaarheid' : leesbaarheid, 'Woorden': woorden, 'Grand total' : grand_total}).sort_values(by='Grand total')

"""

