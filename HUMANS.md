# HUMANS.md

## Cel dokumentu

`HUMANS.md` to instrukcja dla człowieka pracującego z repozytorium, które używa naszego systemu docs, workflow i autopilota.

Ten dokument jest dla:

- ownera, który decyduje o zakresie, ryzyku i akceptacji;
- operatora, który pilnuje przebiegu pracy z Codexem;
- engineera, który chce zrozumieć źródła prawdy, bramki jakości, recovery i git policy.

`HUMANS.md` mówi, jak człowiek ma pracować z systemem. `AGENTS.md` mówi, jak agent ma wykonywać pracę.

## Przykład wykorzystania

Poniższy przykład pokazuje, jak człowiek może przeprowadzić realny projekt przez AI Workflow. Traktuj go jako inspirację i praktyczny runbook, nie jako sztywny scenariusz do kopiowania 1:1.

### Aplikacja przykładowa: WorkshopHub

Załóżmy, że budujesz `WorkshopHub`: aplikację Laravel do publikowania warsztatów, zapisów uczestników, płatności Stripe, maili potwierdzających i panelu organizatora.

Projekt ma kilka typów ryzyka:

- landing page i publiczny katalog warsztatów to zwykle low/medium risk;
- płatności Stripe, maile, dane uczestników, migracje, kolejki i panel organizatora wymagają dokładniejszego workflow;
- realne maile, realne płatności, production data, sekrety i produkcyjne migracje są high-risk albo critical-risk i wymagają zgody ownera.

Ten przykład pokazuje trzy tryby pracy:

- spokojny dzień, gdy prowadzisz jeden task ręcznie z Codexem;
- szybki dzień, gdy uruchamiasz autopilota dla gotowych tasków;
- poboczny side-task, który można zrobić szybko bez naruszania pełnego workflow.

### 1. Instalacja AI Workflow w repo

Najpierw sprawdzasz, czy repo aplikacji ma już własne pliki i katalogi, których nie wolno nadpisać. Pełna polityka jest w `docs/ai-workflow/ai/installation.md`.

```bash
cd ~/Code/workshophub
test -e README.md && echo "README.md exists"
test -e AGENTS.md && echo "AGENTS.md exists"
test -e HUMANS.md && echo "HUMANS.md exists"
test -e docs && echo "docs exists"
test -e docs/ai-workflow && echo "docs/ai-workflow exists"
test -e scripts && echo "scripts exists"
test -e scripts/ai-workflow && echo "scripts/ai-workflow exists"
test -e .github && echo ".github exists"
test -e .github/workflows/ai-workflow-validate.yml && echo "ai-workflow CI exists"
git status --short
```

Jeśli preflight nie pokazuje kolizji w workflow-owned namespace'ach, kopiujesz tylko dedykowane przestrzenie AI Workflow:

```bash
mkdir -p docs scripts .github/workflows
if [ ! -e docs/ai-workflow ]; then cp -R ../ai-workflow/docs/ai-workflow docs/; else echo "docs/ai-workflow exists: classify before sync"; fi
if [ ! -e scripts/ai-workflow ]; then cp -R ../ai-workflow/scripts/ai-workflow scripts/; else echo "scripts/ai-workflow exists: classify before sync"; fi
if [ ! -e .github/workflows/ai-workflow-validate.yml ]; then cp ../ai-workflow/.github/workflows/ai-workflow-validate.yml .github/workflows/; else echo "ai-workflow CI exists: classify before sync"; fi
if [ ! -e AGENTS.md ]; then cp ../ai-workflow/AGENTS.md AGENTS.md; else echo "AGENTS.md exists: merge required"; fi
if [ ! -e HUMANS.md ]; then cp ../ai-workflow/HUMANS.md HUMANS.md; else echo "HUMANS.md exists: merge required"; fi
```

Nie kopiuj szeroko `docs/`, `scripts/` ani `.github/`, bo w prawdziwym repo te katalogi mogą już należeć do aplikacji. Jeżeli `AGENTS.md` albo `HUMANS.md` istnieją, Codex ma zaproponować merge sekcji AI Workflow, a nie nadpisywać plik. `README.md` zawsze traktuj jako dokument aplikacji; możesz dodać tylko krótki link do `HUMANS.md` albo `docs/ai-workflow/`.

Po skopiowaniu `docs/ai-workflow/repo/*.md` mogą nadal opisywać upstreamowe repo `ai-workflow`. To normalne po instalacji template'u, ale nie wolno używać tych plików jako kontekstu aplikacji `WorkshopHub`.

Pierwszy prompt do Codexa:

```text
Run AI Workflow installation preflight and phase-0-repo-intake for this repository. This is a Laravel app called WorkshopHub. Detect existing README.md, AGENTS.md, HUMANS.md, docs, scripts and .github collisions. Do not overwrite target-owned files. Detect and replace stale ai-workflow docs/ai-workflow/repo runtime files using docs/ai-workflow/ai/templates/repo. Do not touch product code.
```

Oczekiwany efekt:

- kolizje instalacyjne są oznaczone jako resolved albo blocked;
- istniejące root `AGENTS.md` i `HUMANS.md` są zachowane albo mają zatwierdzony merge;
- `docs/ai-workflow/repo/context.md` opisuje `WorkshopHub`, nie `ai-workflow`;
- `docs/ai-workflow/repo/repo-intake.md` zawiera komendy, safe environment i restricted zones tego repo;
- `docs/ai-workflow/repo/status.md` mówi, że repo jest gotowe albo blokuje dalszą pracę konkretnym powodem;
- `docs/ai-workflow/repo/memory.md` jest puste albo zawiera wyłącznie repo-local memory dla `WorkshopHub`.

### 2. Repo intake i bezpieczne komendy

W repo Laravel typowe komendy mogą wyglądać tak:

```bash
composer install
npm install
php artisan test
npm run build
php artisan migrate --pretend
git diff --check
```

To są przykłady. Codex nie powinien ich zgadywać. Ma sprawdzić realne pliki repo, np. `composer.json`, `package.json`, konfigurację testów, migracje i środowisko lokalne. Jeśli czegoś nie da się ustalić, powinien wpisać `not configured`, a nie wymyślać komendę.

Prompt:

```text
Fill docs/ai-workflow/repo/context.md and docs/ai-workflow/repo/repo-intake.md for WorkshopHub. Record install/test/build commands, safe test DB policy, migration policy, mail strategy, Stripe sandbox strategy, forbidden production commands, and restricted zones.
```

Dobre `repo-intake.md` powinno odpowiedzieć między innymi:

- czy wolno uruchamiać migracje i na jakiej bazie;
- czy maile idą przez fake/log/array driver;
- czy Stripe działa tylko w sandboxie;
- które pliki mogą zawierać sekrety;
- jakie komendy trzeba uruchomić przed `PASS`;
- które działania wymagają owner approval.

Jeśli safe test database albo fake mail/Stripe strategy nie są jasne, workflow powinien zatrzymać implementację tasków zależnych od tych elementów.

### 3. Walidacja pomysłu

Zaczynasz od surowego brain dumpu:

```text
Mam pomysł na WorkshopHub: landing page, katalog warsztatów, zapisy uczestników, płatność Stripe, mail potwierdzający i panel organizatora.
```

Prompt do Codexa:

```text
Run phase-0-idea-validation for WorkshopHub. Tell me what is strong, what is weak, what is missing, which decisions block context creation, and whether we can create project context.
```

Codex powinien rozdzielić pomysł na:

- co zostaje: np. publiczny katalog warsztatów, prosty zapis, panel organizatora;
- co jest słabe: np. brak polityki zwrotów, brak procesu anulowania, brak zgód marketingowych;
- czego brakuje: np. model danych uczestnika, status płatności, strategia maili, rollback płatności;
- decyzje ownera: np. czy płatność jest wymagana od razu, czy najpierw zapis bez płatności;
- blocker: np. brak decyzji, czy maile mają być synchroniczne, queue, czy tylko log w MVP.

Jeśli wynik jest `accepted` albo `accepted-with-changes`, można stworzyć project context. Jeśli wynik jest `blocked`, nie przechodź do architektury.

### 4. Context, architektura i QA

Po zaakceptowaniu pomysłu tworzysz project context:

```text
Create docs/ai-workflow/projects/workshophub/intake/context.md from the accepted idea validation. Keep it project-specific.
```

Następnie architektura:

```text
Run phase-1-architecture for WorkshopHub. Cover Laravel boundaries, models, payments, mail, queue, admin panel, validation, test strategy, rollback and external effects.
```

Architecture QA:

```text
Run phase-1-architecture-qa. Try to break the architecture. Fail it if payments, mail, permissions, migrations, rollback, or tests are underspecified.
```

Na tym etapie Codex powinien wykryć, że:

- Stripe wymaga sandbox policy i approval przed real payment flow;
- mail potwierdzający nie może wysyłać realnych maili bez zgody;
- migracje wymagają safe database strategy;
- panel organizatora może dotykać permissions/auth;
- rollback dla płatności i maili musi być opisany, jeśli task jest produkcyjnie istotny.

Architecture QA nie jest formalnością. Jeśli brakuje decyzji albo rollbacku, wynik powinien być `FAIL` i powrót do `phase-1-architecture-fix-loop`.

### 5. Plan projektu, taski i packaging

Po architekturze planujesz projekt:

```text
Run phase-2-project-plan for WorkshopHub. Create task sequence, dependencies, risk class, DoD, spec path, quality path and docs/ai-workflow/projects/workshophub/tasks.md.
```

Przykładowy task index:

```text
WH-LANDING-001-public-landing-page
WH-WORKSHOPS-002-workshop-listing
WH-PAYMENTS-003-stripe-checkout
WH-MAIL-004-confirmation-email
WH-ADMIN-005-organizer-dashboard
```

Plan QA:

```text
Run phase-2-plan-qa. Verify task IDs, dependency order, risk class, spec paths, quality paths, and hidden blockers.
```

Packaging:

```text
Run phase-2-task-packaging. Package only independent tasks. Do not package tasks with internal dependencies.
```

Przykład poprawnej decyzji:

- `WH-LANDING-001` może iść solo, bo nie zależy od płatności;
- `WH-WORKSHOPS-002` może zależeć od modelu warsztatów;
- `WH-PAYMENTS-003` nie powinien być pakowany z mailem potwierdzającym, jeśli mail zależy od statusu płatności;
- `WH-ADMIN-005` może wymagać auth/permissions, więc nie jest side-taskiem.

Jeśli package ukrywa zależności, packaging QA powinno dać `FAIL`.

### 6. Dzień spokojny: użytkownik prowadzi jeden task ręcznie

Masz więcej czasu i chcesz ręcznie przejść jeden prosty task: `WH-LANDING-001-public-landing-page`.

Specyfikacja:

```text
Prepare phase-3-specification for WH-LANDING-001-public-landing-page. I want to review the spec before implementation.
```

Spec QA:

```text
Run phase-3-spec-qa for WH-LANDING-001-public-landing-page.
```

Implementacja:

```text
Implement WH-LANDING-001-public-landing-page now, exactly according to the accepted spec. Do not touch payment or mail code.
```

Quality:

```text
Run phase-5-quality for WH-LANDING-001-public-landing-page. Include commands, manual checks, skipped checks and residual risk.
```

W tym trybie człowiek może:

- czytać spec przed implementacją;
- zatrzymać Codexa po QA;
- poprosić o diff summary;
- ręcznie sprawdzić UI;
- zdecydować, czy wynik jest wystarczający do distillation.

To nadal nie oznacza, że wolno oznaczyć `PASS` bez evidence. Jeśli `npm run build` albo `php artisan test` nie działa, Codex musi zapisać powód i wpływ na `PASS`.

### 7. Dzień szybki: autopilot

Innego dnia się spieszysz i chcesz, żeby Codex wykonał serię gotowych tasków.

Prompt:

```text
Start supervised autopilot for ready low/medium-risk WorkshopHub tasks only. Do not execute high-risk payment, mail, migration, production, or external API actions without owner approval. Commit only after QUALITY PASS.
```

Autopilot nadal musi przejść:

```text
spec refresh/create
-> spec QA
-> implementation
-> quality
-> fix loop, jeśli FAIL
-> distillation
-> checkpoint, jeśli wypada
-> next task
```

Autopilot powinien zrobić STOP, jeśli trafi na:

- `WH-PAYMENTS-003-stripe-checkout` bez jasnej Stripe sandbox policy;
- mail potwierdzający, który wysyła realne wiadomości;
- migrację bez safe database strategy;
- auth/permissions bez zgody ownera;
- brak testów potrzebnych do evidence-backed `PASS`.

Dobry prompt do wznowienia po STOP:

```text
Resolve the autopilot stop for WH-PAYMENTS-003. Show the missing owner decisions, recommended safe default, rollback impact, and the exact phase we should return to. Do not implement yet.
```

### 8. Side-task bez naruszania workflow

Side-task to mała, lokalna, niskiego ryzyka zmiana poza aktywnym planem albo jawnie oznaczona przez ownera jako poboczna.

Przykład:

```text
This is a side-task: change the CTA copy on the landing page from "Join now" to "Reserve your workshop seat". Confirm it is low-risk, local, outside active plan scope, then implement and run relevant checks.
```

Side-task jest dopuszczalny, jeśli:

- nie dotyka płatności, danych, migracji, auth, permissions, sekretów, maili ani external effects;
- nie zmienia architektury;
- nie zmienia acceptance criteria aktywnego taska;
- można go zweryfikować prostą komendą albo manual checkiem;
- nie koliduje z aktywnym write-setem.

Jeśli podczas side-taska okazuje się, że trzeba zmienić flow płatności, dodać pole do bazy, zmienić maila albo ruszyć panel admina, to przestaje być side-task. Wtedy wracasz do normalnego workflow: plan/spec/QA/implementation/quality.

### 9. Review decyzji AI i rollback jednej decyzji

Po kilku taskach chcesz sprawdzić decyzje podjęte przez AI.

Prompt:

```text
Review all decisions for WorkshopHub. Show auto-resolvable, high-impact and critical-risk decisions, with recommendation, chosen option and rollback impact.
```

Załóżmy, że Codex wcześniej wybrał synchroniczną wysyłkę maili potwierdzających, a ty chcesz rollback do kolejki.

Prompt:

```text
Roll back decision WH-DEC-004 from synchronous confirmation email to queued mail dispatch. Route this through the correct workflow phase, update decisions, architecture/plan/spec if needed, and do not implement until gates are satisfied.
```

Rollback decyzji nie jest zwykłym `git revert`. Codex powinien ustalić:

- czy decyzja wpływa na architekturę;
- czy plan tasków wymaga zmiany;
- czy istnieją specyfikacje, które trzeba odświeżyć;
- czy potrzeba `phase-1-architecture-fix-loop`, `phase-2-plan-fix-loop`, `phase-3-spec-fix-loop` albo `phase-5-fix-loop`;
- jakie testy i rollback notes są wymagane.

Jeśli decyzja dotyczy produkcji, maili, płatności albo danych uczestników, Codex powinien zatrzymać się po decyzję ownera przed implementacją.

### 10. Quality, distillation, checkpoint i final-owner-yes

Po zakończonych taskach uruchamiasz distillation:

```text
Run phase-6-distillation for completed WorkshopHub tasks. Capture only reusable decisions, constraints and future risks.
```

Checkpoint:

```text
Run phase-7-checkpoint. Compare repo, architecture, plan, tasks, quality evidence, decisions and memory. Detect drift.
```

Final check:

```text
Run phase-8-final-check for WorkshopHub. Do not close the project. If technical pass succeeds, stop at awaiting-owner-final-yes.
```

Jeśli final check jest technicznie zielony, projekt nadal nie jest zamknięty bez ownera.

Jawna zgoda ownera:

```text
final-owner-yes: I approve closing WorkshopHub project scope described in the final check.
```

Różnica jest ważna:

- technical pass mówi, że repo, docs, evidence, memory i plan są spójne;
- `final-owner-yes` mówi, że człowiek akceptuje zamknięcie zakresu projektu.

Bez tej zgody workflow powinien zatrzymać się na `awaiting-owner-final-yes`.

### Opcjonalne użycie ChatGPT

Cały workflow musi dać się przejść z Codexem. ChatGPT może być dodatkiem do brainstormingu albo drugiego review, ale nie zastępuje repo artifacts.

Przykładowy prompt do ChatGPT:

```text
Review this WorkshopHub architecture for missing risks. Do not change the workflow source of truth; return critique only.
```

Po takim review wracasz do Codexa:

```text
Compare this external review with current WorkshopHub architecture and decisions. If it identifies valid gaps, route them through the correct workflow phase. Do not implement directly from the review.
```

Najważniejsza zasada z przykładu: AI Workflow nie ma spowalniać każdej drobnej pracy. Ma wymusić jasny status, decyzje i evidence tam, gdzie brak kontroli mógłby zepsuć projekt.

## Model mentalny

System działa dobrze tylko wtedy, gdy rozdzielamy kilka warstw:

- **Repo state**: rzeczywisty kod, migracje, config, testy, pliki i aktualny stan gita.
- **Agent contract**: `AGENTS.md`, czyli zasady wykonawcze dla Codexa.
- **Workflow docs**: `docs/ai-workflow/ai/workflow.md` i `docs/ai-workflow/ai/workflow/`, czyli proces faz, bramek, QA i fix loopów.
- **Repo runtime docs**: `docs/ai-workflow/repo/`, czyli globalny context repo, repo intake, status i repo memory.
- **Project docs**: `docs/ai-workflow/projects/<project>/`, czyli aktywna przestrzeń projektu: intake, architektura, plan, specs, quality, decisions, distillations, checkpoints, autopilot.
- **Human docs**: `docs/ai-workflow/humans/`, czyli artefakty pisane dla człowieka: runbooki, audyty, decyzje, podsumowania, zgody.

Najważniejsza zasada: **repo state jest prawdą o tym, co faktycznie istnieje, a docs są kontraktem i pamięcią procesu**. Jeśli dokumentacja mówi jedno, a repo pokazuje drugie, to jest drift i trzeba go rozwiązać przed dalszą implementacją.

## Źródła Prawdy

Kiedy nie wiesz, co wolno zrobić albo jaka faza jest aktualna, czytaj źródła w tej kolejności:

1. `AGENTS.md` - kontrakt wykonawczy dla agenta, stop conditions, quality rules i artifact boundaries.
2. `docs/ai-workflow/ai/workflow.md` - główny router faz workflow.
3. `docs/ai-workflow/ai/workflow/<phase>.md` - szczegółowa specyfikacja konkretnej fazy.
4. `docs/ai-workflow/ai/workflow/overview.md` - globalny opis workflow, statusu, autopilota i recovery.
5. `docs/ai-workflow/ai/autopilot.md` - checklist startu i warunki działania autopilota.
6. `docs/ai-workflow/repo/context.md` - globalny opis repo.
7. `docs/ai-workflow/repo/repo-intake.md` - repo-level bootstrap/intake, szczególnie przed utworzeniem pierwszego projektu.
8. `docs/ai-workflow/ai/external-memory.md` - uniwersalna pamięć rekomendacji i ulepszeń workflow, nie repo-specific.
9. `docs/ai-workflow/repo/status.md` - repo-level status bieżącej pracy.
10. `docs/ai-workflow/projects/<project>/status.md` - project-local status bieżącej pracy.
11. `docs/ai-workflow/projects/<project>/...` - artefakty projektu: plan, specyfikacje, evidence, decyzje, checkpointy, runtime.

Jeśli źródła są sprzeczne, nie proś Codexa o zgadywanie. Poproś o reconciliation albo escalation.

## Układ Dokumentów

Canonical project workspace:

```text
docs/ai-workflow/projects/<project>/
  status.md
  README.md
  project-memory.md
  intake/
  architecture/
  planning/
  specs/
  quality/
  decisions/
  escalations/
  distillations/
  checkpoints/
  autopilot/
```

Znaczenie katalogów:

- `intake/`: wejściowy kontekst i audyt repo.
- `architecture/`: decyzje architektoniczne i ich QA.
- `planning/`: plan projektu i packaging.
- `specs/`: specyfikacje tasków gotowe do implementacji albo dependency-gated.
- `quality/`: evidence dla PASS/FAIL, QA i bramek.
- `decisions/`: decyzje ownera i decyzje auto-resolvable zapisane przez Codexa.
- `escalations/`: blokady, których autopilot nie może rozwiązać sam.
- `distillations/`: wiedza po zakończonych taskach.
- `checkpoints/`: okresowa synchronizacja stabilnego stanu.
- `autopilot/`: runtime autopilota.

`docs/ai-workflow/repo/context.md` jest miejscem na globalny opis repo: czym jest repo, jaki ma stack, domenę, główne moduły, granice i lokalne zasady.

`docs/ai-workflow/repo/repo-intake.md` jest repo-level artefaktem bootstrap. Używaj go, gdy workflow został dopiero dodany do repo albo zanim powstanie pierwszy `docs/ai-workflow/projects/<project>/`.

W upstreamowym repo `ai-workflow` pliki `docs/ai-workflow/repo/context.md`, `repo-intake.md`, `status.md` i `memory.md` mogą opisywać samo `ai-workflow`. Po skopiowaniu workflow do innego repo, np. aplikacji Laravel, te pliki są tylko skopiowanym runtime. Repo intake musi je zastąpić faktami o aktualnym repo, używając neutralnych template'ów z `docs/ai-workflow/ai/templates/repo/`.

`docs/ai-workflow/ai/external-memory.md` jest miejscem na uniwersalne wnioski o naszym workflow: rekomendacje, antywzorce, zasady i pomysły do przeniesienia do template'u `ai-workflow`. Nie zapisuj tam faktów domenowych konkretnego repo.

`docs/ai-workflow/humans/` nie jest miejscem na specs, QA evidence ani runtime. To miejsce na dokumenty dla ludzi.

## Pełny Workflow

Pełny workflow jest wymagany dla zadań wynikających z aktywnego planu projektu.

Fazy:

1. `phase-0-idea-validation.md` - weryfikacja brain dumpu / pomysłu przed contextem.
2. `context.md` - zaakceptowany context projektu.
3. `phase-0-repo-intake.md` - rozpoznanie repo, komend, struktur, ryzyk, istniejących zasobów.
4. `phase-1-architecture.md` - decyzje architektoniczne, granice domen, odpowiedzialności komponentów.
5. `phase-1-architecture-qa.md` - kontrola jakości architektury.
6. `phase-1-architecture-fix-loop.md` - poprawki architektury po FAIL.
7. `phase-2-project-plan.md` - sekwencja tasków z kontraktami wykonawczymi.
8. `phase-2-plan-qa.md` - kontrola planu.
9. `phase-2-plan-fix-loop.md` - poprawki planu po FAIL.
10. `phase-2-task-packaging.md` - decyzja, czy taski można grupować.
11. `phase-2-packaging-qa.md` - QA paczek, jeśli powstały.
12. `phase-3-specification.md` - spec taska albo paczki.
13. `phase-3-spec-qa.md` - sprawdzenie, czy spec nadaje się do implementacji.
14. `phase-3-spec-fix-loop.md` - poprawki specyfikacji po FAIL.
15. `phase-4-implementation.md` - zmiany w kodzie albo docs zgodne ze specem.
16. `phase-5-quality.md` - testy, review, manual checks i evidence.
17. `phase-5-fix-loop.md` - poprawki implementacji po FAIL.
18. `phase-6-distillation.md` - zapisanie wiedzy po tasku.
19. `phase-7-checkpoint.md` - synchronizacja po ustalonej kadencji albo drift.
20. `phase-8-final-check.md` - finalne domknięcie planu, zwykle z owner final approval.

Reguła jest prosta:

- `PASS` pozwala przejść tylko do następnej poprawnej fazy.
- `FAIL` wraca do właściwego fix loopa.
- Brak evidence nie jest warningiem. To brak podstaw do PASS.

## Jak Czytać Status

Zawsze zacznij od:

- `docs/ai-workflow/repo/status.md`;
- `docs/ai-workflow/projects/<project>/status.md`.

Najważniejsze pola:

- `workflow-requirement`: czy pełny workflow jest obowiązkowy.
- `workflow-scope`: czy task wynika z planu, czy jest side-taskiem.
- `active-project`: aktywny projekt docs.
- `active-plan-status`: status planu.
- `current-task`: aktualny task.
- `current-phase`: aktualna faza.
- `phase-result`: wynik fazy.
- `next-phase`: następna dozwolona faza.
- `blocking-reason`: konkretny blocker.
- `autopilot-mode`: tryb autopilota.
- `autopilot-state`: stan runtime.
- `last-stable-pass`: ostatni punkt, do którego można bezpiecznie wrócić.

Jeśli status mówi, że następna faza to `phase-4-implementation`, ale spec nie ma PASS albo nie ma evidence, nie startuj implementacji. Najpierw poproś Codexa o reconciliation.

## Jak Pracować Z Codexem

Najbezpieczniej wydawać polecenia fazami:

```text
idea validation
repo intake
architektura
qa architektury
plan projektu
plan qa
task packaging
specyfikacja
spec qa
implement now
faza jakosci
fix loop
destylacja
checkpoint
final check
```

Dobre polecenie mówi:

- jaki jest zakres;
- czy to plan, QA, fix loop, implementacja czy autopilot;
- czy wolno pisać do plików;
- czy wolno commitować;
- jakie STOP conditions obowiązują.

Przykład:

```text
Uruchom autonomous-execution dla tasków TASK-01..TASK-16 z aktywnego planu, sekwencyjnie, bez real external effects, z commitem dopiero po QUALITY PASS.
```

`implement now` pisz tylko wtedy, gdy:

- plan jest zatwierdzony;
- spec jest gotowy albo ma zostać literalnie zapisany z zaakceptowanego `/plan`;
- wymagane decyzje są zamknięte;
- status wskazuje implementację jako następną fazę.

Jeśli chcesz tylko analizę, plan albo QA, powiedz to wprost. W tych fazach Codex nie powinien zmieniać kodu produktu.

ChatGPT może być użyty jako opcjonalny dodatek do brainstormingu albo drugiego review, ale pełny workflow musi być możliwy do przejścia wyłącznie z Codexem.

## Autopilot

Autopilot to nie jest tryb "rób wszystko bez zasad". To deterministyczna pętla wykonawcza z bramkami.

Typowy cykl autopilota:

```text
preflight
-> spec refresh/create
-> spec QA
-> spec fix loop, jeśli FAIL
-> implementation
-> quality
-> fix loop, jeśli FAIL
-> distillation
-> checkpoint, jeśli wypada
-> next task
-> final check
-> awaiting-owner-final-yes
```

Przed każdą fazą Codex powinien sprawdzić:

- `docs/ai-workflow/repo/status.md`;
- `docs/ai-workflow/projects/<project>/status.md`;
- `autopilot-state.md`, jeśli autopilot jest aktywny;
- wymagane artefakty fazy;
- zależności taska;
- dirty workspace i overlap write-set;
- drift między repo, planem, specem, evidence i statusem;
- retry counters;
- STOP conditions.

Autopilot może iść dalej tylko po evidence-backed `PASS`.

## Runtime Autopilota

Runtime autopilota jest w:

```text
docs/ai-workflow/projects/<project>/autopilot/autopilot-state.md
docs/ai-workflow/projects/<project>/autopilot/autopilot-ledger.md
docs/ai-workflow/projects/<project>/autopilot/autopilot-events.md
```

Znaczenie:

- `autopilot-state.md`: aktualny task, faza, retry, budżet, ostatni stabilny PASS, checkpoint cadence.
- `autopilot-ledger.md`: append-only historia działań, evidence, decyzji, driftów i przejść.
- `autopilot-events.md`: eventy dla ownera, czyli rzeczy wymagające uwagi człowieka.

Jeśli autopilot się zatrzyma, najpierw czytaj `autopilot-events.md`, potem `autopilot-state.md`, potem ledger.

## Decyzje I Zgody

Każda decyzja powinna mieć klasę.

`auto-resolvable`:

- Codex może wybrać rekomendację;
- musi zapisać decyzję w `docs/ai-workflow/projects/<project>/decisions/`;
- workflow idzie dalej.

`high-impact`:

- decyzja wpływa na architekturę, scope, trwały model danych, vendorów, koszty, kontrakty, API albo ryzyko biznesowe;
- Codex zapisuje rekomendację i alternatywę;
- owner decyduje przed dalszą pracą.

`critical-risk`:

- decyzja dotyczy produkcji, danych, prawa, finansów, bezpieczeństwa, sekretów, destrukcyjnych operacji albo real external effects;
- Codex ma zrobić hard STOP;
- wymagana jest jawna zgoda ownera.

Dobre decyzje mają:

- rekomendację;
- wpływ rekomendacji;
- alternatywę;
- wpływ alternatywy;
- wybraną opcję;
- powód;
- wpływ późniejszego override.

## STOP Conditions

Codex ma się zatrzymać przed:

- produkcyjnym deployem albo zmianą infrastruktury produkcyjnej;
- destrukcyjną migracją DB albo bulk zmianą realnych danych;
- zmianami sekretów, credentiali, private keys, OAuth credentials albo production env;
- billingiem, pricingiem, płatnościami, KYC, compliance, tokenomics albo funds flow;
- legal/ToS-sensitive scrapingiem, privacy, consent, retention albo data rights;
- wyborem płatnego vendora z kosztem, lock-inem, limitem albo data-rights impact;
- realnymi mailami, alertami, ticketami, fakturami, płatnościami albo external API writes;
- force-push, usuwaniem branch/tag, release publishing albo destrukcyjnymi operacjami git/release;
- kontynuacją po retry limit;
- kontynuacją przy blocking drift;
- oznaczeniem `PASS` bez evidence.

Złożoność nie wystarcza do critical-risk. Critical-risk wymaga realnego ryzyka nieodwracalności, produkcji, prawa, finansów, bezpieczeństwa albo skutku zewnętrznego.

## Evidence-Backed PASS

`PASS` jest wiarygodny tylko wtedy, gdy ma evidence.

Evidence powinno mówić:

- co było testowane;
- jakie komendy uruchomiono;
- jaki był wynik komend;
- które artefakty lub ścieżki kodu sprawdzono;
- czego nie dało się sprawdzić;
- jaki jest residual risk;
- czy DoD jest spełnione w 100%.

Evidence zapisuj w:

```text
docs/ai-workflow/projects/<project>/quality/
```

Jeśli nie ma testów, dependency, sekretów albo usług, Codex ma:

- użyć fake/test path z evidence, jeśli to nie psuje poprawności;
- albo zatrzymać workflow, jeśli correctness zależy od brakującej rzeczy.

Nie akceptuj `PASS`, który opiera się tylko na deklaracji bez artefaktu.

## Recovery

Po przerwaniu, restarcie, kompakcji kontekstu albo rozjeździe statusów:

1. Odczytaj `docs/ai-workflow/projects/<project>/autopilot/autopilot-state.md`.
2. Odczytaj `docs/ai-workflow/projects/<project>/autopilot/autopilot-ledger.md`.
3. Odczytaj `docs/ai-workflow/repo/status.md`.
4. Odczytaj `docs/ai-workflow/projects/<project>/status.md`.
5. Sprawdź ostatnie quality evidence.
6. Sprawdź `git status`.
7. Wznów tylko od ostatniego evidence-backed `PASS`.

Jeśli state, ledger, status, artefakty i repo się nie zgadzają, Codex powinien utworzyć escalation artifact i zatrzymać się.

Nie pozwalaj autopilotowi "kontynuować z pamięci rozmowy", jeśli artefakty nie potwierdzają stanu.

## Git Policy

Bezpieczna polityka:

- pracuj na osobnej gałęzi dla większego/autonomicznego zakresu;
- commit po tasku tylko po `QUALITY PASS`;
- jeden commit powinien odpowiadać jednemu spójnemu zakończonemu zakresowi;
- push/PR tylko zgodnie z policy albo po zgodzie ownera;
- nie commituj stanu z FAIL jako gotowego;
- nie używaj `git reset --hard`, `git clean`, `git checkout --`, force-push albo usuwania branch/tag bez jawnej zgody.

Przed pushem człowiek powinien sprawdzić:

```bash
git status
git diff --stat
git diff --check
```

Jeśli worktree zawiera cudze lub historyczne zmiany, nie zakładaj, że Codex może je revertować. Ma pracować z nimi albo zatrzymać się przy konflikcie.

## Przenoszenie Flow Do Innego Repo

Minimalny zestaw do przeniesienia:

1. `AGENTS.md` - kontrakt dla agentów.
2. `HUMANS.md` - instrukcja dla ludzi.
3. `docs/ai-workflow/ai/workflow.md`.
4. `docs/ai-workflow/ai/workflow/`.
5. `docs/ai-workflow/ai/autopilot.md`.
6. `docs/ai-workflow/repo/` z `context.md`, `repo-intake.md`, `status.md`, `memory.md`.
7. `docs/ai-workflow/ai/templates/`.
8. `docs/ai-workflow/projects/<project>/` z canonical layoutem.
9. `docs/ai-workflow/humans/` na artefakty dla człowieka.

Przed pierwszym autopilotem w nowym repo trzeba ustalić:

- repo runtime layer: global context, install, test, lint, build, safe artisan/CLI commands;
- safe test environment;
- politykę migracji i rollbacku;
- politykę sekretów;
- politykę real external effects;
- git branch/commit/push policy;
- retry budget;
- final owner approval protocol.

Nie startuj autopilota w nowym repo bez intake, architektury, Architecture QA, planu, Plan QA, packaging decision, specs i Spec QA.

## Antywzorce

Unikaj:

- implementacji bez aktualnego statusu;
- implementacji z dependency-gated specem bez refresh/spec QA;
- traktowania warningów jako PASS;
- trzymania decyzji tylko w czacie;
- mieszania human docs z AI runtime artifacts;
- tworzenia duplikatów artefaktów zamiast reconciliation;
- ukrywania skipped tests;
- live API/credentials jako jedynej ścieżki QA;
- autopilota bez retry budget;
- final check bez owner final approval;
- pushowania bez przejrzenia statusu i diffu.

## Szybka Checklista Startu

Przed startem pracy:

- `AGENTS.md` istnieje i pozostaje template-owned.
- `HUMANS.md` opisuje, jak człowiek ma pracować z workflow.
- `docs/ai-workflow/repo/context.md` opisuje repo globalnie.
- `docs/ai-workflow/repo/status.md` wskazuje aktywny workspace.
- `docs/ai-workflow/projects/<project>/status.md` wskazuje task i następną fazę.
- Plan projektu ma PASS.
- Spec kolejnego taska ma PASS albo ma być odświeżony przed implementacją.
- Quality evidence istnieje dla ostatniego PASS.
- Decyzje high-impact i critical-risk są zamknięte albo jawnie zablokowane.
- Safe test environment jest znany.
- Real external effects są wyłączone albo jawnie zatwierdzone.
- Retry budget jest ustawiony.
- Git policy jest jasna.
- Wiesz, co ma zatrzymać autopilota.

Jeśli którykolwiek punkt jest niejasny, poproś Codexa o preflight/reconciliation zamiast startować implementację.
