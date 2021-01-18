# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

#SHELL := /bin/sh
PY_VERSION := 3.8

export PYTHONUNBUFFERED := 1

SRC_DIR := functions
SAM_DIR := .aws-sam
TEMPLATE_DIR := .

# Region for deployment
AWS_DEPLOY_REGION ?= eu-west-1

# CloudFormation deployment variables
CFN_ARTEFACT_S3_BUCKET ?= ilyiny-sagemaker-demo-artefacts
CFN_TEMPLATE_DIR := cfn_templates
PROJECT_NAME ?= sagemaker-studio-vpc
VPC_CIDR ?= 10.2.0.0/16
FIREWALL_SN_CIDR ?= 10.2.1.0/24
NAT_GW_SN_CIDR ?= 10.2.2.0/24
SAGEMAKER_SN_CIDR ?= 10.2.3.0/24


# Stack name used when deploying the app for manual testing
APP_STACK_NAME ?= sagemaker-studio-demo

PYTHON := $(shell /usr/bin/which python$(PY_VERSION))

.DEFAULT_GOAL := package

build:

package: build 
	aws cloudformation package \
		--template-file $(CFN_TEMPLATE_DIR)/sagemaker-studio-vpc.yaml \
		--s3-bucket $(CFN_ARTEFACT_S3_BUCKET) \
		--output-template-file $(CFN_TEMPLATE_DIR)/packaged.yaml

deploy: package
	aws cloudformation deploy \
		--template-file $(CFN_TEMPLATE_DIR)/packaged.yaml \
		--stack-name $(APP_STACK_NAME) \
		--parameter-overrides \
		ProjectName=$(PROJECT_NAME) \
		VpcCIDR=$(VPC_CIDR) \
		FirewallSubnetCIDR=$(FIREWALL_SN_CIDR) \
		NATGatewaySubnetCIDR=$(NAT_GW_SN_CIDR) \
		PrivateSubnetCIDR=$(SAGEMAKER_SN_CIDR) \
		--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM

