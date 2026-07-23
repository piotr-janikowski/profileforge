# Data Model - ProfileForge

## Raw profiles (Examples from Three Different Sources)

Each source sends data as JSON, but the values are inconsistent in terms of formatting, capitalization, and completeness.

### Source 1: Web Form

```json
{
  "name": "Michał Schabowy",
  "age": "46",
  "phone": "798.756.321",
  "comment": "Za darmo albo zwrot"
}
```

### Source 2: Partner API

```json
{
  "first_name": "Janusz",
  "last_name": "rolada",
  "age": "55",
  "email": "",
  "phone": "621564 432"
}
```

### Source 3: CSV Import

```json
{
  "full_name": "mateusz kluska",
  "nickname": "kluska",
  "age": "25 ",
  "email": " kluska@gmail",
  "phone": "+48 456 756 754",
  "comment": ""
}
```

## Canonical Profile (Normalized Data Model)

Regardless of the data source, every profile stored in the database follows the same schema:

```json
{
  "first_name": "Michał",
  "last_name": "Schabowy",
  "age": 46,
  "phone_number": "+48798756321",
  "email": null,
  "comment": "Za darmo albo zwrot",
  "source": "web_form",
  "created_at": "2026-07-23T10:00:00Z"
}
```

- `first_name`, `last_name` - always stored separately, even if the source provides a single `name` or `last_name` field.
- `phone_number` - always normalized to same format - E.164 (`+` followed by the country code, without spaces or dots).
- `email` - always lowercase with leading/trailing whitespace removed.
- `age` - always stored as an integer, never as a string.
- `source` - identifies where the record originated.
- `created_at` - timestamp indicating when the record was ingested into the system.
- `null` for every missing value.