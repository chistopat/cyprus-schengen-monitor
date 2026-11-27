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
