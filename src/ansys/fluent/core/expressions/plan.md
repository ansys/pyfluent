## Objective
We are interested in breaking up the expressions package into "framework" / "generic" and "fluent" sub-packages, reflecting that the user-facing builder class and the ast representation should be generic. The parser and registry modules are specialised for Fluent. The long-term aim is to reuse the generic framework to allow building of CFX expressions for PyCFX.
## Feasibility
This is very feasible. Looking at the code, the split is fairly clean already:
Generic (reusable):
-	Expr base + operator overloads, Kind, Literal, Quantity, UnaryOp, BinOp, Compare, KeywordArg, RawName — none of these touch Fluent semantics.
-	Param, Signature, _Registry mechanics in _registry.py — the machinery is generic; only the catalog contents are Fluent.
-	SlotAccessor base and the _GroupFacade/_SigInvoker wiring in builder.py are generic patterns.
Fluent-specific (needs a peer for CFX):
-	Variable (uses FluentExprNamingStrategy) → CFX needs its own naming.
-	LocationList (renders ['a','b']) → CFX doesn't use a list arg; it uses a @location postfix on the call (e.g. areaAve(Pressure)@inlet1).
-	Call rendering shape (Name(a,b) no spaces) → CFX uses lowerCamel and a location postfix.
-	The registry contents and the parser & discovery layers are wholly Fluent-shaped.
The most awkward divergence is the location model: Fluent takes a list argument, CFX takes a single location as a call postfix. That means a shared Call node isn't quite enough — CFX needs its own call node. Everything else (arithmetic composition, quantities, literals, registry mechanics, group-facade UX) can be reused.
## Approach for this first pass
Keep the AST/registry files untouched, and add a parallel cfx_builder.py under the same packagewhich:
-	Reuses the generic AST bits (Literal, Quantity, RawName, UnaryOp, BinOp, Compare, _coerce, Kind, Expr) and the Param type.
-	Adds two CFX-only AST nodes: CfxVariable (own naming map) and CfxCall (renders name(args)@location).
-	Adds a CfxSignature + tiny CFX_REGISTRY (subset of reductions + math to prove the pattern).
-	Ships CfxExpressionBuilder with the same discoverable UX (b.reductions.area_ave(...), b.math.sqrt(...), b.literal(...), etc.). No discovery yet — no CFX field_info analog available in-tree.

Later refactor (out of scope now, but flagged): pull Param/Signature/_Registry/SlotAccessor/_GroupFacade/_SigInvoker into a _framework.py module, and turn Fluent + CFX into thin backends that each provide a registry + AST node set.
## Notes / open questions for the follow-up refactor
-	__fluent_expr__ is misnamed once CFX starts using it; a rename to something like __cfd_expr__ or a plain render() visitor method is the obvious next step but you asked to defer.
-	_registry.Param.coerce still references coerce_location_list, which is Fluent-shaped. The CFX signature avoids that path by never using Kind.LOCATION_LIST, so it's fine — but once we extract a shared framework module, LocationList should move to the Fluent side.
-	Discovery is Fluent-only right now. A CFX Discovery (surface names, valid variables) would slot in the same way once we have a CFX session/settings analog.
-	Consider adding a parser for CFX later; not needed for the builder-emit path.
-	Once the pattern settles, the natural refactor is: expressions/framework/{ast.py, registry.py, slots.py, facade.py} + expressions/fluent/{builder.py, registry.py, parser.py, discovery.py} + expressions/cfx/{builder.py, registry.py}, plus a re-export shim at the current location.

