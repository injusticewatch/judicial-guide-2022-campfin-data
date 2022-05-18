import sys
import csv
import json
from dateutil.parser import parse

csv.field_size_limit(sys.maxsize)

START_DATE = parse('2020-01-01')
COMMITTEES = [
  '37023',
  '36898',
]

TOP_DONOR_COUNT = 5

if __name__ == '__main__':
  input_file =  'data/raw/receipts.txt' # sys.argv[1]

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
        firstName = row['FirstName'].strip()
        lastName = row['LastOnlyName'].strip()
        # zipCode = row['Zip'].strip()

        acc[committee_id]['donations'].append({
          "firstName": row['FirstName'],
          "lastName": row['LastOnlyName'],
          "occupation": row['Occupation'],
          "employer": row['Employer'],
          "amount": float(row['Amount']),
          "aggregateAmount": float(row['AggregateAmount']),
        })

        donor = next((
          x for x in acc[committee_id]['topDonors'] if x['firstName'] == firstName and x['lastName'] == lastName), None) # and x['Zip'] == zipCode

        # if they are, add to aggregate total
        # if they're not, create a new dict
        if donor:
          donor["aggregateAmount"] += float(row['Amount'])
        else:
          acc[committee_id]['topDonors'].append({
            "firstName": row['FirstName'],
            "lastName": row['LastOnlyName'],
            "occupation": row['Occupation'],
            "employer": row['Employer'],
            "aggregateAmount": float(row['Amount']),
          })
          
      # TODO: order and slice to top 5 top donors

        acc[committee_id]['totalDonations'] += float(row['Amount'])

    print(json.dumps(
      list(acc.values())
    ))