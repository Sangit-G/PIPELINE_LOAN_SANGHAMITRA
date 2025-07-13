STEP WISE EXECUTION OF PIPELINE PROJECT FOR DETERMINING WHETHER A PERSON WILL REPAY THE LOAN ON TIME OR WILL BE A DEFAULTER BY NOT REAYING ON TIME OR UNABLE TO REPAY.

      Prerequisites- Github Account, Vs-code,Mysql Workbench, Streamlit app.
                 a)Firstly i have created a Github repository named- "PIPELINE_LOAN_SANGHAMITRA" and then in Vs-code created my virtual environment workspace and there i synced my github 
                  repo with vs-code.
                  
                 b)Next i will create a file called .gitignore to remove or delete those files/packages that is not required for us in our project . It will be created in git hub repo and 
                 then pull it in vs code.
                 
                 c)Next create all necessary files and folder reuired for my project to execute--
                      i)Notebook Folder
                        .DATA Folder
                          .Loan_Default.CSV File
                          .Pipeline_Project.ipynb File
                      ii)Setup.py File - For creatung my ML prject as a package so that others can use it too.
                    iii)requirements.txt File and containing all necessary libraries to install at once.
                    iv)src(source) Folder
                         .Components Folder-all modules we will be creating i.e. Data_ingestion,Data_transformation,model_trainer and using.
                            .__init__.py- so that python understands components Folder as a package.
                            .Data_ingestion.py- to read data from database and fetching in Vscode my project folder, then splitting data into train,test,raw etc.
                            .Data_tranformation.py-after fetching data to transform data by changing data types, encoding,imputing,scaling.
                            .model_trainer.py-all training code, all models used, evaluating my model.

                          .pipeline-
                             .__init__.py-To recognize pipeline as a package.
                             .training_pipeline.py-It will trigger all components.
                             .prediction_pipeline.py-After training it will predict for the new data.

                          .exception.py-For exception handling purpose.
                          
                          .loggers.py-Keeps code modular and organized, especially in large projects and triggers the components Folder.
                          
                          .utils.py-Any functionalities that will be written in a common way, that can be used everywhere.
                          
                  v)app.py-contains streamlit app code for running my model.
                  vi) Artifacts,Logs folders get created automatically when they gets triggered on model training as they contains train,test.raw data and every informations
                  about each stages that gets invoked upon training.
                  
