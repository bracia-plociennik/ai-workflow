# 0. REPO INTAKE / INITIAL AUDIT - Codex

Ta faza jest obowiązkowym wejściem do pracy z repozytorium objętym pełnym workflow.

Celem nie jest implementacja. Celem jest ustalenie prawdziwego stanu repo, docsów, komend, ryzyk i brakujących decyzji, zanim powstanie architektura, plan albo autopilot.

Faza 0 ma dwa możliwe poziomy artefaktu:

- `docs/ai/REPO-INTAKE.md` - repo-level bootstrap/intake dla workflow i autopilota, także wtedy, gdy nie istnieje jeszcze żaden projekt.
- `docs/projects/<what_we_doing>/intake/0_initial_audit.md` - project/context-specific intake, gdy istnieje konkretny projekt, produkt, feature, context albo plan.

## Warunek wejścia

Fazę 0 można uruchomić, gdy:

- repo jest dostępne lokalnie;
- istnieje konkretna intencja pracy, projekt docs albo materiał wejściowy;
- użytkownik chce rozpocząć workflow, audyt albo przygotowanie repo pod workflow/autopilot.

`0_context.md` jest opcjonalny. Brak contextu nie blokuje fazy 0.

Brak aktywnego projektu nie blokuje repo-level intake. W takim przypadku artefaktem fazy jest `docs/ai/REPO-INTAKE.md`, a nie project-local `0_initial_audit.md`.

## Cel fazy

Codex ma:

- rozpoznać strukturę repo;
- rozpoznać stack, frameworki, entrypointy, testy, build i runtime;
- sprawdzić, czy repo ma aktualny kontrakt dla agentów i ludzi;
- ustalić canonical docs layout;
- znaleźć stare, zdublowane, przeniesione albo sprzeczne artefakty;
- wykryć high-risk areas i restricted zones;
- ustalić bezpieczne komendy walidacyjne;
- przygotować albo odświeżyć `docs/ai/REPO-INTAKE.md`, jeśli audyt dotyczy repo-level workflow/bootstrap;
- przygotować artefakt `docs/projects/<what_we_doing>/intake/0_initial_audit.md`, jeśli audyt dotyczy konkretnego projektu/contextu;
- wypisać decyzje ownera potrzebne przed kolejnymi fazami.

## Zakres fazy

Faza 0 obejmuje:

- strukturę repo i główne katalogi;
- stack technologiczny i dependency manifests;
- komendy install/test/lint/build/dev/scheduler;
- runtime i lokalne ograniczenia, bez zakładania narzędzi specyficznych dla repo;
- obecny stan docsów;
- `AGENTS.md` jako kontrakt wykonawczy;
- `HUMANS.md` jako instrukcję dla człowieka;
- `docs/ai/WORKFLOW.md`;
- `docs/ai/workflow/`;
- `docs/ai/AUTOPILOT.md`;
- `docs/ai/STATUS.md`;
- `docs/ai/REPO-INTAKE.md`;
- `docs/ai/EXTERNAL-MEMORY.md`;
- `docs/ai/templates/`;
- `docs/ai/REPO-MEMORY.md`;
- `docs/projects/<what_we_doing>/STATUS.md`, jeśli projekt już istnieje;
- `docs/projects/<what_we_doing>/PROJECT-MEMORY.md`, jeśli projekt już istnieje;
- `docs/human/` jako katalog artefaktów dla człowieka;
- istniejące intake/architecture/planning/specs/quality/decisions/escalations/distillations/checkpoints/autopilot dla aktywnego projektu;
- dirty git state i potencjalne konflikty write-set;
- politykę sekretów, migracji, real external effects, retry, checkpointów i git.

## Out-of-scope

Faza 0 nie obejmuje:

- implementacji produktu;
- refactoru repo;
- automatycznego tworzenia architektury;
- automatycznego tworzenia planu projektu;
- uruchamiania autopilota;
- zmian w kodzie produktu;
- wykonywania destructive commands;
- tworzenia lub rotowania sekretów;
- produkcyjnych migracji lub operacji na realnych danych.

## Priorytet źródeł

Jeśli źródła są sprzeczne:

1. repo state;
2. root `AGENTS.md`;
3. `docs/ai/WORKFLOW.md` i szczegółowe pliki `docs/ai/workflow/`;
4. `docs/ai/STATUS.md`;
5. `docs/projects/<what_we_doing>/STATUS.md`;
6. zatwierdzona architektura;
7. zatwierdzony plan;
8. specyfikacje tasków;
9. context i notatki pomocnicze.

Context pomaga zrozumieć intencję, ale nie nadpisuje repo ani zatwierdzonych artefaktów.

## Lokalizacja artefaktów

Repo-level intake, jeśli nie ma jeszcze projektu albo audyt dotyczy tylko gotowości workflow/autopilota:

```text
docs/ai/REPO-INTAKE.md
```

Context, jeśli istnieje:

```text
docs/projects/<what_we_doing>/intake/0_context.md
```

Project/context-specific initial audit:

```text
docs/projects/<what_we_doing>/intake/0_initial_audit.md
```

Jeśli aktywny workspace nie istnieje, faza 0 może zakończyć się na `docs/ai/REPO-INTAKE.md` i zaproponować utworzenie workspace'u, ale nie może go stworzyć bez zatwierdzenia użytkownika.

## Obowiązkowe sprawdzenia repo

Codex musi sprawdzić:

- język, framework, package manager i główne dependency manifests;
- entrypointy backend/frontend/CLI/scheduler;
- konfigurację testów;
- konfigurację lint/build/typecheck;
- migracje, modele danych i wysokiego ryzyka persistence zones;
- integracje zewnętrzne, mail, webhooks, queue, scheduler, storage;
- pliki środowiskowe i politykę sekretów bez czytania lub ujawniania wartości sekretów;
- wygenerowane/runtime/dependency dirs, których nie należy edytować;
- istniejące local instructions, np. nested `AGENTS.md`.

Wynik musi odróżniać fakty z repo od hipotez.

## Obowiązkowe sprawdzenia docs/workflow

Codex musi sprawdzić, czy istnieją i są użyteczne:

- `AGENTS.md`;
- `HUMANS.md`;
- `docs/ai/WORKFLOW.md`;
- `docs/ai/workflow/`;
- `docs/ai/AUTOPILOT.md`;
- `docs/ai/STATUS.md`;
- `docs/ai/REPO-INTAKE.md`;
- `docs/ai/EXTERNAL-MEMORY.md`;
- `docs/ai/REPO-MEMORY.md`;
- `docs/ai/templates/`;
- `docs/projects/README.md`;
- `docs/projects/<what_we_doing>/README.md`, jeśli projekt istnieje;
- `docs/projects/<what_we_doing>/STATUS.md`, jeśli projekt istnieje;
- `docs/projects/<what_we_doing>/PROJECT-MEMORY.md`, jeśli projekt istnieje;
- `docs/human/README.md`;
- `docs/human/<project>/`, jeśli istnieją project-local human docs.

Codex musi też wykryć:

- stare ścieżki po migracji docsów;
- duplikaty artefaktów;
- artefakty puste albo nieużyteczne;
- konflikty między repo-level i project-local status;
- brak quality evidence mimo statusu `PASS`;
- brak decision artifacts dla decyzji, które są w czacie lub statusie;
- dependency-gated specs, które nie mogą wejść bez refresh/spec QA.

## Szybka Checklista Startu

Audit ma odpowiedzieć, czy poniższe warunki są spełnione:

- `AGENTS.md` istnieje i jest dostosowany do repo.
- `HUMANS.md` istnieje i opisuje pracę człowieka z workflow.
- `docs/ai/REPO-INTAKE.md` istnieje i opisuje repo-level workflow/bootstrap readiness.
- `docs/ai/EXTERNAL-MEMORY.md` istnieje i jest rozdzielony od repo-specific memory.
- `docs/ai/STATUS.md` wskazuje aktywny workspace albo jasno mówi, że go nie ma.
- `docs/projects/<what_we_doing>/STATUS.md` istnieje, jeśli projekt jest aktywny.
- Canonical docs layout jest jasny.
- Plan projektu, jeśli istnieje, ma QA evidence.
- Spec kolejnego taska, jeśli istnieje, ma PASS albo wymaga refresh/spec QA.
- Quality evidence istnieje dla ostatniego deklarowanego PASS.
- Decyzje high-impact i critical-risk są zapisane albo jawnie brakujące.
- Safe test environment jest znany.
- Real external effects są wyłączone albo wymagają owner approval.
- Retry budget jest ustawiony albo wymaga decyzji ownera.
- Git branch/commit/push policy jest znana.
- Stop triggers są jasne.

Ta checklista ma trafić do `docs/ai/REPO-INTAKE.md` przy repo-level bootstrap intake albo do `0_initial_audit.md` przy project/context-specific intake.

## Repo Adaptation Layer

Audit musi ustalić albo oznaczyć jako brakujące:

- install commands;
- test commands;
- lint/format check commands;
- build commands;
- scheduler/queue commands;
- safe inspection commands;
- commands forbidden without owner approval;
- safe environment variables for testing;
- known local runtime caveats.

Nie wolno wpisywać do audit ani `AGENTS.md` komend, których nie da się wiarygodnie wyprowadzić z repo.

## Ryzyka I Restricted Zones

Audit musi wskazać:

- high-risk areas repo;
- restricted/generated/runtime directories;
- files that may contain secrets;
- external integrations;
- scheduler/cron/queue risks;
- DB/migration risks;
- billing/payment/legal/security risks, jeśli występują;
- real external side effects.

Jeśli obszar jest high-risk, mikro-task nie powinien być domyślnym trybem pracy.

## Context

Jeśli istnieje `0_context.md`, Codex musi:

1. sprawdzić, czy dotyczy bieżącego repo albo projektu;
2. wskazać, które informacje są użyteczne dla audytu;
3. wskazać informacje zignorowane;
4. oznaczyć konflikty z repo;
5. oznaczyć blocking unknowns;
6. dodać sekcję "Analiza kontekstowa" do audit artifact.

Jeśli context jest surowy, nie traktuj go jako zatwierdzonej decyzji.

## Artifact Reconciliation

Jeśli artefakty już istnieją, Codex nie tworzy duplikatu domyślnie.

Każdy istniejący artefakt należy sklasyfikować:

- `current`;
- `incomplete`;
- `outdated`;
- `conflicting`;
- `duplicate`.

Przy rename/move trzeba wskazać canonical path i stare ścieżki, których nie należy przywracać.

## Decyzje Ownera

Audit musi wypisać decyzje wymagane przed dalszym workflow.

Każda decyzja powinna mieć:

- klasę: `auto-resolvable`, `high-impact`, `critical-risk`, `blocked-by-missing-facts`;
- rekomendację;
- wpływ rekomendacji;
- alternatywę;
- wpływ alternatywy;
- czy blokuje następną fazę.

MUST decisions blokują dalszy workflow. NICE TO HAVE nie blokują, ale powinny być zapisane.

## Reguła STOP

Faza 0 kończy się STOP, jeśli:

- repo nie jest dostępne;
- brak faktów uniemożliwia poprawny audit;
- źródła są sprzeczne i konflikt wpływa na correctness następnych faz;
- brakuje `AGENTS.md`;
- nie da się ustalić canonical docs layoutu;
- status mówi `PASS`, ale nie istnieje wymagane evidence;
- dalsza praca wymaga critical-risk action.

## Reguła Zmian W Repo

Faza 0 jest fazą audytu.

Codex może:

- czytać repo;
- uruchamiać nie-mutujące komendy rozpoznawcze;
- przygotować artefakt audytu, jeśli użytkownik zatwierdził wykonanie fazy;
- zaproponować zmiany do `AGENTS.md`, `HUMANS.md`, workflow docs albo layoutu.

Codex nie może bez zgody:

- zmieniać kodu produktu;
- refactorować repo;
- zmieniać `AGENTS.md`;
- zmieniać `HUMANS.md`;
- tworzyć nowych project workspaces;
- usuwać duplikatów;
- uruchamiać migracji produkcyjnych;
- wykonywać real external effects.

## Minimalny Kontrakt Artefaktu

`docs/ai/REPO-INTAKE.md` musi zawierać repo-level bootstrap contract:

- metadata: repo, path, date, result, active project workspace if any;
- sources reviewed;
- required AI workflow files and their status;
- required workflow phase files and their status;
- canonical docs layout check;
- repo adaptation layer;
- safe environment;
- repo risk register;
- artifact reconciliation;
- readiness checklist;
- owner decisions required;
- gate decision;
- evidence.

`docs/projects/<what_we_doing>/intake/0_initial_audit.md` musi zawierać project/context-specific contract:

- metadata: data, repo, workspace, scope;
- sources reviewed;
- current repo state;
- stack/runtime summary;
- command map discovered;
- safe test environment;
- docs/workflow layout status;
- canonical artifact paths;
- existing operational artifacts;
- missing operational artifacts;
- empty/outdated/conflicting/duplicate artifacts;
- old paths not to revive;
- AGENTS.md adaptation findings;
- HUMANS.md findings;
- workflow docs findings;
- status files findings;
- memory files findings;
- external memory findings;
- human docs findings;
- high-risk areas;
- restricted zones;
- external integrations and side effects;
- DB/migration safety notes;
- git/branch/dirty workspace notes;
- context analysis, if context exists;
- quick start checklist results;
- MUST recommendations;
- NICE TO HAVE recommendations;
- owner decisions required;
- blocking unknowns;
- non-blocking unknowns;
- gate decision: PASS / BLOCKED.

## Gate Wyjścia

Faza 0 może przejść dalej tylko jeśli:

- właściwy audit artifact istnieje:
  - `docs/ai/REPO-INTAKE.md` dla repo-level bootstrap intake;
  - `docs/projects/<what_we_doing>/intake/0_initial_audit.md` dla project/context-specific intake;
- MUST recommendations są zaakceptowane, odrzucone albo świadomie odroczone przez ownera;
- nie ma blocking unknowns wpływających na architekturę;
- canonical docs layout jest jasny;
- status wskazuje następną fazę;
- wymagane decyzje ownera są zapisane.

Jeśli gate nie jest spełniony, następny krok to decyzje ownera albo fix przygotowania repo, nie architektura.

## Output Końcowy

Na końcu fazy Codex powinien podać krótko:

- czy audit powstał;
- gdzie jest artifact;
- najważniejsze MUST;
- najważniejsze NICE TO HAVE;
- decyzje ownera;
- blocking unknowns;
- czy można przejść dalej;
- jaka jest następna poprawna faza.

## Prompt Bazowy

```text
Przeprowadź 0. REPO INTAKE / INITIAL AUDIT.

Zbadaj repo, docs/workflow layout, AGENTS.md, HUMANS.md, statusy, memory, templates, human docs, komendy, safe test env, high-risk areas, restricted zones, external side effects, migrations, git state i istniejące artefakty projektu.

Jeśli istnieje context, użyj go pomocniczo i nie traktuj go jako source of truth.

Jeśli nie ma aktywnego projektu albo celem jest bootstrap workflow/autopilota, utwórz albo zaktualizuj:
docs/ai/REPO-INTAKE.md

Jeśli istnieje aktywny projekt/context, utwórz albo zaktualizuj:
docs/projects/<what_we_doing>/intake/0_initial_audit.md

Nie zmieniaj kodu produktu.
Nie wdrażaj zmian w AGENTS.md/HUMANS.md bez zgody.
Nie zgaduj komend, decyzji ani layoutu.

Na końcu podaj gate decision i następną poprawną fazę.
```
