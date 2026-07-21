@echo off
REM ============================================================
REM IndexNow batch submission for Aetas Wealth
REM Sends all 76 sitemap URLs to Bing's IndexNow API in one call
REM ============================================================

cd /d "%~dp0"

echo Submitting 76 URLs to IndexNow...
echo.

curl -X POST "https://api.indexnow.org/indexnow" ^
  -H "Content-Type: application/json; charset=utf-8" ^
  -H "Host: api.indexnow.org" ^
  -d "@payload.json" ^
  -w "\nHTTP Status: %%{http_code}\n"

echo.
echo Done. A status of 200 or 202 means success.
echo.
pause
