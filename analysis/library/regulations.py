main = ['reg25_0811', 'reg25_081', 'reg25_0812', 'reg25_082',
        'reg25_112', 'reg25_113', 'reg25_111',
        'reg21_003', 'reg21_053', 'reg21_057',
        'reg21_102', 'reg21_401', 'reg21_352', 'reg21_354',
        'reg25_092', 'reg37_0012', 'reg25_036']

mainless = ['reg25_0811', 'reg25_081', 'reg25_0812', 'reg25_082',
        'reg25_112', 'reg25_111',
        'reg21_003',
        'reg21_102', 'reg21_401', 'reg21_352', 'reg21_354',
        'reg25_092', 'reg37_0012', 'reg25_036']

mainplus = ['reg25_0811', 'reg25_081', 'reg25_0812', 'reg25_082', 'reg25_112', 'reg25_113', 'reg25_111',  'reg21_003',
          'reg21_053',  'reg21_057',  'reg21_102', 'reg21_401',  'reg21_352', 'reg21_354', 'reg21_3541', 'reg25_092',
          'reg37_0012', 'reg25_036', 'reg21_203', 'reg21_055', 'reg21_002', 'reg21_404', 'reg21_458']

schedules = ['reg25_0811', 'reg25_081', 'reg25_0812', 'reg25_082']
class_size = ['reg25_112', 'reg25_113', 'reg25_111']
certification = ['reg21_003', 'reg21_053', 'reg21_057']
contracts = ['reg21_102', 'reg21_401', 'reg21_352', 'reg21_354']
behavior = ['reg25_092', 'reg37_0012', 'reg25_036']

labels = {'reg25_0811': '25.0811 - Minimum First Day of Instruction',
          'reg25_081': '25.081 - Minimum Minutes of Operation',
          'reg25_0812': '25.0812 - Minimum Last Day of Instruction',
          'reg25_082': '25.082 - Pledge of Allegiance and Minute of Silence',
          'reg25_112': '25.112 - Class Size Maximum',
          'reg25_113': '25.113 - Notice of Class Size',
          'reg25_111': '25.111 - Maximum Student Teacher Ratio',
          'reg21_003': '21.003 - Teacher Certification Required',
          'reg21_053': '21.053 - Presentation of Teacher Certificates',
          'reg21_057': '21.057 - Notice of Uncertified Teacher',
          'reg21_102': '21.102 - Maximum Probationary Contract Length',
          'reg21_401': '21.401 - Minimum Service Days Required for Teachers',
          'reg21_352': '21.352 - Teacher Evaluation',
          'reg21_354': '21.354 - Administrator Evaluation',
          'reg21_3541': '21.3541 - Principal Evaluation',
          'reg25_092': '25.092 - Minimum Attendance for Class Credit',
          'reg37_0012': '37.0012 - Designation of Campus Behavior Coordinator',
          'reg25_036': '25.036 - Transfers',
          'reg28_0216': '21.0216 - District Grading Policy (includes false positives)',
          'reg28_0214': '21.0214 - Finality of Grade',
          'reg21_203': '21.203 - Annual Teacher Evaluation',
          'reg21_055': '21.055 - Local Permit with Approval',
          'reg21_002': '21.002 - Teacher Employment Contracts',
          'reg21_404': '21.404 - Planning and Preparation Time',
          'reg21_458': '21.458 - Teacher Mentors',
          'reg28_044': '21.044 - Health Advisory Council and Health Instruction',
          'reg21_451': '21.451 - Professional Development Requirements',
          'reg21_051': '21.051 - Teacher Field Based Experience',
          'reg25_114': '25.114 - P.E. Student Teacher Ratios',
          'reg45_206': '45.206 - Bidding',
          'reg45_205': '45.205 - Provider Term of Contract',
          'reg25.083': '25.082 - School Day Interruptions',
          'reg21_353': '21.353 - Teacher Appraisal Limited to Classroom',
          'reg25_084': '25.084 - Year-Round Attendance (includes false positives)',
          'reg21_0031': '21.0031 - Failure to Obtain Certification Contract Void',
          'reg37_008': '37.008 - Disciplinary Alternative Education',
          'reg37_007': '37.007 - Expulsion for Serious Offenses',
          'reg44_02': '44.092 - Reduce Energy Consumption',
          'reg21_402': '21.402 - Minimum Salary',
          'reg21_405': '21.504 - Duty-Free Lunch',
          'reg11_255': '11.255 - Drop-out Prevention Review (includes false positives?)',
          'reg37_002': '37.002 - Student Removal from Classroom',
          'reg29_0821': '29.0821 - Optional Flexible Year Program'

          }

labels_short = {'reg25_0811': ' Minimum First Day',
                'reg25_081': 'Minimum Minutes',
                'reg25_0812': 'Minimum Last Day',
                'reg25_082': 'Pledge and Minute of Silence',
                'reg25_112': 'Class Size Maximum',
                'reg25_113': 'Notice of Class Size',
                'reg25_111': 'Maximum Student Teacher Ratio',
                'reg21_003': 'Teacher Certification ',
                'reg21_053': 'Presentation of Certificates',
                'reg21_057': 'Notice of Uncertified Teacher',
                'reg21_102': 'Maximum Probationary Contract Length',
                'reg21_401': 'Minimum Service Days',
                'reg21_352': 'Teacher Evaluation',
                'reg21_354': 'Principal Evaluation',
                'reg25_092': 'Minimum Attendance for Credit',
                'reg37_0012': 'Campus Behavior Coordinator',
                'reg25_036': 'Transfers'}

similar = {'25.0811': ['25.0811', '25_081', '25.0812'],
           '25.112': ['25.112', '25.113', '25.111'],
           '21.003': ['21.003', '21.053', '21.044', '21.057', '21.055'],
           '21.102': ['21.102'],
           '21.401': ['21.401'],
           '25.092': ['25.092'],
           '21.352': ['21.352'],
           '21.354': ['21.354'],
           '37.0012': ['37.0012'],
           '25.036': ['25.036']
           }

number = {'reg25_0812': '25.0812',
          'reg21_003': '21.003'}
