

    # Reshape long to wide 
    df = certification[['teacher_id', 'district',
                    'cert_area', 'cert_subject',
                    'cert_grade_low', 'cert_grade_high']]
    df['idx'] = df.groupby('teacher_id').cumcount()
    certs = certification[['teacher_id','certified', 'vocational']].groupby('teacher_id').max()
    df = df.merge(certs, how = 'left', on = 'teacher_id')
    df['cert_area_idx'] = 'cert_area_' + df.idx.astype(str)
    df['cert_subject_idx'] = 'cert_subject_' + df.idx.astype(str)
    df['cert_grade_low_idx'] = 'cert_grade_low_' + df.idx.astype(str)
    df['cert_grade_high_idx'] = 'cert_grade_high_' + df.idx.astype(str)


    areas = df.pivot(index='teacher_id',columns='cert_area_idx', values='cert_area')
    subjects = df.pivot(index='teacher_id',columns='cert_subject_idx', values='cert_subject')
    low_grades = df.pivot(index='teacher_id',columns='cert_grade_low_idx', values='cert_grade_low')
    high_grades = df.pivot(index='teacher_id',columns='cert_grade_high_idx', values='cert_grade_high')

    teacher_cert_wide = pd.concat([areas, subjects, low_grades, high_grades], axis = 1)
    max_certs = len(list(teacher_cert.filter(regex = ("cert_area"))))
    variables = []
    for num in range(0, max_certs):
        string = '_' + str(num) + '$'
        variables = variables + list(areas.filter(regex = (string)))
        variables = variables + list(subjects.filter(regex = (string)))
        variables = variables + list(low_grades.filter(regex = (string)))
        variables = variables + list(high_grades.filter(regex = (string)))
    teacher_cert_wide = teacher_cert_wide[variables]

    teacher_cert = teacher_yesno.merge(teacher_cert_wide, left_index = True, right_index = True)