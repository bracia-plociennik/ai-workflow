To jest intake tematyczny do „FRONTEND SKILL”, nie formalny `phase-0-repo-intake PASS`. Obecny repo intake pozostaje zablokowany przez drift artefaktów workflow i istniejący dirty worktree.

# Request Batch Triage

| item | group | theme | risk | routing | target project/workspace | dependencies | owner decision | reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1. Co działa dobrze | frontend-skill-intake | wzorce do zachowania | low | same-project-task-group | repo/frontend, chat read-only | kod, historia, screenshoty | not-required | Ekstrakcja sprawdzonych wzorców bez zmian. |
| 2. Co jest słabe | frontend-skill-intake | findings i dług techniczny | low | same-project-task-group | repo/frontend, chat read-only | aktualny kod i historyczne fix-loopy | not-required | Audyt statyczny bez implementacji. |
| 3. Co odrzucono/usunięto | frontend-skill-intake | negatywne wzorce | low | same-project-task-group | repo/frontend, chat read-only | legacy memory i repo state | not-required | Ważne jest zapisanie również warunków, w których decyzja była lokalna, a nie uniwersalna. |
| 4. Braki 2026, skill i poprawki CHT | frontend-hardening | przyszły skill i produkt | medium | full-workflow-required | przyszły `FRONTEND SKILL` oraz CHT | recovery workflow, zaakceptowany projekt/spec | required before writes | KYC, auth, portfele i transakcje wymagają formalnego scope, failure-path QA i owner approval. |

Grouped requests:

- Punkty 1–3 oraz część „skillową” punktu 4 tworzą jeden read-only corpus wiedzy.
- Implementacja poprawek CHT jest osobnym, średniego ryzyka strumieniem.

Standalone requests:

- Przyszłe zmiany produktu powinny wejść jako formalny projekt `frontend-hardening` albo zaakceptowany change request do właściwego aktywnego projektu.

Blockers / owner decisions:

- Brak blokera dla niniejszego audytu.
- Formalne taski i writes blokuje obecny stan repo intake oraz decyzja `OD-REPO-RECOVERY-2026-07-20-001`.

Authority boundary:

- Ten triage nie przyznaje prawa do implementacji, tworzenia artefaktów, tasków, change requestów, commitów ani skillu.

# Task Idea Validation

Co zostaje:

- Charakterystyczna estetyka CHT, server-first rendering, adaptery danych, uczciwe source/provenance labels, selektywne użycie Radix i spójny Lucide.
- Rozdzielenie statusu dostawcy, własności portfela, on-chain KYC i statusu indeksowania.
- Feedback klienta jako centralny wymóg nowego skillu: projektować nie tylko success path, lecz cały system prowadzonego odzyskiwania procesu.

Co jest słabe / do poprawy lub usunięcia:

- W jednym backlogu nie należy mieszać stworzenia ogólnego skillu z wdrożeniem zmian w produkcie.
- Historyczne `PASS` nie może być traktowane jako dowód obecnego UI; wiele kontroli nie miało live-browser UX QA.
- „Radix został odrzucony” albo „Connect wallet został usunięty” byłyby błędnymi generalizacjami. To były lokalne decyzje dla konkretnych widoków.

Czego brakuje:

- Bieżącego browser/visual QA, E2E, accessibility automation, RUM Core Web Vitals i telemetryki błędów.
- Akceptowanego scope dla przyszłej implementacji oraz decyzji, czy recovery KYC ma być inline, w dialogu czy przez przejście z resumable intent.

Blokery / decyzje:

- Brak dla read-only intake.
- Przed implementacją potrzebne są workflow recovery i formalny spec.

Rekomendowany routing:

- Teraz: advisory frontend intake.
- Następnie: osobny skill-creation workflow.
- Poprawki produktu: pełny workflow z failure-path matrix, spec QA i phase-5 quality.

# Findings-first

Nie znalazłem P0. Najważniejsze problemy:

## P1 — brak wspólnego guided recovery

W Buy Tokens blokada KYC kończy się tekstem błędu i `return false`. Nie ma CTA do KYC, osadzonego KYC, zachowania intencji zakupu ani automatycznego powrotu do przerwanego kroku. Widać to w [`ensureOnChainKycApproved`](/Users/jakubplociennik/ai-system/onlinen-workspace/clients/tokenuj/projects/cht/frontend/components/dashboard/buy-tokens/DashboardBuyTokensForm.client.tsx:2039).

Jednocześnie sam ekran KYC ma już dobry zalążek rozwiązania: jawny state machine, komunikaty, refresh, link do Settings i inline Sumsub w [`DashboardKycPanel`](/Users/jakubplociennik/ai-system/onlinen-workspace/clients/tokenuj/projects/cht/frontend/components/dashboard/kyc/DashboardKycPanel.client.tsx:143). Problemem nie jest więc brak KYC UI, tylko brak połączenia go z operacją, która została zablokowana.

Wymagany wzorzec:

```text
Operacja
→ blokada z rozpoznanym kodem
→ wyjaśnienie co się stało
→ właściwa akcja naprawcza
→ zachowanie danych/intencji
→ rewalidacja
→ powrót do przerwanego kroku
```

## P1 — frontend finansowy bez pełnej siatki testów

Frontend ma 10 testów helperów `.test.mjs`, ale nie ma `test` scriptu, testów komponentowych, E2E, screenshot regression ani automatycznego a11y. Typecheck/lint/build nie dowodzą działania KYC, wallet popupów, błędnych sieci, odrzuconych podpisów, timeoutów, powrotów z Transak ani focus management.

Dla takiego UI standardem powinny być Playwright journeys z `@axe-core/playwright`, failure injection i visual snapshots. Playwright oficjalnie wspiera zarówno [accessibility testing](https://playwright.dev/docs/accessibility-testing), jak i [visual comparisons](https://playwright.dev/docs/test-snapshots).

## P2 — niepełna dostępność interakcji

- Custom language i currency listbox używają ról ARIA, ale nie implementują kompletnego sterowania strzałkami, aktywnego elementu i roving focus. Lepiej zastosować Radix Select lub natywny `<select>`.
- Brak skip linku.
- `DashboardState` zawsze ma `role="status"`, również dla błędów.
- Link renderowany przez wspólny `Button` dostaje tylko `aria-disabled`, ale nadal może być fokusowalny i aktywny: [`Button.tsx`](/Users/jakubplociennik/ai-system/onlinen-workspace/clients/tokenuj/projects/cht/frontend/components/ui/Button/Button.tsx:121).
- Dialog potwierdzenia zakupu używa `modal={false}` w [`DashboardBuyTokensForm`](/Users/jakubplociennik/ai-system/onlinen-workspace/clients/tokenuj/projects/cht/frontend/components/dashboard/buy-tokens/DashboardBuyTokensForm.client.tsx:1628). Dla finansowego potwierdzenia wymaga to ponownego uzasadnienia i browser a11y QA.
- Loading gate dashboardu to pusty `div`, a przy nieautoryzacyjnym błędzie bez lokalnej sesji stan wraca do `checking`, więc może zostać pusty bez końca: [`DashboardShellClient`](/Users/jakubplociennik/ai-system/onlinen-workspace/clients/tokenuj/projects/cht/frontend/components/dashboard/shell/DashboardShellClient.tsx:207).

Skill powinien bazować co najmniej na WCAG 2.2, w tym focus not obscured, target size, consistent help i accessible authentication. [W3C opisuje nowe kryteria WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/).

## P2 — kosztowne assety i brak performance budget

- `frontend/public` ma około 33 MB.
- `bg-shape-build-trust.svg` ma 13,54 MB i zawiera 26 osadzonych obrazów PNG base64. To jest raster opakowany w SVG, a nie lekki wektor.
- Dwa Inter variable fonts mają łącznie około 1,78 MB.
- Istniejący `.next` ma 2,9 GB, ale jest wygenerowany i nie odpowiada aktualnemu HEAD, więc nie jest dowodem obecnego bundle size.
- Providerzy Web3Auth i WalletConnect są dynamicznie importowani — to akurat dobra decyzja.

Należy wprowadzić budżety i RUM. Zalecane granice p75 to LCP ≤ 2,5 s, INP ≤ 200 ms i CLS ≤ 0,1, osobno mobile/desktop. [web.dev definiuje te progi](https://web.dev/articles/vitals).

## P2 — tłumaczenie nie jest prawdziwą lokalizacją

Google Translate jest ładowany globalnie po stronie klienta, dla każdej trasy, przez [`GoogleTranslateProvider`](/Users/jakubplociennik/ai-system/onlinen-workspace/clients/tokenuj/projects/cht/frontend/components/providers/GoogleTranslateProvider.tsx:12). Tymczasem:

- HTML zawsze pozostaje `lang="en"`;
- nie ma osobnych URL-i, canonicali ani `hreflang`;
- treść tłumaczona przez DOM mutation nie jest stabilnym, indeksowalnym wariantem;
- zewnętrzny skrypt może wpływać na prywatność, niezawodność i CWV.

Dla publicznego marketingu należy wdrożyć server-rendered locale routes. `next-intl` obsługuje App Router, Server Components i lokalizowane ścieżki, więc jest rozsądnym kandydatem. [Dokumentacja next-intl](https://next-intl.dev/).

## P2 — za duże odpowiedzialności komponentów

Największe pliki:

- admin dashboard: 2631 linii;
- Buy Tokens: 2243;
- landing mapper: 2089;
- Settings: 1701;
- Dashboard Shell: 1383;
- Rewards actions: 784;
- KYC panel: 544.

To nie jest wyłącznie problem długości. Buy Tokens miesza walidację formularza, KYC, Transak, przygotowanie transakcji, wallet provider, gas top-up, indexing, retry, dialog i copy. Trudno zapewnić kompletność negatywnych ścieżek, gdy każdy flow ma własne lokalne stringi i stany.

## P2 — brak runtime resilience i observability

Nie znaleziono:

- `error.tsx`, `global-error.tsx`, `loading.tsx`, `not-found.tsx`;
- Web Vitals RUM;
- instrumentacji błędów;
- frontendowego correlation ID surface;
- retry/offline UX;
- CSP i nagłówków bezpieczeństwa w `next.config.ts`.

Nagłówki mogą być dodawane przez reverse proxy, więc jest to „brak dowodu w frontendzie”, nie dowód braku na deploymencie. Dla providerów portfelowych CSP powinno najpierw wejść jako `Report-Only`, z inwentaryzacją wymaganych originów.

## P3 — pozostałości mocków i legacy

- Formularz nadal ma `aria-label="Mock buy tokens form"` i komunikat `Confirm the mock agreement`.
- Nadal istnieją typy i pola z `Mock`/`mockAmount`, choć przepływy są częściowo realne.
- `frontend/components/sections` zawiera 24 nieużywane pliki z GFIX, Picsum i mock content. Canonical landing ich nie importuje.
- Dwa śledzone, wygenerowane i nieużywane pliki `.module.css` duplikują SCSS.
- `next.config.ts` nadal pozwala na `fastly.picsum.photos`, prawdopodobnie wyłącznie przez legacy.
- [`llms.txt`](/Users/jakubplociennik/ai-system/onlinen-workspace/clients/tokenuj/projects/cht/frontend/public/llms.txt:43) był ostatnio przeglądany 2026-05-07.

# 1. Co wyszło dobrze i powinno wejść do FRONTEND SKILL

## Architektura

- Next.js App Router, React 19 i strict TypeScript.
- Server Components jako default, thin route orchestration i małe client islands. Takie podejście jest zgodne z aktualnym [modelem Server/Client Components Next.js](https://nextjs.org/docs/app/getting-started/server-and-client-components).
- Public landing pobiera content i presale równolegle na serwerze: [`page.tsx`](/Users/jakubplociennik/ai-system/onlinen-workspace/clients/tokenuj/projects/cht/frontend/app/(public)/page.tsx:12).
- Dashboard weryfikuje cookie na serwerze i równolegle pobiera content/runtime: [`dashboard/layout.tsx`](/Users/jakubplociennik/ai-system/onlinen-workspace/clients/tokenuj/projects/cht/frontend/app/(app)/dashboard/layout.tsx:9).
- Warstwa adapterów normalizuje DTO, stare nazwy brandu, nullable content i API drift. Komponenty nie konsumują surowego backendu.
- Backend/on-chain pozostaje authority; UI zachowuje source/provenance zamiast spłaszczać każdy zielony status do „ready”.
- Provider KYC, wallet provider, ownership proof i on-chain eligibility są rozdzielone.
- Purchase lifecycle rozróżnia `Submitted`, `Confirming` i `Indexed`, zamiast udawać natychmiastową finalność.
- Nie wprowadzano fake price, fake tokenomics, fake reviews ani fałszywych claims, gdy dane były niedostępne.

## UI i „non-AI look”

Historyczne screenshoty nie są dowodem obecnego renderingu, ale pokazują kierunek, który warto zachować:

- charakterystyczny kontrast czerni, jasnego płótna i złota;
- asymetryczne kompozycje zamiast powtarzalnego „gradient bento SaaS”;
- realna grafika tokena i domain-specific diagrams;
- wyraźne rozdzielenie marketingu od operacyjnego dashboardu;
- dashboard ma spokojniejszą, finansową hierarchię, modularne karty i oszczędne akcenty;
- landing prowadzi przez narrację: obietnica → utility → wiarygodność → sposób działania → FAQ → CTA.

Skill powinien zawierać „AI-look lint”:

- usuń generyczne hasła bez dowodu;
- nie buduj wszystkiego z identycznych kart i pills;
- nie używaj gradientów, glow i glassmorphism bez znaczenia;
- nie generuj fake metrics, testimonials ani abstrakcyjnych ikon;
- stosuj nierówny rytm editorial, realny content i specyficzne stany domenowe;
- zachowuj jeden charakterystyczny motyw marki, nie dziesięć efektów.

## UI primitives, Radix, shadcn i ikony

Obecny wybór jest rozsądny:

- Radix dla dialogów, selectów i accordionów;
- Lucide jako główny system ikon kontrolnych;
- lokalne SVG dla brandu i payment/provider assets;
- CVA, `clsx` i `tailwind-merge` do wariantów;
- DOMPurify do CMS rich text;
- native CSS/SVG lub Recharts tam, gdzie wykres przekazuje realne dane.

[`components.json`](/Users/jakubplociennik/ai-system/onlinen-workspace/clients/tokenuj/projects/cht/frontend/components.json:1) oznacza konfigurację shadcn, ale shadcn nie jest typową biblioteką runtime — daje kod komponentów do posiadania i modyfikacji. Tak też opisuje go [oficjalna dokumentacja shadcn](https://ui.shadcn.com/docs).

Ważna aktualizacja na lipiec 2026: domyślną bazą nowych projektów shadcn stało się Base UI, podczas gdy CHT jest oparte o Radix. [Changelog shadcn](https://ui.shadcn.com/docs/changelog/2026-07-base-ui-default). Skill powinien więc mówić:

- wybierz jedną headless foundation na projekt;
- nie mieszaj Radix i Base UI przypadkowo;
- w istniejącym CHT pozostaw Radix, dopóki migracja nie ma konkretnego zysku;
- nie wykonuj hurtowego „shadcn makeover”.

## Motion i media

Dobre rozwiązania:

- respektowanie `prefers-reduced-motion`;
- `saveData` i opóźnione uruchamianie hero video;
- lazy loading mediów poza hero;
- native scroll-snap dla roadmap/team zamiast kolejnej biblioteki carousel;
- pełny SSR tekstu, a dopiero po hydration możliwość zwinięcia;
- lokalne fonty i kontrolowane fallbacki.

## SEO, LLM i GEO

Aktualny fundament:

- centralne metadata;
- canonical, Open Graph i Twitter;
- `robots.ts`, `sitemap.ts`;
- prywatny dashboard `noindex,nofollow,nocache`;
- Organization, WebSite, FAQPage i Review JSON-LD;
- bez Product/Offer/FinancialProduct/AggregateRating, gdy brak podstaw;
- bezpieczny JSON-LD serializer;
- statyczny `llms.txt` z wyraźnym zakazem publikowania KYC, wallet i prywatnych runtime facts.

[`metadata.ts`](/Users/jakubplociennik/ai-system/onlinen-workspace/clients/tokenuj/projects/cht/frontend/lib/seo/metadata.ts:28) jest dobrą bazą.

Dla skillu ważne: Google w aktualnym przewodniku mówi, że widoczność w AI search nadal bazuje na podstawowych praktykach SEO i nie wymaga specjalnego schema ani osobnego „AI markup”. [Google AI optimization guide](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).

`llms.txt` można utrzymywać, ale trzeba nazywać go eksperymentalną propozycją, nie standardem gwarantującym widoczność. [Specyfikacja llms.txt sama określa się jako proposal](https://llmstxt.org/).

# 2. Co wymagało i nadal wymaga poprawek

Historyczne fix-loopy pokazały wartościowe lekcje:

- Sidebar: clipping i collapse nie wystarczyły; potrzebne były hover/focus expansion, usunięcie zbędnych CTA i poprawa dostępnej nazwy dialogu.
- Buy Tokens: nieograniczony fetch potrafił zawieszać build/prerender; każde zewnętrzne źródło musi mieć timeout i jawny unavailable state.
- KYC: konieczne były kontrast statusu, CTA i ponowne użycie FAQ.
- Referral: copy action wymaga rozdzielenia `COPY CODE` od `COPY LINK`; redundantne visible success notification usunięto.
- Settings: usunięto duplikat akcji i fake static password strength.
- Staking: konieczne były kontrast, typography, hover i reduced motion.
- Mobile menu: test musiał czekać na kolejny render tick po kliknięciu.
- Anchor aliases z backendu wymagały normalizacji do aktualnych ID.
- SVG `<title>` w tokenomics powodował hydration mismatch.

Najważniejsza zasada skillu: każda wizualna implementacja przechodzi osobny fix-loop desktop/mobile oraz pełne sprawdzenie po poprawce, nie tylko kontrolę zmienionej linii.

# 3. Co odrzucono, usunięto lub należy usunąć

## Słusznie odrzucone i nieprzywracać

- Nieistniejące endpointy `/api/public/landing` i `/api/presale/info`.
- Hardcoded production sales/presale/tokenomics values.
- Legacy GFIX/GFI copy.
- Fake reviews, testimonials i Picsum assets.
- Unsupported Product, Offer, FinancialProduct i AggregateRating schema.
- Surowe `dangerouslySetInnerHTML` poza wspólnym sanitizerem.
- Custom KYC upload/formularz przechowujący PII po stronie CHT; Sumsub inline jest lepszą granicą.
- Fake success, fake wallet verification i utożsamienie provider login z ownership proof.
- Duplikaty widocznych notification po copy.
- Static password strength.
- Niepotrzebne biblioteki carousel i animation, gdy CSS/native browser wystarczają.

## Usunąć po formalnej weryfikacji importów

- `frontend/components/sections/**`;
- dwa wygenerowane `.module.css`;
- legacy mock nazwy w realnym Buy Tokens;
- `fastly.picsum.photos` po usunięciu legacy;
- nadmiar nieużywanych fontów;
- 13,54 MB pseudo-SVG z embedded PNG;
- martwe runtime mock types i pola;
- nieużywany `runtime` prop KYC.

## Nie generalizować jako „odrzucone”

- Radix Dialog miał konkretny problem w landing mobile drawer; Radix nadal jest używany poprawnie w dashboardzie.
- Desktop Connect CTA było kiedyś usunięte dla mockowego scope, ale realny wallet flow uzasadnił jego powrót.
- Token Sale Price Schedule pominięto, bo nie było odpowiadającego projektu i źródła danych — nie dlatego, że taka sekcja jest zawsze zła.

# 4. Czego brakuje w FRONTEND SKILL i obecnym CHT

## Obowiązkowy model stanów

Każda operacja powinna projektować:

```text
idle
validation
blocked
awaiting-user
awaiting-wallet
submitted
confirming
indexed
complete
recoverable-error
terminal-error
```

Dla każdego stanu skill ma wymagać:

- co się stało;
- z jakiego źródła pochodzi status;
- czy użytkownik, wallet, provider, backend czy chain musi coś zrobić;
- primary CTA;
- secondary CTA;
- retry/resume policy;
- czy zachowujemy wpisane dane;
- bezpieczne diagnostic details;
- zasady live region i focus management.

## Centralny kontrakt problemu

Proponowany model:

```ts
type GuidedProblem = {
  code: string;
  title: string;
  explanation: string;
  authority: "frontend" | "backend" | "provider" | "wallet" | "chain";
  recovery: {
    primaryAction: Action;
    secondaryAction?: Action;
    resumeIntent?: ResumeIntent;
  };
  retryable: boolean;
  correlationId?: string;
};
```

KYC purchase blocker powinien otworzyć `GuidedRecoveryPanel`:

- „Zakup został zatrzymany, ponieważ on-chain KYC nie jest jeszcze zatwierdzone.”
- CTA: `Dokończ KYC tutaj`.
- Alternatywa: `Przejdź do KYC`.
- Zachowane: kwota, waluta, metoda płatności, referral.
- Po zmianie statusu: rewalidacja.
- Powrót: do purchase summary, ale bez automatycznego podpisania transakcji.

## Failure-path catalogue

FRONTEND SKILL musi wymagać testowania co najmniej:

- brak sesji i wygaśnięta sesja;
- brak walleta;
- wallet nieudowodniony;
- zła sieć;
- KYC wymagane, review pending, provider approved/on-chain pending, odrzucone;
- niewystarczający gas;
- niewystarczające środki;
- user rejected signature;
- wallet popup zamknięty lub zablokowany;
- timeout/RPC unavailable;
- backend 401/403/409/422/429/500;
- transaction submitted, ale indexer opóźniony;
- transaction reverted;
- Transak return, cancel, pending i provider unavailable;
- offline/reconnect;
- duplicate action/idempotency conflict.

Toast nie powinien być jedynym miejscem dla błędu finansowego. Potrzebny jest status przy operacji, a toast może być tylko podsumowaniem.

## Zalecany zestaw bibliotek

| Obszar | Decyzja |
| --- | --- |
| Next/React/TypeScript | Zachować. |
| Radix | Zachować jako foundation CHT. |
| shadcn | Używać selektywnie jako źródła posiadanego kodu; nie migrować hurtowo. |
| Lucide | Zachować jako jeden system control icons. |
| Playwright + axe | Dodać jako główny E2E/a11y stack. |
| Vitest Browser Mode | Rozważyć dla primitives i komponentów w realnej przeglądarce. |
| Zod | Dodać tam, gdzie runtime API/CMS payload wymaga walidacji poza TypeScript. |
| next-intl | Dodać przy przejściu na prawdziwe locale routes. |
| TanStack Query | Tylko jeśli centralizujemy client-side server state, retry, dedup i invalidation. Domyślne retry trzeba dostosować do finansowych operacji; [TanStack Query domyślnie ponawia błędne query trzy razy](https://tanstack.com/query/latest/docs/framework/react/guides/important-defaults). |
| React Hook Form | Tylko dla złożonych formularzy, gdy obecny ręczny state rzeczywiście przeszkadza. |
| Storybook | Opcjonalnie dla design-system matrix; nie zastępuje E2E. |
| Redux/Zustand | Nie dodawać bez konkretnego problemu wspólnego client state. |
| Kolejne icon/carousel/animation packs | Nie dodawać bez uzasadnienia bundle i UX. |

## Landing, subpages i dashboard flow

Landing:

```text
Problem / obietnica
→ czym jest CHT
→ utility i evidence
→ compliance/trust
→ jak zacząć
→ ryzyka i FAQ
→ jedno główne CTA
```

Subpages powinny powstawać tylko dla osobnego search/user intent:

- how to buy / onboarding;
- KYC i eligibility;
- legal/documents;
- utility;
- company/team;
- support/FAQ.

Nie tworzyć cienkich SEO pages, które powtarzają landing.

Dashboard:

```text
Readiness checklist
wallet → ownership → KYC → gas/funds
→ główna akcja
→ wallet/provider interaction
→ submitted
→ confirming
→ indexed
→ recovery lub następna akcja
```

Overview powinien mówić użytkownikowi nie tylko „co ma”, lecz także „co powinien teraz zrobić” i dlaczego dana akcja jest niedostępna.

## SEO/GEO 2026

Dodać do skillu:

- SSR-first public content;
- real locale URLs, canonical i hreflang;
- author/source/date/freshness dla treści wysokiego zaufania;
- źródła i metodologia claims;
- JSON-LD wyłącznie zgodny z widoczną treścią;
- spójna aktualizacja route registry, sitemap, metadata i `llms.txt`;
- żadnego private/dashboard content w LLM surface;
- żadnego specjalnego „AI schema” bez standardu;
- publiczne dokumenty w parsowalnym HTML, nie wyłącznie w PDF;
- treści odpowiedzialne, konkretne i cytowalne zamiast keyword stuffing.

# Adaptive Data / Integration Matrix

| Source Shape | Expected Canonical State | Expected Derived Output | Forbidden States/Rows | Failure Behavior | Automated Check | Manual Trace |
| --- | --- | --- | --- | --- | --- | --- |
| Sumsub/provider + backend KYC + chain readback | osobne statusy i authority | eligibility + guided next action | provider approved = purchase eligible | inline KYC lub prowadzone przejście, resume | brak pełnego E2E | wymagany |
| Wallet provider + backend ownership proof | connected ≠ proven | jasny readiness state | provider success = ownership verified | challenge/sign/retry/settings CTA | helper tests częściowe | wymagany |
| Prepared package + tx receipt + indexer | prepared → submitted → confirming → indexed | timeline i dashboard refresh | sam tx hash jako wystarczający dowód | retry, manual refresh, support details | backend/history evidence | wymagany live/local E2E |
| Transak session/status | provenance only | pending/return/cancel status | provider status = settlement | resume purchase po środkach | brak provider E2E | owner sandbox |
| CMS content | canonical adapter | SSR UI + metadata/schema | fake sales, legacy brand, unsupported schema | unavailable zamiast invent data | historyczne scans | bieżący visual QA brak |

