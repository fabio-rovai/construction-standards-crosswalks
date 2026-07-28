#!/usr/bin/env python3
"""
Falsifiability rate: the fraction of unordered named-class pairs that provably
cannot share an instance.

A crosswalk into an ontology can only be *rejected* by a reasoner if the
ontology can contradict something. Disjointness is where that power lives, and
where it sits in the hierarchy decides how far it reaches: an axiom between two
top-level branches propagates to every pair of their descendants, an axiom
between two leaf siblings reaches only itself. Counting axioms therefore says
nothing; this script measures reach.

A pair (A, B) counts as provably disjoint iff some declared disjointness
(C, D) exists with A subsumed by C and B subsumed by D (named subsumption
closure only; no reasoner needed for this fragment). Pairs related by
subsumption are excluded from the denominator's disjoint-eligible reading only
in the report notes - the headline rate uses all unordered pairs of named,
non-deprecated classes, same as the companion industrial-ontology-crosswalks
repository, so the numbers are comparable across both.

Run:  python metrics/falsifiability.py            (all four sources)
      python metrics/falsifiability.py --write    (also write metrics/results.json)
"""
import itertools
import json
import os
import sys
from collections import defaultdict

from rdflib import Graph, OWL, RDF, RDFS, URIRef

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

SOURCES = [
    ("BOT", os.path.join(ROOT, "sources", "bot.ttl"), "https://w3id.org/bot#"),
    ("IFC4 ADD2", os.path.join(ROOT, "sources", "ifc4-add2.ttl"),
     "http://ifcowl.openbimstandards.org/IFC4_ADD2#"),
    ("COBie (lifted)", os.path.join(ROOT, "lift", "out", "cobie-lifted.ttl"),
     "https://w3id.org/tesseract/construction-crosswalks/cobie-lifted#"),
    ("Uniclass (lifted)", os.path.join(ROOT, "lift", "out", "uniclass-lifted.ttl"),
     "https://w3id.org/tesseract/construction-crosswalks/uniclass-lifted#"),
]


def measure(path: str, ns: str) -> dict:
    g = Graph()
    g.parse(path, format="turtle")

    classes = {c for c in g.subjects(RDF.type, OWL.Class)
               if isinstance(c, URIRef) and str(c).startswith(ns)}

    # ancestors via named rdfs:subClassOf closure (every class is its own ancestor)
    parents: dict[URIRef, set[URIRef]] = defaultdict(set)
    for s, o in g.subject_objects(RDFS.subClassOf):
        if isinstance(s, URIRef) and isinstance(o, URIRef) and s in classes and o in classes:
            parents[s].add(o)

    ancestors: dict[URIRef, frozenset[URIRef]] = {}

    def anc(c: URIRef, seen: frozenset = frozenset()) -> frozenset:
        if c in ancestors:
            return ancestors[c]
        out = {c}
        for p in parents.get(c, ()):
            if p not in seen:
                out |= anc(p, seen | {c})
        ancestors[c] = frozenset(out)
        return ancestors[c]

    for c in classes:
        anc(c)

    # declared disjointness, as distinct unordered pairs (owl:disjointWith is
    # symmetric and some serialisations state both directions)
    declared = set()
    for s, o in g.subject_objects(OWL.disjointWith):
        if isinstance(s, URIRef) and isinstance(o, URIRef) and s in classes and o in classes:
            declared.add(frozenset((s, o)))
    for adl in g.subjects(RDF.type, OWL.AllDisjointClasses):
        members = []
        for lst in g.objects(adl, OWL.members):
            node = lst
            while node and node != RDF.nil:
                first = g.value(node, RDF.first)
                if isinstance(first, URIRef) and first in classes:
                    members.append(first)
                node = g.value(node, RDF.rest)
        for a, b in itertools.combinations(members, 2):
            declared.add(frozenset((a, b)))

    # a pair is provably disjoint iff its ancestor sets meet a declared pair crosswise
    disjoint_pairs = 0
    total_pairs = 0
    ordered = sorted(classes)
    declared_list = [tuple(p) for p in declared]
    for i, a in enumerate(ordered):
        aa = ancestors[a]
        for b in ordered[i + 1:]:
            total_pairs += 1
            bb = ancestors[b]
            for c, d in declared_list:
                if (c in aa and d in bb) or (d in aa and c in bb):
                    disjoint_pairs += 1
                    break

    rate = (100.0 * disjoint_pairs / total_pairs) if total_pairs else 0.0
    return {
        "classes": len(classes),
        "declared_disjoint_pairs": len(declared),
        "unordered_class_pairs": total_pairs,
        "provably_disjoint_pairs": disjoint_pairs,
        "falsifiability_rate_pct": round(rate, 2),
    }


def main() -> None:
    results = {}
    print(f"{'source':<20}{'classes':>9}{'declared':>10}{'pairs':>12}{'disjoint':>10}{'rate':>9}")
    for name, path, ns in SOURCES:
        if not os.path.exists(path):
            print(f"{name:<20}  (missing - run the lifts first)")
            continue
        r = measure(path, ns)
        results[name] = r
        print(f"{name:<20}{r['classes']:>9}{r['declared_disjoint_pairs']:>10}"
              f"{r['unordered_class_pairs']:>12}{r['provably_disjoint_pairs']:>10}"
              f"{r['falsifiability_rate_pct']:>8.2f}%")
    if "--write" in sys.argv:
        out = os.path.join(HERE, "results.json")
        with open(out, "w") as f:
            json.dump(results, f, indent=2)
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
