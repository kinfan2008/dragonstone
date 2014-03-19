import os



def populate():
    python_User = add_User('Python','000000','tylu6244841@126.com')

    python_UserProfile=add_UserProfile(user=python_User)

    add_Experiment(userId=python_UserProfile,title="Official Python Tutorial",payment=100,description='sadadadadadadad',startTime='2014-03-06',endTime='2014-03-10',maxPosition = 8)

    add_Experiment(userId=python_UserProfile,title="Official college Tutorial",payment=200,description='sadadadadadadad',startTime='2014-03-07',endTime='2014-03-11',maxPosition=8)
    
    add_Experiment(userId=python_UserProfile,title="Official Python Tutorial",payment=500,description='sadadadadadadad',startTime='2014-03-08',endTime='2014-03-15',maxPosition=8)

    fan_User = add_User('fan','000000','tylu6244841@126.com')

    fan_UserProfile=add_UserProfile(user=fan_User)
    add_Experiment(userId=fan_UserProfile,title="Official fan Tutorial",payment=700,description='sadadadadadadad',startTime='2014-03-03',endTime='2014-03-12',maxPosition=8)

    add_Experiment(userId=fan_UserProfile,title="Official fan2 Tutorial",payment=800,description='sadadadadadadad',startTime='2014-03-04',endTime='2014-03-14',maxPosition=8)

def add_UserProfile(user,website="http://docs.python.org/2/tutorial/",gender='Male',educationLevel='Master',firstLanguage='English',age=0):
    p = UserProfile.objects.get_or_create(user=user,website=website,age=age,gender=gender,educationLevel=educationLevel,firstLanguage=firstLanguage)[0]
    return p

def add_User(name,password,email):
    c =User.objects.get_or_create(username=name,password=password,email=email)[0]
    return c

def add_Experiment(userId,title,payment,description,startTime,endTime,maxPosition,currentOffer=0,isOverdue=True,educationDemand='Master',language='English'):
    
    x =Experiment.objects.get_or_create(userId=userId,title=title,payment=payment,description=description,educationDemand=educationDemand,startTime=startTime,endTime=endTime,maxPosition=maxPosition,currentOffer=currentOffer,isOverdue=isOverdue,language=language)[0]
    return x

def add_ApplyRecord(applicantId,experimentId,ApplyTime,isProcessed=True,isOffered=False,isAccepted=False,isValid=True):
    k = ApplyRecord.objects.get_or_create(applicantId=applicantId,experimentId=experimentId,ApplyTime=ApplyTime,isProcessed=isProcessed,isOffered=isOffered,isAccepted=isAccepted,isValid=isValid)[0]
    return k
if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE','dragon_stone.settings')
    from dragon.models import UserProfile,Experiment,ApplyRecord
    from django.contrib.auth.models import User
    populate()
