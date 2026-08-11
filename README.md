# Construction standards crosswalks

[![Sponsor](https://img.shields.io/github/sponsors/fabio-rovai?label=Sponsor&logo=GitHub%20Sponsors&logoColor=EA4AAA&color=EA4AAA)](https://github.com/sponsors/fabio-rovai)

**Open, machine-readable crosswalks between the data standards a building
actually passes through - IFC, COBie, Uniclass 2015 and the W3C Building
Topology Ontology - and the measurement that shows why most construction data
mappings can never be machine-checked.**

Maintained by [Tesseract Academy](https://gov.tesseract.academy). Companion
repository to
[industrial-ontology-crosswalks](https://github.com/fabio-rovai/industrial-ontology-crosswalks),
using the same method and directly comparable metrics.

## At a glance

- **Three crosswalk pairs, 49 correspondences and 7 asserted non-mappings**:
  BOT to IFC4 ADD2, COBie 2.4 (BS 1192-4) to IFC4, and Uniclass 2015 to IFC4.
  All 96 distinct IRIs resolve against the pinned sources
  (`scripts/verify_iris.py`) and all three sets pass SHACL
  (`shapes/crosswalk-shapes.ttl`). Every Uniclass code was verified against the
  live NBS service before use; none are approximated.
- **The classification layer of construction is 0% falsifiable.** COBie and
  Uniclass assert no disjointness (they are spreadsheets and tables, not
  ontologies), so *no mis-mapping into them can ever be rejected by a
  reasoner*. Every AI tool that "maps your model to Uniclass" is operating in a
  regime where the machine cannot tell a right answer from a wrong one. The
  check has to live somewhere else - which is what these curated,
  SHACL-shaped, human-argued mapping files are.
- **BOT reaches 80.95% falsifiability from 9 disjointness axioms; IFC4 ADD2
  reaches 11.45% from 2,443.** Nine axioms at the top of a seven-class
  hierarchy propagate to 17 of 21 class pairs; IFC4's thousands sit between
  leaf siblings and reach almost nothing. Axiom placement beats axiom count,
  replicating the finding of the industrial repository on a second domain.
- **The same label flips verdicts two rows apart.** `bot:Zone = IfcZone` is the
  canonical false friend of linked building data (a spatial superclass against
  a non-spatial grouping), while `cobie:Zone = IfcZone` is exactly right. No
  lexical matcher can see the difference; the mapping files record both
  verdicts with the argument for each
  ([`crosswalks/bot-ifc/DIVERGENCES.md`](crosswalks/bot-ifc/DIVERGENCES.md)).
- **Part-whole errors are refused, not just omitted.** Uniclass
  `EF_20_10_30 Framed structures` to `IfcBeam` is asserted as a NON-mapping: a
  beam is part of a frame, not a kind of one, and since Uniclass carries no
  axioms, nothing but a curator will ever reject it.

Nothing here is redistributed from a standards body. Uniclass titles are
quoted for identification with per-code source URLs; COBie sheet names follow
BS 1192-4; BOT is CC BY (W3C LBD CG); ifcOWL is buildingSMART's rendering of
ISO 16739-1.

## Reproduce it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python lift/cobie_to_rdf.py         # COBie worksheet model -> OWL
.venv/bin/python lift/uniclass_to_rdf.py      # verified Uniclass codes -> SKOS/OWL
.venv/bin/python scripts/sssom_to_rdf.py      # SSSOM -> RDF + SHACL validation
.venv/bin/python scripts/verify_iris.py       # every crosswalk IRI must exist
.venv/bin/python metrics/falsifiability.py    # the falsifiability table
```

## What is here

| Path | What it is |
|---|---|
| [`crosswalks/bot-ifc/`](crosswalks/bot-ifc/) | The flagship. 8 correspondences and 3 asserted non-mappings between the W3C Building Topology Ontology and ifcOWL IFC4 ADD2, plus [`DIVERGENCES.md`](crosswalks/bot-ifc/DIVERGENCES.md), which is the part worth reading. |
| [`crosswalks/cobie-ifc/`](crosswalks/cobie-ifc/) | COBie 2.4 / BS 1192-4 worksheets to IFC4: 19 correspondences and 2 asserted non-mappings, following the documented handover mapping re-expressed against ifcOWL IRIs with per-row arguments. |
| [`crosswalks/uniclass-ifc/`](crosswalks/uniclass-ifc/) | Uniclass 2015 to IFC4: 22 correspondences and 2 asserted non-mappings across the EF/Ss/SL/En/Co strata, every code verified against uniclass.thenbs.com (April 2026 table versions). |
| [`lift/`](lift/) | The lifts that give COBie and Uniclass IRIs to map to, with the interpretation made explicit instead of implicit. |
| [`metrics/falsifiability.py`](metrics/falsifiability.py) | The falsifiability measurement and [`results.json`](metrics/results.json). |
| [`shapes/crosswalk-shapes.ttl`](shapes/crosswalk-shapes.ttl) | SHACL shapes: every correspondence must carry subject, object, a recognised predicate, justification, confidence and a substantive argument. |
| [`scripts/`](scripts/) | SSSOM to RDF conversion and the IRI existence check. |
| [`SOURCES.lock`](SOURCES.lock) | sha256 pins for every fetched source. |

## The falsifiability table

| Source | Classes | Declared disjoint pairs | Provably disjoint class pairs | Falsifiability |
|---|---:|---:|---:|---:|
| BOT | 7 | 9 | 17 / 21 | **80.95%** |
| IFC4 ADD2 | 1,286 | 2,443 | 94,626 / 826,255 | **11.45%** |
| COBie 2.4 (lifted) | 18 | 0 | 0 / 153 | **0.00%** |
| Uniclass 2015 (lifted) | 27 | 0 | 0 / 351 | **0.00%** |

Falsifiability = the fraction of unordered named-class pairs that provably
cannot share an instance (named subsumption closure over declared
disjointness). It is the ceiling on what any reasoner can ever reject. For the
two 0% rows that ceiling is the floor: correctness there is carried entirely
by curation, which is why every row in these mapping files carries an argument
and every refused mapping is recorded with one too.

## Why this exists

AI is arriving in construction as classifiers, extractors and copilots that
move data between exactly these standards. Where the target standard cannot
reject a wrong answer, "it validated" means nothing, and accuracy claims rest
entirely on the mapping tables the tool was built on. Those tables are usually
private, unargued and unversioned. These are public, argued row by row,
SHACL-checked, IRI-verified and pinned. Disagreement is welcome: file an issue
against the specific row and bring the counterexample.

## License

[CC BY 4.0](LICENSE). Cite via [`CITATION.cff`](CITATION.cff).

---

## Sponsor

If this work is useful to you, you can support its continued development through [GitHub Sponsors](https://github.com/sponsors/fabio-rovai).
