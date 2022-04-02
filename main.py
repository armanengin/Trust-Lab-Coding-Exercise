from warcio.archiveiterator import ArchiveIterator
import re
import requests

regex = re.compile(
    "(?=.*covid)(?=.*economy)")

entries = 0
matching_entries = 0
hits = 0
matching_urls = []

# r = re.compile(r'\bcovid\b | \b19\b', flags=re.I | re.X)
# s = "These are covid 19 oranges and apples and pears, but not pinapples or .."
# r.findall(s)


# file_name = "http://commoncrawl.s3.amazonaws.com/crawl-data/CC-MAIN-2019-30/segments/1563195523840.34/waarc/CC-MAIN-20190715175205-20190715200159-00000.warc.gz"

common_path = "http://commoncrawl.s3.amazonaws.com/"
file_path = "crawl-data/CC-MAIN-2020-16/segments/1585370490497.6/warc/CC-MAIN-20200328074047-20200328104047-00078.warc.gz"
file_name = common_path + file_path
# if len(sys.argv) > 1:
#     file_name = sys.argv[1]

stream = None
if file_name.startswith("http://") or file_name.startswith(
    "https://"
):
    stream = requests.get(file_name, stream=True).raw
else:
    stream = open(file_name, "rb")

for record in ArchiveIterator(stream):
    print(entries)
    if entries > 2000:
        break
    if record.rec_type == "warcinfo":
        continue

    if not ".com/" in record.rec_headers.get_header(
        "WARC-Target-URI"
    ):
        continue

    entries = entries + 1
    contents = (
        record.content_stream()
        .read()
        .decode("utf-8", "replace")
    )


    m = regex.search(contents)
    if m:
        matching_entries = matching_entries + 1
        hits = hits + 1
        m = regex.search(contents, m.end())
        matching_urls.append(contents)
        print("There is a matching entry")


print(
    "Python: "
    + str(hits)
    + " matches in "
    + str(matching_entries)
    + "/"
    + str(entries)
)