import csv
from unittest import skip
import requests
import json

class Entry:
  def __init__(self, name, playcount, change, rank):
    self.name = name
    self.playcount = playcount
    self.change = change
    self.rank = rank


def replaceCSV(newArtists):
    idx = 0
    rank = 1
    with open('Artists.csv', 'w', encoding='utf-8') as f:
        for l in newArtists:
            idx += 1
            f.write(str(l.change) + "," + str(idx) + "," + l.name + "," + str(l.playcount) + "," + str(l.rank))
            f.write('\n')            


def loadPrevList():

    with open('Artists.csv', newline='', encoding='utf-8') as csvfile:
        artists = list(csv.reader(csvfile))

    return artists

def loadLastFM():

    response = requests.get(
        "http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user=earljw&api_key=f754abe8f31a6125cf170af8c912a5ff&format=json&limit=600")
    
    return response.json()

def writeHTML(newArtists):
    lastRank = 0
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
            if p.rank != lastRank or p.rank == 1:
                f.write(str(p.rank))
            f.write("</td>")
            f.write("<td>")
            f.write(p.name)
            f.write("</td>")
            f.write("<td>")
            f.write(str(p.playcount))
            f.write("</td>")
            f.write("</tr>")
            lastRank = p.rank
        f.write("</table></body></html>")

def main():
    oldArtists = loadPrevList()
    newArtistsJson = loadLastFM()

    newArtists = []
    rank = 0
    lastPlaycount = -1
    skipping = 1
    for i in newArtistsJson["topartists"]["artist"]:
        if i["playcount"] != lastPlaycount:
            if skipping > 0:
                rank += skipping
                skipping = 1
            else:
                rank = rank + 1
        else:
            skipping += 1
        entry = Entry(i["name"], i["playcount"], 0, rank) 
        newArtists.append(entry)
        lastPlaycount = i["playcount"]
        
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
                #j.change = newidx - oldidx
                if len(k) > 4:
                    j.change = j.rank - int(k[4])
                else:
                    j.change = 0
                break

    replaceCSV(newArtists)
    writeHTML(newArtists)


main()