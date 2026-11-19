# Linguistic resources

The application seed lexicon is stored in `data/dictionary.json`. It contains
single words and multiword expressions with source references on each entry.
Entries can link Portuguese, Kimbundu and Kikongo terms. The SQLite `dictionary`
table is seeded from that file at startup without inserting duplicates; older
databases gain the Kikongo column automatically.

The initial entries were checked against the public Kimbundu archive, whose
historical lexicon is based on Assis Júnior and records editorial status and
page references. The app keeps these entries marked `unverified` pending review
by Kimbundu speakers; source attribution does not imply contemporary validation.

The initial Kikongo equivalents were checked against the Kia Kongo Léxikongo
and its notes on noun classes and regional variation. These entries also remain
`unverified` pending review by Kikongo speakers. The spelling and vocabulary
may vary across Kikongo varieties.

The seed lexicon also includes Kikongo terms for the sun, earth, dog, pig,
mother, father, family, chair, car, dances, chief and nose. Their individual
source references are stored with each entry in `data/dictionary.json`.

This directory can also host additional resources such as:

- Bilingual dictionaries.
- Linguistic corpora.
- Example sentences.
- Grammatical annotations.
- Academic references and datasets.

No linguistic resource is considered verified until it has been reviewed by
Kimbundu or Kikongo speakers or linguists. Entries contributed by the community
remain unverified until such a review takes place.
