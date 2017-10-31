from locust import HttpLocust, TaskSet, task
import json

auth_token = "Basic YWRtaW46YWRtaW4="

auth_dict = {'Authorization': auth_token}

class FileUploadTaskSet(TaskSet):
    grasshopper = 0
    id = ""

    data = {'ct':bytearray(0), 'nm':bytearray(0)}
    # ba = bytearray(0)

    indexes = {"patient_name":797, "patient_id":813, "series":1238, "study":1176, "instance":480}

    import_session_id = ""

    def on_start(self):
        self.id = "{:0>3}".format(FileUploadTaskSet.grasshopper)
        FileUploadTaskSet.grasshopper += 1
        self.create_import_session()
        f = open("data/nm.dcm", "rb")
        self.data['nm'] = bytearray(f.read())
        f.close()
        f = open("data/ct.dcm", "rb")
        self.data['ct'] = bytearray(f.read())
        f.close()

    def change_data(self, data, patient, study, series, instance):
        change_string_in_data(data, self.indexes['patient_name'], patient)
        change_string_in_data(data, self.indexes['patient_id'], patient)
        change_string_in_data(data, self.indexes['study'], study)
        change_string_in_data(data, self.indexes['series'], series)
        change_string_in_data(data, self.indexes['instance'], instance)

    def create_import_session(self):
        json_msg = {"id": -1,"name": "Locust","userId": -1,"user": "","filesImported": 0,"filesAdded": 0,"filesRejected": 0,"created": 0,"lastUpdated": 0}
        r = self.client.post("/import/sessions", headers=auth_dict, json=json_msg, name="Create Import Session")
        self.import_session_id = r.json()['id']

    @task(10)
    def upload_image(self):
        for study in range(2):
            for series in range(2):
                for instance in range(1):
                    self.change_data(self.data['nm'], self.id, study, series, instance)
                    r = self.client.post("/images", headers=auth_dict, data=self.data['nm'], name="Upload Image")
                    print("posting image for patient {0}, study:{1}, series:{2}, instance:{3}\tResponse:{4}".format(self.id, study, series, instance, r))

    @task(10)
    def upload_image_in_import_session(self):
        for study in range(2):
            for series in range(2):
                for instance in range(20):
                    self.change_data(self.data['ct'], self.id, study, series, instance)
                    r = self.client.post("/import/sessions/{0}/images".format(self.import_session_id), headers=auth_dict, data=self.data['ct'], name="Upload Image in Session")
                    print("posting image in import session for patient {0}, study:{1}, series:{2}, instance:{3}\tResponse:{4}".format(self.id, study, series, instance, r))
                    if (r.status_code != 201):
                        print("URL: /import/sessions/{0}/images".format(self.import_session_id))

    # @task(1)
    def delete_patients(self):
        r = self.client.get("/metadata/patients", headers=auth_dict, name="Get Patients for delete")
        self.patient_id_list = [patient_obj['id'] for patient_obj in r.json()]
        for patient_id in self.patient_id_list:
            ir = self.client.get("/metadata/patients/{patient_id}/images".format(patient_id=patient_id), headers=auth_dict, name="Get Images for Patient")
            image_id_list = [image_obj['id'] for image_obj in ir.json()]
            dr = self.client.post("/images/delete", headers=auth_dict, json=image_id_list, name="Delete Images")

def change_string_in_data(data, index, new_value):
    if type(new_value) is not str:
        new_value = str(new_value)
    for letter in new_value:
        data[index] = letter
        index += 1

class MyLocust(HttpLocust):
    task_set = FileUploadTaskSet
    min_wait = 1 * 1000
    max_wait = 10 * 1000

