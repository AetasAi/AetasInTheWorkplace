IndexNow batch submission for Aetas Wealth
============================================

This package submits all 76 sitemap URLs to Bing IndexNow in one POST request.
Bing will then prioritise crawling these pages within hours rather than days.

Files in this package:
  - submit-to-indexnow.bat   Windows script that runs the submission
  - payload.json             The list of URLs and your API key
  - README.txt               This file

HOW TO USE:

1. Extract all three files into the same folder anywhere on your computer
   (e.g. C:\Temp\indexnow-batch\)

2. Double-click submit-to-indexnow.bat

3. A black Command Prompt window opens, runs curl, and prints the response.

4. Look for "HTTP Status: 200" or "HTTP Status: 202" — both mean success.

5. Press any key to close the window.

WHAT YOU'RE LOOKING FOR:

  200 OK                      - All URLs submitted successfully
  202 Accepted                - URLs accepted, queued for crawling (also success)
  400 Bad Request             - Malformed payload (let me know)
  403 Forbidden               - Key validation failed (check the key file is live)
  422 Unprocessable Entity    - URLs don't match the host (let me know)
  429 Too Many Requests       - Rate limited (wait and retry)

ONE-TIME USE:

You only need to run this once. After the response is 200/202, Bing will
process the queue over the next few hours and your pages will be re-crawled
with the new schema picked up.

If you want to do this again in future (e.g. after a major content update),
just double-click the .bat file again. No re-setup needed as long as the key
file at https://aetas-wealth.com/05c082a578194ff5a6d02ad11d2a1456.txt remains.
