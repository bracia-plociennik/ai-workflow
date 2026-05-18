# HUMANS.md

## Cel dokumentu

`HUMANS.md` to instrukcja dla człowieka pracującego z repozytorium, które używa naszego systemu docs, workflow i autopilota.

Ten dokument jest dla:

- ownera, który decyduje o zakresie, ryzyku i akceptacji;
- operatora, który pilnuje przebiegu pracy z Codexem;
- engineera, który chce zrozumieć źródła prawdy, bramki jakości, recovery i git policy.

`HUMANS.md` mówi, jak człowiek ma pracować z systemem. `AGENTS.md` mówi, jak agent ma wykonywać pracę.

## Model mentalny

System działa dobrze tylko wtedy, gdy rozdzielamy kilka warstw:

- **Repo state**: rzeczywisty kod, migracje, config, testy, pliki i aktualny stan gita.
- **Agent contract**: `AGENTS.md`, czyli zasady wykonawcze dla Codexa.
- **Workflow docs**: `docs/ai/workflow.md` i `docs/ai/workflow/`, czyli proces faz, bramek, QA i fix loopów.
- **Repo runtime docs**: `docs/repo/`, czyli globalny context repo, repo intake, status i repo memory.
- **Project docs**: `docs/projects/<project>/`, czyli aktywna przestrzeń projektu: intake, architektura, plan, specs, quality, decisions, distillations, checkpoints, autopilot.
- **Human docs**: `docs/humans/`, czyli artefakty pisane dla człowieka: runbooki, audyty, decyzje, podsumowania, zgody.

Najważniejsza zasada: **repo state jest prawdą o tym, co faktycznie istnieje, a docs są kontraktem i pamięcią procesu**. Jeśli dokumentacja mówi jedno, a repo pokazuje drugie, to jest drift i trzeba go rozwiązać przed dalszą implementacją.

## Źródła Prawdy

Kiedy nie wiesz, co wolno zrobić albo jaka faza jest aktualna, czytaj źródła w tej kolejności:

1. `AGENTS.md` - kontrakt wykonawczy dla agenta, stop conditions, quality rules i artifact boundaries.
2. `docs/ai/workflow.md` - główny router faz workflow.
3. `docs/ai/workflow/<phase>.md` - szczegółowa specyfikacja konkretnej fazy.
4. `docs/ai/workflow/overview.md` - globalny opis workflow, statusu, autopilota i recovery.
5. `docs/ai/autopilot.md` - checklist startu i warunki działania autopilota.
6. `docs/repo/context.md` - globalny opis repo.
7. `docs/repo/repo-intake.md` - repo-level bootstrap/intake, szczególnie przed utworzeniem pierwszego projektu.
8. `docs/ai/external-memory.md` - uniwersalna pamięć rekomendacji i ulepszeń workflow, nie repo-specific.
9. `docs/repo/status.md` - repo-level status bieżącej pracy.
10. `docs/projects/<project>/status.md` - project-local status bieżącej pracy.
11. `docs/projects/<project>/...` - artefakty projektu: plan, specyfikacje, evidence, decyzje, checkpointy, runtime.

Jeśli źródła są sprzeczne, nie proś Codexa o zgadywanie. Poproś o reconciliation albo escalation.

## Układ Dokumentów

Canonical project workspace:

```text
docs/projects/<project>/
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

`docs/repo/context.md` jest miejscem na globalny opis repo: czym jest repo, jaki ma stack, domenę, główne moduły, granice i lokalne zasady.

`docs/repo/repo-intake.md` jest repo-level artefaktem bootstrap. Używaj go, gdy workflow został dopiero dodany do repo albo zanim powstanie pierwszy `docs/projects/<project>/`.

`docs/ai/external-memory.md` jest miejscem na uniwersalne wnioski o naszym workflow: rekomendacje, antywzorce, zasady i pomysły do przeniesienia do template'u `ai-workflow`. Nie zapisuj tam faktów domenowych konkretnego repo.

`docs/humans/` nie jest miejscem na specs, QA evidence ani runtime. To miejsce na dokumenty dla ludzi.

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

- `docs/repo/status.md`;
- `docs/projects/<project>/status.md`.

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

- `docs/repo/status.md`;
- `docs/projects/<project>/status.md`;
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
docs/projects/<project>/autopilot/autopilot-state.md
docs/projects/<project>/autopilot/autopilot-ledger.md
docs/projects/<project>/autopilot/autopilot-events.md
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
- musi zapisać decyzję w `docs/projects/<project>/decisions/`;
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
docs/projects/<project>/quality/
```

Jeśli nie ma testów, dependency, sekretów albo usług, Codex ma:

- użyć fake/test path z evidence, jeśli to nie psuje poprawności;
- albo zatrzymać workflow, jeśli correctness zależy od brakującej rzeczy.

Nie akceptuj `PASS`, który opiera się tylko na deklaracji bez artefaktu.

## Recovery

Po przerwaniu, restarcie, kompakcji kontekstu albo rozjeździe statusów:

1. Odczytaj `docs/projects/<project>/autopilot/autopilot-state.md`.
2. Odczytaj `docs/projects/<project>/autopilot/autopilot-ledger.md`.
3. Odczytaj `docs/repo/status.md`.
4. Odczytaj `docs/projects/<project>/status.md`.
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
3. `docs/ai/workflow.md`.
4. `docs/ai/workflow/`.
5. `docs/ai/autopilot.md`.
6. `docs/repo/` z `context.md`, `repo-intake.md`, `status.md`, `memory.md`.
7. `docs/ai/templates/`.
8. `docs/projects/<project>/` z canonical layoutem.
9. `docs/humans/` na artefakty dla człowieka.

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
- `docs/repo/context.md` opisuje repo globalnie.
- `docs/repo/status.md` wskazuje aktywny workspace.
- `docs/projects/<project>/status.md` wskazuje task i następną fazę.
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
