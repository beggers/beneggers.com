"""
This script generates the requisite terrafrom to deploy the site.
"""

import mime_types

import json
import os


GENERATED_FILE_COMMENT = """# This file is generated by the gen_tf.py script.
# Do not edit this file directly.
"""

SUBDOMAIN_MODULE_BLOCK = """
module "{tf_suitable_subdomain}" {{
  source = "./zone_deployment"

  content_type   = "{content_type}"
  domain_aliases = {domain_aliases}
  file           = "{file_name}"
  file_directory = "../{file_dir}/"
  fqdn           = "{fqdn}"
  source_hash    = filemd5("../{full_file_path}")
  zone_id        = aws_route53_zone.main.zone_id
}}
"""

# TODO we could generate this directly from the output file in zone_deployment/
SUBDOMAIN_OUTPUT_BLOCK = """
output "{tf_suitable_subdomain}_cloudfront_distribution_id" {{
  value = module.{tf_suitable_subdomain}.cloudfront_distribution_id
}}

output "{tf_suitable_subdomain}_hosted_zone_id" {{
  value = module.{tf_suitable_subdomain}.hosted_zone_id
}}

output "{tf_suitable_subdomain}_bucket_id" {{
  value = module.{tf_suitable_subdomain}.bucket_id
}}

output "{tf_suitable_subdomain}_bucket_regional_domain_name" {{
  value = module.{tf_suitable_subdomain}.bucket_regional_domain_name
}}

output "{tf_suitable_subdomain}_cert_arn" {{
  value = module.{tf_suitable_subdomain}.cert_arn
}}

output "{tf_suitable_subdomain}_cert_validation_record" {{
  value = module.{tf_suitable_subdomain}.cert_validation_record
}}

"""

DOMAIN_FILE = "main.tf"
OUTPUT_FILE = "outputs_autogen.tf"

TERRAFORM_DIRETORY = "terraform"


config = json.load(open("config.json", "r"))


def main():
    content_dir = config["content_dir"]
    filenames = get_filenames(content_dir)
    if not filenames:
        print("No files found in the pages directory.")
        return
    generate_domain_file(filenames)
    generate_output_file(filenames)


def get_filenames(path):
    files = []
    for root, _, fs in os.walk(path):
        for f in fs:
            files.append(os.path.join(root, f))
    files.sort()
    return files


def generate_domain_file(filenames):
    blocks = []
    for filename in filenames:
        subdomain, extension = filename_to_subdomain_and_extension(filename)
        content_type = mime_types.extensions_to_types[extension]
        # Cool and normal best practices.
        domain_aliases = list_as_string(
            ["www.${var.domainName}"] if subdomain == "index" else []
        )
        block = generate_subdomain_module_block(
            subdomain,
            content_type,
            config["content_dir"],
            domain_aliases,
            os.path.dirname(filename),
            os.path.basename(filename),
        )
        blocks.append(block)

    write_blocks_to_file(blocks, os.path.join(TERRAFORM_DIRETORY, DOMAIN_FILE))


def generate_subdomain_module_block(
    subdomain, content_type, content_dir, domain_aliases, file_dir, file_name
):
    return SUBDOMAIN_MODULE_BLOCK.format(
        tf_suitable_subdomain=tf_suitable(subdomain),
        content_type=content_type,
        content_dir=content_dir,
        domain_aliases=domain_aliases,
        file_name=file_name,
        file_dir=file_dir,
        full_file_path=os.path.join(file_dir, file_name),
        fqdn=fqdn(subdomain),
    )


def generate_output_file(filenames):
    blocks = []
    for filename in filenames:
        subdomain, _ = filename_to_subdomain_and_extension(filename)
        block = generate_subdomain_output_block(subdomain)
        blocks.append(block)

    write_blocks_to_file(blocks, os.path.join(TERRAFORM_DIRETORY, OUTPUT_FILE))


def generate_subdomain_output_block(subdomain):
    return SUBDOMAIN_OUTPUT_BLOCK.format(
        tf_suitable_subdomain=tf_suitable(subdomain),
    )


def list_as_string(l):
    return "[" + ", ".join([f'"{item}"' for item in l]) + "]"


def fqdn(subdomain):
    if subdomain == "index":
        return "${var.domainName}"
    return f"{subdomain}.${{var.domainName}}"


def write_blocks_to_file(blocks, filepath):
    with open(filepath, "w") as f:
        f.write(GENERATED_FILE_COMMENT)
        f.writelines(blocks)


def filename_to_subdomain_and_extension(filename):
    # TODO this logic is mostly replicated in ssg.py.
    extension = filename.split(".")[-1]
    subdomain = filename.split(".")[:-1]
    if len(subdomain) != 1:
        raise ValueError(f"Invalid filename (does it have a period in it?): {filename}")
    subdomain = subdomain[0]
    url = subdomain.replace(config["content_dir"], "").split("/")
    url = url[1:] if url[0] == "" else url
    if url[-1] == "index" and len(url) > 1:
        url = url[:-1]
    url.reverse()
    subdomain = ".".join(url)

    return subdomain, extension


def tf_suitable(subdomain):
    # Terraform doesn't like dashes or periods in variable names.
    # Also, names MUST start with an underscore or letter.
    suitable = subdomain.replace(".", "_").replace("-", "_")
    if suitable[0].isdigit():
        suitable = "_" + suitable
    return suitable


if __name__ == "__main__":
    main()
