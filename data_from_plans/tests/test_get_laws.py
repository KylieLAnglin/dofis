from data_from_plans import extract_laws


def test1_get_laws_basic():
    test_one_input = 'This is a law called 25.081 and it should be extracted.'
    test_one_expected_output = [25.081]
    test_one_actual_output = extract_laws.get_laws(test_one_input)
    assert test_one_expected_output == test_one_actual_output


def test2_get_one_law():
    test_one_input = 'This is a law called 25.081 25.081 and only one should be extracted.'
    test_one_expected_output = [25.081]
    test_one_actual_output = extract_laws.get_laws(test_one_input)
    print(test_one_expected_output)
    assert test_one_expected_output == test_one_actual_output


def test3_get_laws_more_complex():
    test_input = 'this law has a trailing char it\'s 25.081(c)'
    test_expected_output = [25.081]
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output


def test4_get_laws_with_trailing_letter():
    test_input = 'this law has a trailing char -- 25.081c'
    test_expected_output = [25.081]
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output


def test5_get_laws_with_trailing_colon():
    test_input = 'this law is called 25.082: end of test'
    test_expected_output = [25.082]
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output


def test6_get_laws_with_trailing_comma():
    test_input = 'it is 25.081, or .'
    test_expected_output = [25.081]
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output


def test7_get_long_number_law():
    test_input = 'it is 25.0812 and it is good'
    test_expected_output = [25.0812]
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output


def test8_get_no_law_short():
    test_input = 'it is 21.13 and it is bad'
    test_expected_output = []
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output


def test9_get_no_law_long():
    test_input = 'it is 2221.112 and it is bad'
    test_expected_output = []
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output


def test10_with_law_sign():
    test_input = '(EB LEGAL)(Ed. Code 25.0811)Âaa Currently Students may not begin school before the 4th Monday of August.'
    test_expected_output = [25.0811]
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output


def test11_with_close_paren():
    test_input = 'Code 25.112)(Ed. is a law'
    test_expected_output = [25.112]
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output


def test12_a_reg():
    test_input = '39.054 is not exemptable'
    test_expected_output = []
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output

def test13():
    test_input = '(Ed. Code 21.003(a)) 90 Percent Attendance Rule '
    test_expected_output = [21.003]
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output

def test14():
    test_input = '(Ed. Code 212.003(a)) 90 Percent Attendance Rule '
    test_expected_output = []
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output

def test15():
    test_input = '(Ed. Code 1.111(a)) 90 Percent Attendance Rule '
    test_expected_output = []
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output


def test15():
    test_input = 'TEC§21.003 A person may not be employed as a teacher,'
    test_expected_output = [21.003]
    test_actual_output = extract_laws.get_laws(test_input)
    assert test_actual_output == test_expected_output