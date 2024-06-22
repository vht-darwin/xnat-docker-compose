import pyxnat
import yaml
import os

with open("upload_files_config.yaml") as stream:
  config_dict = yaml.safe_load(stream)


#project_id = 'darwin'
#subject_id = "trainingdata"
#resource_name = 'NIFTI'
#server_location = 'http://vht-dev.shef.ac.uk/:80'

xnat = pyxnat.Interface(server=config_dict["server_location"], user='admin', password='admin')

#print(xnat.projects())

project = xnat.select.project(config_dict["project_id"])
subject = project.subject(config_dict["subject_id"])
resource = subject.resource(config_dict["resource_name"])

#file_names = os.path(config_dict["local_data_folder"]).isfile()

file_names = (file for file in os.listdir(config_dict["local_data_folder"]) if os.path.isfile(os.path.join(config_dict["local_data_folder"], file)))
#resource.file('Thing').get()

for file_name in file_names:
  print(f"Uploading {file_name}")
  resource.file(file_name).insert(config_dict['local_data_folder'] + file_name)
  print(f"Uploaded {file_name}")

