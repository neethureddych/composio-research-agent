
import csv
from pathlib import Path
from html import escape
from collections import defaultdict


def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


research = read_csv("output/final_research.csv")
auth = read_csv("output/auth_distribution.csv")
toolkits = read_csv("data/composio_toolkits.csv")

total_apps = len(research)
toolkit_total = len(toolkits)

# Calculate category coverage from the corrected final dataset
category_stats = defaultdict(lambda: {"total": 0, "matched": 0})

for row in research:
    category = row["category"]
    category_stats[category]["total"] += 1

    if row["composio_match"] == "Found in Composio catalogue":
        category_stats[category]["matched"] += 1

total_matches = sum(x["matched"] for x in category_stats.values())
coverage_percent = total_matches / total_apps * 100 if total_apps else 0

category_rows = ""

for category, values in sorted(category_stats.items()):
    total = values["total"]
    matched = values["matched"]
    pct = matched / total * 100 if total else 0

    category_rows += f"""
    <tr>
      <td>{escape(category)}</td>
      <td>{total}</td>
      <td>{matched}</td>
      <td>{pct:.1f}%</td>
      <td><div class="bar"><span style="width:{pct}%"></span></div></td>
    </tr>
    """

# Authentication distribution
auth_rows = ""

for row in auth:
    method = row["authentication_method"]
    count = int(row["toolkit_count"])

    auth_rows += f"""
    <tr>
      <td>{escape(method)}</td>
      <td>{count:,}</td>
    </tr>
    """

# Verification counts
credential_verified = sum(
    row["credential_verification_status"]
    == "Verified against official documentation"
    for row in research
)

credential_pending = total_apps - credential_verified

doc_counts = defaultdict(int)

for row in research:
    doc_counts[row["research_status"]] += 1

pages_ok = doc_counts["Page fetched - manual verification required"]
http_review = doc_counts["HTTP response - manual review required"]
missing_url = doc_counts["Fetch failed: MissingSchema"]

# Known documentation exceptions
exceptions = []

for row in research:
    if row["research_status"] != "Page fetched - manual verification required":
        exceptions.append(row)

exception_rows = ""

for row in exceptions:
    exception_rows += f"""
    <tr>
      <td>{escape(row['app_name'])}</td>
      <td>{escape(row['research_status'])}</td>
      <td>{escape(row['status_code'] or 'N/A')}</td>
      <td>{escape(row['docs_url'] or 'No URL supplied')}</td>
    </tr>
    """

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Composio App Ecosystem Research</title>
<style>
:root {{
  --bg:#f5f7fb;
  --ink:#172033;
  --muted:#68748a;
  --line:#e4e9f1;
  --blue:#5267df;
}}
* {{box-sizing:border-box}}
body {{
  margin:0;
  background:var(--bg);
  color:var(--ink);
  font:15px/1.6 Segoe UI,Arial,sans-serif;
}}
header {{
  background:#111a35;
  color:white;
  padding:55px max(7%,calc((100% - 1120px)/2));
}}
header .tag {{
  color:#aebaff;
  text-transform:uppercase;
  letter-spacing:2px;
  font-size:12px;
  font-weight:bold;
}}
h1 {{
  font-size:clamp(32px,5vw,52px);
  line-height:1.1;
  margin:18px 0;
}}
header p {{max-width:760px;color:#d1d8ed}}
main {{max-width:1120px;margin:32px auto;padding:0 22px}}
section {{
  background:white;
  border:1px solid var(--line);
  border-radius:15px;
  padding:26px;
  margin:22px 0;
}}
h2 {{font-size:22px;margin-top:0}}
h3 {{font-size:17px}}
.metrics {{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(145px,1fr));
  gap:12px;
  margin-top:25px;
}}
.metric {{
  background:#202c50;
  border-radius:12px;
  padding:17px;
  color:white;
}}
.metric b {{font-size:30px;display:block}}
.metric span {{font-size:13px;color:#d1d8ed}}
table {{border-collapse:collapse;width:100%;font-size:13px}}
th,td {{
  text-align:left;
  padding:11px 9px;
  border-bottom:1px solid var(--line);
  overflow-wrap:anywhere;
}}
th {{color:var(--muted);font-size:11px;text-transform:uppercase}}
.bar {{
  height:9px;
  min-width:70px;
  background:#edf0f7;
  border-radius:10px;
  overflow:hidden;
}}
.bar span {{
  display:block;
  height:100%;
  background:linear-gradient(90deg,#5267df,#8a65d6);
}}
.note {{
  background:#f1f4ff;
  border-left:4px solid var(--blue);
  padding:14px;
  margin:15px 0;
}}
.warning {{
  background:#fff8e9;
  border-left:4px solid #d69b35;
  padding:14px;
  margin:15px 0;
}}
.cols {{
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
  gap:22px;
}}
li {{margin:8px 0}}
footer {{
  text-align:center;
  padding:30px;
  color:var(--muted);
  font-size:13px;
}}
@media(max-width:650px) {{
  section {{padding:17px}}
  header {{padding:40px 22px}}
  table {{font-size:11px}}
}}
</style>
</head>
<body>

<header>
<div class="tag">Product Operations · Research Case Study</div>
<h1>Mapping the<br>Composio App Ecosystem</h1>
<p>
A research pipeline examining catalogue coverage, authentication
patterns, credential accessibility and documentation availability
across the 100 applications specified in the assignment.
</p>
<div class="metrics">
  <div class="metric"><b>{total_apps}</b><span>Target applications</span></div>
  <div class="metric"><b>{coverage_percent:.0f}%</b><span>Exact-name catalogue coverage</span></div>
  <div class="metric"><b>{toolkit_total:,}</b><span>Toolkit records collected</span></div>
  <div class="metric"><b>{credential_verified}</b><span>Credential records verified</span></div>
</div>
</header>

<main>

<section>
<h2>01 · Executive summary</h2>
<p>
The research covers exactly 100 applications across 10 assignment
categories, with 10 apps in each category. A Python research pipeline
fetches documentation pages, collects Composio toolkit catalogue
records, compares application names, and organizes authentication
and credential-access findings.
</p>
<div class="note">
<b>Key finding:</b> {total_matches} of {total_apps} applications
({coverage_percent:.1f}%) have an exact normalized-name match
in the collected Composio catalogue.
</div>
<p>
An exact-name match is a discovery signal only. It does not prove
that all API actions, permissions or workflows are supported.
</p>
</section>

<section>
<h2>02 · Category-wise catalogue coverage</h2>
<p>Exact-name matches compared with the 100 target applications.</p>
<table>
<thead>
<tr><th>Category</th><th>Apps</th><th>Matches</th><th>Coverage</th><th>Visual</th></tr>
</thead>
<tbody>{category_rows}</tbody>
</table>
<p>
Productivity and Project Management has the highest exact-name
coverage (90%). Ecommerce has the lowest (30%).
</p>
</section>

<section>
<h2>03 · Authentication patterns</h2>
<p>
Authentication scheme occurrences across the collected toolkit
records.
</p>
<table>
<thead><tr><th>Authentication method</th><th>Occurrences</th></tr></thead>
<tbody>{auth_rows}</tbody>
</table>
<div class="warning">
These are scheme occurrences, not unique toolkits. One toolkit
may support multiple authentication methods. The catalogue-wide
distribution does not establish the authentication method for
every target application.
</div>
</section>

<section>
<h2>04 · Credential-access verification</h2>
<div class="metrics">
  <div class="metric"><b>{credential_verified}</b><span>Verified against official documentation</span></div>
  <div class="metric"><b>{credential_pending}</b><span>Pending verification</span></div>
</div>
<p>
The five verified apps are Slack, Discord, Intercom, Zendesk and
Twilio. Their review covers credential setup and authentication
information from official documentation.
</p>
<p>
The remaining {credential_pending} applications are explicitly
marked pending. No credential-access conclusion is claimed for them.
</p>
</section>

<section>
<h2>05 · Documentation-fetch results</h2>
<div class="metrics">
  <div class="metric"><b>{pages_ok}</b><span>Pages fetched; manual verification required</span></div>
  <div class="metric"><b>{http_review}</b><span>HTTP responses requiring review</span></div>
  <div class="metric"><b>{missing_url}</b><span>Missing documentation URL</span></div>
</div>
<p>
A successful fetch means the automated request received the recorded
successful HTTP response. It does not mean the API, authentication,
or buildability was manually verified.
</p>
<h3>Exceptions requiring manual review</h3>
<table>
<thead>
<tr><th>Application</th><th>Fetch result</th><th>HTTP status</th><th>Documentation URL</th></tr>
</thead>
<tbody>{exception_rows}</tbody>
</table>
</section>

<section>
<h2>06 · Research pipeline</h2>
<div class="cols">
<div>
<h3>Automated steps</h3>
<ul>
<li>Read the corrected 100-app assignment CSV.</li>
<li>Fetch documentation pages with Python requests and BeautifulSoup.</li>
<li>Capture page titles, descriptions, status codes and evidence URLs.</li>
<li>Collect toolkit records through the Composio SDK.</li>
<li>Compare normalized app names with toolkit names and slugs.</li>
<li>Calculate category coverage and authentication distributions.</li>
<li>Export consolidated research and review CSV files.</li>
</ul>
</div>
<div>
<h3>Human verification steps</h3>
<ul>
<li>Review whether alternate toolkit names are genuine aliases.</li>
<li>Verify authentication and credential setup using official docs.</li>
<li>Check REST or GraphQL API availability and API breadth.</li>
<li>Review existing MCP support and available actions.</li>
<li>Identify gated credentials, permissions and practical blockers.</li>
<li>Assess buildability for specific workflows.</li>
</ul>
</div>
</div>
</section>

<section>
<h2>07 · Limitations and next steps</h2>
<ul>
<li>Exact-name matching can miss integrations listed under alternate names.</li>
<li>Potential aliases must be checked before being counted as matches.</li>
<li>Documentation fetch success does not prove API functionality.</li>
<li>Only five credential-access records have been verified so far.</li>
<li>API breadth, REST/GraphQL details, MCP coverage and buildability still require systematic verification.</li>
<li>HTTP errors may reflect access restrictions or automated-request handling, not API unavailability.</li>
</ul>
<div class="warning">
<b>Research status:</b> This is a partially verified research dataset,
not a completed manual audit of all 100 applications. Pending fields
are deliberately disclosed rather than presented as confirmed facts.
</div>
<h3>Next improvements</h3>
<ul>
<li>Expand official documentation verification across all categories.</li>
<li>Review all 31 exact-name misses for legitimate alternate toolkit names.</li>
<li>Inspect toolkit actions and confirm actual integration coverage.</li>
<li>Complete API surface, credential accessibility and buildability assessments.</li>
</ul>
</section>

<section>
<h2>08 · Project artifacts</h2>
<ul>
<li><code>output/final_research.csv</code> — consolidated 100-app dataset.</li>
<li><code>output/research_results.csv</code> — documentation-fetch results.</li>
<li><code>output/credential_access_review.csv</code> — credential verification records.</li>
<li><code>output/auth_distribution.csv</code> — authentication scheme occurrences.</li>
<li><code>data/app_composio_comparison.csv</code> — exact-name catalogue comparison.</li>
<li><code>data/composio_toolkits.csv</code> — collected toolkit catalogue.</li>
<li><code>src/</code> — Python research and reporting scripts.</li>
</ul>
</section>

</main>
<footer>
Composio App Ecosystem Research · November 2026
</footer>
</body>
</html>
"""

Path("output/case_study.html").write_text(html, encoding="utf-8")

print("Corrected HTML case study created!")
print("Apps:", total_apps)
print("Exact-name matches:", total_matches)
print("Categories:", len(category_stats))
print("Toolkit records:", toolkit_total)
print("Credential verified:", credential_verified)
print("Credential pending:", credential_pending)
print("Documentation fetches:", pages_ok)
print("HTTP review:", http_review)
print("Missing documentation URL:", missing_url)
print("File: output/case_study.html")
