import requests
import csv 



def get_abstract_from_doi(doi):
    base_url = "https://api.crossref.org/works/"
    url = f"{base_url}{doi}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses (4xx and 5xx)
        result = response.json()
        abstract = result['message']['abstract']
        abstract = abstract.removeprefix('<jats:title>Abstract</jats:title><jats:p>')
        abstract = abstract.removesuffix('</jats:p>')
        return abstract
    except Exception as e:
        print(f"Error fetching abstract for DOI {doi}: {e}")
        return None
    
# 0 Conference
# 1 Year
# 2 Title
# 3 DOI
# 4 Abstract
# 5 AuthorNames-Deduped
# 6 Award

abstracts_found = 0
abstracts_missing = 0
with open("papers.csv", "r") as source: 
	reader = csv.reader(source)
	with open("papers-abstracted.csv", "w") as result:
		writer = csv.writer(result) 
		for r in reader: 
			print(r[1], r[3])
			if r[4] != '':
				abstract = r[4]
			else:
				abstract = get_abstract_from_doi(r[3])
				if abstract is None:
					print('\tskipped')
					abstracts_missing += 1
					abstract = ''
				else:
					print('\tfound')
					abstracts_found += 1
			writer.writerow((r[0], r[1], r[2], r[3], abstract, r[5], r[6]))
print(abstracts_found, ' of ' , abstracts_missing + abstracts_found)
