from locust import HttpLocust, TaskSet, task
import random

auth_token = "Basic YWRtaW46YWRtaW4="

auth_dict = {'Authorization': auth_token}


class MetadataTaskSet(TaskSet):
    patient_id_list = []
    study_id_list = []
    series_id_list = []
    seriestype_id_list = []
    seriestag_id_list = []
    image_id_list = []

    def on_start(self):
        self.get_patients()
        self.get_studies()
        self.get_series()
        self.get_seriestags()
        self.set_or_create_seriestype()


    @task(1)
    def get_patients(self):
        r = self.get("/metadata/patients")
        self.patient_id_list = [patient_obj['id'] for patient_obj in r.json()]

    @task(1)
    def query_patients(self):
        json_msg = {
            "startIndex": 0, "count": 10, "order": {
                "orderBy": "patientID",
                "orderAscending": True
            },
            "queryProperties": [
                {
                    "propertyName": "patientID",
                    "operator": "like",
                    "propertyValue": "Pat"
                }
            ]
        }
        r = self.client.post("/metadata/patients/query", headers=auth_dict, json=json_msg)

    @task(1)
    def get_patient(self):
        r = self.get("/metadata/patients/{0}".format(get_random_id(self.patient_id_list)), "getPatient")

    @task(1)
    def get_patient_images(self):
        r = self.get("/metadata/patients/{0}/images".format(get_random_id(self.patient_id_list)), "getPatientImages")
        self.image_id_list = [image_data_obj['id'] for image_data_obj in r.json()]

    @task(1)
    def get_studies(self):
        r = self.get("/metadata/studies?patientid={0}".format(get_random_id(self.patient_id_list)), "getStudies")
        self.study_id_list = [study_obj['id'] for study_obj in r.json()]

    @task(1)
    def query_studies(self):
        json_msg = {
            "startIndex": 0, "count": 10,
            "order": {
                "orderBy": "studyDate",
                "orderAscending": True
            },
            "queryProperties": [
                {
                    "propertyName": "studyInstanceUID",
                    "operator": "like",
                    "propertyValue": "1.2"
                }
            ]
        }
        r = self.client.post("/metadata/studies/query", headers=auth_dict, json=json_msg)

    @task(1)
    def get_study(self):
        r = self.get("/metadata/studies/{0}".format(get_random_id(self.study_id_list)), "getStudy")

    @task(1)
    def get_study_images(self):
        r = self.get("/metadata/studies/{0}/images".format(get_random_id(self.study_id_list)), "getStudyImages")
        self.image_id_list = [image_data_obj['id'] for image_data_obj in r.json()]

    @task(1)
    def get_series(self):
        r = self.get("/metadata/series?studyid={0}".format(get_random_id(self.study_id_list)), "getSeries")
        self.series_id_list = [series_obj['id'] for series_obj in r.json()]

    @task(1)
    def query_series(self):
        json_msg = {"startIndex": 0, "count": 10,
                    "order": {
                        "orderBy": "seriesDate",
                        "orderAscending": True
                    },
                    "queryProperties": [
                        {
                            "propertyName": "seriesInstanceUID",
                            "operator": "like",
                            "propertyValue": "1.2"
                        }
                    ]
                    }
        r = self.client.post("/metadata/series/query", headers=auth_dict, json=json_msg)

    @task(1)
    def get_series_by_id(self):
        r = self.get("/metadata/series/{0}".format(get_random_id(self.series_id_list)), "getSeriesById")

    @task(1)
    def get_series_source(self):
        r = self.get("/metadata/series/{0}/source".format(get_random_id(self.series_id_list)), "getSeriesSource")

    @task(1)
    def delete_seriestypes(self):
        r = self.client.delete("/metadata/series/{0}/seriestypes".format(get_random_id(self.series_id_list)), headers=auth_dict, name="deleteSeriesType")

    @task(1)
    def get_seriestypes(self):
        r = self.get("/metadata/series/{0}/seriestypes".format(get_random_id(self.series_id_list)), "getSeriesTypes")

    @task(1)
    def delete_seriestype(self):
        r = self.client.delete("/metadata/series/{series_id}/seriestypes/{seriestype_id}".format(
            series_id=get_random_id(self.series_id_list),seriestype_id=get_random_id(self.seriestype_id_list)),
                               headers=auth_dict, name="deleteSeriesTypes")

    @task(1)
    def put_seriestype(self):
        r = self.client.put("/metadata/series/{series_id}/seriestypes/{seriestype_id}".format(
            series_id=get_random_id(self.series_id_list), seriestype_id=get_random_id(self.seriestype_id_list)),
                                headers=auth_dict, name="putSeriestype")

    @task(1)
    def get_seriestags(self):
        r = self.get("/metadata/series/{0}/seriestags".format(get_random_id(self.series_id_list)), "getSeriesTags")

    @task(1)
    def post_seriestags(self):
        json_msg={"id": -1, "name": "locust"}
        r = self.client.post("/metadata/series/{0}/seriestags".format(get_random_id(self.series_id_list)),
                             headers=auth_dict, json=json_msg, name="postSeriesTags")

    @task(1)
    def delete_seriestag(self):
        r = self.client.delete("/metadata/series/{series_id}/seriestags/{seriestag_id}".format(
            series_id=get_random_id(self.series_id_list), seriestag_id=get_random_id(self.seriestag_id_list)),
            headers=auth_dict, name="deleteSeriesTags")

    @task(1)
    def get_seriestags(self):
        r = self.get("/metadata/seriestags")
        self.seriestag_id_list = [tag_obj['id'] for tag_obj in r.json()]

    @task(1)
    def get_imagesdata(self):
        r = self.get("/metadata/images?seriesid={0}".format(get_random_id(self.series_id_list)), name="getImagesData")
        self.image_id_list = [image_data_obj['id'] for image_data_obj in r.json()]

    @task(1)
    def query_imagesdata(self):
        json_msg = {
            "startIndex": 0,
            "count": 10,
            "queryProperties": [
                {
                    "propertyName": "imageType",
                    "operator": "like",
                    "propertyValue": "ORIGINAL"
                }
            ]
        }
        r = self.client.post("/metadata/images/query", headers=auth_dict, json=json_msg)

    @task(1)
    def get_imagedata(self):
        r = self.get("/metadata/images/{0}".format(get_random_id(self.image_id_list)), name="getImageData")

    @task(1)
    def get_flatseries(self):
        r = self.get("/metadata/flatseries")

    @task(1)
    def get_flatseries_by_id(self):
        r = self.get("/metadata/flatseries/{0}".format(get_random_id(self.series_id_list)), name="getFlatSeriesById")

    @task(1)
    def query_flatseries(self):
        json_msg =  {"startIndex": 0, "count": 10,
                     "order": {
                         "orderBy": "patientId",
                         "orderAscending": True
                     },
                     "queryProperties": [
                         {
                             "propertyName": "patientName",
                             "operator": "like",
                             "propertyValue": "Patient"
                         }
                     ]
                     }
        r = self.client.post("/metadata/flatseries/query", headers=auth_dict, json=json_msg)

    def set_or_create_seriestype(self):
        r = self.get("/seriestypes")
        self.seriestype_id_list = [st_obj['id'] for st_obj in r.json()]
        if (len(self.seriestype_id_list) < 1):
            json_msg = {"id":-1,"name":"LocustSeriesType"}
            r = self.client.post("/seriestypes/", headers=auth_dict, json=json_msg)
            self.seriestype_id_list = [r.json()['id']]

    def get(self, url, name=""):
        if (len(name)>0):
            return self.client.get(url, headers=auth_dict, name=name)
        return self.client.get(url, headers=auth_dict)


def get_random_id(ids_array):
    if (len(ids_array) > 0):
        return random.choice(ids_array)
    return 0


class MyLocust(HttpLocust):
    task_set = MetadataTaskSet
    min_wait = 1 * 1000
    max_wait = 10 * 1000
