all: clean data/final/campfin.json

.PHONY:
clean:
	rm -f data/final/*
# data/raw/*

data/final/campfin.json: data/raw/receipts.txt
	time python3 scripts/process_receipts.py $< > $@

data/raw/receipts.txt:
	wget -nv -O $@ "https://www.elections.il.gov/CampaignDisclosureDataFiles/Receipts.txt"