import pyxnat
import yaml
import os
from faker import Faker
from faker.providers import DynamicProvider
import uuid

def define_fakers() -> Faker:
  fake = Faker()
  gender_provider = DynamicProvider(
      provider_name="gender",
      elements=["male", "female"],
  )
  fake.add_provider(gender_provider)

  hand_provider = DynamicProvider(
      provider_name="hand",
      elements=["left", "right"],
  )
  fake.add_provider(hand_provider)

  education_provider = DynamicProvider(
      provider_name="education",
      elements=list(map(str, list(range(0, 5)))),
  )
  fake.add_provider(education_provider)

  race_provider = DynamicProvider(
      provider_name="race",
      elements=["American Indian/Alaska Native", "Asian", "Black or African American", "Native Hawaiian or other Pacific Islander", "White", "Unknown"],
  )
  fake.add_provider(race_provider)

  ethnicity_provider = DynamicProvider(
      provider_name="ethnicity",
      elements=["African", "Caribbean", "Indian", "Japanese", "Korean", "European/Anglo Saxon", "Latin American", "Arabic", "Vietnamese"],
  )
  fake.add_provider(ethnicity_provider)

  height_provider = DynamicProvider(
      provider_name="height",
      elements=list(map(str, list(range(60, 78)))),
  )
  fake.add_provider(height_provider)

  weight_provider = DynamicProvider(
      provider_name="weight",
      elements=list(map(str, list(range(99, 300)))),
  )
  fake.add_provider(weight_provider)

  recuritment_source_provider = DynamicProvider(
      provider_name="recruitment_source",
      elements=["source1", "source2", "source3"],
  )
  fake.add_provider(recuritment_source_provider)

  return fake

fake = define_fakers()

with open("upload_files_config.yaml") as stream:
  config_dict = yaml.safe_load(stream)


#project_id = 'darwin'
#subject_id = "trainingdata"
#resource_name = 'NIFTI'
#server_location = 'http://vht-dev.shef.ac.uk/:80'

xnat = pyxnat.Interface(server=config_dict["server_location"], user='admin', password='admin')

#print(xnat.projects())

project = xnat.select.project(config_dict["project_id"])
#subject = project.subject(config_dict["subject_id"])
#resource = subject.resource(config_dict["resource_name"])

#file_names = os.path(config_dict["local_data_folder"]).isfile()

file_names = (file for file in os.listdir(config_dict["local_data_folder"]) if os.path.isfile(os.path.join(config_dict["local_data_folder"], file)))
#resource.file('Thing').get()
file_names = sorted(file_names)
file_names_data = file_names[::2]
file_names_labels = file_names[1::2] 

#for file_name in file_names:
for pos, file_name_data in enumerate(file_names_data):
  print("Creating Subject and Resource")
  id = uuid.uuid4()
  subject = project.subject(f'UHS-{pos}')

  subject.create()
  #subject.attrs.set('dob', "12/12/1990")
  subject.attrs.set('dob', str(fake.date_of_birth(minimum_age=18,maximum_age=112)))
  subject.attrs.set('gender', fake.gender())
  subject.attrs.set('handedness', fake.hand())
  #subject.attrs.set('education', fake.education())
  subject.attrs.set('race', fake.race())
  subject.attrs.set('ethnicity', fake.ethnicity())
  subject.attrs.set('height', fake.height())
  subject.attrs.set('weight', fake.weight())
  subject.attrs.set('recruitment_source', fake.recruitment_source())
  resource = subject.resource('mri_scan')
  print(f"Uploading {file_name_data}")
  resource.create()
  resource.file(file_name_data).insert(config_dict['local_data_folder'] + file_name_data)
  print(f"Uploading {file_names_labels[pos]}")
  resource.file(file_names_labels[pos]).insert(config_dict['local_data_folder'] + file_names_labels[pos])
  print(f"Uploaded {file_name_data}")

