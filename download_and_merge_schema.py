#!/usr/bin/env python3
import click
import requests
from linkml_runtime.utils.schemaview import SchemaView
from linkml_runtime.linkml_model.meta import SchemaDefinition
from linkml_runtime.dumpers import yaml_dumper


@click.command()
@click.option('--source-url', required=True, help='URL of the LinkML schema YAML to download')
@click.option('--destination', required=True, type=click.Path(), help='Path to save the merged schema')
def main(source_url, destination):
    """
    Fetches a LinkML schema from a URL, merges all its imports, and writes the merged schema as YAML to the destination.
    """
    # Download the source schema
    click.echo(f"Downloading schema from {source_url}...")
    response = requests.get(source_url)
    response.raise_for_status()

    # Save the downloaded content to a temporary file
    tmp_schema_path = "downloaded_schema.yaml"
    with open(tmp_schema_path, "w") as f:
        f.write(response.text)

    # Load the schema into SchemaView
    click.echo("Loading and merging imports...")
    sv = SchemaView(tmp_schema_path)
    merged_schema: SchemaDefinition = sv.schema

    # Save the merged schema as YAML
    click.echo(f"Saving merged schema to {destination}...")
    with open(destination, "w") as f:
        f.write(yaml_dumper.dumps(merged_schema))

    click.echo("Done!")


if __name__ == '__main__':
    main()
