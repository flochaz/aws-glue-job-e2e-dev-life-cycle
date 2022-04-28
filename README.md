
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
2. setup virtual env
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

### Local dev experience

AWS Glue service offer a way to run your job remotely while developping locally through the [Interactive Sessions feature](https://docs.aws.amazon.com/glue/latest/dg/interactive-sessions.html).

1. Set up interactive session:
  ```bash
  pip install -r requirements-dev.txt
  SITE_PACKAGES=$(pip show aws-glue-sessions | grep Location | awk '{print $2}')
  jupyter kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_pyspark
  jupyter kernelspec install $SITE_PACKAGES/aws_glue_interactive_sessions_kernel/glue_spark 
  ```

### setup cdk

1. Install CDK
2. Install deps
   ```bash
   pip install -r requirements.txt
   ```
3. Bootstrap account
   ```bash
   cdk bootstrap
   ```

### Deploy to dev env

```bash
cdk deploy infrastructure
```

### Deploy through pipeline

1. Create a repo by deploying the pipeline stack
2. Push code to repo
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





You should explore the contents of this project. It demonstrates a CDK app with an instance of a stack (`infrastructure_stack`)
which contains an Amazon SQS queue that is subscribed to an Amazon SNS topic.

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization process also creates
a virtualenv within this project, stored under the .venv directory.  To create the virtualenv
it assumes that there is a `python3` executable in your path with access to the `venv` package.
If for any reason the automatic creation of the virtualenv fails, you can create the virtualenv
manually once the init process completes.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

You can now begin exploring the source code, contained in the hello directory.
There is also a very trivial test included that can be run like this:

```
$ pytest
```

To add additional dependencies, for example other CDK libraries, just add to
your requirements.txt file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
