import pandas as pd
import requests
from bs4 import BeautifulSoup
import progressbar
import time
import re

# Use the Excel file provided by Springer
df = pd.read_excel(r'../Free+English+textbooks.xlsx')
rowCount = df.shape[0]

progress = progressbar.ProgressBar(maxval=rowCount, redirect_stdout=True).start()
for p in range(rowCount):
    url = df.iloc[p, 18]
    year = str(df.iloc[p, 4])
    author = str(df.iloc[p, 1])
    title = str(df.iloc[p, 0])
    filename = author + ' ('+year+') '+title
    filenameValid = re.sub("[/:*?<>|]", "-", filename)
    # Use your own username or custom location
    saveLocation = '../books/' + filenameValid + '.'

    try:
        with open(saveLocation + 'pdf') as f:
            pass
        # with open(saveLocation + 'epub') as f:
        #     pass
        print('Already downloaded:', title)
        progress.update(p + 1, force=True)
        continue
    except FileNotFoundError:
        pass

    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html5lib')

    success = []
    for fmt in ['pdf', 'epub']:
        table = soup.find('a', attrs={'class': f'test-book{fmt}-link'})
        if not table and fmt == 'epub':
            # print('EPUB not available:', title)
            continue

        table = table.get("href")
        link = "https://link.springer.com" + table

        r2 = requests.get(link)
        with open(saveLocation + fmt, 'wb') as f:
            f.write(r2.content)

        success.append(f'[{fmt.upper()}]')

    print('Successful download:', title, *success)
    progress.update(p + 1, force=True)

progress.update(rowCount, force=True)
