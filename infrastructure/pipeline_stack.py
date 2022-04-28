from constructs import Construct
from aws_cdk import (
    CfnOutput,
    Stack,
    aws_codecommit as codecommit,
    pipelines as pipelines,
)

from infrastructure.pipeline_stage import GlueJobPipelineStage

class GlueJobPipelineStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creates a CodeCommit repository called 'GlueJobRepo'
        repo = codecommit.Repository(
            self, 'GlueJobRepo',
            repository_name= "GlueJobRepo"
        )
        
        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.code_commit(repo, "master"),
                commands=[
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                    "pip install -r requirements-dev.txt",
                    "pip install -r requirements.txt",  # Instructs Codebuild to install required packages
                    "jupyter nbconvert --to script ./glue_job_source/data_cleaning_and_lambda.ipynb",
                    "npx cdk synth",
                ],
                primary_output_directory="infrastructure/cdk.out"
            ),
        )

        deploy = GlueJobPipelineStage(self, "Staging")
        deploy_stage = pipeline.add_stage(deploy)
        
        CfnOutput(self, "glue job repo", value="git remote add origin " + repo.repository_clone_url_grc)