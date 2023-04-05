import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import argparse
import urllib




class Docscraper():

    def __init__(self, url, name):

        self.url = url
        self.name = name
        self.linklist = []


    def get_urls(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        linklist = []
        for link in soup.find_all('a'):
            endurl = link.get('href')
            if endurl:
                linklist.append(self.url+endurl)
        self.linklist = linklist

        print(f"Found {len(linklist)} links")

    def all_pdf_download(self):
        searched = 0
        print(self.name)
        for url in self.linklist:
            try:

                base_url = self.url

                folder_path = str(r"C:\Users\d.los\Downloads\pdfscraper brabant\websitefiles_" + self.name)
                if not os.path.exists(folder_path):
                    folder_path = os.mkdir(folder_path)

                # print("====== 1. Set savepath: {} ======".format(folder_path))

                # print("====== 2. Start searching ======")
                response = requests.get(base_url)
                response = requests.get(base_url, headers={'User-Agent': 'Custom'})
                soup = BeautifulSoup(response.text, "html.parser")

                search_res = soup.select("a[href$='.pdf']")

                # print(search_res)

                search_res = soup.get('a')
                if search_res and (search_res) != 0:
                    print("{} files found!!!".format(len(search_res)), 'in', self.name)
                    searched += len(search_res)

                    # print("====== 3. Start downloading ======")
                    for counter, link in enumerate(search_res):
                        # Name the pdf files using the last portion of each link which are unique in this case
                        filename = link['href'].split('/')[-1]
                        file_save_path = os.path.join(folder_path, link['href'].split('/')[-1])
                        # if args.print_all:
                        #     print("[{}/{}] {}".format(counter + 1, len(search_res), filename))
                        with open(file_save_path, 'wb') as f:
                            f.write(requests.get(urljoin(base_url, link['href'])).content)
                # print("====== 4. Finished!!! ======")
                # print("====== ============== ======")
            except:
                pass
        print(f'Downloaded {searched} documents')

if __name__ == "__main__":

    # ==== voorbeelcode =====
    # testlink
    # links = {'site' : 'https://www.africau.edu/'}
    # 'https://www.africau.edu/images/default/sample.pdf'

    # for key, value in links.items():
    #     s = Docscraper(value, key)
    #     s.get_urls()
    #     s.all_pdf_download()


    import pandas as pd

    gemeenten_brabant = pd.read_csv(r'support info/gemeenten in brabant.csv')
    gemeenten_websites = pd.read_csv(r'support info/gemeentewebsites nederland.csv')

    # merge the two datasets into one that contains 1. gemeentenamen 2. urls of that gemeente
    brabantframe = pd.merge(gemeenten_brabant, gemeenten_websites, how = 'left', left_on = 'Brabant_name', right_on = 'Gemeente_name')

    links = dict(zip(brabantframe['Brabant_name'], brabantframe['Gemeente_url']))

    for key, value in links.items():
        s = Docscraper(value, key)
        s.get_urls()
        s.all_pdf_download()




