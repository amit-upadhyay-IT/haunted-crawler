## haunted-crawler

> A crawler for downloading all files of a particular extension present within a server.


**TODO**:
- The program won't work properly if there is a referenced url and it contains a '.' in it's path (as it will ignore the next calls if not matched with `match_type`). I should explicitly check and ignore the apt extensions.
- The downloading and crawing are working synchronously, make them async.
- I think there can be an easy solution using regex, just make sure that the url has particular extension using regex otherwise recursively crawl for other links
