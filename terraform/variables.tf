##################################
# Global / Project variables
##################################

variable "project" {
  type        = string
  description = "Project name"
}

variable "environment" {
  type        = string
  description = "Environment name (dev/prod)"
}

##################################
# Database variables
##################################

variable "db_name" {
  type        = string
  description = "Database name"
}

variable "db_username" {
  type        = string
  description = "Database master username"
}

variable "db_password" {
  type        = string
  sensitive   = true
  description = "Database master password"
}
