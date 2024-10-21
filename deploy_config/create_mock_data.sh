#!/bin/bash

# generate mock data
python manage.py generate_mock_data center Center center/fixture/center.csv
python manage.py generate_mock_data vaccine Vaccine vaccine/fixture/vaccine.csv
python manage.py generate_mock_data user User user/fixture/demo-user.csv
python manage.py generate_mock_data center Storage center/fixture/storage.csv \
  --fk "center,Center,center,center_name" "vaccine,Vaccine,vaccine,vaccine_name"
python manage.py generate_mock_data campaign Campaign campaign/fixture/campaign.csv \
  --fk "center,Center,center,center_name" "vaccine,Vaccine,vaccine,vaccine_name" \
  --date-fields "start_date,end_date"
