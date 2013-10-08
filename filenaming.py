

from datetime import date, time, datetime

str_prefix="scn_"

num_iter=15         # int: Number of iterations to try
str_date=""         # String: current date as string 
str_time=""         # String: current time as string
str_datetime_now="" # String: combined time and date to an unique string
str_filename=""

#now=date.today()

#str_date=now.strftime("%Y-%m-%d")
#str_date=date.today().strftime("%Y-%m-%d")
str_date=datetime.now().strftime("%Y-%m-%d")
str_time=datetime.now().strftime("%H_%M_%S")


str_out="Heute ist: "+str_date+". Uhrzeit ist: "+str_time
print(str_out)


str_datetime_now=str_date+"_-_"+str_time
str_filename=str_prefix+str_datetime_now+".jpg"
str_out="Filename: "+str_filename
print(str_out)

i=0

while i<=num_iter:
    str_filename=str_prefix+str_datetime_now+"_"+str(i)+".jpg"
    print(str_filename)
    i=i+1
#end while

