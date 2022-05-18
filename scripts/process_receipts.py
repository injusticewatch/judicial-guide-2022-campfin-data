import sys
import csv
import json
import operator
from dateutil.parser import parse

csv.field_size_limit(sys.maxsize)

START_DATE = parse('2020-01-01')
COMMITTEES = [
  '37023',
  '36898',
]

TOP_DONOR_COUNT = 5

if __name__ == '__main__':
  input_file = sys.argv[1] # 'data/raw/receipts.txt'

  acc = {}
  for committee in COMMITTEES:
    acc[committee] = {
      "committee": committee,
      "totalDonations": 0,
      "donations": [],
      "topDonors": [],
    }

  with open(input_file, 'r', encoding='latin-1') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')

    # consider trimming earlier dates at front of txt file
    for row in reader:
      committee_id = row['CommitteeID']
      receipt_date = parse(row['RcvDate'])

      if (receipt_date >= START_DATE) and (committee_id in COMMITTEES):
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

        # TODO: look at in-kind contributions

    # TODO: order and slice to top 5 top donors
    committeeList = list(acc.values())
    for committee in committeeList:
      committee['topDonors'].sort(key=operator.itemgetter('aggregateAmount'), reverse=True)

    print(json.dumps(
      committeeList
    ))