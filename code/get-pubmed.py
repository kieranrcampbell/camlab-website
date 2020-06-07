

from pymed import PubMed
import yaml
pubmed = PubMed(tool="camlab", email="kieranrcampbell@gmail.com")

def get_author(author):
    if author['lastname'] != None:
        print(author)
        if "Kieran" in author['firstname'] and "Campbell" in author['lastname']:
            return f"<b>{author['lastname']}, {author['firstname']}</b>"
    return f"{author['lastname']}, {author['firstname']}"

def get_paper_dict(paper):
    authors = [get_author(author) for author in paper.authors]
    author_str = '; '.join(authors)
    paper_dict = {
        'title': paper.title,
        'journal': paper.journal,
        'authors': author_str,
        'paper_url': f"https://doi.org/{paper.doi}",
        'date': str(paper.publication_date)
    }
    return paper_dict


results = pubmed.query("Kieran R Campbell[Author]", max_results=500)
paper_dicts = [get_paper_dict(paper) for paper in results]


for pd in paper_dicts:
    line = yaml.dump(pd)
    lines = ['---\n', line, '---']
    with open(f"../content/publications/{pd['title']}md", 'w') as f:
        f.writelines(lines)
        