@echo off
REM ============================================================
REM IndexNow: submit /book.html to Bing
REM ============================================================

echo Submitting https://aetas-wealth.com/book.html to IndexNow...
echo.

curl -X POST "https://api.indexnow.org/indexnow" ^
  -H "Content-Type: application/json; charset=utf-8" ^
  -d "{\"host\":\"aetas-wealth.com\",\"key\":\"05c082a578194ff5a6d02ad11d2a1456\",\"keyLocation\":\"https://aetas-wealth.com/05c082a578194ff5a6d02ad11d2a1456.txt\",\"urlList\":[\"https://aetas-wealth.com/book.html\"]}" ^
  -w "\nHTTP Status: %%{http_code}\n"

echo.
echo Look for HTTP Status: 200 or 202 - both mean success.
echo.
pause
