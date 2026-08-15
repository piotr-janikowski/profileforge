# Entity Resolution - reguła dopasowania

## Kiedy uznajemy dwa profile za tę samą osobę

1. Dokładna zgodność znormalizowanego e-maila, **LUB**
2. Dokładna zgodność znormalizowanego numeru telefonu, **LUB**
3. Podobieństwo imienia i nazwiska (fuzzy match) **powyżej progu 90%**.

W przypadku fuzzy matchingu wybieramy profil z **najwyższym wynikiem podobieństwa**. Dopasowanie zostaje zaakceptowane tylko wtedy, gdy wynik wynosi co najmniej **90%**.

## Dlaczego taka kolejność

E-mail i numer telefonu są traktowane jako silniejsze identyfikatory niż imię i nazwisko.

Najpierw wykonywane jest dokładne dopasowanie po e-mailu, ponieważ prawidłowo znormalizowany adres e-mail zazwyczaj jednoznacznie identyfikuje osobę.

Jeżeli nie ma dopasowania po e-mailu, sprawdzany jest dokładnie znormalizowany numer telefonu. Jest on również silnym identyfikatorem, ale może być współdzielony, np. przez członków rodziny lub kilka osób korzystających z numeru firmowego.

Dopiero gdy nie znaleziono dopasowania po żadnym z tych identyfikatorów, stosowany jest fuzzy matching imienia i nazwiska. Imię i nazwisko są słabszym sygnałem, ponieważ różne osoby mogą mieć takie same dane, a dodatkowo mogą występować literówki, różne transliteracje lub odmiany zapisu.

## Znane ograniczenia

### False positive - błędne połączenie dwóch różnych osób

Dokładna zgodność e-maila lub numeru telefonu może spowodować błędne połączenie dwóch osób, jeżeli dany identyfikator jest współdzielony.

Przykłady:

- wspólny adres e-mail używany przez kilka osób,
- firmowy numer telefonu używany przez wielu pracowników,
- numer telefonu należący wcześniej do innej osoby.

W takim przypadku Entity Resolution uzna profile za tę samą osobę, mimo że faktycznie mogą należeć do różnych osób.

### False positive przy fuzzy matchingu

Dwie różne osoby mogą mieć bardzo podobne lub identyczne imię i nazwisko. Przy wyniku fuzzy matchingu ≥ 90% mogą zostać błędnie uznane za tę samą osobę.

Dlatego fuzzy matching jest stosowany dopiero po nieudanych próbach dokładnego dopasowania po e-mailu i telefonie.

### Brak weryfikacji aktualności danych

System nie określa, które źródło zawiera bardziej aktualne dane. W przypadku konfliktu wartości istniejących i przychodzących obecna reguła zawsze zachowuje wartość istniejącą w profilu.

## Reguła scalania (merge precedence)

Obowiązuje zasada:

> **Uzupełniamy braki, nie nadpisujemy istniejących danych.**

Dla każdego pola:

- `existing = None` + `incoming = wartość` → **uzupełniamy istniejące pole**,
- `existing = wartość` + `incoming = None` → **zostawiamy istniejącą wartość**,
- `existing = wartość` + `incoming = inna wartość` → **zostawiamy istniejącą wartość**,
- `existing = None` + `incoming = None` → **pozostawiamy `None`**.

Przykład:

```text
Existing:
email = "jan@example.com"
phone_number = None

Incoming:
email = "other@example.com"
phone_number = "123456789"

Result:
email = "jan@example.com"
phone_number = "123456789"
```

Nowy e-mail nie nadpisuje istniejącego e-maila, ponieważ obecna wersja systemu nie posiada dodatkowych informacji pozwalających określić, która wartość jest bardziej aktualna lub wiarygodna.

Jest to **świadome uproszczenie pierwszej wersji Entity Resolution**. W przyszłości reguła może zostać rozszerzona o wiarygodność źródła, datę aktualizacji, historię zmian lub inne sygnały jakości danych.
