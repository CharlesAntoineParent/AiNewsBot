## v1.0.0 (2024-09-11)

### Feat

- **API-KEY**: Added az keyvault as the manager of api key
- **api**: added all working apis
- **scrapper-&-paperchooser**: scrapper app and tests implemented, paperchooser app implemented

### Fix

- **Test**: Bad call to azure function making the tests fail
- **pydantic**: Fix warning pydantic that causes test failure
- **CI-deploy**: Added the old config
- **CI-deployment**: Fix type in azure registery name
- **CI-deployment**: Modified connection to azure registery
- **CI-deployment**: Switch login version
- **CI-deploy**: remove connection to docker hub
- **ci**: test new pull image
- **CI**: Fix docker hub login
- **deploy-ci**: remove condition for skip
- **deploy-ci**: added container into deploy job
- **Deployment-ci**: Fix docker hub login
- **Deployment**: Fix docker hub connection
- **Deployment**: Fix container build and push task
- **paperchooser**: Fix return type, module name and getattr function. All in paperchooser
