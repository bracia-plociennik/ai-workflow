# 1. FAZA ARCHITEKTURY - ChatGPT

Ta faza służy do zamknięcia decyzji architektonicznych przed planowaniem tasków.

Celem nie jest opis systemu dla samego opisu.
Celem jest usunięcie niepewności, które później powodują błędy w planie projektu i rework w implementacji.

## Zasada ogólna

Architektura ma być proporcjonalna do skali zmiany.

- Dla małych zmian wystarczy lżejszy dokument architektoniczny obejmujący tylko ten fragment systemu, który realnie wpływa na taski.
- Dla większych zmian architektura powinna objąć pełny zakres systemu istotny dla planowania i implementacji.

## Kiedy uruchamiać tę fazę

Zanim poprosisz o podział na zadania.

Najpierw robisz analizę architektoniczną projektu lub zmiany.

## Opcjonalny audyt repo przed architekturą

ChatGPT powinien najpierw ocenić, czy warto wykonać audyt istniejącego repo i dokumentacji przed stworzeniem architektury.

Jeśli taki audyt może istotnie poprawić jakość architektury:

- ChatGPT powinien zapytać, czy chcesz wykonać audyt istniejącego repo.
- Brak audytu nie blokuje stworzenia architektury.
- Jeśli architektura powstaje bez audytu, ChatGPT musi to jasno zaznaczyć i wskazać ryzyko wynikające z braku weryfikacji istniejącego stanu.

## Cel fazy

AI ma zobaczyć system lub właściwy wycinek systemu, zanim zacznie dzielić pracę na taski.

Bez tego często powstają taski, które później trzeba zmieniać, scalać albo odwracać.

## **Minimalny zakres artefaktu docs/projects/<what_we_doing>/architecture/1_architecture_phase.md**

Dokument architektury powinien zawierać co najmniej:

- cele systemu lub zmiany
- granice systemu i out-of-scope
- komponenty i ich odpowiedzialności
- zależności między komponentami
- główne przepływy danych lub integracji
- decyzje architektoniczne podjęte
- decyzje architektoniczne do podjęcia
- ryzyka architektoniczne
- assumptions dopuszczone na tym etapie
- unknowns blocking
- unknowns non-blocking
- wpływ architektury na plan projektu

## **Reguła kompletności architektury**

Architektura jest wystarczająco kompletna, jeśli wiadomo co najmniej:

- jakie są granice systemu lub zmiany
- które komponenty są odpowiedzialne za które części rozwiązania
- jakie są kluczowe zależności i integracje
- gdzie znajduje się główna logika
- gdzie przebiega walidacja, jeśli ma znaczenie dla zadania
- jakie są główne constraints techniczne
- jakie ryzyka mogą wpłynąć na sequencing lub implementację
- które decyzje wymagają użytkownika
- które niewiadome są blocking, a które non-blocking

## **Klasyfikacja unknowns**

Każdy unknown musi zostać oznaczony jako:

- blocking
- non-blocking

### **Unknown blocking**

To unknown, który wpływa na:

- zakres tasków
- kolejność tasków
- sposób integracji
- sposób implementacji
- ryzyko istotnego reworku

Jeśli istnieje unknown blocking:

- nie przechodź do finalnego planu projektu
- najpierw domknij decyzję albo uzyskaj decyzję użytkownika

### **Unknown non-blocking**

To unknown, który nie blokuje planu projektu na obecnym etapie.

Może zostać przeniesiony dalej tylko wtedy, gdy ma:

- przypisanego ownera
- opis wpływu
- warunek lub moment domknięcia

## **Reguła dla ryzyk istotnych**

Każde istotne ryzyko architektoniczne musi mieć:

- decyzję
- albo ownera
- albo warunek domknięcia

Istotne ryzyko bez decyzji, ownera lub warunku domknięcia blokuje zakończenie tej fazy.

## **Architecture Gate przed planem projektu**

Nie przechodź do fazy planu projektu, jeśli:

- istnieją unknowns blocking
- istnieją istotne ryzyka bez decyzji, ownera lub warunku domknięcia
- sposób implementacji zależy od nierozstrzygniętej decyzji architektonicznej
- architektura jest zbyt ogólna, by podzielić pracę bez ryzyka reworku

## **Zakaz odkładania architektury na implementację**

Implementacja nie jest miejscem na rozstrzyganie architektury.

Jeśli sposób implementacji zależy od nierozstrzygniętej decyzji architektonicznej:

- nie przechodź dalej do planu lub implementacji
- najpierw zamknij decyzję albo uzyskaj decyzję użytkownika

## **Output kontrolny na końcu fazy**

Na końcu tej fazy ChatGPT powinien krótko wypisać:

- decyzje architektoniczne zamknięte
- decyzje architektoniczne otwarte
- unknowns blocking
- unknowns non-blocking
- istotne ryzyka i ich ownerów lub decyzje
- czy można przejść do planu projektu bez ryzyka reworku

## Prompt bazowy

Prompt powinien brzmieć mniej więcej tak:

```json
Przeanalizuj projekt jak architekt systemu.

Najpierw oceń, czy przed stworzeniem architektury warto wykonać audyt istniejącego repo lub docs.
Jeśli tak - zapytaj o zgodę na taki audyt.
Jeśli nie wykonujemy audytu, zaznacz wyraźnie, że architektura powstaje bez audytu istniejącego systemu.

Następnie przygotuj architekturę proporcjonalną do skali zmiany.

Wypisz:
- cele systemu lub zmiany
- granice systemu i out-of-scope
- komponenty i ich odpowiedzialności
- zależności między komponentami
- główne przepływy danych lub integracji
- decyzje architektoniczne już podjęte
- decyzje architektoniczne do podjęcia
- ryzyka architektoniczne
- unknowns z podziałem na:
  - blocking
  - non-blocking
- dla każdego istotnego ryzyka:
  - decyzję
  - albo ownera
  - albo warunek domknięcia
- wpływ architektury na późniejszy podział tasków

Na końcu podaj:
- 1 rekomendację architektoniczną
- 1 sensowną alternatywę
- informację, czy można przejść do planu projektu bez ryzyka reworku

DoD fazy:
powstał artefakt docs/projects/<what_we_doing>/architecture/1_architecture_phase.md
```

---
