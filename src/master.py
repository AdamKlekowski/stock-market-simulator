import os
i=0
for startIndex in range(0,2500,100):
	for num in range(0,301,50):
		f=open('./args','w')
		f.write(str(i)+','+str(startIndex)+','+str(num))
		f.close()
		i+=1
		os.system('python3 main.py')
		
