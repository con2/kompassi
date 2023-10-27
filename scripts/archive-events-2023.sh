#!/bin/bash
set -xueo pipefail

# cannot migrate hitpoint2017 to zero because it would take down half of the programme management with it
python manage.py labour_archive_signups hitpoint2017 worldcon75 yukicon2019 yukicon2018 yukicon2017 yukicon2016 shippocon2016 popcult2017 nippori2017 mimicon2016 lakeuscon2016 kuplii2017 kuplii2016 kuplii2015 hitpoint2015 finncon2016 desucon2017 desucon2016 frostbite2017 frostbite2016

for event in worldcon75 yukicon2019 yukicon2018 yukicon2017 yukicon2016 shippocon2016 popcult2017 nippori2017 mimicon2016 lakeuscon2016 kuplii2017 kuplii2016 kuplii2015 hitpoint2015 finncon2016 desucon2017 desucon2016 frostbite2017 frostbite2016 tracon2017; do
  python manage.py migrate $event zero
done
