# This file is generated by the gen_tf.py script.
# Do not edit this file directly.

module "about" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "about.html"
  file_directory = "../public/"
  fqdn           = "about.${var.domainName}"
  source_hash    = filemd5("../public/about.html")
  zone_id        = aws_route53_zone.main.zone_id
}

module "favicon" {
  source = "./zone_deployment"

  content_type   = "image/x-icon"
  domain_aliases = []
  file           = "favicon.ico"
  file_directory = "../public/"
  fqdn           = "favicon.${var.domainName}"
  source_hash    = filemd5("../public/favicon.ico")
  zone_id        = aws_route53_zone.main.zone_id
}

module "index" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = ["www.${var.domainName}"]
  file           = "index.html"
  file_directory = "../public/"
  fqdn           = "${var.domainName}"
  source_hash    = filemd5("../public/index.html")
  zone_id        = aws_route53_zone.main.zone_id
}

module "interesting_rfcs" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "interesting-rfcs.html"
  file_directory = "../public/"
  fqdn           = "interesting-rfcs.${var.domainName}"
  source_hash    = filemd5("../public/interesting-rfcs.html")
  zone_id        = aws_route53_zone.main.zone_id
}

module "rfc7873_interesting_rfcs" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "rfc7873.html"
  file_directory = "../public/interesting-rfcs/"
  fqdn           = "rfc7873.interesting-rfcs.${var.domainName}"
  source_hash    = filemd5("../public/interesting-rfcs/rfc7873.html")
  zone_id        = aws_route53_zone.main.zone_id
}

module "rfc8446_interesting_rfcs" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "rfc8446.html"
  file_directory = "../public/interesting-rfcs/"
  fqdn           = "rfc8446.interesting-rfcs.${var.domainName}"
  source_hash    = filemd5("../public/interesting-rfcs/rfc8446.html")
  zone_id        = aws_route53_zone.main.zone_id
}

module "rfc8484_interesting_rfcs" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "rfc8484.html"
  file_directory = "../public/interesting-rfcs/"
  fqdn           = "rfc8484.interesting-rfcs.${var.domainName}"
  source_hash    = filemd5("../public/interesting-rfcs/rfc8484.html")
  zone_id        = aws_route53_zone.main.zone_id
}

module "rfc8890_interesting_rfcs" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "rfc8890.html"
  file_directory = "../public/interesting-rfcs/"
  fqdn           = "rfc8890.interesting-rfcs.${var.domainName}"
  source_hash    = filemd5("../public/interesting-rfcs/rfc8890.html")
  zone_id        = aws_route53_zone.main.zone_id
}

module "rfc9113_interesting_rfcs" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "rfc9113.html"
  file_directory = "../public/interesting-rfcs/"
  fqdn           = "rfc9113.interesting-rfcs.${var.domainName}"
  source_hash    = filemd5("../public/interesting-rfcs/rfc9113.html")
  zone_id        = aws_route53_zone.main.zone_id
}

module "_60_40_posts" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "60-40.html"
  file_directory = "../public/posts/"
  fqdn           = "60-40.posts.${var.domainName}"
  source_hash    = filemd5("../public/posts/60-40.html")
  zone_id        = aws_route53_zone.main.zone_id
}

module "posts" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "index.html"
  file_directory = "../public/posts/"
  fqdn           = "posts.${var.domainName}"
  source_hash    = filemd5("../public/posts/index.html")
  zone_id        = aws_route53_zone.main.zone_id
}

module "joy_of_shipping_posts" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "joy-of-shipping.html"
  file_directory = "../public/posts/"
  fqdn           = "joy-of-shipping.posts.${var.domainName}"
  source_hash    = filemd5("../public/posts/joy-of-shipping.html")
  zone_id        = aws_route53_zone.main.zone_id
}

module "oxygen_posts" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "oxygen.html"
  file_directory = "../public/posts/"
  fqdn           = "oxygen.posts.${var.domainName}"
  source_hash    = filemd5("../public/posts/oxygen.html")
  zone_id        = aws_route53_zone.main.zone_id
}

module "pets_vs_cattle_posts" {
  source = "./zone_deployment"

  content_type   = "text/html"
  domain_aliases = []
  file           = "pets-vs-cattle.html"
  file_directory = "../public/posts/"
  fqdn           = "pets-vs-cattle.posts.${var.domainName}"
  source_hash    = filemd5("../public/posts/pets-vs-cattle.html")
  zone_id        = aws_route53_zone.main.zone_id
}
