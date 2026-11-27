# SEO audit — 27 November 2026

## Scope and evidence

The audit covers six pages in Russian, English and Greek for Cyprus: 18 HTML documents. Production is `https://chistopat.github.io/cyprus-schengen-monitor/`. The ChatGPT Site is the previous host, not the production canonical.

Keyword research is **provisional**. Searches in RU, EN and EL showed recurring coverage of current membership, the accession date, the 2027 target, procedural news and border arrangements. These observations identify topics; they do not measure demand. Google Keyword Planner access was attempted. The user then cancelled Google Ads setup because they do not want payment information linked. No advertising campaign was launched and no payment details were entered. No search volumes, keyword difficulty scores or traffic forecasts have been invented. The following is a candidate topic map, not a volume-validated semantic core.

## Candidate topics by page

| Page | Russian query candidates | English query candidates | Greek query candidates | Intent |
| --- | --- | --- | --- | --- |
| Overview | Кипр Шенген; входит ли Кипр в Шенген | Cyprus Schengen; is Cyprus in Schengen | Κύπρος Σένγκεν; είναι η Κύπρος στη Σένγκεν | Current status and a direct answer |
| Forecast | когда Кипр войдет в Шенген; Кипр Шенген 2027 | when will Cyprus join Schengen; Cyprus Schengen 2027 | πότε θα ενταχθεί η Κύπρος στη Σένγκεν; Κύπρος Σένγκεν 2027 | Timing, conditions and uncertainty |
| Timeline | Кипр Шенген новости; вступление Кипра в Шенген | Cyprus Schengen news; Cyprus Schengen accession timeline | Κύπρος Σένγκεν νέα; χρονολόγιο ένταξης Κύπρου | Recent developments with dated evidence |
| Participants | вступление Кипра в Шенген Совет ЕС; Греция Кипр Шенген | Cyprus Schengen EU Council; Greece Cyprus Schengen | Κύπρος Σένγκεν Συμβούλιο ΕΕ; Ελλάδα Κύπρος Σένγκεν | Decision makers and political positions |
| Sources | Кипр Шенген официальные документы | Cyprus Schengen official documents | Κύπρος Σένγκεν επίσημα έγγραφα | Primary documents and evidence quality |
| Privacy | Brand + конфиденциальность | Brand + privacy / analytics | Brand + απόρρητο | Visitor information, not an acquisition page |

The broad visa/application cluster is excluded: the site does not provide a visa application service. Search volume, if obtained later, must not be added across close variants as if each represented a distinct audience. Planner advertising competition is not organic SEO difficulty. Any later export must record country, language, Google-only vs partner network, date range and whether the values are exact estimates or ranges. Search Console will provide observed queries after the site receives impressions, not a pre-launch demand estimate.

Observed result examples, checked on the audit date: [RU coverage](https://gk-lawfirm.com/ru/blog/cyprus-schengen-zone/), [EN coverage](https://gk-lawfirm.com/publications/cyprus-schengen-zone/), [EL coverage](https://www.alphanews.live/politics/pote-anamenei-i-kyvernisi-tin-pliri-entaxi-tis-kyprou-stin-sengken/). These are evidence of competing coverage, not sources for estimated keyword volumes or copied content.

## Implemented changes

- Unique titles and descriptions for every page and language; no `meta keywords` tag.
- Separate crawlable language URLs. Russian remains at the root, English at `/en/`, Greek at `/el/` with `lang="el-CY"`.
- Self-canonical URLs per language. A translated page is not canonicalised to Russian. Reciprocal RU/EN/el-CY alternates and an English `x-default` appear in HTML and sitemap.
- A language switch preserves the current page. No IP- or browser-language redirects are used.
- Translated navigation, full timeline entries, source labels, search/filter controls, consent and privacy text. English and Greek maps have translated embedded labels.
- Localised Open Graph and Twitter metadata, image alt text, image format and verified 1400×800 dimensions.
- Accurate `WebPage`, `WebSite` and `BreadcrumbList` JSON-LD. No invented organisation, author, review, rating or official affiliation. The snapshot date is retained rather than refreshed automatically on every build.
- Visible direct answers to membership/timing questions, links to official evidence and internal links to the forecast and timeline.
- The footer discloses that this is not a media outlet, that content was collected and prepared by AI, and that the authors disclaim responsibility for accuracy and consequences of use. Political targets remain separate from adopted legal dates.
- Static HTML supplies the content without JavaScript. JavaScript adds timeline search/filtering, fragment opening and consent-based analytics.
- One sitemap contains all 18 canonical URLs and language relationships. All page, asset and fragment links are checked during deployment.
- Search Console verification metadata is configurable and present. Search Console ownership was verified using the HTML tag. The sitemap was submitted, and Google accepted a priority indexing request for the Russian homepage. Indexing itself is pending.

## Validation

Run `python build.py` followed by `python scripts/audit_site.py`. The generated `metadata-audit.json` contains the complete page-level title, description, canonical and language inventory, including character counts. Checks cover missing/duplicate metadata, exactly one H1, duplicate IDs, translation leftovers (excluding native language labels), reciprocal alternates, JSON-LD, social tags, local targets and fragments, and sitemap coverage.

Title and description lengths are editorial checks, not fixed Google limits. Search results may rewrite titles and snippets. This audit does not promise rankings, snippets, rich results or indexing. A volume-validated semantic core remains out of scope after cancellation of Ads setup.

## Hosting and migration limits

GitHub project Pages is served below `/cyprus-schengen-monitor/`. A `robots.txt` there is informational: crawlers look for `https://chistopat.github.io/robots.txt`. The existing user homepage repository is not changed by this migration. Direct submission of the full sitemap URL in Search Console handles discovery without changing another site's robots file. Root-level crawl restrictions must still be checked after deployment.

The previous ChatGPT Site is unchanged at the user’s explicit request. No redirects or canonical changes were published there. The GitHub site uses self-canonical URLs.

## Source and guidance references

- [Current Cyprus status — European Commission](https://home-affairs.ec.europa.eu/policies/schengen/schengen-area_en)
- [Localised versions and hreflang — Google Search Central](https://developers.google.com/search/docs/specialty/international/localized-versions)
- [Titles — Google Search Central](https://developers.google.com/search/docs/appearance/title-link)
- [Supported metadata — Google Search Central](https://developers.google.com/search/docs/crawling-indexing/special-tags)
- [Sitemap construction and submission — Google Search Central](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap)
- [robots.txt — Google Search Central](https://developers.google.com/search/docs/crawling-indexing/robots/intro)
- [Keyword Planner requirements — Google Ads Help](https://support.google.com/google-ads/answer/7337243)
- [Official Google Analytics MCP](https://github.com/googleanalytics/google-analytics-mcp)

An existing source-data error was also corrected in all languages: the RIK interview of 10 October names Deputy Minister Nicolas Ioannides, not Makis Ioannides. [RIK interview](https://news.rik.cy/article/2026/10/10/plere-entaxe-tes-kupriakes-demokratias-ston-khoro-sengken-entos-tou-2027-anamenei-e-kubernese/).

## Integration verification

GA4 account discovery and a realtime report succeeded through the official MCP for property `566046374` (`Cyprus Schengen Monitor`). The report contained `page_view`, `timeline_filter` and engagement events. This establishes that the connection can read received measurements; these counts are not a traffic baseline. The browser check confirmed zero external Google tag scripts before consent and one after acceptance.

OAuth uses only `analytics.readonly`, with credentials stored outside Git and mode 0600. The personal OAuth application remains in Testing with one test user. Google expires Testing refresh tokens after seven days; this connection will need re-authorisation. [Google OAuth token-expiration rules](https://developers.google.com/identity/protocols/oauth2).

Search Console accepted the sitemap submission and a priority indexing request for the Russian homepage. On the initial sitemap fetch, Search Console reported `Couldn't fetch`, although independent HTTPS requests returned HTTP 200 and valid XML. It was submitted once more after the successful live-page check. Sitemap processing and actual indexing remain external pending steps, not verified completion.

The link to the original ChatGPT monitoring Page was removed from the public site at the user's request. The old ChatGPT Site itself is unchanged.
