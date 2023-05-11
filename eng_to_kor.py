import itertools

INITIAL = 0x001
MEDIAL = 0x010
FINAL = 0x100
CHAR_LISTS = {
    INITIAL: list(
        map(
            chr,
            [
                0x3131,
                0x3132,
                0x3134,
                0x3137,
                0x3138,
                0x3139,
                0x3141,
                0x3142,
                0x3143,
                0x3145,
                0x3146,
                0x3147,
                0x3148,
                0x3149,
                0x314A,
                0x314B,
                0x314C,
                0x314D,
                0x314E,
            ],
        )
    ),
    MEDIAL: list(
        map(
            chr,
            [
                0x314F,
                0x3150,
                0x3151,
                0x3152,
                0x3153,
                0x3154,
                0x3155,
                0x3156,
                0x3157,
                0x3158,
                0x3159,
                0x315A,
                0x315B,
                0x315C,
                0x315D,
                0x315E,
                0x315F,
                0x3160,
                0x3161,
                0x3162,
                0x3163,
            ],
        )
    ),
    FINAL: list(
        map(
            chr,
            [
                0x3131,
                0x3132,
                0x3133,
                0x3134,
                0x3135,
                0x3136,
                0x3137,
                0x3139,
                0x313A,
                0x313B,
                0x313C,
                0x313D,
                0x313E,
                0x313F,
                0x3140,
                0x3141,
                0x3142,
                0x3144,
                0x3145,
                0x3146,
                0x3147,
                0x3148,
                0x314A,
                0x314B,
                0x314C,
                0x314D,
                0x314E,
            ],
        )
    ),
}
CHAR_INITIALS = CHAR_LISTS[INITIAL]
CHAR_MEDIALS = CHAR_LISTS[MEDIAL]
CHAR_FINALS = CHAR_LISTS[FINAL]
CHAR_SETS = {k: set(v) for k, v in CHAR_LISTS.items()}
CHARSET = set(itertools.chain(*CHAR_SETS.values()))
CHAR_INDICES = {k: {c: i for i, c in enumerate(v)} for k, v in CHAR_LISTS.items()}


def is_hangul_compat_jamo(c):
    return 0x3130 <= ord(c) <= 0x318F  # Hangul Compatibility Jamo


def is_supported_hangul(c):
    return is_hangul_syllable(c) or is_hangul_compat_jamo(c)


def is_hangul_syllable(c):
    return 0xAC00 <= ord(c) <= 0xD7A3  # Hangul Syllables


def check_hangul(c, jamo_only=False):
    if not ((jamo_only or is_hangul_compat_jamo(c)) or is_supported_hangul(c)):
        raise ValueError(
            f"'{c}' is not a supported hangul character. "
            f"'Hangul Syllables' (0xac00 ~ 0xd7a3) and "
            f"'Hangul Compatibility Jamos' (0x3130 ~ 0x318f) are "
            f"supported at the moment."
        )


def get_jamo_type(c):
    check_hangul(c)
    assert is_hangul_compat_jamo(c), f"not a jamo: {ord(c):x}"
    return sum(t for t, s in CHAR_SETS.items() if c in s)


def join_jamos_char(init, med, final=None):
    chars = (init, med, final)
    for c in filter(None, chars):
        check_hangul(c, jamo_only=True)

    idx = tuple(
        CHAR_INDICES[pos][c] if c is not None else c
        for pos, c in zip((INITIAL, MEDIAL, FINAL), chars)
    )
    init_idx, med_idx, final_idx = idx
    # final index must be shifted once as
    # final index with 0 points to syllables without final
    final_idx = 0 if final_idx is None else final_idx + 1
    return chr(0xAC00 + 28 * 21 * init_idx + 28 * med_idx + final_idx)


def join_jamos(s, ignore_err=True):
    last_t = 0
    queue = []
    new_string = ""

    def flush(n=0):
        new_queue = []
        while len(queue) > n:
            new_queue.append(queue.pop())
        if len(new_queue) == 1:
            if not ignore_err:
                raise ValueError(f"invalid jamo character: {new_queue[0]}")
            result = new_queue[0]
        elif len(new_queue) >= 2:
            try:
                result = join_jamos_char(*new_queue)
            except (ValueError, KeyError):
                # Invalid jamo combination
                if not ignore_err:
                    raise ValueError(f"invalid jamo characters: {new_queue}")
                result = "".join(new_queue)
        else:
            result = None
        return result

    for c in s:
        if c not in CHARSET:
            if queue:
                new_c = flush() + c
            else:
                new_c = c
            last_t = 0
        else:
            t = get_jamo_type(c)
            new_c = None
            if t & FINAL == FINAL:
                if not (last_t == MEDIAL):
                    new_c = flush()
            elif t == INITIAL:
                new_c = flush()
            elif t == MEDIAL:
                if last_t & INITIAL == INITIAL:
                    new_c = flush(1)
                else:
                    new_c = flush()
            last_t = t
            queue.insert(0, c)
        if new_c:
            new_string += new_c
    if queue:
        new_string += flush()
    return new_string


def eng_kor(abc):
    stack = ""
    middle = {
        "hk": "ㅘ",
        "ho": "ㅙ",
        "hl": "ㅚ",
        "nj": "ㅝ",
        "np": "ㅞ",
        "nl": "ㅟ",
        "ml": "ㅢ",
    }
    ja = {
        "r": "ㄱ",
        "R": "ㄲ",
        "s": "ㄴ",
        "e": "ㄷ",
        "E": "ㄸ",
        "f": "ㄹ",
        "a": "ㅁ",
        "q": "ㅂ",
        "Q": "ㅃ",
        "t": "ㅅ",
        "T": "ㅆ",
        "d": "ㅇ",
        "w": "ㅈ",
        "W": "ㅉ",
        "c": "ㅊ",
        "z": "ㅋ",
        "x": "ㅌ",
        "v": "ㅍ",
        "g": "ㅎ",
    }
    mo = {
        "k": "ㅏ",
        "o": "ㅐ",
        "i": "ㅑ",
        "O": "ㅒ",
        "j": "ㅓ",
        "p": "ㅔ",
        "u": "ㅕ",
        "P": "ㅖ",
        "h": "ㅗ",
        "y": "ㅛ",
        "n": "ㅜ",
        "b": "ㅠ",
        "m": "ㅡ",
        "l": "ㅣ",
    }
    final = {
        "rt": "ㄳ",
        "sw": "ㄵ",
        "sg": "ㄶ",
        "fr": "ㄺ",
        "fa": "ㄻ",
        "fq": "ㄼ",
        "ft": "ㄽ",
        "fx": "ㄾ",
        "fv": "ㄿ",
        "fg": "ㅀ",
        "qt": "ㅄ",
    }
    mid_key, fi_key, ja_key, mo_key = (
        list(middle.keys()),
        list(final.keys()),
        list(ja.keys()),
        list(mo.keys()),
    )
    for mid in mid_key:
        abc = abc.replace(mid, middle[mid])

    for f in fi_key:
        if (
            f in abc
            and (abc[abc.index(f) - 1] in mo_key)
            and (
                (abc.index(f) + 2 >= len(abc))
                or (abc[abc.index(f) + 2] == " ")
                or (abc[abc.index(f) + 2] in ja_key)
            )
        ):
            abc = abc.replace(f, final[f])

    for a in abc:
        if a in ja:
            stack += ja[a]
        elif a in mo:
            stack += mo[a]
        else:
            stack += a
    return stack


print(join_jamos(eng_kor(input())))
