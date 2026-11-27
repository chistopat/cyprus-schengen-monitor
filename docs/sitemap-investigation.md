# Sitemap fetch investigation — 27 November 2026

## Verified server response

The production `sitemap.xml` returns HTTP 200, `Content-Type: application/xml`, no redirect and no `X-Robots-Tag` restriction. Its XML contains 18 distinct canonical URLs under the verified project URL prefix. It matches the built artifact. A synthetic request with a Googlebot User-Agent also returns 200; this is a server check, not proof of an actual Googlebot visit.

The domain-root `https://chistopat.github.io/robots.txt` returns 404. This is not a disallow directive. Search Console shows no manual actions and no security issues.

## Actual Google live fetch

Search Console's live URL inspection tested the sitemap itself on 27 November 2026 at 15:00:51 Asia/Nicosia. It reported:

- Crawled as: Google Inspection Tool smartphone.
- Crawl allowed: Yes.
- Page fetch: Successful.
- Indexing allowed: Yes.

The tested-page SOURCE panel displayed the XML declaration, the `urlset`, canonical page URLs and the expected XHTML language alternates. Google therefore retrieved the sitemap content in this live test. This is separate from processing by the sitemap ingestion system.

## Sitemaps report

The original sitemap was submitted again after that successful live fetch. The report still showed `Type: Unknown`, an empty `Last read`, `Couldn't fetch` and zero discovered pages. No specific HTTP, DNS or XML parsing error was exposed in its details.

A minimal additional map, `sitemap-pages.xml`, was generated with the same 18 canonical URLs, without extension elements. It passed the official Sitemap Protocol XSD validation, was deployed by a successful GitHub Actions run, and returned HTTP 200 with the exact built XML before being submitted. It also initially showed `Unknown`, an empty `Last read`, `Couldn't fetch` and zero discovered pages. The multilingual primary map and HTML hreflang links remain unchanged.

This experiment has not confirmed that XHTML extensions caused the problem. The available evidence establishes successful live retrieval, but does not establish successful sitemap ingestion. A queue or reporting delay at Google is a possibility, not a confirmed cause. Do not mark this issue resolved until the Sitemaps report shows `Success` and the discovered-page count is 18.

## Changes and checks

- Added `dist/sitemap-pages.xml` and its deterministic generation in `scripts/localize.py`.
- Extended the existing site audit to require exact canonical URL coverage and no duplicate entries in the fallback map.
- Build, 18-page metadata/link audit, JavaScript syntax checks and GitHub Pages deployment passed.
- The previous ChatGPT Site was not changed. The existing domain-root homepage repository was not changed.

## References

- [Google: Sitemaps report, fetch diagnostics and status definitions](https://support.google.com/webmasters/answer/7451001)
- [Google: language alternates in XML sitemaps](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Sitemap Protocol schema](https://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd)

## Follow-up at 18:27 Asia/Nicosia

The GitHub repository was created on 27 November 2026 at 12:27 UTC (14:27 Cyprus time). The site is only about four hours old, not an established property with a confirmed search-traffic decline.

### Search visibility

- A Google search for the complete English homepage URL returned the EN, EL and RU homepages. The site is served in search, although it was absent from the first page for `cyprus schengen monitor`.
- English URL Inspection reported `Page is indexed`, last crawled by Googlebot smartphone at 15:01:46 Cyprus time, successful fetch, crawling/indexing allowed and the inspected English URL as Google's canonical. Discovery showed links from the RU/EL homepages and no referring sitemaps.
- Manual actions and Security issues both reported `No issues detected`. Temporary Removals had no requests in the last six months.
- Search Console Performance and Indexing overview reports were still processing initial data. No query-level ranking cause or traffic trend can be established from those reports yet.
- The exact queried brand was missing from the visible English name (`Cyprus Monitor`) and the homepage title. The visible English name and all three homepage titles now include `Cyprus Schengen Monitor`. This fixes an observed naming inconsistency; it is not evidence that it was the sole cause of ranking.
- Google displayed the domain-level site label `GitHub Pages documentation`. Google does not support distinct site names for a project subdirectory. Project-level WebSite markup cannot guarantee a separate site label. Changing the existing domain homepage or migrating to a custom domain is outside this change.

### Sitemap experiments and discovery

- Fresh HTTPS retrieval of the primary XML map returned 200, `application/xml`, no redirect or indexing restriction. The minimal XML map validates against the official Sitemap Protocol XSD (`xmllint`).
- Resubmitting the original XML map was accepted, but the report remained `Unknown`, `Couldn't fetch`, zero discovered URLs. The details page offered no specific HTTP/DNS/parser failure.
- Added Google's supported text sitemap at `sitemap.txt`, containing the exact same 18 canonical URLs, one per line. Build/audit and deployment passed; public HTTPS retrieval returned 200, `text/plain; charset=utf-8`, with bytes matching the build. Search Console accepted its submission but initially displayed the same `Unknown` / `Couldn't fetch` / zero state. The symptom therefore also occurs without any XML namespace or extension.
- Google's live inspection of `sitemap.txt` at 18:27:09 Cyprus time reported `Crawl allowed: Yes`, `Page fetch: Successful`, `Indexing allowed: Yes`.
- Added a non-blocking domain-root `robots.txt` in `chistopat/chistopat.github.io` advertising the primary XML and text maps. The root file now returns HTTP 200 and its deployment passed. The existing domain homepage was not changed. The previous root 404 was not itself a crawl block, but the project-directory robots file did not provide crawler discovery.

The remaining ingestion failure is **not resolved**. A transient Google ingestion/reporting issue or low crawl demand on a new property remains plausible; neither is confirmed. Do not claim a format fix or successful processing until the report shows `Success` and the map's 18 URLs. Availability in Google's live inspection and sitemap ingestion are distinct observations.

References: [Google URL Inspection caveats](https://support.google.com/webmasters/answer/9012289), [Sitemap fetch errors and low crawl demand](https://support.google.com/webmasters/answer/7451001), [supported text sitemap format](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap), [subdirectory site-name limitation](https://developers.google.com/search/docs/appearance/site-names).
