resource "aws_route53_zone" "main" {
  name = var.domainName
}

resource "aws_route53_record" "main_a" {
  zone_id = aws_route53_zone.main.zone_id
  name    = var.domainName
  type    = "A"
  alias {
    name                    = aws_cloudfront_distribution.main.domain_name
    zone_id                 = aws_cloudfront_distribution.main.hosted_zone_id
    evaluate_target_health  = false
  }
}