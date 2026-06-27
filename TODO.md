# TODO

## ✅ i18n: fix hardcoded Chinese in PortfolioPage.tsx (~70 strings) — DONE

The manual entry forms (trade, cash, corporate action), CSV import section, and event history section in PortfolioPage.tsx have hardcoded Chinese strings. The rest of the page already uses `PORTFOLIO_TEXT[language]`. Need to add matching i18n keys and refactor.

## ✅ i18n: fix hardcoded Chinese in StockScreeningPage.tsx (~100 strings) — DONE

Virtually the entire StockScreeningPage (headings, labels, status text, table headers, alerts, tooltips, helper function return strings) is hardcoded Chinese with no i18n infrastructure. Needs full i18n keys added to `uiText.ts` and comprehensive refactoring. Also has hardcoded `zh-CN` date locale on lines 325 and 377.
