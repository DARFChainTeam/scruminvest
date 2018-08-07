#Users if this contract get ether and amount of ether is enought variable singup become true for particular address

Users: public({
    project: bool, # why bool? address? - 
  #	project_address: address,
    signup: bool, # ?
  	
	   
}[address])

#Create Projects and set addition data of project's describe

Projects: public({
    projectID: int128,
    project_owner_address: address,
   	project_token: address(ERC20),
    IPFSDescribe: bytes32, # address of project in IPFS
   }[int128])

# Depo for user's ethers
ether_depo:public(wei_value)
#Token Darf
darftoken:address(ERC20)
#Адресс куда будут перечилятся денежки
beneficiar:address
#id of UserStory
nextUserStoryID:int128
#id of Project
nextProjectID:int128
#id of UserList
nextUserListID:int128

  
UserList:
  ({address:address,
   summa:wei_value,
   UserStoryID:int128
   }[int128])

# A list of the owners addresses (there are a maximum of 5 owners)
owners: public(address[5])

UserStory: public({
    projectID:int128,
    user_address:address,
  	UserStoryID:int128, 
    IPFSHash: bytes32,
    project_accept: bool,
    user_signin:bool, # several users?
    project_signin:bool, #several team members? 
    start_date:timestamp,
    duration:timedelta,
    confirm_end_from_project:bool,  #several team members? 
    confirm_end_from_user:bool, # several users?
    StoryAmountDarf:uint256,
    StoryAmountTokens:uint256
        }[int128])

@public
def signup_check() -> bool:
    check_result: bool = False
    if self.Users[msg.sender].signup:
        check_result = True
    return check_result
    
@public
@payable
def __default__():
# check what's been sent (DARF or ETH) 
# if ETh...
    if self.signup_check():
        self.ether_depo += msg.value
        self.darftoken.transfer(msg.sender, as_unitless_number(msg.value*500))
    else:
        #return darf - (ether = 20 or 10 darf)
        #send this amount of ether to beneficiar address
        #write all information to Users
        self.Users[msg.sender].signup = True
        self.Users[msg.sender].project = True
# if DARF...


@public
def get_ballance_of_depo() -> uint256(wei):
    return self.ether_depo
    
@public
def create_project(owner_address: address,token:address,IPFSDescribe:bytes32):
    assert self.Users[msg.sender].signup == True
    assert self.Users[msg.sender].project == True
    ProjectID: int128 = self.nextProjectID
    self.Projects[ProjectID] = {projectID:ProjectID, project_owner_address:owner_address,  IPFSDescribe:IPFSDescribe}
    self.nextProjectID = ProjectID + 1

@public
def change_project_info(ProjectID:int128, NewIPFSDescribe:bytes32):
    assert self.Projects[ProjectID].project_owner_address != msg.sender
    self.Projects[ProjectID].IPFSDescribe = NewIPFSDescribe
    
@public
def start_user_story(projectID:int128,IPFSHash:bytes32,storyAmountDarf:uint256): # initiation of userstory
    assert self.Users[msg.sender].signup == True
    UserStoryID: int128 = self.nextUserStoryID
    self.UserStory[UserStoryID] = {projectID:projectID,
                                   IPFSHash:IPFSHash,
                                   project_accept: False,
                                   user_address:msg.sender,
                                   user_signin:False,
                                   project_signin:False,
                                   start_date:0,
                                   duration:0,
                                   confirm_end_from_project:False,
                                   confirm_end_from_user:False,
                                   StoryAmountDarf:storyAmountDarf,
                                   StoryAmountTokens:0
                                   }
    self.nextUserStoryID = UserStoryID + 1
    
@public
def accept_user_story_from_project(UserStoryID:int128): # team accepts userstory for work from backlog 
# team send their tokens to userstory if agree   
    ProjectID: int128 = self.UserStory[UserStoryID].projectID
    assert self.Projects[ProjectID].project_owner_address != msg.sender
    self.UserStory[UserStoryID].project_accept = True
    
@public
def sign_in_user_story_from_user(UserStoryID:int128): # investors signup userstory when negotiations finished 
  # investors  send DARF to userstory if agree   

    ProjectID: int128 = self.UserStory[UserStoryID].projectID
    assert self.UserStory[UserStoryID].user_address != msg.sender
    assert self.UserStory[UserStoryID].user_signin != True
    self.UserStory[UserStoryID].user_signin = True
    project_signin: bool = self.UserStory[UserStoryID].project_signin
    if  project_signin == True:
        self.UserStory[UserStoryID].start_date = block.timestamp

@public
def sign_in_user_story_from_project(UserStoryID:int128): # team signup userstory when negotiations finished 
    ProjectID: int128 = self.UserStory[UserStoryID].projectID
    assert self.Projects[ProjectID].project_owner_address != msg.sender
    assert self.UserStory[UserStoryID].project_signin != True
    self.UserStory[UserStoryID].project_signin = True
    user_signin: bool = self.UserStory[UserStoryID].user_signin
    if user_signin == True:
        self.UserStory[UserStoryID].start_date = block.timestamp
@public
def confirm_end_from_project(UserStoryID:int128): # team finished the userstory and initiate acceptance from investors
    ProjectID: int128 = self.UserStory[UserStoryID].projectID
    assert self.Projects[ProjectID].project_owner_address != msg.sender
    assert block.timestamp < self.UserStory[UserStoryID].start_date +self.UserStory[UserStoryID].duration
    self.UserStory[UserStoryID].confirm_end_from_project = True

@public
def confirm_end_from_user(UserStoryID:int128): # investors accept work  
    assert self.UserStory[UserStoryID].user_address != msg.sender
    ProjectID: int128 = self.UserStory[UserStoryID].projectID
    project_address: address = self.Projects[ProjectID].project_owner_address
    storyAmountDarf: uint256 = self.UserStory[UserStoryID].StoryAmountDarf/100*95
    FullStoryAmountDarf: uint256 = self.UserStory[UserStoryID].StoryAmountDarf/100*95
    self.UserStory[UserStoryID].confirm_end_from_user = True
    self.darftoken.transfer(project_address, as_unitless_number(storyAmountDarf))
    self.ether_depo = self.ether_depo - as_wei_value(FullStoryAmountDarf/500, "wei")
    # 5% tokens & ETH to us
    
# if team fails... deadline is broken, undersing LT then 50% of sum and one on investors initiate refunding 
def userstory_fail_refund (UserStoryID):
    assert self.UserStory[UserStoryID].user_address != msg.sender
    PH: {
      UserStoryID: int128,
      Payment: int128,
      UserAddress: address
    }
    
