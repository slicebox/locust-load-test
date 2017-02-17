from locust import HttpLocust, TaskSet, task
from os import listdir
import os
from collections import defaultdict
import random
import json
import requests
import binascii

auth_token = "Basic YWRtaW46YWRtaW4="

auth_dict = {'Authorization': auth_token}

class MetadataTaskSet(TaskSet):

    patient_id_list = []

    patient_id = 0

    count = 10

    study_date_list = []

    report_id_list = []

    import_session_id = ""

    # def on_start(self):
    #     self.id = MetadataTaskSet.grasshopper
    #     MetadataTaskSet.grasshopper += 1

    @task
    def get_patients(self):
        # print("Get patients")
        study_id_list = []
        series_id_list = []
        url = "/metadata/patients" + ("" if  self.count < 0 else "?count={0}".format(self.count))
        # r = self.client.get(url, headers=auth_dict, name="Get Patients" if self.count < 0 else "Get Patients, count: {0}".format(self.count))
        r = self.client.get(url, headers=auth_dict)
        self.patient_id_list = [patient_obj['id'] for patient_obj in r.json()]
        print("Number of patients found = {0}".format(len(self.patient_id_list)))
        for patient_id in self.patient_id_list:
            sr = self.client.get("/metadata/studies?patientid={patient_id}".format(patient_id=patient_id), headers=auth_dict, name="Get Studies")
            study_id_list = [study_obj['id'] for study_obj in sr.json()]
            for study_id in study_id_list:
                str = self.client.get("/metadata/series?studyid={study_id}".format(study_id=study_id), headers=auth_dict, name="Get Series")
                series_id_list = [series_obj['id'] for series_obj in str.json()]
                for series_id in series_id_list:
                    self.client.get("/metadata/series/{id}/seriestags".format(id=series_id), headers=auth_dict, name="Get Series Tags")

class MyLocust(HttpLocust):
    task_set = MetadataTaskSet
    min_wait = 1 * 1000
    max_wait = 10 * 1000

