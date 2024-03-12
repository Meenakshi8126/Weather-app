# Create a compute instance and assign the service account
# Set the environment variables for the docker image as metadata
# Run the docker image using startup script
# Pull the docker image from the registry

# IAM role
resource "aws_iam_role" "ec2_role" {
  name = "ec2_role"

  assume_role_policy = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Principal": {
            "Service": "ec2.amazonaws.com"
          },
          "Action": "sts:AssumeRole"
        }
      ]
    }
  EOF
}

# Attach an IAM policy for S3 access to the IAM role
resource "aws_iam_role_policy_attachment" "s3_policy_attachment" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# security group 
resource "aws_security_group" "instance_sg" {
  name        = "instance_sg"
  description = "Allow SSH and HTTP inbound traffic"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 instance
resource "aws_instance" "app" {
  ami                    = "ami-0f403e3180720dd7e" 
  instance_type          = "t2.micro"
  vpc_security_group_ids = [aws_security_group.instance_sg.id]
  iam_instance_profile   = aws_iam_role.ec2_role.name
  user_data = <<-EOF
              #!/bin/bash
              yum install docker -y
              service docker start
              docker pull your-registry-name/weather-app 
              docker run your-registry-name/wather-app:latest 
              EOF
  metadata_options {
    # Set the environment variables for the Docker image as metadata
    http_tokens                 = "optional"
    http_put_response_hop_limit = 2
    # Add your environment variables here
    custom_env_vars = {
      FREQUENCY = "daily"
      FOLDER    = "weather_data"
      COUNTRY   = "Prague,CZ"
      OUTPUT    = "weather.html"
    }
  }
}
