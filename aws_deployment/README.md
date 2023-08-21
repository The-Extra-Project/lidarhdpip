
# lidarhd infrastructure deployment using CDK Python package.


This gives the general scripts for the reproduction of the tech stack that we have implemented on the lidarhd infrastructure. 

## Diaclaimer:

This implementation has neither being put in actual production or has been tested for security. thus its only for demonstration purposes only and if someone is interested to put the application on prod: please feel free to reachout to the extra labs team.

## Build steps:

1. you need to have the AWS account setup along with insure that your logged in account has the sufficient IAM policies in order to login. else if 



2. The `cdk.json` file is configured to use the run using poetry pacakge, thus first you need to run 
    - `poetry shell`command in order to be able to setup the local virtualenv
    - Run the 'cdk synth' command in order to compile the cloudtemplate.
        - run again the command 'CDK bootstrap' in case the tempalte needs other parameters (as defined in the .env.example) of the given transaction.

3. also WIP: ability to test the application deployment (unit tests), 

## other Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation
