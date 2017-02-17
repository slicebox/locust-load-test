## Locust - Python Load Test
Load test for Slicebox using Locust, a load testing tool in Python. It will spawn users (called locusts) that represent 
a virtual user who sends requests to the server.
Read more about Locust here: http://docs.locust.io/en/latest/what-is-locust.html

### CreatePatientListTest.py
Simulates creating a list of patients whith information on studies, series, instances and series tags.

If the variable count is set to a positive integer this will limit the number of requested patients and may be used to
simulate pagination. 

### FileUploadTest.py
Upload files to Slicebox. Both uploading routes, i.e. direct and in an import session, are implemented.

The upload functions use the same base file but changes some attributes so Slicebox will not treat them as the same file
for each upload. Every spawned locust will use a different Patient Name and Id. The basic upload function uploads two studies
with two series each and one image in each series. The import session based upload function upload two studies with two 
series and twenty images in each series. 
- upload_image
- upload_image_in_import_session
- delete_patients (Disabled/Commented)

## Instructions to run local
- Important Note: Locust only runs on Python 2.7+ but not Python 3.
- To install locust if you already have Python - run: `pip install locustio`
- To change from the default admin user and password change the auth_token variable in each file
- Run `locust -f TEST_FILE.py --host=https://LINK TO slicebox` in the same folder as the test file to start the tool with bsi-dev as base url.
- Go to http://localhost:8089/
- Input appropriate test values and start the test.
