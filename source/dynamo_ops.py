import boto3
access = 'AKIAI3MUOV6TSGLHK6NA'
secret = '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'

requests = [
        {
         'url' : 'https://s3.amazonaws.com/scanapprakesh/test.txt',
         'location' : '/home/rakesh/Desktop/test.txt',
         'email' : 'rake@nexb.com',
         'status' : 'NOT STARTED'
         },
        {
         'url' : 'https://s3.amazonaws.com/scanapprakesh/test1.txt',
         'location' : '/home/rakesh/Desktop/test1.txt',
         'email' : 'rakes@nexb.com',
         'status' : 'NOT STARTED'
         }
        ]

resource = boto3.resource('dynamodb',region_name='us-west-1', aws_access_key_id=access, aws_secret_access_key=secret)
table = resource.Table('scanapp')
# for request in requests:
#     table.put_item(
#         Item=request
#         )

item  = table.get_item(Key={'email':'rakes@nexb.com', 'status':'NOT STARTED'})
print item['Item']