from constructs import Construct
from aws_cdk import (
    CfnOutput,
    Duration,
    Stack,
    aws_iam as iam,
    aws_sqs as sqs,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    aws_glue_alpha as glue,
    aws_glue as cfnGlue,
    custom_resources as cr,
    aws_s3 as s3,
)

import os

class InfrastructureStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        database = glue.Database(self, "payments",
            database_name="payments"
        )
        
        glue_role = iam.Role(
            self, 'cdkGlueRole',
            assumed_by=iam.ServicePrincipal('glue.amazonaws.com'),
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name('service-role/AWSGlueServiceRole')]
        )
        
        # TODO: Parameterize s3 bucket
        glue_role.add_to_policy(iam.PolicyStatement(
            resources=["arn:aws:s3:::awsglue-datasets/examples/medicare/*"],
            actions=[ 
                "s3:GetObject",
                "s3:PutObject"
                ]
        ))

        glue_trigger = cfnGlue.CfnTrigger(self, "glue-daily-trigger",
            name = "etl-trigger",
            schedule = "cron(5 * * * ? *)", # every hour at X.05, every day
            type="SCHEDULED",
            actions=[
                {
                    "jobName": "glue_crawler-daily"
                }
            ],
            start_on_creation=True
        )
        
        crawler_name = 'crawler_medicare'
        glue_crawler = cfnGlue.CfnCrawler(
            self, crawler_name,
            name=crawler_name,
            database_name=database.database_name,
            role=glue_role.role_arn,
            targets={"s3Targets": [{"path": "s3://awsglue-datasets/examples/medicare/"}]},
        )
        glue_trigger.add_depends_on(glue_crawler)
        
        aws_custom = cr.AwsCustomResource(self, "startCrawler",
            on_update=cr.AwsSdkCall(
                service="Glue",
                action="startCrawler",
                parameters={
                    "Name": crawler_name,
                },
                physical_resource_id=cr.PhysicalResourceId.of(crawler_name)
            ),
            policy=cr.AwsCustomResourcePolicy.from_sdk_calls(
                resources=cr.AwsCustomResourcePolicy.ANY_RESOURCE
            )
        )

        glue.Job(self, "PySparkEtlJob",
            role=glue_role,
            executable=glue.JobExecutable.python_etl(
                glue_version=glue.GlueVersion.V3_0,
                python_version=glue.PythonVersion.THREE,
                script=glue.Code.from_asset(os.path.join(os.path.dirname(__file__), "../glue_job_source/data_cleaning_and_lambda.py")),
            ),
            description="an example python ETL job"
        )
        
        CfnOutput(self, "aws/Config UPDATE", value="glue_role_arn=" + glue_role.role_arn)