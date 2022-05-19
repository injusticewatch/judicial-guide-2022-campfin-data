all: clean data/final/campfin.json

.PHONY:
clean:
	rm -f data/final/*
# data/raw/*

data/final/campfin.json: data/raw/receipts-trimmed.txt
	time python3 scripts/process_receipts.py $< > $@

data/raw/receipts-trimmed.txt: data/raw/receipts.txt
	head -n 1 $< >> $@
	tail -n +5000000 $< >> $@

data/raw/receipts.txt:
	wget -nv -O $@ "https://www.elections.il.gov/CampaignDisclosureDataFiles/Receipts.txt"