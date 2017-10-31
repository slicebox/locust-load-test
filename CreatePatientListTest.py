from locust import HttpLocust, TaskSet, task
import random

auth_token = "Basic YWRtaW46YWRtaW4="

auth_dict = {'Authorization': auth_token}

class CreatePatientListTaskSet(TaskSet):

    count = 500

    # @task(1)
    def get_patients(self):
        url = "/metadata/patients" + ("" if  self.count < 0 else "?count={0}".format(self.count))
        r = self.client.get(url, headers=auth_dict)
        patient_id_list = [patient_obj['id'] for patient_obj in r.json()]
        for patient_id in patient_id_list:
            sr = self.client.get("/metadata/studies?patientid={patient_id}".format(patient_id=patient_id), headers=auth_dict, name="Get Studies")
            study_id_list = [study_obj['id'] for study_obj in sr.json()]
            for study_id in study_id_list:
                str = self.client.get("/metadata/series?studyid={study_id}".format(study_id=study_id), headers=auth_dict, name="Get Series")
                series_id_list = [series_obj['id'] for series_obj in str.json()]
                for series_id in series_id_list:
                    self.client.get("/metadata/series/{id}/seriestypes".format(id=series_id), headers=auth_dict, name="Get Series Types")

    # @task(1)
    def get_patients_by_flatseries(self):
        url = "/metadata/flatseries" + ("" if  self.count < 0 else "?count={0}".format(self.count))
        r = self.client.get(url, headers=auth_dict)
        series_id_list = [flat_obj['series']['id'] for flat_obj in r.json()]
        for series_id in series_id_list:
            # print("Patient {0} Study {1} Series {2}".format(patient_id, study_id, series_id))
            r = self.client.get("/metadata/series/{id}/seriestypes".format(id=series_id), headers=auth_dict, name="Get Series Types")
            # print("{0} {1}".format(series_id, r.json()))

    @task(1)
    def get_patients_by_flatseries_with_bulk_types(self):
        url = "/metadata/flatseries" + ("" if  self.count < 0 else "?count={0}".format(self.count))
        r = self.client.get(url, headers=auth_dict)
        series_id_list = [flat_obj['series']['id'] for flat_obj in r.json()]
        json_msg = {"ids": series_id_list}
        r = self.client.post("/seriestypes/series/query", headers=auth_dict, json=json_msg)
        # for obj in r.json():
        #     print(obj)

class MyLocust(HttpLocust):
    task_set = CreatePatientListTaskSet
    min_wait = 1 * 100
    max_wait = 10 * 100

