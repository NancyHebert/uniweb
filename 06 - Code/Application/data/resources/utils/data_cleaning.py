"""
@param the object the UniWeb return in form of:
{
	"123": {
	    "profile/membership_information": {
	      "first_name": "A",
	      "last_name": "B",
	      "account_type": [
	        "1",
	        "Professor"
	      ],
	      "position_title": [
	        "2",
	        "Full Professor",
	        "1"
	      ],
	      "academic_unit": [
	        "25",
	        "Epidemiology, Public Health and Preventive Medicine",
	        "Medicine",
	        "University of Ottawa"
	      ],
	      "email": "AB@uottawa.ca",
	      "homepage": "http://www.AB.ca"
        },
        "biography": []
    },
    {
    	....
    }
}

@return an object array in this format:
[
	{
		"id":"123",
		"profile/membership_information": {
			"first_name": "A",
			"last_name": "B",
			"account_type": "Professor" ,
			"position_title": "Full Professor",
			"academic_unit": "Epidemiology, Public Health and Preventive Medicine",
			"email": "AB@uottawa.ca",
			"homepage": "http://www.AB.ca"
		}
		"biography": null
	},
	{
		...
	}
]
"""

def cleanProfessorsList(obj):
	cleanObjectArray = []
	for k, v in obj.items():
		cleanObj = {}
		cleanObj['id'] = k
		# clean keys and arrays of individual profs objects
		cleanKeys(v)
		cleanArrays(v)
		# copy sections (keys and values) from the UW object
		for sectionKey, sectionValue in v.items():
			cleanObj[sectionKey] = sectionValue
		cleanObjectArray.append(cleanObj)

	return cleanObjectArray




"""
@param the object that UniWeb returns

@return: @param object 
- without "profile/" in keys,
- replace items like "account_type": ["1", "Professor"] by
				     "account_type": "Professor"
 
 No need to return anything explicitly,
 as operations are done in-place on the dictionary (mutable object type)
"""
def cleanProfObj(obj):
	for k, v in obj.items():
		cleanObj = {}
		cleanObj['id'] = k
		# clean keys and arrays
		cleanKeys(v)
		cleanArrays(v)
		# copy sections (keys and values) from the UW object
		for sectionKey, sectionValue in v.items():
			cleanObj[sectionKey] = sectionValue
		return cleanObj


# remove page name "profile/" or "cv/" before section names (key)
def cleanKeys(obj):
	keys = list(obj.keys()) # list() to create a copy of the mutable keys list
	for k in keys:
		if any(pageName in k for pageName in ["profile/", "cv/"]):
			obj[k.split('/')[1]] = obj.pop(k)


# clean array that has multple elements e.g. "account_type": ["1", "Professor"], by:
# replacing the array by the second element inside it e.g. "account_type": "Professor"
def cleanArrays(obj):
	for k, v in obj.items():
		if isinstance(v, list):
			if len(v) >= 2 and isinstance(v[0], str) and isInt(v[0]):
				# print('k, v in list: ', k, '\t', v)
				# clean the array, except "interest" (needed in TSS to construct tree of interests)
				if k == 'interest':
				    v.pop(0)
				else:
					obj[k] = v[1]
			elif len(v) == 0:
				 obj[k] = None
			else:
				for listElement in v:
					if isinstance(listElement, dict):
						cleanArrays(listElement)

		elif isinstance(v, dict):
			cleanArrays(v)


# auxiliary function to determine if a string value is integer
def isInt(value):
	try:
		int(value)
		return True
	except ValueError:
  		return False 


