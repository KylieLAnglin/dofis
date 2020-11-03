#!/bin/bash
CAMPUS=0
DISTRICT=0

echo "running data_from_tea"

if [[ $DISTRICT = 1 ]]
then
    python d01_clean_tea_data.py
    python d02_append_years.py
fi

if [[ $CAMPUS = 1 ]]
then
    python c01_clean_tea_data.py
    pyton c01_append_years.py
fi

echo "done"