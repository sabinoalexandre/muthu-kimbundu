# Linguistic resources

The application seed lexicon is stored in `data/dictionary.json`. It contains
single words and multiword expressions with source references on each entry.
The SQLite `dictionary` table is seeded from that file at startup without
inserting duplicates.

The initial entries were checked against the public Kimbundu archive, whose
historical lexicon is based on Assis Júnior and records editorial status and
page references. The app keeps these entries marked `unverified` pending review
by Kimbundu speakers; source attribution does not imply contemporary validation.

This directory can also host additional resources such as:

- Bilingual dictionaries.
- Linguistic corpora.
- Example sentences.
- Grammatical annotations.
- Academic references and datasets.

No linguistic resource is considered verified until it has been reviewed by
Kimbundu speakers or linguists. Entries contributed by the community remain
unverified until such a review takes place.
