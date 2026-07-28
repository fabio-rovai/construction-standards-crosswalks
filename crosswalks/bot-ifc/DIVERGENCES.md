# Where BOT and IFC4 genuinely disagree

The mapping rows carry the correspondences. This file carries the arguments
behind the refusals, because the refusals are where the information is.

## D1. `bot:Zone` is not `IfcZone`, and the same label flips two crosswalks

The single most instructive pair in this repository. In BOT, `Zone` is the
**spatial superclass**: `Site`, `Building`, `Storey` and `Space` are all kinds
of `bot:Zone`, and BOT makes the four siblings pairwise disjoint. In IFC4,
`IfcZone` is a **subclass of `IfcGroup`**: an arbitrary, non-spatial
aggregation of `IfcSpace` instances with no geometry, no containment semantics
and no place in the spatial structure tree.

Assert `bot:Zone = IfcZone` and every BOT site, building and storey becomes an
IFC group. Nothing in either schema will object: Uniclass-style classification
tools will not notice, SHACL on the mapping file will not notice, and IFC4's
own disjointness (11.45% falsifiability, concentrated between leaf siblings)
does not reach the pair. The refusal has to be made by a curator and recorded.

Two rows away, in `cobie-ifc`, the *same* IFC entity is the **correct** target:
COBie's `Zone` sheet and `IfcZone` are both non-spatial aggregations of spaces.
One label; one correct mapping and one canonical mis-mapping; the difference is
invisible to every lexical matcher ever built. This is the shortest available
argument that construction-standards alignment is a semantic problem, not a
string problem.

## D2. `IfcVirtualElement` breaks the physicality of `bot:Element`

`bot:Element` is defined as a constituent with a *characteristic technical
function, form or position* - the physical component reading. IFC4 files
`IfcVirtualElement` under `IfcElement`, and a virtual element is exactly the
thing that has none of those: it is an imaginary boundary used to split an
open-plan space where no wall exists.

So `bot:Element ⊇ IfcElement` fails on one member, and the honest rendering is
`closeMatch` plus an asserted non-mapping for the virtual case. Promote the
close match to `owl:equivalentClass` and every virtual boundary in every model
becomes a physical component; BOT's `Zone ⊥ Element` axiom then does reach it,
which makes this one of the few construction mis-mappings a reasoner *can*
catch - but only after the damage is asserted, and only because BOT put its
nine disjointness axioms at the top of the hierarchy where they propagate
(80.95% falsifiability from nine axioms, against IFC4's 11.45% from 2,443).
Axiom placement, not axiom count.

## D3. `bot:Interface` has no IFC4 home

`IfcRelSpaceBoundary` covers the space-to-element boundary and nothing else.
`bot:Interface` also qualifies element-element junctions (a thermal bridge
between two walls) and zone-zone adjacencies. IFC4 can *state* connectivity
(`IfcRelConnectsElements`) but cannot *qualify the junction itself* as a
first-class thing carrying transmittance or fire-rating properties. A
relationship assertion and a reified junction are different ontological
categories, which is why the tempting `Interface = IfcRelConnectsElements` row
is an asserted non-mapping.

## D4. IFC4 has no facility and no complex

`IfcFacility` arrives in IFC 4.3; IFC4 ADD2 tops out at `IfcBuilding`, and has
no entity at all for the campus/complex granularity that Uniclass gives a whole
table (`Co`). Crosswalks written against IFC4 must either stop at buildings or
lean on `IfcSite` composition conventions, and should say which they chose.
This repository says it: `Co_25_10_32` anchors to `IfcSite` at 0.6 confidence,
and the gap is recorded rather than papered over.
