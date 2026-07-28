#!/usr/bin/env python3
"""
Lift the COBie worksheet model (BS 1192-4:2014 / COBie 2.4) to a minimal OWL
rendering so its sheets can be crosswalked by IRI.

COBie is a spreadsheet exchange standard, not an ontology: it publishes no IRIs,
no classes and no axioms. Anything mapped "to COBie" is therefore mapped to an
interpretation. This lift makes that interpretation explicit, inspectable and
pinned, instead of leaving it implicit in prose: one owl:Class per data
worksheet, with the sheet's stated purpose as the definition. No further axioms
are invented - in particular no disjointness, because BS 1192-4 asserts none,
and inventing rigour a source does not have is exactly the failure this
repository measures.

Run:  python lift/cobie_to_rdf.py     (writes lift/out/cobie-lifted.ttl)
"""
import os

from rdflib import Graph, Literal, Namespace, RDF, RDFS, OWL, URIRef

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "cobie-lifted.ttl")

COBIE = Namespace("https://w3id.org/tesseract/construction-crosswalks/cobie-lifted#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")

# Worksheet -> definition, quoted or condensed from the BS 1192-4 sheet purposes.
SHEETS = {
    "Contact": "A person or organisation participating in the exchange, keyed by email address.",
    "Facility": "The facility being handed over: the project, site and building context for every other sheet.",
    "Floor": "A vertical level or sectioning of the facility, including roofs and external levels.",
    "Space": "A location within a floor to which components and functions are assigned.",
    "Zone": "A named aggregation of spaces sharing a function, such as a fire compartment or department.",
    "Type": "A specification of a kind of equipment or product, carrying warranty, spare and maintenance data.",
    "Component": "An individually named, managed occurrence of a Type installed in a space.",
    "System": "A named aggregation of components delivering a service, such as a heating circuit.",
    "Assembly": "An identified aggregation of types or components into a larger whole.",
    "Connection": "A logical connection between two components.",
    "Spare": "A spare part or consumable associated with a type.",
    "Resource": "A material, tool or training resource required by a job.",
    "Job": "A planned task - preventative maintenance, operation or safety procedure - on a type.",
    "Impact": "A recorded economic, environmental or social impact of the facility or its parts.",
    "Document": "A reference to an external document applying to a row of another sheet.",
    "Attribute": "A named value attached to a row of another sheet.",
    "Coordinate": "A point, line or box locating a floor, space or component.",
    "Issue": "A recorded issue, risk or clash concerning two rows of other sheets.",
}


def main() -> None:
    g = Graph()
    g.bind("cobie", COBIE)
    g.bind("owl", OWL)
    g.bind("skos", SKOS)

    ont = URIRef(str(COBIE)[:-1])
    g.add((ont, RDF.type, OWL.Ontology))
    g.add((ont, RDFS.label, Literal("COBie 2.4 / BS 1192-4 worksheet model, lifted")))
    g.add((ont, RDFS.comment, Literal(
        "One owl:Class per COBie data worksheet. Lifted by Tesseract Academy for "
        "crosswalk purposes; not a product of any standards body. COBie asserts "
        "no disjointness and none is invented here.")))

    for name, definition in SHEETS.items():
        c = COBIE[name]
        g.add((c, RDF.type, OWL.Class))
        g.add((c, RDFS.label, Literal(name)))
        g.add((c, SKOS.definition, Literal(definition)))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    g.serialize(OUT, format="turtle")
    print(f"wrote {OUT}: {len(SHEETS)} classes")


if __name__ == "__main__":
    main()
