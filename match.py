import pymongo, math, json

similarity_points = dict()

def compare(person,potential):
    points = 0
    for person_att in person:
        for potential_att in potential:
            if(person_att.lower() == potential_att.lower()):
                points = points + 1
    return points

def similar(person,json_data):

    for potential in json_data:
        if potential['id'] == person['id'] or person['id'] in potential["other_matches"]:
            similarity_points[potential['id']]=-1
        else:
            #compare age. the older the age gap the better.
            similarity_points[potential['id']]=similarity_points.get(potential['id'],0) + math.fabs(int(person['age'])-int(potential['age']))

            #compare school. potentially implement geographic location / other similarity.
            if(person['school'].lower() == potential['school'].lower()):
                similarity_points[potential['id']]=similarity_points.get(potential['id'],0)+1

            #compare hobbies
            similarity_points[potential['id']]=similarity_points.get(potential['id'],0)+compare(person['hobbies'],potential['hobbies'])

            #compare animal
            similarity_points[potential['id']]=similarity_points.get(potential['id'],0)+compare(person['animals'],potential['animals'])

            #compare food
            similarity_points[potential['id']]=similarity_points.get(potential['id'],0)+compare(person['foods'],potential['foods'])

            #similarity_points{people['id'],similarity_points.get(people['id']) + get_picture_similarity}
    
    highest = 0
    match = ""
    for key, value in similarity_points.iteritems():
        if(value > highest):
            highest = value
            match = key

    return match

def match():
    data = """[{"id":"id1", "name": "Abe", "age": "22", "school":"school 1", "hobbies": ["acting"], "animals":["dog"], "foods":["apple"],"other_matches": ["hello"]},
    {"id":"id2", "name": "Bella", "age": "22", "school":"school 2", "hobbies": ["baseball"], "animals":["cat"], "foods":["apple"],"other_matches": [""]},
    {"id":"id3", "name": "Cat", "age": "21", "school":"school 3", "hobbies":["acting"], "animals":["dog"], "foods":["orange"],"other_matches": [""]},
    {"id":"id4", "name": "Dan", "age": "20", "school":"school 4", "hobbies": ["nothing"], "animals":["bunny"], "foods":["poo"],"other_matches": [""]}]"""

    json_data = json.loads(data)

    match = similar(json_data[0],json_data)

    for person in json_data:
        if match == person['id']:
            print json_data[0]['other_matches']
            json_data[0]['other_matches'].append(match)
            print json_data[0]['other_matches']

if __name__ == "__main__":
    match() 



