#!/usr/bin/env python3

import aws_cdk as cdk

from infrastructure.infrastructure_stack import InfrastructureStack
from infrastructure.pipeline_stack import WorkshopPipelineStack


app = cdk.App()
InfrastructureStack(app, "infrastructure")
WorkshopPipelineStack(app, "WorkshopPipelineStack")


app.synth()
