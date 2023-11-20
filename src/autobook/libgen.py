from grab_fork_from_libgen import LibgenSearch

res = LibgenSearch('fiction', q='cloud cuckoo land')

res.get_results()

filters = {
    "author(s)": "Anthony Doerr",
    # "title": "Cloud Cuckoo Land"
}

res.get(save_to='.',**filters)