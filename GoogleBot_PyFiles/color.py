def is_valid_hex(candidate):
    try:
        assert candidate.startswith("#")
        hex(int(candidate[1:], 16))
    except ValueError:
        return False

    except AssertionError:
        return False

    return True