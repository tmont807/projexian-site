# Security

To report a security issue with projexian.com, email tyler@projexian.com. Please do not open a public issue.

How the site is protected:
- Static site: no server code, no database, no logins.
- Served only over HTTPS by GitHub Pages.
- Strict Content Security Policy: scripts, fonts and data load only from the site itself; forms post only to FormSubmit.
- No cookies, analytics, ad trackers or third-party scripts.
- Forms: spam honeypot plus FormSubmit verification, input length limits, consent checkbox, and a notice not to submit sensitive data.
- Daily rebuild from public SAM.gov and USAspending.gov data; if a data pull fails, the previous data is kept.
- GitHub Actions versions are kept current by Dependabot.
