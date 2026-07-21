# ============================================================
#  Aetas Performance - Logo + strapline deployment
#  1) Simplifies the logo to rings + "AETAS" (drops Performance/tagline
#     from the lockup) using a crisp SVG.
#  2) Adds the strapline "Financial wellbeing that drives business
#     Performance" (script + flourish + fade-in) as a soft band under
#     the logo, inside the sticky header - matching the Wealth site.
#  Then commits and pushes. Cloudflare Pages redeploys on push.
#
#  Run from the Performance repo root, e.g.:
#      cd C:\Repos\AetasInTheWorkplace
#      .\deploy-performance-brand.ps1
# ============================================================
$ErrorActionPreference = "Stop"

if (-not (Test-Path "CNAME") -or ((Get-Content -Raw "CNAME").Trim() -ne "performance.aetas-wealth.com")) {
    Write-Error "This does not look like the Aetas Performance repo root (CNAME missing or not 'performance.aetas-wealth.com'). Aborting."
    exit 1
}

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

# --- 1) Write the new AETAS logo SVG ---
$svg = @'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 789.3 170.0" role="img" aria-label="Aetas">
  <title>Aetas</title>
  <g transform="translate(10.00,10.00) scale(0.50000)">
    <g fill="none" stroke-width="14" stroke-linecap="round">
      <circle cx="198" cy="197" r="92" stroke="#005357"/>
      <circle cx="152" cy="102" r="92" stroke="#0d2c6c"/>
      <circle cx="95" cy="193" r="92" stroke="#00aabb"/>
      <path d="M 157.25 279.48 A 92 92 0 0 1 131.49 260.57" stroke="#005357"/>
      <path d="M 136.62 128.47 A 92 92 0 0 1 163.77 111.61" stroke="#005357"/>
    </g>
  </g>
  <g fill="#0d2c6c"><path transform="translate(200.00,144.00) scale(0.16738,-0.16738)" d="M499 124H237L195 0H16L270 702H468L722 0H541ZM455 256 368 513 282 256ZM1030 565V423H1259V291H1030V137H1289V0H859V702H1289V565ZM1965 702V565H1779V0H1608V565H1422V702ZM2548 124H2286L2244 0H2065L2319 702H2517L2771 0H2590ZM2504 256 2417 513 2331 256ZM2888 210H3070Q3074 171 3097.0 150.5Q3120 130 3157 130Q3195 130 3217.0 147.5Q3239 165 3239 196Q3239 222 3221.5 239.0Q3204 256 3178.5 267.0Q3153 278 3106 292Q3038 313 2995.0 334.0Q2952 355 2921.0 396.0Q2890 437 2890 503Q2890 601 2961.0 656.5Q3032 712 3146 712Q3262 712 3333.0 656.5Q3404 601 3409 502H3224Q3222 536 3199.0 555.5Q3176 575 3140 575Q3109 575 3090.0 558.5Q3071 542 3071 511Q3071 477 3103.0 458.0Q3135 439 3203 417Q3271 394 3313.5 373.0Q3356 352 3387.0 312.0Q3418 272 3418 209Q3418 149 3387.5 100.0Q3357 51 3299.0 22.0Q3241 -7 3162 -7Q3085 -7 3024.0 18.0Q2963 43 2926.5 92.0Q2890 141 2888 210Z"/></g>
</svg>
'@
[System.IO.File]::WriteAllText([System.IO.Path]::GetFullPath("aetas-logo.svg"), $svg, $utf8NoBom)
Write-Host "Wrote aetas-logo.svg"

# --- markup pieces ---
$logoImg = '<img class="brand-logo" fetchpriority="high" src="/aetas-logo.svg" alt="Aetas" width="241" height="52" style="height:52px;width:auto;max-width:none;display:block">'
$band = '<div class="brand-strapline" style="background:#f4f6fb;border-top:1px solid #e6e8ee;"><div class="aetas-strap" style="max-width:1200px;margin-inline:auto;padding-inline:clamp(1.25rem,4vw,2.5rem);padding-block:8px;text-align:left;font-size:0.9rem;font-weight:600;letter-spacing:0.02em;color:#00205B;font-family:''Open Sans'',-apple-system,BlinkMacSystemFont,sans-serif;">Financial wellbeing that drives business <span class="wb">Performance</span></div></div>'
$head = @'
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&display=swap" rel="stylesheet">
<style id="aetas-strap-style">
@keyframes aetasStrapIn{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:translateY(0)}}
.aetas-strap{animation:aetasStrapIn 1s ease .15s both}
.aetas-strap .w{color:#00205B;font-weight:700}
.aetas-strap .wb{font-family:'Dancing Script',cursive;font-weight:700;font-size:1.55em;color:#00747E;line-height:1;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='130' height='9' viewBox='0 0 130 9'%3E%3Cpath d='M2 6 C 34 2, 96 2, 128 5' stroke='%2300aabb' stroke-width='2.4' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");background-repeat:no-repeat;background-position:left 100%;background-size:100% 7px;padding:0 2px 5px}
</style>
'@
$headRepl = ($head -replace '\$','$$$$') + "`n</head>"

# --- regexes ---
$opt = [System.Text.RegularExpressions.RegexOptions]::Singleline
$brandRx = [regex]::new('<span class="brand-mark"><img[^>]*></span>\s*<span class="brand-text">\s*<span class="brand-name">AETAS</span>\s*<span class="brand-division">Performance</span>\s*(?:<span class="brand-tagline">[^<]*</span>\s*)?</span>', $opt)
$hdrRx = [regex]::new('(<header class="site-header">.*?)</header>', $opt)
$bandEval = { param($m) $m.Groups[1].Value + $band + "`n</header>" }

$changed = 0
Get-ChildItem -Path . -Recurse -Filter *.html | ForEach-Object {
    $raw = [System.IO.File]::ReadAllText($_.FullName)
    $new = $raw
    # logo
    if (($new -notmatch 'brand-logo') -and $brandRx.IsMatch($new)) {
        $new = $brandRx.Replace($new, $logoImg, 1)
    }
    # strapline band (+ head css/font), only where there is a site header
    if (($new -notmatch 'brand-strapline') -and $hdrRx.IsMatch($new)) {
        if ($new -notmatch 'aetas-strap-style') {
            $new = [regex]::Replace($new, '</head>', $headRepl, 1)
        }
        $new = $hdrRx.Replace($new, $bandEval, 1)
    }
    if ($new -ne $raw) {
        [System.IO.File]::WriteAllText($_.FullName, $new, $utf8NoBom)
        $changed++
        Write-Host ("  updated: " + $_.FullName.Substring((Get-Location).Path.Length + 1))
    }
}
Write-Host ("Updated $changed page(s).")

if ($changed -eq 0) { Write-Warning "Nothing changed - not committing."; exit 0 }

git add -A
$pending = git status --porcelain
if ([string]::IsNullOrWhiteSpace($pending)) {
    Write-Host "No changes to commit."
} else {
    git commit -m "Simplify logo to AETAS + add 'wellbeing drives Performance' strapline (script) site-wide"
    git push
    Write-Host ""
    Write-Host "Committed and pushed. Cloudflare Pages will redeploy in a minute or two."
}
