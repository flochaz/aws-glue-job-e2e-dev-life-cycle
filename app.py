#!/usr/bin/env python3

import aws_cdk as cdk

from infrastructure.infrastructure_stack import InfrastructureStack
from infrastructure.pipeline_stack import GlueJobPipelineStack


app = cdk.App()
InfrastructureStack(app, "infrastructure")
GlueJobPipelineStack(app, "GlueJobPipelineStack")


app.synth()
