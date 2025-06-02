MIXS_SCHEMA_URL=https://raw.githubusercontent.com/GenomicsStandardsConsortium/mixs/refs/heads/main/src/mixs/schema/mixs.yaml
MIXS_SCHEMA_FILE=mixs.yaml

LINKML_META_URL=https://raw.githubusercontent.com/linkml/linkml-model/refs/heads/main/linkml_model/model/schema/meta.yaml
LINKML_META_FILE=meta.yaml

.PHONY: download-mixs
mixs.yaml:
	@echo "Downloading MIxS schema..."
	curl -L $(MIXS_SCHEMA_URL) -o $(MIXS_SCHEMA_FILE)
	@echo "Downloaded $(MIXS_SCHEMA_FILE)"

#.PHONY: merge-schema
#merge-schema:
#	@echo "Merging schema from URL and saving to mixs_merged.yaml..."
#	uv run python ./download_and_merge_schema.py \
#	  --source-url $(LINKML_META_URL) \
#	  --destination $(LINKML_META_FILE)
#	@echo "Done!"

biosample.yaml: mixs_to_biosample.yaml mixs.yaml
	 uv run linkml-map derive-schema --output $@ --transformer-specification $^

biosample-clean:
	rm -rf biosample.yaml
	rm -rf mixs.yaml

biosample-all: biosample-clean biosample.yaml