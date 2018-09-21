# Deployment
A deployment strategy breaks the run-time dependency on the git source tree
## Architecture
The `deployment` subdirectory contains links to the files to be deployed. The 
relative path of these files is the parent directory of `deployment:` ie `drs-deposit/DRS-BATCH-PROCESSING`
## Implementation
These bash scripts live in the `deployment` directory
+ `makeLinks` contains an in-file dictionary of files and directories.
+ `copylinksToBin` copies the links in its directory to another directory
## Usage
### Adding files to the deployment
+ Make sure the file is accessible from `deployment/..`
+ Add its name to the `here` document in `makeLinks`
### Removing files from the deployment
+ Remove the link from the `deployment` folder
+ Remove the file from the `here` document in `makeLinks`
### Running a deployment
Do this after the content list is adjusted, or if there are no new
contents, only changed ones
+ cd `...drs-deposit/DRS-BATCH-PRoCESSING/deployment/`
+ `./copyLinksToBin [folder, default='~/bin']`
The optional argument can be any folder. 

**tip** To be useful, it should be a folder on your path.