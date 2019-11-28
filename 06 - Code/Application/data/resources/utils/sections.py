def concatPagesSections(sections):
    """ put together the name and page (profile or cv), to use in UniWeb queries  	"""
    sectionsArray = []
    for row in sections:
        sectionsArray.append(row['page']+'/'+row['name'])
    return sectionsArray