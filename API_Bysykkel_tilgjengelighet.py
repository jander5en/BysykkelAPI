# coding=utf-8
import json
import requests
import geocoder

while True:
    stations = requests.get('https://oslobysykkel.no/api/v1/stations', headers = {'Client-Identifier': '3a46c43689be4fc2b8f58aca57206a28'})
    availability = requests.get('https://oslobysykkel.no/api/v1/stations/availability', headers = {'Client-Identifier': '3a46c43689be4fc2b8f58aca57206a28'})
    parsed_stations = json.loads(stations.text)
    parsed_availability = json.loads(availability.text)
    #print(parsed_stations['stations'][0]['center']['latitude'])

    print("\nLegg inn adressen: ")
    print("(Hvis gateadresse legg gatenummer først, exit for å avslutte)")
    adresse = str("\'" + raw_input() + ", Oslo, NO\'")
    if adresse == "\'exit, Oslo, NO\'":
        print("\nThank you, come again!")
        break

    g = geocoder.osm(adresse)
    if g.latlng == None:
        print("\n ERROR ERROR BIP BOP BIIIP..... \n")
        continue
    print(g.latlng)

    funnet = False
    for counter in range(0,len(parsed_stations['stations'])):
        if (parsed_stations['stations'][counter]['center']['latitude'] < float(g.latlng[0]+0.005)) and (parsed_stations['stations'][counter]['center']['latitude'] > float(g.latlng[0]-0.005)):
            if (parsed_stations['stations'][counter]['center']['longitude'] < float(g.latlng[1]+0.005)) and (parsed_stations['stations'][counter]['center']['longitude'] > float(g.latlng[1]-0.005)):
                print("")
                print (parsed_stations['stations'][counter]['title'])
                print ("Antall sykler tilgjengelig: " + str(parsed_availability['stations'][counter]['availability']['bikes']))
                print ("Antall ledige låser: " + str(parsed_availability['stations'][counter]['availability']['locks']))
                funnet = True
    if funnet == False:
        print("\nDet er desverre ingen stativer i nærheten av adressen du søkte på")
