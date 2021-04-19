# 2021-b-qgis-google-sheets-plugin

## Testing

To access the test application it's necessary to add tester's GDrive address in Google Cloud Platform by admin:

1. install by OSGeo4W Shell

```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

2. download python script, credentials.json, test data (`sample/eq-data.csv`) from GitHub

3. upload csv file to GDrive

4. in case of using another data it's necessary to change the file name in the row 106

5. run python script in QGIS
