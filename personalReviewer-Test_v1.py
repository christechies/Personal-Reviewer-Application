class manageFiles:
    '''
    This class manages all the things file INNER BACK-END related
    # finding current diretory
    # editing current directory if not yet initialize
    # checking of directory files
    # logs
    '''
    def __init__(self):
        self.oss = __import__('os')
        self.dtime = __import__('datetime')
        self.folders = ['MainFolder_','UserLF','SubjectMF','AppLogs']
        self.curwd = self.oss.getcwd() + '\\' + self.folders[0]
        self.subs = self.curwd+'\\'+self.folders[2]
        self.logs = self.curwd+'\\'+self.folders[1]
        self.appLog = self.curwd+'\\'+self.folders[3]
        self.dy2 = self.dtime.date.today()
        self.time = self.dtime.datetime.now()
        
    def check_dir(self):
        
        try:
            
            if self.folders[0] not in self.oss.listdir():
                self.oss.mkdir(self.oss.getcwd()+'\\'+self.folders[0])
            for i in self.folders[1:]:
                if i in self.oss.listdir(self.curwd):
                    continue
                else:
                    self.oss.mkdir(self.curwd+'\\'+i)
        except FileNotFoundError:
            return False
        return True
    
    def make_logs(self):
        with open(self.curwd+'\\'+ 'selfCheck.txt','a+') as curcwd:
            curcwd.write('Self Check Successful ~'+ str(self.dy2.strftime("%d/%m/%Y")) + '------'+ '['+ str(self.time.strftime("%H:%M:%S"))+ ']' + '\n')
        
    
    def check_sub(self):
        for x in self.oss.listdir(self.subs):
            print('+---' + x)
    
    def find_logs(self,log_codes):
        if log_codes in self.oss.listdir(self.logs):
            return True
        return False
    
class manageProcess(manageFiles):
    '''
    This class manages all the things BACK-END process related
    # set review type ~ description, enumerate, choices, mixed
    # set retrieve data from file
    # randomize questions
    # set & log score
    # reset
    # check scores
    '''
    def __init__(self):
        self.rand = __import__('random')
        self.strings = __import__('string')
        self.pick = __import__('pickle')
        self.timed = __import__('time')
        self.strlistA = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.strlistB = [i.upper() for i in self.strlistA]
        self.numlist = list(range(0,10))
        self.allchar = [self.strlistA,self.strlistB,self.numlist]
        self.correct_ans = []
        self.wrong_ans = []
        self.temp_dicta = {}
        self.mainKeys = []
        super().__init__()
    
    def tally_score(self,state_ans,ans_key):
        if state_ans == True:
            self.correct_ans.append(ans_key)
        else:
            self.wrong_ans.append(ans_key)
        
    def setQuestions(self,keys,qType):
        if qType == 'd':
            for i in keys:
                userAns = input(self.temp_dicta[i]+ '? ' + '\t')
                print('\n')
                if userAns.lower() ==  i.lower():
                    self.tally_score(state_ans = True,ans_key = i)
                else:
                    self.tally_score(state_ans = False,ans_key = i)
        
        if qType == 'c':
            for i in keys:
                choices = [i,self.rand.choice(keys),self.rand.choice(keys)]
                self.rand.shuffle(choices)
                q = input(self.temp_dicta[i] + '? \n' + 'a. {0} -- b. {1} -- c. {2}'.format(choices[0],choices[1],choices[2])+ '\t' )
                print('\n')
                if q == i:
                    self.tally_score(state_ans=True,ans_key=i)
                else:
                    self.tally_score(state_ans = False,ans_key = i)
                    
    def setReview(self,queType='',subject=None,textfile=None):
        if subject == None and textfile != None:
            for i in self.oss.listdir(self.subs):
                if textfile in self.oss.listdir(self.subs + '\\'+i):
                    self.textLoc = self.subs + '\\' + i + '\\' + textfile
                    break
                else:
                    continue
        if subject != None and textfile == None:
            self.textLoc = [self.subs+'\\'+subject+'\\'+ i for i in self.oss.listdir(self.subs+'\\'+subject)]
        if subject != None and textfile != None:
            try:
                with open(self.subs+ '\\'+subject+'\\'+ textfile) as fl:
                    fl.read()
                self.textLoc = self.subs+ '\\'+subject+'\\'+ textfile
            except FileNotFoundError:
                suggest = input('File not present nor located, would you like to create such subject[subfolder]? (yes/no) --')
                if suggest in ['Y','y']:
                    self.oss.mkdir(self.subs + '\\'+subject)
                    return 'Such subject directory has now been successfully created!'
                elif suggest in ['N','n']:
                    return 'Understood!'
                else:
                    return 'Response has not been understood!'
             
        if isinstance(self.textLoc,list):
            
            for i in self.textLoc:
                with open(i,'r+') as fl:
                    fl2 = fl.readlines()
                    fl2 = [i.strip('\n') for i in fl2]
                    if '' in fl2:
                        fl2.remove('')
                    mid_point = fl2.index('#enums')
                    keys_temp = fl2[1:mid_point][0::2]
                    vals_temp = [i[1:] for i in fl2[1:mid_point][1::2]]
                    temp_dict = dict((keys_temp[i],vals_temp[i]) for i in range(len(keys_temp)))
                        #separate logic for enumeration type of notes
                    enVal = fl2[mid_point+1:len(fl2)][0::2]
                    enKeys = [i.split('-')[1] for i in fl2[mid_point+1:len(fl2)][1::2]]
                    ent_dict = dict((enKeys[i],enVal[i]) for i in range(len(enKeys)))
                temp_dictb = dict((i[0],i[1]) for i in list(list(temp_dict.items()) + list(ent_dict.items())))
                self.temp_dicta = dict((i[0],i[1]) for i in list(list(self.temp_dicta.items()) + list(temp_dictb.items())))
        else:
            with open(self.textLoc,'r+') as fl:
                fl2 = fl.readlines()
                fl2 = [i.strip('\n') for i in fl2]
                if '' in fl2:
                    fl2.remove('')
                mid_point = fl2.index('#enums')
                keys_temp = fl2[1:mid_point][0::2]
                vals_temp = [i[1:] for i in fl2[1:mid_point][1::2]]
                temp_dict = dict((keys_temp[i],vals_temp[i]) for i in range(len(keys_temp)))
                        #separate logic for enumeration type of notes
                enVal = fl2[mid_point+1:len(fl2)][0::2]
                enKeys = [i.split('-')[1] for i in fl2[mid_point+1:len(fl2)][1::2]]
                ent_dict = dict((enKeys[i],enVal[i]) for i in range(len(enKeys)))
            self.temp_dicta = dict((i[0],i[1]) for i in list(list(temp_dict.items()) + list(ent_dict.items())))
        
        
         #randomize and store
        self.mainKeys = [i for i in self.temp_dicta.keys()]
        self.rand.shuffle(self.mainKeys)
        self.setQuestions(self.mainKeys,queType)
        
        
                
    
    def setScore(self):
        print('\n')
        self.curr_score=str(len(self.correct_ans)) + '/' +str(len(self.mainKeys))
        score_state = 'Your score is {}'.format(self.curr_score)
        return score_state
    
    def create_code(self):
        code_set = self.allchar
        code = ''
        self.rand.shuffle(code_set)
        for i in code_set:
            code += str(self.rand.choice(i))
        return code
    
    def save_score(self,code):
        print('\n')
        with open(self.logs + '\\'+ 'UserScoresMain[pre-update]' + '.txt', 'a+') as fl:
            fl.write(str(self.dy2.strftime("%d/%m/%Y")) + '----'+ '['+ str(self.time.strftime("%H:%M:%S"))+ ']' + '-----'+'%.2f' % ((len(self.correct_ans)/len(self.mainKeys))*100)+'%'+'['+str(len(self.correct_ans))+ '\\'+str(len(self.mainKeys)) +']'+'\n')           
        with open(self.logs + '\\'+ 'UserScoresMain[' +code+ ']'+ '.txt', 'a+') as fln:
            fln.write(str(self.dy2.strftime("%d/%m/%Y")) + '----'+ '['+ str(self.time.strftime("%H:%M:%S"))+ ']' + '-----'+'%.2f' % ((len(self.correct_ans)/len(self.mainKeys))*100)+'%'+'['+str(len(self.correct_ans))+ '\\'+str(len(self.mainKeys)) +']'+'\n')
        print('You have successfully answered these questions: ')
        for i in self.correct_ans:
            print(i + '\n'+ '-'+ self.temp_dicta[i])
        print('\n\n')
        print('You have futilely answered these questions: ')
        for x in self.wrong_ans:
            print(x + '\n'+ '-'+ self.temp_dicta[x])
        self.timed.sleep(100)
    '''
    [on update]
    def checkProgress(self):
        pass
    def take_break(self,code):
        
        with open(self.appLog+'\\'+code+'.pkl','wb') as fl:
            correct_ans = self.correct_ans
            wrong_ans = self.wrong_ans
            mainKey = self.mainKeys
            self.pick.dump(correct_ans,fl)
            self.pick.dump(wrong_ans,fl)
            self.pick.dump(mainKey,fl)
        
        
    
    def cont_rev(self,code):
        #problem checkpoint here
        try:
            with open(self.appLog+'\\'+code+'.pkl','rb') as fl:
                self.pick.load(fl)
                self.mainKeys = mainKey
                print(self.mainKeys)
        except FileNotFoundError:
            return 'Such saved file is lost or has not yet been created'
    '''
class mainRun(manageProcess,manageFiles):
    '''
    This class manages the main runtime of the application itself
    # initializes the app on first run
    # asks input from user & replies
    # process input
    '''
    helps = '''
    SET commands:
    $n ~ new task 
    $@_r ~ review and show score after
    --[on next update] $@_r-SA ~ show answers after answering & show score after
    --[on next update] $@_r-NA ~ dont show answers afteranswering
    $@_r-d ~ answer keyword based on description type review
    $@_r-c ~ choices type review
    --[on next update] $@_r-m ~ mix of d,e,&c //

    -----------------------------
    --[on next update] $c ~ continue
    --[on next update] $@_c_0000 ~ code set ####
    -----------------------------
    --[on next update] $b ~ break
    --[on next update] $@_cc ~ set & also print 4 randomized alphanumeric code
    -----------------------------
    --[on next update] $r ~ reset
    -----------------------------
    
    --[on next update] $cs ~ check score
    --[on next update] $@@_d ~ set date
    
    ----------------------------------------------------------
    ----------------------------------------------------------
    ----------------------------------------------------------
    '''
    def __init__(self):
        super().__init__()
        super(manageProcess,self).__init__()
    def interpret(self,inp_string):
        if inp_string[0] != '$':
            print('Unable to decode your request!')
            self.main()
        else:
            decDex = inp_string.index('-')
            check = inp_string[0:decDex]
            if check == '$n_r':
                print(self.oss.listdir(self.subs))
                sub = input('What subject do you prefer to study right now? \n')
                text = input('Is there any particular textfile that you would like to study? ')
                
                if sub == '':
                    sub = None
                    super().setReview(queType = str(inp_string[decDex+1]),subject=sub,textfile=text+'.txt')
                if text == '':
                    text = None
                    super().setReview(queType = str(inp_string[decDex+1]),subject=sub,textfile=text)
                print(super().setScore())
                super().save_score(code=sub)
            else:
                print('Unable to decode your request!')
                self.main()
    def main(self):
        if self.check_dir() == True:
            print(self.helps)
            self.make_logs()
            ask = input('What would you like to do today? ')
            self.interpret(ask)
            #[used for updated] super().create_code()
            #super().setReview(queType='c',subject='Math',textfile=None)
            #print(super().setScore())
            #super().save_score(code='Math')
            #[on update] super().cont_rev(code='Ab3')
if __name__ == '__main__':
    app = mainRun()
    app.main()