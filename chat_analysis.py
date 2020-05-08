import re
import matplotlib.pyplot as plt
import emoji
import pandas as pd
import numpy as np



file = open(r'./WhatsApp Chat with Vedika.txt',mode='r',encoding="utf8")  # no uploaded text file for privacy concerns
data = file.read()
file.close()

pattern = re.compile('\d+\/\d+\/\d+[^a-z]\s\d+:\d+\s[a-z]+\s[^a-z]\s([a-zA-Z]+):\s+')  # after removing first line
users = re.findall(pattern,data)


count_messages={}    #dictionary
for each in users:
    if each in count_messages.keys():
        count_messages[each]+=1
    else:
        count_messages[each]=1
print(count_messages)

user1 = ''
user2 = ''
for i in count_messages:
	if user1 == '':
		user1 = i
	else:
		user2 = i

mess1 = [] # messages sent by user1
mess2 = [] # messages sent by user2
time1 = [0]*24
time2 = [0]*24


#finding average message length
messages_split = pattern.split(data)
#print (messages_split[:])
size = 2*(count_messages[user1] + count_messages[user2])


for i in range (1,size,2):
	if messages_split[i] == user1:
		messages_split[i+1] = messages_split[i+1][:-1]  # removing \n
		mess1.append(messages_split[i+1])

	else:
		messages_split[i+1] = messages_split[i+1][:-1]
		mess2.append(messages_split[i+1])

total_mess1 = 0
total_mess2 = 0
for i in range (len(mess1)):
	total_mess1 += len(mess1[i])

for i in range (len(mess2)):
	total_mess2 += len(mess2[i])

avg1 = total_mess1/count_messages[user1]
avg2 = total_mess2/count_messages[user2]

print("%.1f" %avg1, "%.1f" %avg2)





index = 0  #find 1st user occurences
while index<len(data):
	index = data.find(user1+':', index)
	if index == -1:
		break
	string = data[index-11:index-3]
	#print (string)
	time = 0

	if string[0]==' ':
		time = int(string[1])
	else:
		time = int(string[0])*10 + int(string[1])

	if string[len(string)-2] == 'p' and time!=12:
		time += 12

	if string[len(string)-2] == 'a' and time==12:
		time = 0

	time1[time] += 1
	index += len(user1)+1


index = 0  #find 2nd user occurences
while index<len(data):
	index = data.find(user2+':', index)
	if index == -1:
		break
	string = data[index-11:index-3]
	#print (string)
	time = 0
	if ((string[0]<'0' or string[0]>'9') and string [0]!=' ') or string[1]<'0' or string[1]>'9':   #sometimes some values might be strange and not follow format
		index += len(user2)+1
		continue
	if string[0]==' ':
		time = int(string[1])
	else:
		time = int(string[0])*10 + int(string[1])

	if string[len(string)-2] == 'p' and time!=12:
		time += 12

	if string[len(string)-2] == 'a' and time==12:
		time = 0

	time2[time] += 1
	index += len(user2)+1

#finding the golden hour to chat
maximum = 0
gold_index = -1
for i in range (24):
	print(time1[i], time2[i])
	if maximum< min(time1[i], time2[i]):
		gold_index = i
		maximum = min(time1[i], time2[i])

print (maximum, gold_index)

#find most used emoji
def extract_emojis(keys):
    emojis=[]
    message = []
    if keys == user1:
    	message = mess1
    else:
    	message =mess2
    for string in message:
        my_str = str(string)
        for each in my_str:
            if each in emoji.UNICODE_EMOJI:
                emojis.append(each)
    return emojis

emoji_dict={}   #emoji dictionary
print("MOST USED EMOJIS")
for keys in count_messages.keys():
    print(keys)
    emoji_dict[keys] = extract_emojis(keys)
    emoji_df = pd.DataFrame(emoji_dict[keys])
    print(emoji_df[0].value_counts()[:5])


#display graph
x = np.arange(24)
time_merge = [time1, time2] #display 2 bar graphs simultaneously
bar1 = plt.bar(x + 0.00, time_merge[0], color = 'b', width = 0.25)
bar2 = plt.bar(x + 0.25, time_merge[1], color = 'r', width = 0.25)

plt.xlabel("Hours(in military time)")
plt.ylabel("Number of text messages sent")
label = ['Messages sent by ' + user1 + '\n Average length of text = ' + "%.1f" %avg1, 
		 'Messages sent by ' + user2 + '\n Average length of text = ' + "%.1f" %avg2]


plt.xticks(np.arange(min(x), max(x)+1, 1.0)) # to display all x values
plt.legend(label, loc='upper right')

#to get the position of 'Preferred Chat Time'
h1 = bar1[gold_index].get_height()
h2 = bar2[gold_index].get_height()
rect = bar1[gold_index]
height = h1
if h1<h2:
	rect = bar2[gold_index]
	height = h2

plt.text(rect.get_x() + rect.get_width(), height, '%s' % str("PCT"), fontsize = 8, 
	ha='center', va='bottom', bbox=dict(facecolor='yellow', alpha=0.5))



plt.title("WhatsApp Chat Analysis")
plt.tight_layout()
plt.show()

