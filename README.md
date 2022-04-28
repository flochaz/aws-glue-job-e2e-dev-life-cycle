
# How to develop, and deploy properly AWS Glue Job using AWS Glue interactive sessions and AWS CDK

This repo aim to demonstrate how to develop AWS Glue Job efficiently:
* Be able to develop locally
* Get a fast feedback loop
* Be able to commit with no manual copy paste between tools

In addition this repo shows how to deploy this AWS Glue Job through a proper CI/CD pipeline leveraging Infrastructure as code.

Two options are proposed here: "Use this repo" or "Do it your self"

## Use This repo

### Prerequisites

1. Clone this repo
   ```bash
   git clone https://github.com/flochaz/aws-glue-job-e2e-dev-life-cycle.git
   cd aws-glue-job-e2e-dev-life-cycle
   ```
1. setup virtual env
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
1. Install CDK
   ```bash
   npm install -g aws-cdk
   ```

### deploy dev env

In order to run glue job locally we will need some specific elements such as
* an iam role to assume while running local notebook
* a glue database to store the data
* a glue crawler to extract the schema and data from raw source csv files
* Trigger the crawler ...

This CDK app will deploy all those for you to be ready to work on the glue job itself

1. Install deps
   ```bash
   pip install -r requirements.txt
   ```
1. Bootstrap account
   ```bash
   cdk bootstrap
   ```
1. Deploy Glue role, crawler etc.

```bash
cdk deploy infrastructure
```

### Local dev experience

AWS Glue service offer a way to run your job remotely while developping locally through the [Interactive Sessions feature](https://docs.aws.amazon.com/glue/latest/dg/interactive-sessions.html).

1. Set up interactive session:
  ```bash
  pip install -r requirements-dev.txt
  SITE_PACKAGES=$(pip show aws-glue-sessions | grep Location | awk '{print $2}')
  jupyter kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_pyspark # Add "--user" if getting "[Errno 13] Permission denied: '/usr/local/share/jupyter'"
  jupyter kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_spark # Add "--user" if getting "[Errno 13] Permission denied: '/usr/local/share/jupyter'"
  ```
1. Setup glue role by copying the output called `awsConfigUPDATE` of the previous `cdk deploy` command into `~/.aws/config` under `[default]`
   ```bash 
   cat ~/.aws/config
   [default]
   glue_role_arn=xxxxxx
   ```
1. Launch notebook
   ```bash
   jupyter notebook # add "--ip 0.0.0.0" if running in a remote IDE such as cloud9 (PS: you will need to open your security group for TCP connection on 8888 port as well !)
   ```
1. Play with `glue_job_source/data_cleaning_and_lambda.ipynb`
1. Commit your changes to git
1. Optionally deploy your changes to dev env
   ```bash
   cdk deploy infrastructure
   ```

### Deploy through pipeline

If deploying to same account / region, first you will need to destroy your dev stack to avoid resource collision (especially glue role, crawler, database etc.)
```bash
cdk destroy infrastructure
```

1. Create a repo by deploying the pipeline stack
   ```bash
   cdk deploy GlueJobPipelineStack
   ```
2. Push code to repo
   ```bash
   # Remove github origin
   git remote remove origin
   # Add code commit repo as origin
   git remote add origin <YOUR CODE COMMIT REPO URL (THE COMMAND SHOULD BE FOUND IN THE PREVIOUS "cdk deploy GlueJobPipelineStack" output)>
   git push -u master
   ```
3. Observe the deployment through code pipeline


## Do it your self

1. Get into your aws account
1. Setup your online IDE: [Cloud 9](https://catalog.us-east-1.prod.workshops.aws/workshops/071bbc60-6c1f-47b6-8c66-e84f5dc96b3f/en-US/10-introduction-and-setup/10-cloud-9)
1. Add your glue job (you can take this one for instance https://github.com/aws-samples/aws-glue-samples/blob/master/examples/data_cleaning_and_lambda.py)
1. Add interactive sessions + notebook CI/CD (optional)
  1. https://docs.aws.amazon.com/glue/latest/dg/interactive-sessions.html 
  1. Quick hack
    1. `vim ~/.aws/config` glue_role_arn
    1. `vim ~/.aws/credentials`
    1. `jupyter notebook —ip 0.0.0.0`
    1. `jupyter nbconvert --to script ./data_cleaning_and_lambda.ipynb`
1. Create your first [CDK app](https://cdkworkshop.com/30-python/20-create-project.html)
1. Add glue infrastructure: https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_glue_alpha/README.html 
  1. Glue database
  1. Glue Role
  1. Glue Crawler
  1. Glue Job
1. Add CI/CD using the [official doc](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.pipelines/README.html) or [workshop](https://cdkworkshop.com/30-python/70-advanced-topics/200-pipelines.html)  


## TODO

[ ] Inject config (such as output_bucket, stage, database name etc ...)
[ ] Add dev life cycle diagram and screenshots
[ ] Add example for external file inclusion in notebook with aws s3 sync watch etc.
[ ] Fix CDK unit tests
[ ] Add integration tests to pipeline
[ ] Describe how to add stage with manual approval