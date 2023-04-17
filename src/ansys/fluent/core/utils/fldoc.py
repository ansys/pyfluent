import pprint
import pydoc
import sys


def docother(self, object, name=None, mod=None, parent=None, maxlen=None, doc=None):
    """Produce text documentation for a data object."""
    if isinstance(object, list):
        indent_len = len(name and name + " = " or "") + 1
        repr = pprint.pformat(object, width=maxlen, compact=True, indent=indent_len)
        repr = "[" + repr[1:].lstrip()
    else:
        repr = self.repr(object)
        if maxlen:
            line = (name and name + " = " or "") + repr
            chop = maxlen - len(line)
            if chop < 0:
                repr = repr[:chop] + "..."
    line = (name and self.bold(name) + " = " or "") + repr
    #  The source have been changed in 3.9, cpython commit id fbf2786c4c89430e2067016603078cf3500cfe94
    if sys.version_info < (3, 9):
        if doc is not None:
            line += "\n" + self.indent(str(doc))
    else:
        if not doc:
            doc = pydoc.getdoc(object)
        if doc:
            line += "\n" + self.indent(str(doc)) + "\n"
    return line
