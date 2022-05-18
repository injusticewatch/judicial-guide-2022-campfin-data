all: clean data/final/campfin.json copy

.PHONY:
clean:
	rm -f data/intermediate/* data/final/*
  # data/raw/*

# wait to copy as a final step in case something breaks
.PHONY:
copy:
	cp data/final/campfin.json data/campfin.json

data/final/campfin.json: data/raw/receipts.txt
	time python3 scripts/process_receipts.py $< > $@

data/raw/receipts.txt:
	wget -O $@ "https://www.elections.il.gov/CampaignDisclosureDataFiles/Receipts.txt"