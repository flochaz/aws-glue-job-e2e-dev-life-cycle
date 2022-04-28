from constructs import Construct
from aws_cdk import (
    Stage
)
from infrastructure.infrastructure_stack import InfrastructureStack

class GlueJobPipelineStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = InfrastructureStack(self, 'GlueJob')