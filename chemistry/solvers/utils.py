SUPERSCRIPTIONS = {key:val for key, val in zip('0123456789-+', '⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺')}
SUBSCRIPTIONS = {key:val for key, val in zip('0123456789', '₀₁₂₃₄₅₆₇₈₉')}

SPECIAL_TO_NORMAL = {key:val for key, val in zip('₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺', '01234567890123456789-+')}
