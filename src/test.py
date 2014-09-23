import urllib2, re
html = urllib2.urlopen("http://www.creative-role-playing.com/fantasy-sounding-names/")
m = re.findall("<td>([a-zA-Z].*?)</td>", html.read())
f = open("fantasy_names.txt", "w")
for x in m:
    f.write(x + "\n")
f.close()
