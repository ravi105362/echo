provider "aws" {
  region  = "eu-central-1"
  access_key = "<add security key>"
  secret_key = "<add secret key>"
}

data "aws_vpc" "default" {
  default = true
}

resource "aws_security_group" "rds" {
  vpc_id      = "${data.aws_vpc.default.id}"
  name        = "rds"
  description = "Allow all inbound for Postgres"
ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
resource "aws_db_instance" "postgres" {
  identifier             = "postgres"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  engine                 = "postgres"
  engine_version         = "14.7"
  skip_final_snapshot    = true
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.rds.id]
  username               = "ravi"
  password               = "ravi12304"
}

output "rds_instance" {
    value = "${aws_db_instance.postgres.endpoint}"
}
