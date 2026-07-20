Poniżej jest blueprint reusable skillu, nie CHT-specific prompt. Wiedza z CHT została przekształcona w ogólne reguły: guided recovery, jawne authority states, brak fake data, kompletność failure paths i evidence-based QA.

# Task Idea Validation

Co zostaje:

- Zakres jest jasny: profesjonalne frontend engineering obejmujące UI, UX, accessibility, performance, SEO/GEO, biblioteki, flows i QA.
- Skill ma służyć zarówno do budowy, jak i audytu lub refaktoru.
- Najważniejszą zasadą pozostaje projektowanie success, blocked, pending, failure i recovery paths.

Co jest słabe / do usunięcia:

- Skill nie może wymuszać Radix, shadcn, Tailwind, TanStack Query ani konkretnego frameworka niezależnie od repo.
- Nie należy umieszczać w głównym `SKILL.md` szczegółów CHT, długich katalogów bibliotek ani historycznych fix-loopów.
- „Professional” i „non-AI look” muszą być rozstrzygane przez konkretne kryteria, nie subiektywne deklaracje.

Czego brakuje:

- Przy późniejszym tworzeniu plików trzeba wybrać lokalizację skillu.
- Forward-testing i walidacja będą osobnym krokiem po utworzeniu rzeczywistego skillu.

Blokery / decyzje:

- Brak dla blueprintu read-only.

Rekomendowany routing:

- Najpierw zaakceptować strukturę.
- Potem wygenerować pełny `SKILL.md` i references.
- Dopiero później utworzyć, zwalidować i forward-testować skill.

# Plan Quality Contract

- Plan classification: read-only
- DoD source: bieżące polecenie oraz frontend intake CHT.
- Testable DoD / acceptance conditions: zawiera strukturę skillu, decision trees, checklisty, failure matrix, output contract i Definition of Done.
- Artifact QA route: not-applicable
- Artifact QA trigger: brak artefaktu.
- Implementation Quality Closure route: not-applicable
- Required verification: logiczna kontrola kompletności blueprintu; rzeczywista walidacja dopiero po utworzeniu skillu.
- Quality-ready criteria: reguły są reusable, evidence-based, framework-aware i nie zawierają zależności od CHT.
- Owner opt-out: none
- Not-applicable reason: wynik istnieje wyłącznie w chacie.
- Blocking decision: none
- Next route: pełny read-only draft `SKILL.md`, a następnie owner-approved skill creation.

# Proponowana tożsamość skillu

Nazwa folderu:

```text
build-professional-frontends
```

Zakres:

- budowanie nowych frontendów;
- implementacja designu;
- audyt i code review;
- naprawa UI/UX;
- landing pages;
- dashboardy;
- onboarding, auth i formularze;
- transactional, financial i Web3 flows;
- accessibility;
- performance;
- SEO, GEO i i18n;
- dobór bibliotek;
- frontend QA i Definition of Done.

Skill nie powinien zastępować:

- repozytoryjnych `AGENTS.md`;
- design-to-code/Figma skillu;
- formalnego security review;
- product decisions;
- backendowej lub blockchainowej authority;
- framework-specific dokumentacji.

# Proponowana struktura

```text
build-professional-frontends/
├── SKILL.md
├── agents/
│   └── openai.yaml
└── references/
    ├── decision-trees.md
    ├── ui-ux-quality.md
    ├── interaction-and-recovery.md
    ├── accessibility.md
    ├── performance.md
    ├── seo-geo-i18n.md
    ├── library-selection.md
    ├── transactional-flows.md
    └── qa-definition-of-done.md
```

Rekomendacja dla v1:

- Bez `assets/`.
- Bez skryptów.
- Dodać skrypty dopiero, gdy 2–3 realne użycia pokażą powtarzalne, deterministyczne kontrole.
- Nie tworzyć README, changelogu ani quick reference.

Potencjalne skrypty dla v2:

```text
scripts/frontend-intake.mjs
scripts/check-public-assets.mjs
scripts/check-route-contracts.mjs
```

Miałyby wykonywać wyłącznie statyczne, read-only sprawdzenia, takie jak:

- duże assety;
- brak error/loading boundaries;
- test scripts;
- metadata i route coverage;
- mock/placeholder residue;
- niespójne icon libraries;
- surowe `dangerouslySetInnerHTML`;
- brakujące accessibility primitives.

# Frontmatter `SKILL.md`

```yaml
---
name: build-professional-frontends
description: Design, implement, review, and harden professional production frontends across landing pages, dashboards, onboarding, forms, authentication, transactional, financial, and Web3 flows. Use when Codex must make frontend UI/UX decisions, choose component libraries, map happy, blocked, pending, failure, and recovery paths, improve accessibility, responsive behavior, performance, SEO/GEO, internationalization, visual quality, or verify frontend Definition of Done.
---
```

Opis celowo zawiera wszystkie triggery. Sekcja „When to use” w body nie jest potrzebna, bo body ładuje się dopiero po aktywacji skillu.

# Blueprint `SKILL.md`

Poniższy outline powinien pozostać poniżej 500 linii.

```markdown
# Build Professional Frontends

## Objective

Build or review production frontends that are:

- understandable without instruction;
- visually deliberate and domain-specific;
- honest about data and authority;
- usable across happy, blocked, pending, failure, and recovery paths;
- accessible by keyboard and assistive technology;
- responsive and performant;
- indexable where public and private where required;
- verifiable through current evidence.

Obey repository instructions, accepted design, product constraints, risk policy,
and source-of-truth boundaries before applying this skill.

## Operating Rules

1. Inspect repository guidance, framework, design system, routes, tests, data
   sources, integrations, and existing conventions before proposing changes.
2. Preserve established patterns that work unless evidence justifies replacing them.
3. Treat backend, provider, wallet, indexer, and chain states as separate authority
   sources. Never turn partial evidence into success.
4. Design the complete state space before implementing the visual success path.
5. Preserve user input and intent across recoverable failures.
6. Never introduce production fake data, fake metrics, fake reviews, fake status,
   or unsupported claims.
7. Use semantic native HTML first, an established accessible primitive second,
   and custom interaction logic only with a verified reason.
8. Keep Server Components or server rendering as the default when the framework
   supports them. Add client boundaries only for real interaction or browser APIs.
9. Prefer one headless component foundation and one control-icon family.
10. Treat automated checks as supporting evidence, not proof of visual or
    interaction quality.
11. Report skipped browser, accessibility, performance, provider, and visual
    checks explicitly.
12. Do not claim PASS outside an applicable formal quality gate.

## Classify The Task

Classify the request as one or more:

- frontend intake or audit;
- new page or component;
- visual implementation;
- user-flow implementation;
- bug or regression fix;
- accessibility hardening;
- performance hardening;
- SEO/GEO/i18n work;
- design-system work;
- transactional or high-trust flow.

Use `references/decision-trees.md` to select the execution path.

## Discover Current Truth

Inspect:

- closest repository instructions;
- package manifests and framework configuration;
- route tree and server/client boundaries;
- design tokens and shared primitives;
- component and icon foundations;
- API adapters and runtime validation;
- loading, empty, blocked, error, success, and recovery states;
- test, browser, accessibility, visual, and performance tooling;
- metadata, sitemap, robots, structured data, locales, and public/private routes;
- generated, legacy, mock, and unused code;
- current screenshots or a running application when visual judgment is required.

Distinguish:

- current repository fact;
- accepted design or product decision;
- historical context;
- inference;
- recommendation.

## Map User Journeys

For every affected journey, record:

- user goal;
- entry point;
- prerequisites;
- source of truth;
- primary path;
- blocked states;
- pending and asynchronous states;
- recoverable errors;
- terminal errors;
- primary and secondary recovery actions;
- state or input that must be retained;
- resume condition;
- completion evidence;
- next recommended action.

Read `references/interaction-and-recovery.md`.
For wallet, financial, provider, or high-trust flows also read
`references/transactional-flows.md`.

## Design The UI

Apply the UI and UX checklist from `references/ui-ux-quality.md`.

Preserve a deliberate visual identity:

- derive hierarchy from content and user intent;
- use tokens for typography, spacing, color, radius, elevation, and motion;
- vary composition when content requires it;
- avoid template-like repetition and decorative noise;
- use real domain content and states;
- make the primary action visually unambiguous;
- keep secondary actions subordinate but discoverable;
- make dense dashboards scannable rather than merely compact.

## Select Components And Libraries

Read `references/library-selection.md` before introducing a dependency.

Prefer:

1. existing project primitive;
2. semantic native element;
3. existing headless foundation;
4. small project-owned wrapper;
5. new dependency only when it removes material complexity or risk.

Do not introduce a second headless foundation, icon family, form system, state
library, chart library, or animation system without documenting the need,
bundle impact, maintenance cost, and migration boundary.

Treat shadcn as owned component source, not a universal runtime architecture.
Confirm whether the project uses Radix, Base UI, or another foundation before
adding generated components.

## Accessibility

Read `references/accessibility.md` for every user-visible build or review.

Require semantic structure, keyboard support, visible focus, correct accessible
names, appropriate live-region behavior, reduced-motion handling, sufficient
contrast, usable target sizes, zoom-safe layouts, and focus restoration.

Do not approximate complex ARIA widgets. Use native controls or verified
accessible primitives.

## Performance

Read `references/performance.md` for page, route, media, provider, or bundle work.

Set route-specific budgets before optimization. Measure current behavior before
claiming improvement. Track Core Web Vitals at p75 for mobile and desktop.

Load large wallet, provider, chart, editor, and video dependencies only where
required. Optimize media and fonts at source. Do not hide raster payloads in SVG.

## SEO, GEO And Internationalization

Read `references/seo-geo-i18n.md` for public routes.

Make public content server-readable, factual, source-backed, and consistent with
visible UI. Use canonical URLs, correct indexing policy, metadata, structured
data, language semantics, locale routing, and hreflang where applicable.

Treat GEO as an extension of good content architecture and SEO. Do not invent
special AI schema. Treat `llms.txt` as an optional experimental surface, never
as a substitute for indexable content.

Keep private, account, wallet, KYC, admin, and runtime state out of public
metadata, structured data, sitemaps, and LLM-facing files.

## Implement In Slices

Slice work by user-visible capability or recovery path, not arbitrary file count.

For every slice:

1. state the testable outcome;
2. identify server/client and data authority boundaries;
3. implement all applicable states;
4. add or update automated checks;
5. inspect the full changed path;
6. run browser and visual checks when UI changed;
7. re-review after every substantive fix.

Do not perform broad design-system migration inside an unrelated feature.

## Verify

Use `references/qa-definition-of-done.md`.

Verification must cover:

- intent and accepted design;
- happy path;
- blocked and failure paths;
- loading, empty, partial, stale, and retry states;
- keyboard and screen-reader semantics;
- responsive layouts;
- visual hierarchy;
- browser console and runtime errors;
- performance budgets;
- SEO/indexing behavior for public routes;
- privacy and authority boundaries;
- regression risk.

## Output Contract

For audits, report:

1. findings by severity;
2. what should remain;
3. what should be improved;
4. what should be removed or not reintroduced;
5. what is missing;
6. evidence reviewed;
7. skipped checks;
8. residual risk;
9. recommended next route.

For implementation, report:

1. outcome;
2. files or areas changed;
3. user journeys and states covered;
4. validation evidence;
5. skipped checks;
6. remaining findings and residual risk.

Never use empty claims such as “professional”, “accessible”, “optimized”,
“SEO-ready”, or “pixel-perfect” without evidence.
```

# `agents/openai.yaml`

```yaml
interface:
  display_name: "Professional Frontends"
  short_description: "Build and harden production-grade frontend UX"
  default_prompt: "Use $build-professional-frontends to audit this frontend and propose an evidence-backed implementation or hardening plan."

policy:
  allow_implicit_invocation: true
```

Bez ikon i `brand_color` w v1 — nie zostały dostarczone.

# Decision trees

## 1. Audit, fix czy budowa

```text
Czy użytkownik prosi o zmianę?
├─ Nie
│  └─ Wykonaj read-only intake/review
│     ├─ zbierz evidence
│     ├─ findings-first
│     └─ nie implementuj poprawek
└─ Tak
   ├─ Czy istnieje zaakceptowany design/spec?
   │  ├─ Tak → implementuj w jego granicach
   │  └─ Nie
   │     ├─ mała, odwracalna poprawka → zaproponuj minimalny zakres
   │     └─ flow/redesign/architektura → zatrzymaj się na planie lub decyzji
   └─ Po implementacji → pełne QA odpowiednie do ryzyka
```

## 2. Server czy Client Component

```text
Czy komponent wymaga:
state, event handlera, browser API, walleta, providera lub client hooka?
├─ Nie → renderuj po stronie serwera
└─ Tak
   ├─ Czy cała strona tego wymaga?
   │  ├─ Nie → wydziel najmniejszą client island
   │  └─ Tak → uzasadnij szeroką granicę klienta
   └─ Czy dane mogą być pobrane na serwerze i przekazane jako props?
      ├─ Tak → pobierz na serwerze
      └─ Nie → zaprojektuj cache, retry, stale i error states
```

## 3. Native, Radix, shadcn czy custom

```text
Czy projekt ma istniejący primitive?
├─ Tak → rozszerz go
└─ Nie
   ├─ Czy natywny element spełnia UX?
   │  ├─ Tak → użyj native
   │  └─ Nie
   │     ├─ Czy istnieje headless foundation projektu?
   │     │  ├─ Tak → użyj jej
   │     │  └─ Nie → wybierz jedną foundation dla projektu
   │     └─ Czy custom widget ma pełną specyfikację keyboard/focus/ARIA?
   │        ├─ Nie → nie buduj custom
   │        └─ Tak → implementuj i testuj w przeglądarce
```

Dla shadcn:

```text
Czy projekt używa shadcn?
├─ Nie → nie dodawaj tylko dla wyglądu jednego komponentu
└─ Tak
   ├─ sprawdź bazę: Radix / Base UI / inna
   ├─ używaj zgodnej wersji
   └─ traktuj wygenerowany komponent jako kod projektu
```

## 4. Lokalny state, server state czy workflow state

```text
Czy stan istnieje tylko w jednym komponencie i nie pochodzi z serwera?
├─ Tak → local state/reducer
└─ Nie
   ├─ Czy to zdalne dane z cache/refetch/invalidation?
   │  ├─ Tak → server rendering lub server-state library
   │  └─ Nie
   ├─ Czy stan reprezentuje wieloetapowy proces?
   │  ├─ Tak → jawna state machine/reducer
   │  └─ Nie
   └─ Czy wiele niezależnych obszarów musi go współdzielić?
      ├─ Tak → dopiero wtedy rozważ shared store
      └─ Nie → nie dodawaj globalnego store
```

## 5. Recovery path

```text
Operacja nie może być kontynuowana
├─ Czy znamy przyczynę?
│  ├─ Nie → neutralny unavailable state + retry + diagnostyka
│  └─ Tak
│     ├─ Czy user może ją naprawić?
│     │  ├─ Tak → wyjaśnij + primary CTA
│     │  └─ Nie → pokaż kto/co musi zadziałać i przewidywalny następny krok
│     ├─ Czy operacja jest wznawialna?
│     │  ├─ Tak → zachowaj intent/input i resume token
│     │  └─ Nie → jasno powiedz co trzeba zacząć od nowa
│     └─ Po naprawie
│        ├─ rewaliduj authority
│        ├─ wróć do przerwanego kroku
│        └─ nie wykonuj automatycznie nieodwracalnej akcji
```

## 6. Nowa biblioteka

```text
Czy problem można rozwiązać istniejącym stackiem?
├─ Tak → nie dodawaj dependency
└─ Nie
   ├─ Czy problem jest złożony i powtarzalny?
   │  ├─ Nie → mały project-owned primitive
   │  └─ Tak
   ├─ Oceń:
   │  ├─ accessibility
   │  ├─ bundle/runtime cost
   │  ├─ SSR/RSC compatibility
   │  ├─ maintenance/activity
   │  ├─ API stability
   │  ├─ testability
   │  └─ konflikt z istniejącą foundation
   └─ Dodaj tylko z evidence i zakresem użycia
```

# Checklisty

## UI

- [ ] Hierarchia odpowiada głównemu celowi strony.
- [ ] Primary action jest jednoznaczna.
- [ ] Secondary actions nie konkurują wizualnie z primary.
- [ ] Layout wynika z treści, nie z przypadkowego template.
- [ ] Typografia ma jawne role: display, heading, body, label, caption.
- [ ] Spacing, radius, color, border, elevation i motion używają tokenów.
- [ ] Jeden rodzaj komponentu ma spójny wygląd i zachowanie.
- [ ] Ikony kontrolne pochodzą z jednego zestawu.
- [ ] Brand SVG i provider icons nie są mieszane z control icons.
- [ ] Empty, loading, partial, blocked, error i success są wizualnie rozróżnialne.
- [ ] Status nie opiera się wyłącznie na kolorze.
- [ ] Mobile nie jest tylko pomniejszonym desktopem.
- [ ] Dense dashboard pozostaje skanowalny.
- [ ] Nie ma fake metrics, fake reviews ani placeholderów produkcyjnych.
- [ ] Nie ma przypadkowego „AI look”: nadmiaru pills, glow, gradientów, identycznych kart i generycznego copy.
- [ ] Animacja wyjaśnia zmianę albo hierarchię, zamiast tylko dekorować.

## UX

- [ ] Cel użytkownika można nazwać jednym zdaniem.
- [ ] Entry point i następny krok są oczywiste.
- [ ] Prerequisites są widoczne przed rozpoczęciem kosztownej operacji.
- [ ] User otrzymuje natychmiastowe potwierdzenie rozpoczęcia akcji.
- [ ] Długie procesy pokazują aktualny etap.
- [ ] Intermediate states są jawne.
- [ ] Błąd mówi: co się stało, co to oznacza i co zrobić.
- [ ] Każdy recoverable error ma primary action.
- [ ] Input i intent są zachowywane, jeśli to bezpieczne.
- [ ] Po recovery użytkownik wraca do przerwanego kroku.
- [ ] Nieodwracalna akcja wymaga ponownego jawnego potwierdzenia.
- [ ] Toast nie jest jedynym nośnikiem ważnego błędu.
- [ ] User nie trafia w dead end.
- [ ] Retry jest kontrolowany i nie duplikuje operacji.
- [ ] Cancel/back ma przewidywalne znaczenie.
- [ ] Destructive lub finansowe akcje mają confirmation i odpowiednią modalność.
- [ ] Help/support jest dostępny w miejscu problemu.
- [ ] Diagnostic details nie ujawniają sekretów ani PII.

## Accessibility

- [ ] Semantyczne landmarks i heading hierarchy.
- [ ] Skip link do głównej treści.
- [ ] Pełna obsługa keyboard-only.
- [ ] Widoczny focus na każdym elemencie interaktywnym.
- [ ] Focus nie jest zasłaniany przez sticky UI.
- [ ] Dialog przenosi focus, zatrzymuje go zgodnie z modalnością i przywraca po zamknięciu.
- [ ] Custom listbox/menu implementuje pełny keyboard model albo jest zastąpiony native/headless primitive.
- [ ] Każda kontrolka ma dostępną nazwę.
- [ ] Icon-only button ma `aria-label`.
- [ ] Dekoracyjne ikony są ukryte przed accessibility tree.
- [ ] Formularze mają label, description i powiązany error.
- [ ] Error summary prowadzi do błędnego pola przy dłuższych formularzach.
- [ ] `role="alert"` jest używany dla pilnych błędów, `status` dla spokojnych aktualizacji.
- [ ] Loading surface ma `aria-busy` i zrozumiałą etykietę.
- [ ] Kolor nie jest jedynym sygnałem.
- [ ] Kontrast tekstu, focus ringów i kontrolek jest sprawdzony.
- [ ] Target minimum 24×24 CSS px; preferowane większe cele dotykowe.
- [ ] Layout działa przy zoom 200% i reflow 400%.
- [ ] `prefers-reduced-motion` jest respektowane.
- [ ] Autoplay można zatrzymać lub jest wyłączony przy reduced motion.
- [ ] `html lang` odpowiada faktycznemu językowi.
- [ ] Auth nie wymaga wyłącznie testu pamięciowego lub poznawczego.
- [ ] Axe jest wsparciem; manual keyboard i screen-reader semantics nadal są sprawdzane.

## Performance

- [ ] Ustalono baseline przed optymalizacją.
- [ ] LCP ≤ 2,5 s przy p75.
- [ ] INP ≤ 200 ms przy p75.
- [ ] CLS ≤ 0,1 przy p75.
- [ ] Wyniki są segmentowane mobile/desktop.
- [ ] Każda publiczna i krytyczna app route ma performance budget.
- [ ] Hero/LCP asset jest odpowiednio preloadowany i zoptymalizowany.
- [ ] Pozostałe media są lazy, jeśli nie narusza to UX.
- [ ] Obrazy mają poprawne wymiary i nie powodują CLS.
- [ ] Raster nie jest ukryty jako base64 w dużym SVG.
- [ ] Fonty są subsetowane i używane w minimalnej liczbie wariantów.
- [ ] Provider, wallet, chart, editor i video code ładuje się na żądanie.
- [ ] Third-party scripts nie są ładowane globalnie bez potrzeby.
- [ ] Server rendering nie duplikuje niepotrzebnie client fetch.
- [ ] Cache i invalidation są jawne.
- [ ] Retry nie generuje request storm.
- [ ] Bundle analyzer sprawdza największe chunki.
- [ ] Niepotrzebne biblioteki i icon packs są usunięte.
- [ ] RUM monitoruje rzeczywistych użytkowników.
- [ ] Lab test nie jest przedstawiany jako jedyny dowód.

## SEO

- [ ] Każda publiczna strona odpowiada osobnemu user/search intent.
- [ ] Nie powstają thin lub duplicate pages.
- [ ] Title i description wynikają z kanonicznej treści.
- [ ] Canonical wskazuje właściwy URL.
- [ ] Public/private indexing policy jest jawna.
- [ ] Prywatne app routes mają `noindex`.
- [ ] Sitemap zawiera tylko canonical public URLs.
- [ ] Robots nie zastępuje kontroli dostępu.
- [ ] Heading hierarchy i link text są opisowe.
- [ ] Najważniejsza treść jest dostępna w SSR HTML.
- [ ] Structured data odpowiada widocznej treści.
- [ ] Nie ma unsupported schema ani sztucznych ratingów.
- [ ] Social preview ma poprawny obraz, alt i wymiary.
- [ ] Publiczne dokumenty mają parsowalną stronę HTML.
- [ ] Content ma source, author/reviewer i freshness tam, gdzie zaufanie ma znaczenie.
- [ ] Claims finansowe, zdrowotne, prawne i bezpieczeństwa są zatwierdzone przez właściwą authority.

## GEO/LLM

- [ ] Treść odpowiada konkretnie na pytania użytkownika.
- [ ] Definicje, kroki i ograniczenia są jednoznaczne.
- [ ] Fakty mają publiczne źródła lub widoczną metodologię.
- [ ] Data aktualizacji jest widoczna dla zmiennych treści.
- [ ] Marka, nazwy produktów i terminy są spójne.
- [ ] Nie ma keyword stuffing ani tekstu pisanego wyłącznie „pod AI”.
- [ ] AI-facing content nie ujawnia private routes, PII ani runtime state.
- [ ] `llms.txt`, jeśli istnieje, jest aktualny i traktowany jako eksperymentalny.
- [ ] `llms.txt` nie zastępuje SSR content, sitemap ani metadata.
- [ ] Nie jest dodawane nieistniejące „AI schema”.
- [ ] FAQ wynika z realnych pytań, a nie z generowania sztucznych fraz.

## Internationalization

- [ ] Locale ma własny stabilny URL, jeśli treść ma być indeksowana.
- [ ] `html lang` odpowiada locale.
- [ ] Canonical i `hreflang` są spójne.
- [ ] Liczby, waluty, daty i plurals są lokalizowane.
- [ ] Layout toleruje dłuższy tekst.
- [ ] RTL jest uwzględniony, jeśli wspierany.
- [ ] Tłumaczenie jest server-rendered dla publicznych stron.
- [ ] Zewnętrzny translator nie jest głównym systemem i18n.
- [ ] Copy transakcyjne i prawne przechodzi właściwy review.

# Failure-path matrix

| Flow | Failure / blocked state | Authority | Komunikat dla usera | Primary recovery | Zachować | Resume condition | Minimalny test |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Auth | sesja wygasła | backend auth | Sesja wygasła; operacja nie została wykonana | Zaloguj ponownie | bezpieczny intent, nie sekret | nowa sesja | 401 podczas akcji |
| Auth | brak uprawnień | backend authorization | Konto nie ma uprawnienia do tej operacji | Wróć / skontaktuj się z adminem | bieżący widok | zmiana uprawnienia | 403 |
| Wallet | brak walleta | backend + provider | Najpierw dodaj portfel | Połącz portfel | formularz/intencja | wallet linked | brak walleta |
| Wallet | ownership nieudowodnione | backend proof | Portfel jest połączony, ale niezweryfikowany | Zweryfikuj własność | wpisane dane | proof verified | challenge reject/success |
| Network | zła sieć | wallet/chain config | Portfel jest na niewłaściwej sieci | Zmień sieć | intencja | expected chain | switch reject/success |
| KYC | wymagane | backend/on-chain policy | Operacja wymaga weryfikacji tożsamości | Dokończ KYC tutaj | wszystkie niesensytywne dane | authoritative approval | required → approved |
| KYC | provider approved, chain pending | on-chain readback | Weryfikacja zakończona; zatwierdzenie on-chain trwa | Odśwież status | intencja | on-chain approved | pending → approved |
| KYC | odrzucone/needs action | provider/backend | Weryfikacja wymaga poprawy | Otwórz KYC | intencja | provider resubmission | rejected/needs-action |
| Funds | niewystarczające środki | wallet/chain | Brakuje środków do wykonania operacji | Dodaj środki | kwota i metoda | balance sufficient | insufficient balance |
| Gas | niewystarczający gas | wallet/chain | Brakuje tokena sieciowego na opłatę | Doładuj gas | przygotowana operacja | gas sufficient | gas preflight |
| Wallet action | user rejected | wallet | Podpis został odrzucony; nic nie wysłano | Spróbuj ponownie | prepared intent | nowa zgoda usera | rejection code |
| Wallet action | popup/provider unavailable | wallet provider | Nie można otworzyć portfela | Otwórz/połącz wallet | intencja | provider available | popup blocked |
| Transaction | submitted, not indexed | chain + indexer | Transakcja została wysłana i czeka na indeksowanie | Sprawdź ponownie | tx hash, safe context | indexed event | delayed indexer |
| Transaction | reverted | receipt | Transakcja nie powiodła się | Pokaż przyczynę / przygotuj ponownie | input, nie stary package | nowy preflight | reverted receipt |
| Provider | checkout cancelled | provider session | Płatność została anulowana; zakup tokena nie nastąpił | Wróć do zakupu | amount/currency | nowa sesja | cancel callback |
| API | validation 422 | backend validation | Wskaż konkretne błędne pola | Popraw pola | poprawne pola | valid form | field errors |
| API | rate limit 429 | backend | Zbyt wiele prób; podaj bezpieczny czas retry | Spróbuj później | input | retry-after | 429 |
| API | timeout/5xx | backend/network | Usługa jest chwilowo niedostępna | Ponów / spróbuj później | intent | service restored | timeout/500 |
| Connectivity | offline | browser/network | Brak połączenia; nic nie zostało wysłane | Ponów po połączeniu | input | online | offline/reconnect |
| Duplicate | idempotency conflict | backend | Operacja mogła już zostać rozpoczęta | Sprawdź status | idempotency key | canonical status | duplicate submit |

Reguły przekrojowe:

- Nie mapować nieznanego błędu na success.
- Nie pokazywać raw provider/backend error jako jedynego copy.
- Nie ponawiać automatycznie podpisu, broadcastu ani mutacji.
- Query można retryować według polityki; mutation wymaga idempotency i jawnych warunków.
- Po recovery zawsze ponownie sprawdzić authority.
- Nie używać starego prepared package po zmianie walleta, sieci, kwoty lub eligibility.
- Support details mogą zawierać correlation ID, tx hash, chain, timestamp i bezpieczny error code, ale nie tokeny, PII ani sekrety.

# Definition of Done

## Zakres i źródła

- [ ] Przejrzano repo instructions i lokalne konwencje.
- [ ] Cel użytkownika i acceptance criteria są jawne.
- [ ] Scope i out-of-scope są jawne.
- [ ] Źródła danych i authority są udokumentowane.
- [ ] Nie wprowadzono niezaakceptowanego redesignu lub dependency migration.

## Architektura

- [ ] Server/client boundaries są minimalne i uzasadnione.
- [ ] API/CMS/provider payload ma adapter lub runtime validation adekwatne do ryzyka.
- [ ] Server state, workflow state i local UI state nie są pomieszane.
- [ ] Jedna headless foundation i jedna control-icon family.
- [ ] Brak nieuzasadnionego global state.
- [ ] Brak production fake data i mock copy.
- [ ] Legacy code dodany do scope został usunięty albo jawnie pozostawiony.

## UI i UX

- [ ] Primary user goal można wykonać.
- [ ] Loading, empty, partial, blocked, pending, success i error są obsłużone.
- [ ] Każdy recoverable failure ma następny krok.
- [ ] Input i intent są zachowane tam, gdzie bezpieczne.
- [ ] Recovery wraca do właściwego etapu.
- [ ] Nieodwracalne działanie nie wykonuje się automatycznie po recovery.
- [ ] Responsive layouts sprawdzono w uzgodnionych viewportach.
- [ ] Visual hierarchy i brand consistency sprawdzono na aktualnym renderingu.
- [ ] Nie ma dead ends, fake success ani status ambiguity.
- [ ] Copy wyjaśnia sytuację językiem użytkownika.

## Accessibility

- [ ] Semantic HTML i landmarks.
- [ ] Keyboard-only path.
- [ ] Focus order, focus visibility i focus restoration.
- [ ] Dialog/listbox/menu behavior zgodne z właściwym interaction model.
- [ ] Formularze mają labels, errors i descriptions.
- [ ] Live regions odpowiadają pilności komunikatu.
- [ ] Contrast, non-color cues i target sizes.
- [ ] Reduced motion.
- [ ] Zoom/reflow.
- [ ] Właściwy język dokumentu.
- [ ] Axe bez nierozwiązanych critical/serious issues.
- [ ] Manual a11y trace wykonany; axe nie jest jedynym dowodem.

## Performance

- [ ] Performance baseline i budżet istnieją.
- [ ] LCP, INP i CLS spełniają uzgodnione cele albo odchylenie jest jawne.
- [ ] Brak niepotrzebnych globalnych third-party scripts.
- [ ] Duże zależności są lazy/dynamic, jeśli to poprawne.
- [ ] Media i fonty są zoptymalizowane.
- [ ] Bundle diff został sprawdzony.
- [ ] Brak nieoczekiwanego CLS.
- [ ] RUM lub jawnie opisany brak RUM.

## SEO/GEO/i18n

Dla publicznych routes:

- [ ] Metadata i canonical.
- [ ] Robots/indexing policy.
- [ ] Sitemap coverage.
- [ ] SSR-readable content.
- [ ] Structured data zgodne z widoczną treścią.
- [ ] Social preview.
- [ ] Locale URL, `lang` i `hreflang`, jeśli dotyczy.
- [ ] Freshness/source/author dla treści wymagających zaufania.
- [ ] Brak private facts w publicznych i LLM-facing surfaces.
- [ ] `llms.txt`, jeśli używany, jest aktualny i pomocniczy.

Dla prywatnych routes:

- [ ] `noindex`.
- [ ] Brak danych użytkownika w metadata lub structured data.
- [ ] Robots nie jest traktowany jako zabezpieczenie dostępu.

## Testy i evidence

- [ ] Typecheck.
- [ ] Lint.
- [ ] Unit/component tests dla logiki i primitives.
- [ ] Production build.
- [ ] E2E primary journey.
- [ ] E2E krytycznych failure/recovery paths.
- [ ] Desktop i mobile visual evidence.
- [ ] Keyboard trace.
- [ ] Accessibility scan.
- [ ] Browser console/runtime errors checked.
- [ ] Performance evidence dla scope performance-sensitive.
- [ ] Integrations używają safe mock/sandbox zgodnie z permissions.
- [ ] Skipped checks i ich wpływ są jawne.
- [ ] Po każdej poprawce wykonano pełny re-review aktualnego scope.

## Quality closure

- [ ] Implementacja odpowiada instrukcji i zaakceptowanemu design/spec.
- [ ] Nie ma scope creep.
- [ ] Nie ma nierozwiązanych P0, P1 ani materialnych P2.
- [ ] Residual risks są zapisane.
- [ ] Evidence jest bieżące względem aktualnego kodu.
- [ ] Owner visual/product review jest wykonany, jeśli wymagany.
- [ ] Nie zadeklarowano „professional”, „accessible”, „optimized”, „SEO-ready” ani „pixel-perfect” bez dowodów.

# Odpowiedzialność poszczególnych references

| Reference | Ładować gdy |
| --- | --- |
| `decision-trees.md` | Zawsze przy nowym tasku lub audycie. |
| `ui-ux-quality.md` | Każda user-visible zmiana lub visual review. |
| `interaction-and-recovery.md` | Formularze, onboarding, async actions, błędy i wieloetapowe flows. |
| `accessibility.md` | Każda user-visible zmiana. |
| `performance.md` | Route, media, provider, bundle, page-speed lub optimization. |
| `seo-geo-i18n.md` | Publiczne strony, metadata, content, locales, LLM/GEO. |
| `library-selection.md` | Nowa biblioteka, design system albo primitive. |
| `transactional-flows.md` | Wallet, KYC, payment, transaction, financial, admin mutation. |
| `qa-definition-of-done.md` | Przed implementacją i przed handoffem. |

# Co powinno pozostać poza skillem

Nie wpisywać do reusable skillu:

- nazw CHT/GFIX;
- konkretnych tras projektu;
- konkretnych endpointów;
- wielkości obecnych assetów;
- historycznych statusów workflow;
- szczegółów klienta;
- literalnych komunikatów CHT;
- wymogu używania Radix w każdym repo;
- listy „najlepszych bibliotek” bez decision criteria;
- chwilowych wersji paczek;
- repo-specific Definition of Done.

Takie informacje należą do repo/project context, nie do ogólnego skillu.

Wpływ `skill-creator` na blueprint:

- główny `SKILL.md` pozostaje zwięzłym kontraktem wykonawczym;
- szczegóły trafiają do jednopoziomowych `references/`;
- nie powstają zbędne README i dokumenty pomocnicze;
- frontmatter zawiera pełne triggery;
- decyzje o bibliotekach zachowują odpowiedni stopień swobody;
- walidacja i forward-testing są odrębnym krokiem po utworzeniu plików.
