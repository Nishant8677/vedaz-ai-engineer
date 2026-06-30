from checker.safety import check_regex_safety

def test_safety_regex_pass():
    is_safe, _ = check_regex_safety("You will find a good job soon.")
    assert is_safe == True

def test_safety_regex_fail_death():
    is_safe, _ = check_regex_safety("I predict your death will be soon.")
    assert is_safe == False

def test_safety_regex_fail_guarantee():
    is_safe, _ = check_regex_safety("This is 100% guaranteed to work.")
    assert is_safe == False
