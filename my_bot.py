# import all the modules
from search import *
from telethon import functions, types
from telethon.sync import TelegramClient
from telethon import TelegramClient, sync, events
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon.tl.functions.channels import JoinChannelRequest

# set credentials
api_id = *******
api_hash = '********************************'
username = '**********'
phone='+91XXXXXXXXXX'
token='XXXXXXXXXX:***************-*******************'

# create client object and establish connection
client = TelegramClient('my_bot', api_id, api_hash)
client.connect()

# check for the authorization
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

# create functions to fetch all the channels, groups, and bots
def fetch_all(keyword):
	channels, groups, bots, join_channels, join_groups=search(keyword)
	return channels, groups, bots, join_channels, join_groups

# display all the channels, groups and bots
def display_all_fetched(channels, groups, bots):
	print('Channels Fetched are\n')
	for channel in channels:
		print(channel)

	print('\nGroups Fetched are\n')
	for group in groups:
		print(group)

	print('\nBots Fetched are\n')
	for bot in bots:
		print(bot)

# create functions to join all the public channels and groups
def join_all_fetched(join_channels, join_groups):
        print('Channels\n')
        for channel in join_channels[:10]:
            try:
                client(JoinChannelRequest(channel))
                print('Channel',channel,'joined Successfully!!')
            except Exception as e:
                continue

        print('\nGroups\n')
        for group in join_groups[:10]:
            try:
                client(JoinChannelRequest(group))
                print('Group',group,'joined Successfully!!')    
            except Exception as e:
                continue

# display all the joined channels and groups
def display_all():
        entities={'channel':[],'group':[]}
        for dialog in client.iter_dialogs():
            if dialog.is_group:
                entities['group'].append([dialog.name,dialog.entity.participants_count])
            elif dialog.is_channel:
                entities['channel'].append([dialog.name, dialog.entity.participants_count])
                
        print('Groups are: \n')
        for group in entities['group']:
            print(group)

        print('\nChannels are: \n')
        for channel in entities['channel']:
            print(channel)

# create a function to set details of members of each channel or groups
def set_member_details():
	channel_username=input('\nEnter the username: ')
	participants=client.get_participants(channel_username, aggressive=True)
	members=[]
	for participant in participants:
	    member={}
	    member['id']=participant.id
	    member['access_hash']=participant.access_hash
	    member['first_name']=participant.first_name
	    member['last_name']=participant.last_name
	    member['username']=participant.username
	    member['status']=participant.status
	    member['is_Bot']=participant.bot
	    member['from_contacts']=participant.contact
	    member['is_deleted']=participant.deleted
	    members.append(member)

	for member in members:
	    print(f"""
		Name: {member['first_name']}
		Username: {member['username']}
		UserID: {member['id']}
		Hash: {member['access_hash']}
		Status: {member['status']}
		is_Bot: {member['is_Bot']}
		from_contact: {member['from_contacts']}
		is_deleted: {member['is_deleted']}
		""")
	return members


# broadcast message to all the users
def broadcast_message(members):
	try:
	    message=input('Enter the Message: \n')
	    for member in members:
	        user_id=member['id']
	        user_hash=member['access_hash']
	        
	        receiver = InputPeerUser(user_id, user_hash)
	        client.send_message(receiver, message, parse_mode='html')
	    print('Message Sent Succesfully!!!!')
	except Exception as e: 
	    print(e);


# menu driven
if __name__=='__main__':
	keyword=input('Enter the Keyword to be searched: ')
	channels, groups, bots, join_channels, join_groups=fetch_all(keyword)
	display_all_fetched(channels, groups, bots)
	join_all_fetched(join_channels, join_groups)
	display_all()
	members=set_member_details()
	broadcast_message(members)
	
	# disconnect cient
	client.disconnect()

