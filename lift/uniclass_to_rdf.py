#!/usr/bin/env python3
"""
Lift the web-verified Uniclass 2015 codes to a minimal SKOS/OWL rendering so
they can be crosswalked by IRI.

Uniclass 2015 (NBS) is a classification, not an ontology: it publishes tables
of codes and titles, no IRIs and no axioms. This lift renders exactly the codes
this repository maps - nothing more - each carrying its official code
(skos:notation), its official title (rdfs:label), and the uniclass.thenbs.com
page that confirms it (rdfs:seeAlso). Codes were verified against the live
NBS service (sources/uniclass-verified.json, April 2026 table versions);
none are approximated. No axioms are invented: Uniclass asserts no
disjointness, so no mis-mapping into it can be reasoner-rejected, and that
fact is part of what this repository measures.

Run:  python lift/uniclass_to_rdf.py     (writes lift/out/uniclass-lifted.ttl)
"""
import json
import os

from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, "sources", "uniclass-verified.json")
OUT = os.path.join(HERE, "out", "uniclass-lifted.ttl")

UC = Namespace("https://w3id.org/tesseract/construction-crosswalks/uniclass-lifted#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")


def main() -> None:
    with open(SRC) as f:
        data = json.load(f)

    g = Graph()
    g.bind("uniclass", UC)
    g.bind("owl", OWL)
    g.bind("skos", SKOS)

    ont = URIRef(str(UC)[:-1])
    g.add((ont, RDF.type, OWL.Ontology))
    g.add((ont, RDFS.label, Literal("Uniclass 2015 codes used by these crosswalks, lifted")))
    g.add((ont, RDFS.comment, Literal(
        "Minimal SKOS/OWL rendering of the Uniclass 2015 codes referenced by the "
        "crosswalks in this repository, verified against uniclass.thenbs.com. "
        "Lifted by Tesseract Academy; not a product of NBS. Titles are NBS's; "
        "everything else is interpretation.")))

    tables = {t["code"]: t for t in data["tables"]}
    for t in data["tables"]:
        c = UC[t["code"]]
        g.add((c, RDF.type, OWL.Class))
        g.add((c, RDFS.label, Literal(t["title"])))
        g.add((c, SKOS.notation, Literal(t["code"])))
        g.add((c, RDFS.seeAlso, URIRef(t["source_url"])))

    for row in data["codes"]:
        c = UC[row["code"]]
        g.add((c, RDF.type, OWL.Class))
        g.add((c, RDFS.label, Literal(row["title"])))
        g.add((c, SKOS.notation, Literal(row["code"])))
        g.add((c, RDFS.seeAlso, URIRef(row["source_url"])))
        if row["table"] in tables:
            g.add((c, SKOS.broader, UC[row["table"]]))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    g.serialize(OUT, format="turtle")
    print(f"wrote {OUT}: {len(data['tables'])} tables + {len(data['codes'])} codes")


if __name__ == "__main__":
    main()
