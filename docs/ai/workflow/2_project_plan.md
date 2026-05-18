# 2. FAZA PLANU PROJEKTU - Codex

Ta faza służy do stworzenia planu tasków, który nadaje się do realnego wykonania i minimalizuje ryzyko reworku.

Celem nie jest stworzenie backlogu opisowego.
Celem jest stworzenie sekwencji tasków, które po spełnieniu zależności da się wdrażać bez zgadywania, bez ukrytych zależności i bez doprecyzowywania w trakcie implementacji.

## Warunek wejścia do tej fazy

Do tej fazy przechodzimy dopiero po fazie architektury.

Nie twórz finalnego planu projektu, jeśli:

- istnieją unknowns blocking z fazy architektury
- istnieją istotne ryzyka bez decyzji, ownera lub warunku domknięcia
- sposób podziału tasków zależy od nierozstrzygniętej decyzji architektonicznej

## Zasada ogólna

Plan projektu ma:

- minimalizować ryzyko, nie tylko odzwierciedlać logiczną kolejność prac
- ujawniać zależności przed implementacją, a nie w jej trakcie
- rozbijać pracę na taski średniej wielkości, jednoznacznie wykonawcze
- preferować sequencing liniowy
- dopuszczać równoległość tylko wtedy, gdy jest jawnie bezpieczna

## **Minimalny kontrakt każdego taska**

Każdy task w planie projektu musi zawierać co najmniej:

- ID lub nazwę taska
- cel taska
- zakres taska
- out-of-scope
- Definition of Done
- zależności wejściowe
- typ ryzyka
- główne ryzyko taska
- warunek startu
- warunek zakończenia
- status gotowości:
  - ready
  - conditional
  - blocked
- informację, czy task wymaga decyzji użytkownika przed implementacją

## **Definicja taska niezdefiniowanego**

Task jest niezdefiniowany, jeśli brakuje któregokolwiek z poniższych:

- jasnego celu
- zakresu
- out-of-scope
- DoD
- zależności wejściowych
- typu ryzyka
- głównego ryzyka
- warunku startu
- warunku zakończenia
- statusu gotowości

Task niezdefiniowany:

- nie może wejść do finalnego planu projektu
- nie może przejść do specyfikacji zadania
- nie może zostać oznaczony jako gotowy do implementacji

## **Zasada rozmiaru taska**

Task powinien być średniej wielkości i jednoznacznie wykonawczy.

Zasada praktyczna:

- jeden task = jeden główny rezultat wdrożeniowy

Jeśli task zawiera:

- kilka niezależnych rezultatów
- kilka niezależnych decyzji
- kilka różnych obszarów zmian, które można sensownie rozdzielić

to należy go rozbić.

## **Zasada sequencingu**

Kolejność tasków ma preferować:

- wcześniejsze ujawnienie ryzyk integracyjnych
- wcześniejsze ujawnienie ryzyk architektonicznych
- wcześniejsze ujawnienie ryzyk danych i przepływów
- wcześniejsze zamknięcie niepewności, które mogą powodować rework
- odkładanie polish, refinements i nice-to-have na później

Nie układaj tasków wyłącznie według naturalnej kolejności domenowej, jeśli zwiększa to ryzyko późnego wykrycia problemów.

## **Zasada liniowości i równoległości**

Domyślnie preferuj sequencing liniowy.

Równoległość jest dozwolona tylko wtedy, gdy:

- taski nie mają wspólnych blocking dependencies
- taski nie współdzielą ryzykownej integracji
- taski nie wymagają tych samych decyzji architektonicznych lub biznesowych
- równoległość nie utrudni jakości, checkpointów ani destylacji

Jeśli te warunki nie są spełnione:

- nie oznaczaj tasków jako bezpiecznie równoległych

## **Klasyfikacja zależności**

Każda zależność powinna być oznaczona jako:

- blocking
- informational
- optional

### **Blocking dependency**

Task nie może ruszyć bez spełnienia tej zależności.

### **Informational dependency**

Znajomość wyniku poprawia jakość taska, ale nie blokuje startu.

### **Optional dependency**

Może poprawić wynik lub uprościć pracę, ale nie jest wymagana.

Ukryte zależności są niedozwolone.

Jeśli task w praktyce wymaga wcześniejszego wyniku lub decyzji, musi to być zapisane jawnie.

## **Status gotowości taska**

Każdy task musi mieć jeden z poniższych statusów:

### **Ready**

Task ma pełny kontrakt i może przejść do specyfikacji zadania po spełnieniu zależności.

### **Conditional**

Task istnieje w planie, ale wymaga decyzji użytkownika lub warunku, który jeszcze nie został spełniony.

Task conditional może zostać zaplanowany, ale nie może być traktowany jako gotowy do implementacji.

### **Blocked**

Task nie może przejść dalej z powodu:

- niespełnionej blocking dependency
- brakującego artefaktu
- nierozstrzygniętej decyzji architektonicznej
- brakujących danych wejściowych

## **Taski wymagające decyzji użytkownika**

Jeśli task wymaga decyzji użytkownika:

- musi być oznaczony jako conditional
- decyzja musi być jawnie wskazana
- nie wolno traktować taska jako ready

## **Spike / research task**

Spike lub research task jest dozwolony tylko wtedy, gdy redukuje realną niepewność.

Zasady:

- spike musi być osobnym taskiem
- spike nie może być ukryty w tasku implementacyjnym
- spike musi mieć własny cel, DoD i warunek zakończenia
- spike nie służy do odkładania zwykłej decyzji, którą można podjąć od razu

## **Scope control na etapie planu**

Każdy task musi zawierać out-of-scope.

Task nie może obejmować:

- refactorów niezwiązanych bezpośrednio z celem taska
- dodatkowych ulepszeń “przy okazji”
- rozszerzeń funkcjonalnych nieujętych w scope

Wyjątek:

- mały refactor niezbędny do wykonania taska może wejść do scope tylko wtedy, gdy jest wpisany jawnie do zakresu i DoD

## **Task Gate przed przejściem do specyfikacji zadania**

Task może przejść do Iteracji 3 tylko wtedy, gdy:

- ma pełny kontrakt
- nie jest taskiem niezdefiniowanym
- nie ma blocking unknowns
- jego blocking dependencies są znane
- nie wymaga nierozstrzygniętej decyzji architektonicznej
- wiadomo, jak ocenić jego DoD

Jeśli którykolwiek z tych warunków nie jest spełniony:

- task nie jest gotowy do specyfikacji ani implementacji

## **Output kontrolny na końcu fazy**

Na końcu tej fazy Codex powinien krótko wypisać:

- finalną kolejność tasków
- taski o najwyższym ryzyku
- zależności blocking
- taski conditional
- taski blocked
- taski spike, jeśli istnieją
- informację, czy plan pozwala przejść do specyfikacji tasków bez doprecyzowywania w trakcie implementacji

## Prompt bazowy

Prompt powinien brzmieć mniej więcej tak:

```json
Na podstawie architektury przygotuj plan projektu w postaci tasków implementacyjnych.

Celem planu jest:
- minimalizacja ryzyka
- ujawnienie zależności
- przygotowanie tasków gotowych do późniejszej specyfikacji i implementacji

Każdy task musi zawierać:
- ID lub nazwę taska
- cel taska
- zakres taska
- out-of-scope
- Definition of Done
- zależności wejściowe
- typ ryzyka
- główne ryzyko taska
- warunek startu
- warunek zakończenia
- informację, czy task wymaga decyzji użytkownika przed implementacją
- informację, czy task jest:
  - ready
  - conditional
  - blocked

Dodatkowo:
- ułóż taski w kolejności minimalizującej ryzyko, a nie tylko w kolejności logicznej
- preferuj sequencing liniowy
- oznacz równoległość tylko wtedy, gdy jest jawnie bezpieczna
- nie twórz tasków niezdefiniowanych
- nie mieszaj kilku niezależnych rezultatów w jednym tasku
- jeśli potrzebny jest spike lub research task, dodaj go jako osobny typ taska i tylko wtedy, gdy redukuje realną niepewność

Na końcu podaj:
- finalną kolejność tasków
- taski o najwyższym ryzyku
- zależności blocking
- taski conditional
- taski blocked
- informację, czy plan pozwala przejść do specyfikacji tasków bez doprecyzowywania w trakcie implementacji

DoD fazy:
powstał artefakt docs/projects/<what_we_doing>/planning/2_project_plan.md
```

---
