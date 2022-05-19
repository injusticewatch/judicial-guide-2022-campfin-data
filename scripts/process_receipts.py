import sys
import csv
import json
import operator
from dateutil.parser import parse

csv.field_size_limit(sys.maxsize)

TOP_DONOR_COUNT = 5
START_DATE = parse('2020-01-01')
COMMITTEES = [
  '37023',
  '36898',
  '36935',
  '22125',
  '37437',
  '17671',
  '17003',
  '22504',
  '36948',
  '37329',
  '35455',
  '37037',
  '36823',
  '37005',
  '24028',
  '33886',
  '37113',
  '35444',
  '35501',
  '36738',
  '22396',
  '45918',
  '35454',
  '37013',
  '31848',
  '37089',
  '35610',
  '35457',
  '37044',
  '37138',
  '36890',
  '34220',
  '36983',
  '36982',
  '34284',
  '32876',
  '37090',
  '37152',
  '34313',
  '34246',
  '36989',
  '37128',
  '37424',
  '37447',
  '37236',
  '11855',
  '35389',
  '35459',
  '25568',
  '37231',
  '34372',
  '37162',
  '37012',
  '37074',
  '36810',
  '35715',
  '37124',
  '37252',
  '35720',
  '25937',
  '35684',
  '25470',
  '37373',
  '36795',
  '35650',
  '36932',
  '35789',
  '37042',
  '37036',
  '36985',
  '36865'
]

if __name__ == '__main__':
  input_file = sys.argv[1] # 'data/raw/receipts.txt'

  acc = {}
  for committee in COMMITTEES:
    acc[committee] = {
      "committee": committee,
      "totalDonations": 0,
      "topDonors": [],
    }

  with open(input_file, 'r', encoding='latin-1') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')

    # consider trimming earlier dates at front of txt file
    for row in reader:
      committee_id = row['CommitteeID']
      # print("raw date", row['RcvDate'])
      receipt_date = parse(row['RcvDate'])
      # print("parsed date", receipt_date)

      if row['RcvDate'] and (parse(row['RcvDate']) >= START_DATE) and (committee_id in COMMITTEES):
        # tally total donations across contributors
        acc[committee_id]['totalDonations'] += float(row['Amount'])

        firstName = row['FirstName'].strip()
        lastName = row['LastOnlyName'].strip()
        zipCode = row['Zip'].strip()

        # see if donor is already in topDonors
        # if they are, add to aggregate total
        # if they're not, create a new dict
        donor = next((
          x for x in acc[committee_id]['topDonors'] if x['firstName'].strip() == firstName and x['lastName'].strip() == lastName and x['zipCode'].strip() == zipCode), None)
        if donor:
          donor["aggregateAmount"] += float(row['Amount'])
        else:
          acc[committee_id]['topDonors'].append({
            "firstName": firstName,
            "lastName": lastName,
            "occupation": row['Occupation'],
            "employer": row['Employer'],
            "aggregateAmount": float(row['Amount']),
            "zipCode": zipCode,
          })

    # sort by aggregate donation and slice to top donors
    committeeList = list(acc.values())
    for committee in committeeList:
      committee['topDonors'].sort(key=operator.itemgetter('aggregateAmount'), reverse=True)
      committee['topDonors'] = committee['topDonors'][:TOP_DONOR_COUNT]

    print(json.dumps(
      committeeList
    ))