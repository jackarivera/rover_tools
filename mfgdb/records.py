import boto3
import os
import json

class ManufacturingRecordDb():
    def __init__(
        self, 
        access_id, 
        access_key, 
        db_info_path=(os.path.dirname(__file__) + "/db_info.json"), 
        table_name="ManufacturingRecords", 
        region="us-west-2"
    ):
        
        # register input args
        self.access_id = access_id
        self.access_key = access_key
        self.table_name = table_name
        self.region = region

        # update environment vars
        os.environ['AWS_DEFAULT_REGION'] = self.region

        # create the db resource
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id = self.access_id,
            aws_secret_access_key = self.access_key
        )

        # create the filestore resource (for logs)
        self.s3 = boto3.client(
            's3',
            aws_access_key_id = self.access_id,
            aws_secret_access_key = self.access_key
        )

        # create the table object
        self.table = self.dynamodb.Table(self.table_name)

        # load a list of mandatory data
        self.db_info_path = db_info_path
        with open(self.db_info_path, "r") as read_file:
            self.db_mandatory_cols = json.load(read_file)['MandatoryColumns']

    def get_robot_information(self, serial_number:str):
        
        response = self.table.get_item(
            Key={
                'SerialNumber': serial_number
            }
        )

        if 'Item' not in response:
            print("Serial Number %s not found in DB!" % serial_number)
            return None
        
        print("ROBOT INFORMATION FOR SERIAL %s" % response['Item']['SerialNumber'])
        for key, value in response['Item'].items():
            if 'SerialNumber' in key:
                continue
            print(key, value)

        return response['Item']

    def register_robot(self, item_for_db:dict):
        
        # ensure that all the required columns are present
        for col in self.db_mandatory_cols:
            if col not in item_for_db:
                print('Missing mandatory input for manufacturing DB. DEVICE NOT ADDED TO DB. Please add required information and try again')
                return

        # push item to db
        print("ADDING ROBOT %s to DB" % item_for_db['SerialNumber'])
        self.table.put_item(
            Item=item_for_db
        )

        # validate that the item was pushed successfully
        confirmation = self.get_robot_information(item_for_db['SerialNumber'])
        if confirmation is not None:
            print('Robot %s successfully added to manufacturing db' % item_for_db['SerialNumber'])
        else:
            print('Failed to add robot to manufacturing DB. Contact Engineering for help')

        return confirmation

    def publish_install_log(self, logfile_path:str, serial_number:str):
        try:
            response = self.s3.upload_file(logfile_path, "install-logs", serial_number + ".log")
        except:
            print(response)
            return False

        return True

    def get_local_credentials(credential_file=(os.path.dirname(__file__) + "/credentials.json")):
        try:
            with open(credential_file, "r") as read_file:
                credentials = json.load(read_file)

            return credentials["ACCESS_ID"], credentials["ACCESS_KEY"]
        except IOError as e:
            print('Unable to find local credentials with error %s' % e)
            return None, None

    def test_credentials(access_id, access_key):
        os.environ['AWS_DEFAULT_REGION'] = "us-west-2"
        sts = boto3.client(
            'sts',
            aws_access_key_id = access_id,
            aws_secret_access_key = access_key
        )
        try:
            sts.get_caller_identity()
        except boto3.exceptions.ClientError:
            return False

        return True


                

if __name__ == '__main__':
    access_id, access_key = ManufacturingRecordDb.get_local_credentials()
    db = ManufacturingRecordDb(access_id, access_key)
    db.get_robot_information("000000")
    db.register_robot(
        {
            "SerialNumber":"123457",
            "RobotModel":"Mini",
            "FinalAssemblyNumber":"A700-FOOBAR",
            "FinalAssemblyRevision":"ZZZZZ",
            "FirmwareVersion":"noneofyourbusiness",
            "GUID":"????",
            "Operator":"Obviously TOM",
            "Date":"today",
            "Time":"now",
            "CalibrationData":"calibratedAF",
            "TestResults":"all clear",
            "TestedBy":"dingusboi",
            "InspectionData":"it was all good homie",
            "InspectedBy":"get bent"
        }
    )
    


    

    


