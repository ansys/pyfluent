a.b["b*"]
a.b["b*"].c
a.b["b*"].c.d
a.b["b*"].c.d()
a.b["b*"].c.d = val
a.b["b*"].c.d.cmd1
a.b["b*"].c.d.cmd1(arg1)
a.b["b*"].c.d.is_active
a.b["b*"].c.d.is_active()
a.b["b*"].c.d.set_state
a.b["b*"].c.d.set_state(val1)
a.b["b*"] = a.b["b*"]()
a.b["b*"].c = a.b["b*"].c()
a.b["b*"].c.d = a.b["b*"].c.d()


# alternatively
{b.object_name(): b.c.d() for b in a.b["b*"]}
for c in a.b["b*"].c:
    c.d = val
for d in a.b["b*"].c.d:
    d.cmd(arg1)
for d in a.b["b*"].c.d:
    print(d.is_active())
for d in a.b["b*"].c.d:
    d.set_state(val)
for d in a.b["b*"].c.d:
    user_fn(d)
for c in a.b["b*"].c:
    for e in c.d["d*"].e:
        e.set_state(val)