import requests
import json
 
namsor_base_url = "http://api.namsor.com/onomastics/api/json/gendre/{0}/{1}"
genderize_base_url = "https://api.genderize.io/"

def construct_genderize_query_dict(first_names):
	kvs = [("name[{0}]".format(i), first_name) for i, first_name in enumerate(first_names)]
	return dict(kvs)

def encode_gender(g):
	g = g.lower()
	if g in ["male", "m"]:
		return 1
	elif g in ["female", "f"]:
		return -1
	else:
		return 0

def resultify(name, gender):
	return tuple(name, encode_gender(gender))

def get_genderize_results(first_names):
	query_dict = construct_query_dict(first_names)
	res = requests.get(gender, params=query_dict)
	if res.status_code == requests.codes.ok:
		res_as_dict = json.loads(res.text.strip())
		return map(lambda r: resultify(r['name'], r['gender']), res_as_dict)
	else:
		return []

def genderize_batch_api(first_names):
	results = []
	k = 10
	cur = 0
	while cur < len(first_names):
		names = [first_names[i] for i in range(cur, cur + k)]
		cur += k
		results += get_genderize_results(names)
	return results

def namsor_api(first_name, last_name='None'):
	url = namsor_base_url.format(first_name, last_name)
	res = requests.get(url)
	if res.status_code == requests.code.ok:
		return resultify(r['firstName'], r['gender'])
	else:
		return []