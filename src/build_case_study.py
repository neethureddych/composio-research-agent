import csv
from pathlib import Path
from html import escape

def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

categories = read_csv("output/category_coverage.csv")
auth = read_csv("output/auth_distribution.csv")
research = read_csv("output/final_research.csv")
credentials = read_csv("output/credential_access_review.csv")
toolkits = read_csv("data/composio_toolkits.csv")
pages = read_csv("output/research_results.csv")

total_apps = len(research)
matches = sum(int(x["exact_matches"]) for x in categories)
toolkit_total = len(toolkits)
credential_verified = sum(
    x["verification_status"] == "Verified against official documentation"
    for x in credentials
)
fully_verified = sum(
    x["verification_status"] == "Manually verified against official documentation"
    for x in research
)
credential_only = sum(
    x["verification_status"] == "Credential access verified; other research fields pending"
    for x in research
)
manual_review = sum(
    x["verification_status"] == "Manual review required"
    for x in research
)
pending = sum(
    x["verification_status"] == "Needs official documentation review"
    for x in research
)
pages_ok = sum(str(x.get("status_code", "")) == "200" for x in pages)

category_rows = ""
for x in categories:
    pct = float(x["coverage_percent"])
    category_rows += f"""
    <tr>
      <td>{escape(x['category'])}</td>
      <td>{x['total_apps']}</td>
      <td>{x['exact_matches']}</td>
      <td>{pct:.1f}%</td>
      <td><div class="bar"><span style="width:{pct}%"></span></div></td>
    </tr>"""

auth_rows = ""
max_auth = max(int(x["toolkit_count"]) for x in auth)
for x in auth:
    count = int(x["toolkit_count"])
    width = count / max_auth * 100
    auth_rows += f"""
    <div class="auth-row">
      <div class="auth-label"><span>{escape(x['authentication_method'])}</span><b>{count:,}</b></div>
      <div class="bar"><span style="width:{width:.2f}%"></span></div>
    </div>"""

status_rows = f"""
<div class="status-grid">
  <div><b>{fully_verified}</b><span>Fully manually verified</span></div>
  <div><b>{credential_only}</b><span>Credential review verified; other fields pending</span></div>
  <div><b>{pending}</b><span>Documentation review pending</span></div>
  <div><b>{manual_review}</b><span>Manual review required</span></div>
</div>"""

html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Composio App Ecosystem Research | Case Study</title>
<style>
:root{--bg:#f5f7fb;--ink:#172033;--muted:#68748a;--line:#e4e9f1;--blue:#5267df;--purple:#8a65d6;--white:#fff}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.6 Inter,Segoe UI,Arial,sans-serif}
header{background:#111a35;color:white;padding:64px max(7%,calc((100% - 1120px)/2))}
header .tag{color:#aebaff;text-transform:uppercase;letter-spacing:2px;font-size:12px;font-weight:700}
h1{font-size:clamp(32px,5vw,54px);line-height:1.1;margin:18px 0}
header p{max-width:760px;color:#d1d8ed;font-size:17px}
main{max-width:1120px;margin:34px auto;padding:0 22px}
section{background:white;border:1px solid var(--line);border-radius:16px;padding:28px;margin:22px 0;box-shadow:0 5px 20px #1c2b4a08}
h2{font-size:23px;margin:0 0 14px}
h3{font-size:17px;margin:22px 0 8px}
.sub{color:var(--muted);margin-top:-8px}
.metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(155px,1fr));gap:14px;margin-top:25px}
.metric{background:#202c50;border-radius:13px;padding:20px;color:white}
.metric b{font-size:32px;display:block;line-height:1.2}
.metric span{color:#d1d8ed;font-size:13px}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:left;padding:12px 10px;border-bottom:1px solid var(--line)}
th{color:var(--muted);font-size:12px;text-transform:uppercase}
.bar{height:9px;background:#edf0f7;border-radius:10px;overflow:hidden;min-width:90px}
.bar span{display:block;height:100%;background:linear-gradient(90deg,var(--blue),var(--purple));border-radius:10px}
.auth-row{margin:15px 0}
.auth-label{display:flex;justify-content:space-between;margin-bottom:5px}
.status-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px}
.status-grid div{background:#f3f5fb;border-radius:10px;padding:16px}
.status-grid b{display:block;font-size:27px}
.status-grid span{font-size:13px;color:var(--muted)}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:24px}
li{margin:8px 0}
.note{background:#f4f5ff;border-left:4px solid var(--blue);padding:14px 17px;border-radius:7px}
.warning{background:#fff8e9;border-left:4px solid #d69b35;padding:14px 17px;border-radius:7px}
footer{text-align:center;color:var(--muted);padding:30px;font-size:13px}
@media(max-width:650px){section{padding:19px}header{padding:42px 22px}table{font-size:12px}th,td{padding:9px 5px}}
</style>
</head>
<body>
<header>
<div class="tag">Product Operations · Research Case Study</div>
<h1>Mapping the<br>Composio App Ecosystem</h1>
<p>A research pipeline to assess app coverage, authentication patterns, credential accessibility and integration feasibility across 100 popular applications.</p>
<div class="metrics">
<div class="metric"><b>100</b><span>Target applications</span></div>
<div class="metric"><b>__MATCHES__%</b><span>Exact-name catalogue coverage</span></div>
<div class="metric"><b>__TOOLKITS__</b><span>Composio toolkit records collected</span></div>
<div class="metric"><b>__CREDENTIALS__</b><span>Credential-access sample verified</span></div>
</div>
</header>
<main>
<section>
<h2>01 · Executive summary</h2>
<p>The project compares a target list of 100 applications across nine categories with the Composio toolkit catalogue. It combines automated documentation-page inspection, catalogue extraction, exact-name matching, authentication analysis and a manually reviewed credential-access sample.</p>
<div class="note"><b>Key finding:</b> 72 of the 100 target apps matched the catalogue by normalized exact name. This is a catalogue-name coverage measure, not proof that every matched integration supports every desired workflow.</div>
</section>

<section>
<h2>02 · Category coverage</h2>
<p class="sub">Exact-name matches compared with the target application list.</p>
<table>
<thead><tr><th>Category</th><th>Target</th><th>Matches</th><th>Coverage</th><th>Visual</th></tr></thead>
<tbody>__CATEGORY_ROWS__</tbody>
</table>
<p class="sub">Productivity had the highest exact-name coverage; E-commerce had the lowest.</p>
</section>

<section>
<h2>03 · Authentication patterns</h2>
<p class="sub">Authentication scheme occurrences across the returned toolkit records.</p>
__AUTH_ROWS__
<div class="warning"><b>How to interpret this:</b> These counts are scheme occurrences, not unique toolkits. A toolkit can support more than one authentication method, so the counts overlap.</div>
</section>

<section>
<h2>04 · Verification status</h2>
__STATUS_ROWS__
<p>Credential-access details were manually reviewed for a 10-app sample: Slack, Discord, Microsoft Teams, Zoom, Google Meet, Gmail, Outlook, Intercom, Zendesk and Twilio.</p>
<p>Slack also has additional manually verified research fields in the main dataset. The other nine sample apps have credential-access verification only; their remaining research fields are still pending.</p>
</section>

<section>
<h2>05 · Research agent and workflow</h2>
<div class="cols">
<div>
<h3>Automated steps</h3>
<ul>
<li>Read the target application list from CSV.</li>
<li>Fetch documentation pages using Python requests and BeautifulSoup.</li>
<li>Capture page titles, descriptions, HTTP status and evidence URLs.</li>
<li>Use the Composio SDK to collect toolkit records across catalogue pages.</li>
<li>Normalize names and compare target apps with toolkit names.</li>
<li>Summarize category coverage and authentication scheme occurrences.</li>
<li>Export findings and review queues into CSV files.</li>
</ul>
</div>
<div>
<h3>Human review steps</h3>
<ul>
<li>Confirm whether similar names are genuine aliases.</li>
<li>Inspect official documentation for auth flows and API scope.</li>
<li>Determine whether credentials are self-serve or gated.</li>
<li>Check MCP availability and practical integration blockers.</li>
<li>Assess buildability for a specific workflow.</li>
<li>Resolve access errors and ambiguous documentation.</li>
</ul>
</div>
</div>
</section>

<section>
<h2>06 · Evidence, limitations and next steps</h2>
<ul>
<li>Documentation-page fetch success: __PAGES_OK__ of __PAGES_TOTAL__ pages returned HTTP 200 in the recorded run.</li>
<li>Catalogue collection: __TOOLKITS__ toolkit records collected through the Composio SDK.</li>
<li>Exact-name matching does not detect every alias; fuzzy candidates require human confirmation.</li>
<li>Page fetching confirms that a page responded, not that its API, authentication or buildability details have been verified.</li>
<li>Credential access was reviewed for a 10-app sample, not all 100 apps.</li>
<li>Some research fields for most apps remain pending official documentation review.</li>
</ul>
<div class="warning"><b>Known limitation:</b> Salesforce documentation returned an access error during the recorded fetch. It was flagged for manual review rather than treated as verified.</div>
<h3>Next improvements</h3>
<ul>
<li>Expand official-documentation verification beyond the initial 10-app sample.</li>
<li>Review all fuzzy alias candidates manually.</li>
<li>Verify API breadth, MCP support and workflow-specific buildability.</li>
<li>Deploy this report and publish the source repository with safe setup instructions.</li>
</ul>
</section>
<section>
<h2>07 · Project artifacts</h2>
<ul>
<li><code>output/final_research.csv</code> — consolidated application research records.</li>
<li><code>output/research_results.csv</code> — documentation fetch results.</li>
<li><code>output/category_coverage.csv</code> — category-level exact-name coverage.</li>
<li><code>output/auth_distribution.csv</code> — authentication scheme counts.</li>
<li><code>output/credential_access_review.csv</code> — credential-access review queue and sample.</li>
<li><code>data/composio_toolkits.csv</code> — collected Composio toolkit catalogue.</li>
</ul>
</section>
</main>
<footer>Composio App Ecosystem Research · Generated from project CSV outputs · November 2026</footer>
</body>
</html>
"""

values = {
    "__MATCHES__": f"{matches / total_apps * 100:.0f}",
    "__TOOLKITS__": f"{toolkit_total:,}",
    "__CREDENTIALS__": str(credential_verified),
    "__CATEGORY_ROWS__": category_rows,
    "__AUTH_ROWS__": auth_rows,
    "__STATUS_ROWS__": status_rows,
    "__PAGES_OK__": str(pages_ok),
    "__PAGES_TOTAL__": str(len(pages)),
}

for key, value in values.items():
    html = html.replace(key, value)

Path("output/case_study.html").write_text(html, encoding="utf-8")
print("HTML case study created successfully!")
print("File: output/case_study.html")
print("Apps:", total_apps, "| Exact matches:", matches)
print("Toolkits:", toolkit_total, "| Credential sample:", credential_verified)
print("Page fetches returning HTTP 200:", pages_ok, "of", len(pages))
print("Fully verified research records:", fully_verified)
print("Credential-only verified records:", credential_only)
print("Pending records:", pending, "| Manual review:", manual_review)
