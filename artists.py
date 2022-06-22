import csv
import requests
import json

class Entry:
  def __init__(self, name, playcount, change):
    self.name = name
    self.playcount = playcount
    self.change = change


def replaceCSV(newArtists):
    rank = 0
    with open('Artists.csv', 'w', encoding='utf-8') as f:
        for l in newArtists:
            rank += 1
            f.write(str(l.change) + "," + str(rank) + "," + l.name + "," + str(l.playcount))
            f.write('\n')


def loadPrevList():

    with open('Artists.csv', newline='') as csvfile:
        artists = list(csv.reader(csvfile))

    return artists

def loadLastFM():

    response = requests.get(
        "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=earljw&api_key=KEY_HERE&format=json&limit=600")
    
    return response.json()

def writeHTML(newArtists):
    with open('artists.html', 'w', encoding="utf-8") as f:
        f.write("<html><head></head><body><table>")
        idx = 0
        for p in newArtists:
            idx += 1
            f.write("<tr>")
            f.write("<td>")
            if p.change > 0:
                f.write("<img src='down.png' width='13' height='17'/>")
                f.write(str(p.change))
            if p.change < 0:
                f.write("<img src='up.png' width='13' height='17'/>")
                f.write(str(p.change * -1))
            f.write("</td>")
            f.write("<td>")
            f.write(str(idx))
            f.write("</td>")
            f.write("<td>")
            f.write(p.name)
            f.write("</td>")
            f.write("<td>")
            f.write(str(p.playcount))
            f.write("</td>")
            f.write("</tr>")
        f.write("</table></body></html>")

def main():
    oldArtists = loadPrevList()
    newArtistsJson = loadLastFM()

    newArtists = []
    for i in newArtistsJson["topartists"]["artist"]:
        entry = Entry(i["name"], i["playcount"], 0)
        newArtists.append(entry)
        
    # Now that we have all the data loaded, figure out how much each entry has changed.

    newidx = 0
    oldidx = 0

    for j in newArtists:
        newidx += 1
        found = False
        oldidx = 0
        for k in oldArtists:
            oldidx += 1
            if j.name.encode("ascii", "ignore") == k[2].encode("ascii", "ignore"):
                found = True
            if(found):
                j.change = newidx - oldidx
                break



    replaceCSV(newArtists)
    writeHTML(newArtists)


main()