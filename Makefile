all: clean data/final/campfin.json

.PHONY:
clean:
	rm -f data/final/* data/raw/receipts-trimmed.txt

# condense and drop keys we don't need in prd
data/final/campfin.json: data/final/campfin-pretty.json
	jq -c 'map(del(.contributions))' $< > $@

data/final/campfin-pretty.json: data/raw/receipts-trimmed.txt
	time python3 scripts/process_receipts.py $< > $@

# the receipts file contains donations starting in 1994!
# trim off the start until around the years we want
data/raw/receipts-trimmed.txt: data/raw/receipts.txt
	head -n 1 $< >> $@
	tail -n +5000000 $< >> $@

data/raw/receipts.txt:
	wget -nv -O $@ "https://www.elections.il.gov/CampaignDisclosureDataFiles/Receipts.txt"