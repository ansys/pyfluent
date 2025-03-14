# Copyright (C) 2021 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Provides a module for Scheme Interpreter in Python."""

# flake8: noqa: E266

################ Scheme Interpreter in Python

## (c) Peter Norvig, 2010; See http://norvig.com/lispy2.html

################ Symbol, Procedure, classes

## This code is copied from
## https://github.com/norvig/pytudes/blob/main/py/lispy.py
## and modified as necessary


import io
import re
import sys


class Symbol(str):
    """Symbol."""

    pass


def Sym(s, symbol_table={}):
    """Find or create unique Symbol entry for str s in symbol table."""
    if s not in symbol_table:
        symbol_table[s] = Symbol(s)
    return symbol_table[s]


(
    _quote,
    _if,
    _set,
    _define,
    _lambda,
    _begin,
    _definemacro,
) = map(Sym, "quote   if   set!  define   lambda   begin   define-macro".split())

_quasiquote, _unquote, _unquotesplicing = map(
    Sym, "quasiquote   unquote   unquote-splicing".split()
)


class Procedure:
    """A user-defined Scheme procedure."""

    def __init__(self, params, exp, env):
        """Initialize Procedure."""
        self.params, self.exp, self.env = params, exp, env

    def __call__(self, *args):
        return eval(self.exp, Env(self.params, args, self.env))


################ parse, read, and user interaction


def parse(in_port):
    """Parse a program: read and expand/error-check it."""
    # Backwards compatibility: given a str, convert it to an InputPort
    if isinstance(in_port, str):
        in_port = InputPort(io.StringIO(in_port))
    return expand(read(in_port), toplevel=True)


eof_object = Symbol("#<eof-object>")  # Note: uninterned; can't be read


def count_unescaped_quotes(line):
    """Get count of unescaped quotes."""
    count = 0
    escaped = False
    for c in line:
        if c == "\\":
            escaped = True
        else:
            if c == '"' and not escaped:
                count += 1
            escaped = False
    return count


class InputPort:
    """An input port.

    Retains a line of chars.
    """

    tokenizer = r"""\s*(,@|[('`,)]|"(?:[\\].|[^\\"])*"|;.*|[^\s('"`,;)]*)(.*)"""

    def __init__(self, file):
        """Initialize InputPort."""
        self.file = file
        self.line = ""

    def next_token(self):
        """Return the next token, reading new text into line buffer if needed."""
        while True:
            if self.line == "":
                self.line = self.file.readline()
                # Capture multiline string and replace newline characters with
                # "<newline>" before passing to tokenizer
                if count_unescaped_quotes(self.line) % 2:
                    while True:
                        next_line = self.file.readline()
                        self.line = self.line.rstrip() + "<newline>" + next_line
                        if count_unescaped_quotes(next_line) > 0:
                            break
            if self.line == "":
                return eof_object
            token, self.line = re.match(InputPort.tokenizer, self.line).groups()
            if token != "" and not token.startswith(";"):
                # Replace back "<newline>" to newline character after tokenizing
                token = token.replace("<newline>", "\n")
                return token


def readchar(in_port):
    """Read the next character from an input port."""
    if in_port.line != "":
        ch, in_port.line = in_port.line[0], in_port.line[1:]
        return ch
    else:
        return in_port.file.read(1) or eof_object


def read(in_port):
    """Read a Scheme expression from an input port."""

    def read_ahead(token):
        if "(" == token:
            list_ = None
            to_tuple = False
            cons = None
            while True:
                token = in_port.next_token()
                if token == ")":
                    return (
                        (tuple(list_) if to_tuple else list_)
                        if list_
                        else (tuple(cons) if cons else ([]))
                    )
                if token == ".":
                    if list_:
                        cons = [list_.pop()]
                        if len(list_):
                            to_tuple = True
                        else:
                            list_ = None
                    else:
                        raise SyntaxError("unexpected .")
                else:
                    ahead = read_ahead(token)
                    if cons:
                        cons.append(ahead)
                        ahead = tuple(cons)
                        if list_:
                            cons = None
                    else:
                        list_ = list_ or []
                    if list_ is not None:
                        list_.append(ahead)
        elif ")" == token:
            raise SyntaxError("unexpected )")
        elif token in quotes:
            return [quotes[token], read(in_port)]
        elif token is eof_object:
            raise SyntaxError("unexpected EOF in list")
        else:
            return atom(token)

    # body of read:
    token1 = in_port.next_token()
    return eof_object if token1 is eof_object else read_ahead(token1)


quotes = {"'": _quote, "`": _quasiquote, ",": _unquote, ",@": _unquotesplicing}


def atom(token):
    """Numbers become numbers; #t and #f are booleans; "..." string; otherwise
    Symbol."""
    if token == "#t":
        return True
    elif token == "#f":
        return False
    elif token[0] == '"':
        return token
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            try:
                return complex(token.replace("i", "j", 1))
            except ValueError:
                return Sym(token)


def to_string(x):
    """Convert a Python object back into a Lisp-readable string."""

    def sequence(sep):
        return "(" + sep.join(map(to_string, x)) + ")"

    if x is True:
        return "#t"
    elif x is False:
        return "#f"
    elif isa(x, Symbol):
        return x
    elif isa(x, str):
        return x.replace("'", '"')
    elif isinstance(x, list):
        return sequence(" ")
    elif isinstance(x, tuple):
        return sequence(" . ")
    elif isa(x, complex):
        return str(x).replace("j", "i")
    else:
        return str(x)


def load(file_name):
    """Eval every expression from a file."""
    repl(None, InputPort(open(file_name)), None)


def repl(prompt="lispy> ", in_port=InputPort(sys.stdin), out=sys.stdout):
    """A prompt-read-eval-print loop."""
    sys.stderr.write("Lispy version 2.0\n")
    while True:
        try:
            if prompt:
                sys.stderr.write(prompt)
            x = parse(in_port)
            if x is eof_object:
                return
            val = eval(x)
            if val is not None and out:
                print(to_string(val), file=out)
        except Exception as e:
            print(f"{type(e).__name__}: {e}")


################ Environment class


class Env(dict):
    """An environment: a dict of {'var':val} pairs, with an outer Env."""

    def __init__(self, params=(), args=(), outer=None):
        """Initialize Env."""
        # Bind paarm list to corresponding args, or single param to list of args
        self.outer = outer
        if isa(params, Symbol):
            self.update({params: list(args)})
        else:
            if len(args) != len(params):
                raise TypeError(
                    f"expected {to_string(params)}, given {to_string(args)}"
                )
            self.update(zip(params, args))

    def find(self, var):
        """Find the innermost Env where var appears.

        Raises
        ------
        LookupError
            If a key or index used on a mapping or sequence is invalid.
        """
        if var in self:
            return self
        elif self.outer is None:
            raise LookupError(var)
        else:
            return self.outer.find(var)


def is_pair(x):
    """Check whether given value type is pair or not."""
    return x != [] and isa(x, list)


def cons(x, y):
    """Form a pair."""
    return [x] + y


def callcc(proc):
    """Call proc with current continuation; escape only.

    Raises
    ------
    RuntimeWarning
        If continuation can't be continued.
    """
    ball = RuntimeWarning("Sorry, can't continue this continuation any longer.")

    def throw(retval):
        ball.retval = retval
        raise ball

    try:
        return proc(throw)
    except RuntimeWarning as w:
        if w is ball:
            return ball.retval
        else:
            raise w


def add_globals(self):
    """Add some Scheme standard procedures."""
    import cmath
    import math
    import operator as op

    self.update(vars(math))
    self.update(vars(cmath))
    self.update(
        {
            "+": op.add,
            "-": op.sub,
            "*": op.mul,
            "/": op.truediv,
            "not": op.not_,
            ">": op.gt,
            "<": op.lt,
            ">=": op.ge,
            "<=": op.le,
            "=": op.eq,
            "equal?": op.eq,
            "eq?": op.is_,
            "length": len,
            "cons": cons,
            "car": lambda x: x[0],
            "cdr": lambda x: x[1:],
            "append": op.add,
            "list": lambda *x: list(x),
            "list?": lambda x: isa(x, list),
            "null?": lambda x: x == [],
            "symbol?": lambda x: isa(x, Symbol),
            "boolean?": lambda x: isa(x, bool),
            "pair?": is_pair,
            "port?": lambda x: isa(x, file),
            "apply": lambda proc, l: proc(*l),
            "eval": lambda x: eval(expand(x)),
            "load": lambda fn: load(fn),
            "call/cc": callcc,
            "open-input-file": open,
            "close-input-port": lambda p: p.file.close(),
            "open-output-file": lambda f: open(f, "w"),
            "close-output-port": lambda p: p.close(),
            "eof-object?": lambda x: x is eof_object,
            "read-char": readchar,
            "read": read,
            "write": lambda x, port=sys.stdout: port.write(to_string(x)),
            "display": lambda x, port=sys.stdout: port.write(
                x if isa(x, str) else to_string(x)
            ),
        }
    )
    return self


isa = isinstance

global_env = add_globals(Env())

################ eval (tail recursive)


def eval(x, env=global_env):
    """Evaluate an expression in an environment."""
    while True:
        if isa(x, Symbol):  # variable reference
            return env.find(x)[x]
        elif not isa(x, list):  # constant literal
            return x
        elif x[0] is _quote:  # (quote exp)
            (_, exp) = x
            return exp
        elif x[0] is _if:  # (if test conseq alt)
            (_, test, conseq, alt) = x
            x = conseq if eval(test, env) else alt
        elif x[0] is _set:  # (set! var exp)
            (_, var, exp) = x
            env.find(var)[var] = eval(exp, env)
            return None
        elif x[0] is _define:  # (define var exp)
            if len(x) == 3:
                (_, var, exp) = x
                env[var] = eval(exp, env)
            else:
                env[x[1]] = None
            return None
        elif x[0] is _lambda:  # (lambda (var*) exp)
            (_, vars, exp) = x
            return Procedure(vars, exp, env)
        elif x[0] is _begin:  # (begin exp+)
            for exp in x[1:-1]:
                eval(exp, env)
            x = x[-1]
        else:  # (proc exp*)
            exps = [eval(exp, env) for exp in x]
            proc = exps.pop(0)
            if isa(proc, Procedure):
                x = proc.exp
                env = Env(proc.params, exps, proc.env)
            else:
                return proc(*exps)


################ expand


def expand(x, toplevel=False):
    """Walk tree of x, making optimizations/fixes, and signaling SyntaxError."""
    # require(x, x!=[])                    # () => Error
    if x == []:
        return x
    if not isa(x, list):  # constant => unchanged
        return x
    elif x[0] is _quote:  # (quote exp)
        require(x, len(x) == 2)
        return x
    elif x[0] is _if:
        if len(x) == 3:
            x = x + [None]  # (if t c) => (if t c None)
        require(x, len(x) == 4)
        return list(map(expand, x))
    elif x[0] is _set:
        require(x, len(x) == 3)
        var = x[1]  # (set! non-var exp) => Error
        require(x, isa(var, Symbol), "can set! only a symbol")
        return [_set, var, expand(x[2])]
    elif x[0] is _define or x[0] is _definemacro:
        require(x, len(x) >= 2)
        _def, v, body = x[0], x[1], x[2:]
        if isa(v, list) and v:  # (define (f args) body)
            f, args = v[0], v[1:]  #  => (define f (lambda (args) body))
            return expand([_def, f, [_lambda, args] + body])
        else:
            require(x, len(x) in (2, 3))  # (define non-var/list exp) => Error
            if not isa(v, Symbol):
                return []
            exp = expand(x[2]) if len(x) == 3 else None
            if _def is _definemacro:
                require(x, toplevel, "define-macro only allowed at top level")
                proc = eval(exp)
                require(x, callable(proc), "macro must be a procedure")
                macro_table[v] = proc  # (define-macro v proc)
                return None  #  => None; add v:proc to macro_table
            return [_define, v, exp]
    elif x[0] is _begin:
        if len(x) == 1:
            return None  # (begin) => None
        else:
            return [expand(xi, toplevel) for xi in x]
    elif x[0] is _lambda:  # (lambda (x) e1 e2)
        require(x, len(x) >= 3)  #  => (lambda (x) (begin e1 e2))
        # variables was vars in oss lispy but that shadows a builtin
        variables, body = x[1], x[2:]
        require(
            x,
            (isa(variables, list) and all(isa(v, Symbol) for v in variables))
            or isa(variables, Symbol),
            "illegal lambda argument list",
        )
        exp = body[0] if len(body) == 1 else [_begin] + body
        return [_lambda, variables, expand(exp)]
    elif x[0] is _quasiquote:  # `x => expand_quasiquote(x)
        require(x, len(x) == 2)
        return expand_quasiquote(x[1])
    elif isa(x[0], Symbol) and x[0] in macro_table:
        return expand(macro_table[x[0]](*x[1:]), toplevel)  # (m arg...)
    else:  #        => macroexpand if m isa macro
        return list(map(expand, x))  # (f arg...) => expand each


def require(x, predicate, msg="wrong length"):
    """Signal a syntax error if predicate is false.

    Raises
    ------
    SyntaxError
        If syntax is invalid.
    """
    if not predicate:
        raise SyntaxError(to_string(x) + ": " + msg)


_append, _cons, _let = map(Sym, "append cons let".split())


def expand_quasiquote(x):
    """Expand ```x`` => ``'x``; ```,x`` => ``x``; ```(,@x y)`` => ``(append x y)``."""
    if not is_pair(x):
        return [_quote, x]
    require(x, x[0] is not _unquotesplicing, "can't splice here")
    if x[0] is _unquote:
        require(x, len(x) == 2)
        return x[1]
    elif is_pair(x[0]) and x[0][0] is _unquotesplicing:
        require(x[0], len(x[0]) == 2)
        return [_append, x[0][1], expand_quasiquote(x[1:])]
    else:
        return [_cons, expand_quasiquote(x[0]), expand_quasiquote(x[1:])]


def let(*args):
    """Get variable values."""
    args = list(args)
    x = cons(_let, args)
    require(x, len(args) > 1)
    bindings, body = args[0], args[1:]
    require(
        x,
        all(isa(b, list) and len(b) == 2 and isa(b[0], Symbol) for b in bindings),
        "illegal binding list",
    )
    # variables was vars in oss lispy but that shadows a builtin
    variables, vals = zip(*bindings)
    return [[_lambda, list(variables)] + list(map(expand, body))] + list(
        map(expand, vals)
    )


macro_table = {_let: let}  ## More macros can go here

eval(
    parse(
        """(begin

(define-macro and (lambda args
   (if (null? args) #t
       (if (= (length args) 1) (car args)
           `(if ,(car args) (and ,@(cdr args)) #f)))))

;; More macros can also go here

)"""
    )
)

if __name__ == "__main__":
    repl()
