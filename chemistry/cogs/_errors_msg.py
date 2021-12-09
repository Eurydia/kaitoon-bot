# -*- coding: utf-8 -*-
class KaitoonValueError(ValueError):
    pass


NO_SPACE_BETWEEB_ARGS_MSG = """\
Please leave one empty space between each argument.
Like this ⬇
```
]]command🧊"[<argument 1>]"🧊"[<argument 2>]"🧊"[<argument 3>]"
```
Where
`🧊`: one empty space.\
"""

UNCLOSED_ARGUMENT_MSG = """\
It seems like one of the argument was not properly closed.
Arguments should be open and closed with \" \" \" symbol.
Like this ⬇
```
]]command **"**[<argument 1>]**"** **"**[<argument 2>]**"** **"**[<argument 3>]**"**
```\
"""

NO_ARGUMENT_GIVEN_MSG = """\
No argument is given with your command call.\
"""

NO_ARROW_SEP_FOUND_MSG = """\
I'm unable to distinguish reactants and products.
Reactants and products should be seperated
with \" = \" symbol.
Like this ⬇
```
]]command "[<reactants>]🧊=🧊[<products>]"
```
Where
`🧊`: one empty space.\
"""

INCORRECT_MEDIAN_MSG = """\
Unknown argument for median.
The acceptable symbols for [<median>] are
🔹 \"a\" or \"acidic\" for acidic median, and
🔹 \"b\" or \"basic\" for basic median.\
"""

A_REACTION_COMPONENT_IS_EMPTY_MSG = """\
It seems like one of your input is unspecifed.
Please use \"[u]\" instead for unspecified input.
Like this ⬇
```
]]predict "[<reactants>]" "[u]"
```\
"""

UNSPECIFIED_NOT_ALLOWED_MSG = "Unspecified input is not allowed in this command."

REACTION_COMPONENTS_ARE_UNSPECIFIED_MSG = """\
It looks like the given reactants and products are unspecified.\
"""

# NOT_ENOUGH_ARGS_MSG = \
# """\
# It seems like you did not give me enough
# argument to work with.\
# """

# miss_req_args_msg = \
# """\
# One or more required arguments is missing from your command call.\
# """
