examples:
	@echo "Cleaning data"
	@python clean_data_1.py
	@echo "Exporting into format"
	@python export_phrasevec.py
	@echo "Done. Check that ./pos and ./neg directories are populated."
	ls -la pos | wc -l
	ls -la neg | wc -l
	ls -la unlabeled | wc -l

