# Workflow Overview

# CEL PLIKU

Ten dokument definiuje pełny, deterministyczny workflow realizacji zadań w projekcie.

Cel:

- zapewnienie powtarzalności procesu
- eliminacja zgadywania i decyzji ad-hoc
- wymuszenie jakości przez QA i fix loop
- rozdzielenie faz: idea validation → context → intake → architektura → plan → packaging → spec → implementacja → QA → destylacja

Ten artefakt jest globalną częścią szczegółowej specyfikacji procesu.
`WORKFLOW.md` pozostaje głównym przewodnikiem i kieruje do tego pliku oraz do konkretnych plików faz.

`docs/repo/STATUS.md` jest artefaktem wykonawczym, który przechowuje aktualny stan workflow.
Nie definiuje reguł procesu, ale jest canonical source dla odpowiedzi na pytania:

- jaki task jest aktualnie aktywny,
- jaka jest aktualna faza,
- jaki jest wynik ostatniej fazy,
- jaka jest następna faza,
- czy praca jest workflow-governed czy side-task-only

## Placeholder katalogu roboczego docs

Ścieżki artefaktów w tym pliku używają formy `docs/projects/<what_we_doing>/...`.

`<what_we_doing>` jest placeholderem nazwy aktywnego katalogu roboczego dokumentacji.

W template nie wskazuje aktywnego projektu. W realnym repo powinien zostać ustawiony przez `docs/repo/STATUS.md`, np. `new_product`, `billing_cleanup`, `migration_2026` albo inny katalog projektowy.

Placeholder nie narzuca jednej trwałej nazwy katalogu.

## Zakres obowiązywania pełnego workflow

Pełny workflow z tego dokumentu jest obowiązkowy tylko dla zadań wynikających z aktywnego planu projektu lub planu tematycznego w `docs/projects/<what_we_doing>/...`.

To znaczy:

- jeśli dany katalog docs ma własny:
  - context
  - architekturę
  - plan projektu
  - oraz nadal ma otwarte taski
  wtedy pełny workflow jest obowiązkowy
- jeśli wszystkie taski z tego planu są zakończone i wykonano `8. FINAL CHECK`:
  - plan uznaje się za zamknięty
  - kolejne side taski nie są automatycznie objęte pełnym workflow
  - pełny workflow staje się opcjonalny i działa tylko na życzenie użytkownika
- pełny workflow wraca jako obowiązkowy dopiero wtedy, gdy:
  - powstanie nowy katalog docs z własnym contextem, architekturą i planem projektu
  - albo użytkownik jawnie zażąda pełnego workflow dla side taska

Dla side tasków po zamknięciu planu nadal obowiązują:

- repo-first execution
- stop conditions
- evidence-based quality

Ale nie trzeba wymuszać wszystkich faz z tego dokumentu, jeśli użytkownik tego nie chce i nie pracujemy już w aktywnym planie.

## Kontrakt `docs/repo/STATUS.md`

### Cel

`docs/repo/STATUS.md` ma dawać jeden repo-local, jawny status bieżącej pracy.

Ma eliminować zgadywanie:

- która faza jest aktualna,
- czy ostatnia faza zakończyła się `PASS` czy `FAIL`,
- czy następny krok to fix loop czy przejście dalej,
- czy aktualna praca jest jeszcze częścią aktywnego planu,
- czy jest już side taskiem po zamknięciu planu

### Minimalny zakres pliku

Plik musi zawierać co najmniej:

- `workflow_requirement`
  - `mandatory` albo `optional`
- `workflow_scope`
  - `plan_derived` albo `side_task`
- `active_docs_workspace`
- `active_plan_status`
- `current_task`
- `current_phase`
- `phase_result`
- `next_phase`
- `last_completed_phase`
- `blocking_reason`
- `updated_at`

### Reguła aktualizacji

Dla tasków objętych obowiązkowym workflow `docs/repo/STATUS.md` musi zostać zaktualizowany:

1. przy wejściu w nowy task lub tasks package
2. przy starcie fazy
3. po wyniku fazy:
   - `PASS`
   - `FAIL`
   - `completed`
   - `blocked`
4. przy wejściu w fix loop
5. po `8. FINAL CHECK`
6. przy przejściu z aktywnego planu do side-task mode

Dla side tasków po zamknięciu planu:

- plik nadal powinien wskazywać:
  - że workflow jest optional
  - że task jest side taskiem
- szczegółowe phase tracking jest opcjonalne, jeśli użytkownik nie zażąda pełnego workflow

### Reguła interpretacji

Jeśli `docs/repo/STATUS.md` jest niezsynchronizowany z rzeczywistym stanem pracy:

- należy to potraktować jako drift operacyjny
- przy taskach workflow-governed trzeba go poprawić przed dalszym przejściem przez fazy
- przy side taskach trzeba jawnie oznaczyć rozjazd zamiast zgadywać następny krok

# CODEX AUTOPILOT

Autopilot jest trybem wykonawczym dla zadań wynikających z zatwierdzonego planu projektu.

Autopilot może działać dopiero wtedy, gdy istnieją i przeszły wymagane bramki:

- repo-level context i workflow readiness w `docs/repo/CONTEXT.md` oraz `docs/repo/REPO-INTAKE.md`
- context albo jawnie wskazany materiał wejściowy
- `0_initial_audit.md`
- `1_architecture_phase.md`
- Architecture QA PASS
- `2_project_plan.md`
- Plan QA PASS
- wynik Task Packaging albo jawna decyzja solo execution

Autopilot nie zastępuje właściciela projektu w:

- architekturze
- decyzjach strategicznych
- decyzjach high-impact
- akcjach critical-risk / irreversible
- finalnym zatwierdzeniu projektu

Autopilot wykonuje fazy implementacyjne deterministycznie:

```text
SPEC refresh/create
-> SPEC QA
-> SPEC FIX LOOP, jeśli FAIL
-> IMPLEMENTATION
-> QUALITY
-> FIX LOOP, jeśli FAIL
-> DISTILLATION
-> CHECKPOINT co 3 zakończone taski i po ostatnim tasku
-> NEXT TASK
-> FINAL CHECK
-> AWAITING_OWNER_FINAL_YES
```

## Autopilot Modes

Autopilot ma tryby:

- `supervised`
  - Codex wykonuje workflow, ale raportuje częściej i może częściej zatrzymywać się na owner review.
- `semi_autonomous`
  - Codex wykonuje workflow i wysyła eventy tylko przy decyzjach, STOP, retry limitach albo final approval.
- `autonomous_execution`
  - Codex wykonuje pełną pętlę tasków zgodnie z tym dokumentem, dopóki nie wystąpi STOP, critical-risk, retry limit albo final owner approval.
- `critical_risk_actions_disabled`
  - nie jest trybem pracy, tylko stałą zasadą: critical-risk actions są zawsze zablokowane bez explicit owner approval.

Jeśli owner jawnie zatwierdzi autopilota bez wskazania innego trybu, domyślnym trybem jest `autonomous_execution`.

W zatwierdzonym trybie `autonomous_execution` obowiązują dodatkowe zasady:

- taski są wykonywane sekwencyjnie, chyba że Task Packaging jawnie dopuści package/równoległość;
- autopilot przechodzi dalej tylko po evidence-backed `PASS`;
- warning nie wystarcza do przejścia dalej, jeśli brakuje DoD, test evidence albo gate evidence;
- STOP jest obowiązkowy dla critical-risk, retry limit, blocking drift oraz braku required test/QA evidence;
- auto-resolvable decisions mogą być wybierane automatycznie po zapisaniu rekomendacji i decyzji;
- high-impact i critical-risk decisions wymagają owner protocol;
- real external side effects są domyślnie wyłączone i zastępowane fake/log/array/test adapters;
- final check nie zamyka planu bez stanu `AWAITING_OWNER_FINAL_YES`.

Jeśli tryb autopilota nie został jawnie zatwierdzony, obowiązuje normalny workflow interaktywny.

## Autopilot State Machine

Workflow działa jako automat stanów.

Każda faza jest stanem i ma:

- warunek wejścia
- warunek wyjścia
- możliwe przejście po `PASS`
- możliwe przejście po `FAIL`
- możliwe przejście po `STOP`

Minimalne przejścia:

```text
STATE: SPEC
- complete -> SPEC_QA
- blocking uncertainty -> STOP

STATE: SPEC_QA
- PASS -> IMPLEMENTATION
- FAIL -> SPEC_FIX_LOOP

STATE: SPEC_FIX_LOOP
- fixed -> SPEC_QA
- retry limit reached -> ESCALATION_STOP

STATE: IMPLEMENTATION
- complete -> QUALITY
- critical risk -> CRITICAL_RISK_STOP
- drift requiring plan/architecture change -> DRIFT_STOP

STATE: QUALITY
- PASS -> DISTILLATION
- FAIL -> FIX_LOOP

STATE: FIX_LOOP
- fixed -> QUALITY
- retry limit reached -> ESCALATION_STOP

STATE: DISTILLATION
- complete and checkpoint not due -> NEXT_TASK
- complete and checkpoint due -> CHECKPOINT

STATE: CHECKPOINT
- PASS/completed -> NEXT_TASK or FINAL_CHECK
- drift blocking -> DRIFT_STOP

STATE: FINAL_CHECK
- findings -> route to required fix phase
- no findings -> AWAITING_OWNER_FINAL_YES

STATE: AWAITING_OWNER_FINAL_YES
- owner approves -> FINAL_CHECK PASS / close plan
- owner rejects or requests changes -> route to required fix phase
```

Brak spełnionego warunku wejścia oznacza `STOP`, chyba że brak dotyczy istniejącego artefaktu możliwego do odświeżenia przez Artifact Reconciliation Protocol.

## Autopilot State Artifacts

Autopilot musi utrzymywać artefakty wykonawcze w aktywnym workspace:

- `docs/projects/<what_we_doing>/autopilot/AUTOPILOT_STATE.md`
- `docs/projects/<what_we_doing>/autopilot/AUTOPILOT_LEDGER.md`
- `docs/projects/<what_we_doing>/autopilot/AUTOPILOT_EVENTS.md`

Szablony bazowe są w:

- `docs/ai/templates/autopilot/`

`AUTOPILOT_STATE.md` przechowuje runtime state:

- autopilot mode
- current task
- current phase
- last stable PASS
- retry counters
- completed tasks
- completed distillations since last checkpoint
- last checkpoint
- blockers
- budget status
- next transition

`AUTOPILOT_LEDGER.md` jest append-only operational ledger:

- phase started
- phase completed
- result
- evidence
- decisions
- fix loops
- checkpoints
- drift
- STOP / escalation

`AUTOPILOT_EVENTS.md` przechowuje eventy wymagające uwagi ownera:

- high-impact decision
- critical-risk stop
- retry limit reached
- blocking drift
- recovery inconsistency
- final approval required

Artefakty autopilota są pamięcią workflow. Repo state pozostaje źródłem prawdy o rzeczywistym kodzie.

## Autopilot Preflight

Przed każdą fazą autopilot musi wykonać preflight:

1. Sprawdź `STATUS.md`.
2. Sprawdź `autopilot/AUTOPILOT_STATE.md`, jeśli autopilot jest aktywny.
3. Sprawdź, czy task albo package wynika z zatwierdzonego planu.
4. Sprawdź wymagane artefakty fazy.
5. Wykonaj Artifact Reconciliation dla istniejących artefaktów.
6. Sprawdź zależności taska.
7. Sprawdź dirty workspace i overlap write-set.
8. Sprawdź drift względem repo, architektury, planu, specyfikacji i wykonanych tasków.
9. Sprawdź critical-risk triggers.
10. Sprawdź retry counters.
11. Sprawdź execution budget.

Wynik preflight musi być jednym z:

- `continue`
- `refresh_artifact`
- `fix_loop`
- `stop_escalate`

## Decision Protocol

Jeśli w dowolnej fazie pojawia się wybór, Codex musi sklasyfikować decyzję.

Klasy decyzji:

- `auto-resolvable`
  - decyzja niskiego albo średniego ryzyka
  - zakres jest ograniczony
  - nie zmienia architektury, planu, kosztów, prawa, bezpieczeństwa ani trwałych kontraktów
  - Codex wybiera rekomendację, zapisuje decyzję i kontynuuje
- `high-impact`
  - decyzja wpływa na architekturę, scope, trwały model danych, vendor, koszty, kontrakty, API albo ryzyko biznesowe
  - Codex zapisuje rekomendację i alternatywę
  - workflow zatrzymuje się do decyzji ownera
- `critical-risk`
  - decyzja dotyczy akcji nieodwracalnej, produkcyjnej, prawnej, finansowej, bezpieczeństwa albo real external side effect
  - hard STOP
  - wymaga explicit owner approval
- `blocked-by-missing-facts`
  - Codex najpierw eksploruje repo i artefakty
  - jeśli fakt nadal jest nieznany i wpływa na poprawność, workflow zatrzymuje się

Każda decyzja musi zostać zapisana w artefakcie:

`docs/projects/<what_we_doing>/decisions/<phase_task_name>_decisions.md`

Minimalny zapis decyzji:

```yaml
decision_id: TASK-01-D001
phase: SPEC
classification: auto-resolvable
chosen: recommendation
recommendation: <recommended option>
recommendation_impact: <impact>
alternative: <alternative option>
alternative_impact: <impact>
why_chosen: <reason>
why_rejected: <reason>
can_user_override_later: yes/no
override_impact: <what must be redone if owner overrides>
```

Brak decyzji użytkownika nie oznacza STOP tylko dla `auto-resolvable` decisions.

Brak zastosowania Decision Protocol jest błędem systemowym autopilota.

## Critical Risk / Irreversible Action Protocol

Codex musi zatrzymać workflow i wymagać explicit owner approval przed akcją, która jest materialnie nieodwracalna, produkcyjna, prawna, finansowa, bezpieczeństwa albo ma real external side effect.

Critical-risk actions obejmują:

- usuwanie, nadpisywanie, anonimizowanie albo bulk-changing danych produkcyjnych lub danych użytkowników
- destrukcyjne migracje albo komendy DB bez sprawdzonej ścieżki rollbacku
- zmiany authentication, authorization, wallet ownership, KYC, compliance, payment, billing, pricing, token economics albo funds flow
- ujawnianie, rotowanie, usuwanie, przenoszenie albo zmianę obsługi sekretów, private keys, API keys, OAuth credentials lub produkcyjnych env vars
- deploy do produkcji albo zmiany produkcyjnej infrastruktury, DNS, domen, kolejek, cronów, workerów, storage, backupów lub monitoringu
- legal/ToS-sensitive data collection, scraping, privacy, consent, retention albo provider data rights
- wybór albo zmiana płatnego vendora, jeśli koszt, kontrakt, limity, lock-in albo prawa do danych materialnie wpływają na produkt
- modyfikacje smart contracts, deployment scripts, chain config, token economics, presale, pricing albo funds flow
- wysyłanie realnych maili, alertów, ticketów, invoice, payment albo external API writes do realnych użytkowników/klientów
- force-push na shared branch, usuwanie branch/tag, publikacja release albo inne destrukcyjne operacje git/release

Nie klasyfikuj decyzji jako critical-risk tylko dlatego, że jest złożona, ważna albo wymaga refactoru.

Critical-risk wymaga materialnej nieodwracalności, produkcyjnego wpływu, ekspozycji bezpieczeństwa, skutku prawnego/finansowego albo realnego external side effect.

Artefakt decyzji critical-risk musi zawierać:

```yaml
classification: critical-risk
status: awaiting_owner_approval
workflow_effect: STOP
recommendation: <recommended action>
recommendation_impact: <impact>
alternative: <alternative action>
alternative_impact: <impact>
why_cannot_auto_choose: <irreversible/security/legal/production/financial reason>
required_owner_response: explicit approval
```

## Artifact Reconciliation Protocol

Przed utworzeniem artefaktu fazy Codex musi sprawdzić, czy artefakt dla tego samego taska/package/fazy już istnieje.

Istniejący artefakt nie jest blockerem samym w sobie.

Codex klasyfikuje istniejący artefakt jako:

- `current`
  - zgodny z aktualnym repo, architekturą, planem, zależnościami i wykonanymi taskami
  - akcja: użyj i kontynuuj
- `incomplete`
  - brakuje wymaganych sekcji, decisions, tests, evidence, gates albo dependency status
  - akcja: uzupełnij tylko brakujące elementy
- `outdated`
  - był poprawny wcześniej, ale nie pasuje do aktualnego repo, wykonanych tasków, planu lub architektury
  - akcja: odśwież minimalnie, zapisz drift, kontynuuj
- `conflicting`
  - przeczy architekturze, planowi, wykonanej implementacji albo regułom workflow
  - akcja: fix loop, a jeśli konflikt wpływa na correctness/scope, STOP
- `duplicate`
  - istnieje więcej niż jeden artefakt dla tego samego taska/package/fazy
  - akcja: wybierz canonical, zapisz duplicate event, nie usuwaj bez owner approval

Dependency-gated specifications mogą istnieć przed ukończeniem zależności.

Gdy zależności danego taska zostaną ukończone, Codex musi przed implementacją wykonać:

```text
SPEC_REFRESH -> SPEC_QA -> IMPLEMENTATION
```

Dependency-gated spec nie może być użyty bezpośrednio jako implementation-ready.

## Drift Detection Protocol

Drift to rozjazd między repo state, architekturą, planem, specyfikacją, wykonaniem, artefaktami albo workflow status.

Typy driftu:

- `architecture`
- `plan`
- `spec`
- `implementation`
- `dependency`
- `artifact`
- `workflow-status`
- `memory/checkpoint`

Severity:

- `warning`
  - nie blokuje kontynuacji, ale musi zostać zapisany
- `blocking`
  - wpływa na correctness, scope, sequencing, safety albo Implementation Gate
  - STOP albo powrót do właściwej fazy/fix loop

Minimalny zapis driftu:

```yaml
detected_drift: <description>
drift_type: architecture|plan|spec|implementation|dependency|artifact|workflow-status|memory/checkpoint
severity: warning|blocking
evidence: <file/command/finding>
required_action: <continue/fix_loop/stop/update_plan/update_architecture>
```

Jeśli implementacja wymaga zmiany architektury albo planu projektu, Codex nie może rozstrzygać tego w implementacji.

## Recovery / Idempotency Protocol

Autopilot musi być idempotentny.

Ponowne uruchomienie tej samej fazy nie może:

- dublować artefaktów
- kasować istniejących artefaktów bez zgody
- zgadywać ostatniego stanu
- kontynuować z częściowo zakończonej fazy jako gdyby przeszła PASS

Po przerwaniu, kompakcji kontekstu albo restarcie Codex musi:

1. Odczytać `autopilot/AUTOPILOT_STATE.md`.
2. Odczytać `autopilot/AUTOPILOT_LEDGER.md`.
3. Sprawdzić `STATUS.md`.
4. Sprawdzić istnienie artefaktów ostatnich faz.
5. Sprawdzić `git status`.
6. Zweryfikować, czy ostatni stabilny `PASS` ma evidence.
7. Wznowić tylko od ostatniego stabilnego `PASS`.

Jeśli state, ledger, workflow status i repo są niespójne:

- zapisz escalation artifact w `docs/projects/<what_we_doing>/escalations/`
- STOP

## Workspace Mutation Protocol

Przed mutacją Codex musi sprawdzić dirty workspace.

Zasady:

- nie wolno używać `git reset --hard`, `git checkout --`, `git clean`, `stash` ani destrukcyjnych operacji bez explicit owner approval
- jeśli cudze zmiany dotykają plików, które Codex musi edytować, STOP albo zapisz high-impact decision
- jeśli cudze zmiany są unrelated, Codex może kontynuować, ale nie może ich revertować
- mutacje artefaktów workflow są dozwolone w fazach workflow, jeśli wynik fazy wymaga zapisu artefaktu/statusu
- w fazach analysis, architecture, planning i QA nie wolno zmieniać kodu produktu
- migracje muszą mieć rollback/safety notes w specyfikacji albo QA evidence, jeśli task dotyka persistent data model
- destructive DB/git/release operations są critical-risk

Commity:

- domyślnie autopilot nie musi commitować po każdym tasku
- jeśli tryb autopilota wymaga commitów, commit może powstać dopiero po `QUALITY PASS`
- checkpoint może wskazać rekomendowany commit boundary
- commit nie może ukrywać incomplete/failed quality

## Concurrency Protocol

Domyślnie:

```yaml
max_parallel_tasks: 1
parallel_implementation: disabled
```

Równoległość jest dozwolona tylko wtedy, gdy:

- Task Packaging utworzył package bez zależności wewnętrznych
- package przeszedł Packaging QA
- write-sety są rozdzielne
- taski nie współdzielą migracji, modeli ani krytycznych kontraktów
- nie ma wspólnych high-risk dependencies
- checkpoint i destylacja nie wykonują się równolegle z implementacją
- state/ledger wskazują jednoznaczny owner procesu

Jeśli warunki równoległości nie są spełnione, autopilot działa sekwencyjnie.

## Execution Budget

Autopilot musi mieć budżet wykonania.

Domyślne wartości, jeśli owner nie poda innych:

```yaml
max_runtime_minutes: 300
max_spec_retries_per_task: 2
max_quality_retries_per_task: 2
max_total_retries: 32
max_parallel_tasks: 1
stop_on_budget_exceeded: true
```

Po przekroczeniu budżetu:

- zapisz event
- zapisz escalation artifact w `docs/projects/<what_we_doing>/escalations/`
- STOP

## Retry / Escalation Protocol

Retry limit:

- Spec QA: maksymalnie 2 fix loopy na task/package
- Quality: maksymalnie 2 fix loopy na task/package
- ten sam test albo ten sam typ błędu po 2 fix loopach: STOP

Po retry limit Codex musi utworzyć escalation artifact w `docs/projects/<what_we_doing>/escalations/`:

```yaml
escalation_reason: <why autopilot cannot continue safely>
failed_phase: <phase>
failed_checks:
  - <check>
suspected_cause: <cause if known>
recommended_path: <recommended next step>
alternative_path: <alternative>
risk_if_ignored: <risk>
required_owner_action: <approval/revise spec/manual review/etc>
```

## Event System

Codex wysyła event do ownera tylko gdy:

- decyzja jest high-impact
- decyzja jest critical-risk
- retry limit został osiągnięty
- workflow nie może kontynuować
- `FAIL` powtórzył się co najmniej 2 razy
- brakuje sekretów, dostępów albo zewnętrznych uprawnień
- wykryto blocking drift
- final check czeka na owner final approval

W pozostałych przypadkach:

- Codex zapisuje decyzję/evidence w artefaktach
- wybiera rekomendację dla auto-resolvable decisions
- kontynuuje workflow

Brak eventu oznacza brak potrzeby ingerencji ownera.

## Evidence Protocol

Każdy `PASS` musi mieć evidence.

Minimalny standard evidence:

- wykonane komendy
- wynik komend
- co było testowane
- jaki warunek zaliczenia spełniono
- czego nie dało się sprawdzić
- residual risk
- link albo ścieżka do artefaktu QA/evidence

Brak evidence dla required quality oznacza `FAIL`.

Warning nie może przykryć:

- unmet DoD
- regresji
- błędu correctness
- braku testów
- braku required evidence

## Human Override Protocol

Owner może zmienić wcześniejszą decyzję.

Override musi zostać zapisany:

```yaml
owner_override: true
overrides_decision_id: <id>
previous_choice: <choice>
new_choice: <choice>
requires:
  - re-spec
  - re-QA
  - migration review
  - plan update
  - architecture update
impact: <impact>
```

Jeśli override wpływa na architekturę, plan, persistent data model, public API, provider albo legal/security/cost boundary:

- autopilot musi zatrzymać bieżącą implementację
- wrócić do właściwej fazy

## Final Owner Approval

`8. FINAL CHECK` nie może samodzielnie zamknąć projektu pełnym `PASS`.

Jeśli final check nie znajduje błędów:

- wynik techniczny: `AWAITING_OWNER_FINAL_YES`
- workflow czeka na jawne zatwierdzenie ownera

Dopiero po owner approval:

- final check może zostać oznaczony jako `PASS`
- aktywny plan może zostać zamknięty

Jeśli owner nie zatwierdzi finalnie:

- Codex zapisuje owner feedback
- wraca do właściwej fazy naprawczej

# PRAWIDŁOWY PRZEBIEG WORKFLOW

Ten przebieg dotyczy tylko zadań objętych obowiązkowym workflow zgodnie z sekcją powyżej.

Workflow jest sekwencyjny i bramkowany QA.

Każda faza:

- kończy się QA
- FAIL → fix loop
- PASS → przejście dalej

---

### 000. Idea Validation

- używana, gdy owner zaczyna od brain dumpu, pomysłu albo niezweryfikowanej inicjatywy
- wynik musi być zapisany jako:
  - `docs/projects/<what_we_doing>/intake/000_idea_validation.md`

Warunek przejścia dalej:

- idea ma wynik `accepted` albo `accepted_with_changes`
- brak blocking decisions uniemożliwiających stworzenie contextu

Następny krok:

→ utworzenie `docs/projects/<what_we_doing>/intake/0_context.md`

---

### 0 Context

- context opisuje zatwierdzony zakres projektu po walidacji pomysłu
- może zostać dostarczony bez fazy 000, jeśli owner już ma zaakceptowany kontekst

Następny krok:

→ 0. Repo Intake / Initial Audit

---

### 0. Repo Intake / Initial Audit

- audit wykonywany najczęściej w Codex (kod)
- wynik musi być zapisany jako artefakt:
  - `docs/repo/REPO-INTAKE.md` dla repo-level bootstrap/workflow readiness
  - `docs/projects/<what_we_doing>/intake/0_initial_audit.md` dla konkretnego projektu/contextu

Warunek przejścia dalej:

- audit zakończony
- artefakt istnieje

---

### 1. Architektura (Codex)

Wejście:

- artefakt initial audit

Proces:

- zaprojektowanie architektury rozwiązania

---

### 1.5. Architecture QA

- walidacja architektury

### Jeśli FAIL:

→ 1.7. Architecture Fix Loop

- poprawa architektury
- powrót do 1.5

### Jeśli PASS:

→ przejście do fazy 2

---

### 2. Plan projektu (Codex)

- rozbicie architektury na taski

---

### 2.5. Plan QA

### Jeśli FAIL:

→ 2.6. Plan Fix Loop

→ powrót do 2.5

### Jeśli PASS:

→ 2.7 Task Packaging

---

### 2.7. Task Packaging

- grupowanie tasków w pakiety

---

### 2.9. Packaging QA

### Jeśli FAIL:

→ 2.9.1 Package Fix Loop

→ powrót do 2.9

### Jeśli PASS:

→ faza 3

---

### 3. Specyfikacja

- wykonywana przez Codex

Rzeczywisty wynik fazy:

- operacyjny plan wykonania zadania albo paczki zadań

Artefakt fazy:

- `docs/projects/<what_we_doing>/specs/3_*_specification.md`

Domyślnie po spełnionym Implementation Gate:

→ faza 4

`3.5. Spec QA` jest warunkowa w pracy interaktywnej i obowiązkowa w autopilocie:

- uruchamiaj ją tylko na jawne życzenie użytkownika
- albo jeśli Codex wykryje blocker, konflikt lub istotną niepewność wymagającą walidacji przed implementacją
- albo jeśli spec był dependency-gated i został odświeżony po ukończeniu zależności
- zawsze przed implementacją w trybie autopilota

---

### 3.5. Spec QA

### Jeśli FAIL:

→ 3.7 Spec Fix Loop

→ powrót do 3.5

### Jeśli PASS:

→ faza 4

---

### 4. Implementacja

- realizacja specyfikacji (najczęściej Codex)

---

### 5. QA / Quality Check

### Jeśli FAIL:

→ 5.5 Fix Loop

→ powrót do QA

### Jeśli PASS:

→ destylacja

---

### 6. Destylacja

- zapis wiedzy
- artefakt markdown + commit message

---

### Checkpoint projektu

Co N zadań (np. co 3):

- checkpoint projektu
- podsumowanie postępu
- aktualizacja kontekstu

---

### 8. Final Check

Na końcu całego planu projektu:

- pełna walidacja systemu

Warunki:

- brak warningów
- brak niespójności

### Jeśli FAIL:

→ powrót do odpowiedniej fazy

### Jeśli brak błędów technicznych:

→ `AWAITING_OWNER_FINAL_YES`

### Jeśli owner zatwierdzi finalnie:

→ final check PASS i zamknięcie projektu
