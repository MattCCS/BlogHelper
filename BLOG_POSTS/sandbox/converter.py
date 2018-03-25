import re

url_matching_regex = "(?P<url>https?://[^\s]+)" # source: http://stackoverflow.com/questions/839994/extracting-a-url-in-python

with open("source.py", "r") as f:
    print """<pre style="display:inline-block; border:1px solid Black; padding:5; line-height=1.2em;">\
<code style="line-height=0em;">%s</code></pre>""" % re.sub("(?P<url>https?://[^\s]+)", '<a href="\g<url>">\g<url></a>', f.read())