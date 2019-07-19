import requests
import json
import random
import string
from enochecker import BaseChecker, BrokenServiceException,EnoException, run
from lyrics_creation import create_song_locally
import hashlib
from multiprocessing import Pool
from io import BytesIO
from music_service import MService
session = requests.Session()

pool_process = Pool(5)



class ExplotifyChecker(BaseChecker):

    flag_count = 3
    havoc_count = 1
    noise_count = 0
    service_name = "Explotify"

    port = 80  # default port to send requests to.

    def visit_my_songs(self):
        request = self.http_post("/song")
        if request.status_code != 500 or request.status_code != 404:
            return request
        else:
            raise BrokenServiceException("The service is not working well!!!")

    def generate_random_string(self):
        return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(7))

    def create_random_user_register_object(self,flag):
        
        random_firstname = self.generate_random_string()
        random_lastname = self.generate_random_string()
        random_password = self.generate_random_string()
        random_username = self.generate_random_string()
        random_mobile_number = flag
        
        return {
            "first_name":random_firstname,
            "last_name":random_lastname,
            "password":random_password,
            "username":random_username,
            "mobile_number":random_mobile_number
        }

    def generate_login_object_from_user(self,user):
        return{
            "username":user["username"],
            "password":user["password"]
        }


    def register_service(self,flag):
        self.info("Generating Random user to register on the service")
        random_user = self.create_random_user_register_object(flag)
        print("Here is the flag : " , flag , flush=True)
        print("Here Im registering this random user : ", random_user , flush=True)
        request = self.http_post("/register",data=random_user)
        if request.status_code == "500":
            raise BrokenServiceException("We couldn't register on the service!")
        return random_user

        

       
    def login_on_service(self,user):
        user_for_this_round = user
        user_for_login = self.generate_login_object_from_user(user_for_this_round)
        request = self.http_post("/login",data=user_for_login)
        if request.status_code == "500":
            raise BrokenServiceException("We couldn't login on the service!")
        
    def get_user_info(self):
        info = self.http_get("/user/me")
        if info.status_code == 500:
            raise BrokenServiceException("We couldn't get the flag in the user profile")
        return info

    def download_song_with_hashid(self,hash_id):
        params = {"search_option","hash_id"}
        request = self.http_get(f"/song/{hash_id}/download?search_option=hash_id",stream=True)
        if request.status_code == 500 or request.status_code == 404:
            raise BrokenServiceException("We couldn't download the song from the server")
        return request

    def get_song_with_hashid(self,hash_id):
        params = {"search_option","hash_id"}
        request = self.http_get(f"/song/{hash_id}?search_option=hash_id",stream=True)
        if request.status_code == 500 or request.status_code == 404:
            raise BrokenServiceException("We couldn't download the song from the server")
        return request


    def hash_file_binary(self,binary):
        hash_local = hashlib.sha256(binary)
        return hash_local.hexdigest()

    def create_song_object(self,flag_audio,flag_name):
        letters_flag = list(flag_audio)
        joined_flag_spaces = " ".join(letters_flag)
        return {
            "lyrics":joined_flag_spaces,
            "web_lyrics":False,
            "name_song":flag_name
        }

    


    def create_song_on_service(self,flag_audio,flag_name):
        song_object = self.create_song_object(flag_audio,flag_name)
        self.debug("Checker is creating song")
        response = self.http_post("/song",data=song_object)
        self.debug("Checker created song successfully")
        return response

    def putflag(self):
        

        
        memo = {"flags":{},"last_index":0,"usernames":{}}
       
        
        flag_moment = self.flag
        
        if  self.flag_idx == 0:#memo["last_index"] == 0:
            memo["flags"][str(self.flag_idx)] = self.flag
            memo[self.flag] = "register"
            user_register = self.register_service(self.flag)
            memo["usernames"][self.flag] = user_register
            memo["username"] = user_register
            self.info("Checker Register on service")
            self.login_on_service(user_register)
            self.debug("Checker logged in service with user object : ")
            self.info("Checker logged in")
            
            self.team_db[self.flag] = memo


        elif self.flag_idx == 1:#memo["last_index"] == 1:

            memo[self.flag] = "Testing"
            self.team_db[self.flag] = memo
            return
            memo["flags"][str(self.flag_idx)] = self.flag
            user_register = self.register_service("123456789Flag")
            memo["usernames"][self.flag] = user_register
            self.info("Checker Register on service")
            self.login_on_service(user_register)
            self.debug("Checker logged in service with user object : ")
            self.info("Checker logged in")

            response_server = self.create_song_on_service("dummy song",self.flag)
            
            try:
                song_info = json.loads(response_server.text)
            except Exception as e:
                raise BrokenServiceException("Invalid json format : " + str(e))


            memo["hash_id_name"] = song_info["id_hash"]
            print("Esto es hash_id_name: " , song_info["id_hash"], flush=True)
            memo["hash_id_name"] = song_info["id_hash"]
            memo["hash_id_name"] = song_info["id_hash"]
  
            self.team_db[self.flag] = memo


        
        elif self.flag_idx == 2:#memo["last_index"] == 2:
            memo[self.flag] = "Testing"
            self.team_db[self.flag] = memo
            return
            memo["flags"][str(self.flag_idx)] = self.flag
            user_register = self.register_service("01800Flag")
            memo["usernames"][self.flag] = user_register
            self.info("Checker Register on service")
            self.login_on_service(user_register)
            self.debug("Checker logged in service with user object : ")
            self.info("Checker logged in")
            
            try:
                song_process = pool_process.apply_async(create_song_locally,(self.flag,self.address,self.round,self.team))
            except Exception as e:
                raise EnoException("It is probably checker problem. The exception was : " + str(e))

            response_server = self.create_song_on_service(self.flag,"End of the world")

            try:
                json_response = json.loads(response_server.text)
            except:
                raise BrokenServiceException("Invalid json format : " + str(e))
                

            song_locally = song_process.get()

            try:
                hash_id_local = self.hash_file_binary(song_locally)
            except:
                raise BrokenServiceException("Service could not read the hash_ids from song")
            
            if json_response["id_hash"] != hash_id_local:
                raise BrokenServiceException("Service is broken. Maybe someone is trying to cheat!")
            else:
                memo["hash_id_sound"] = hash_id_local
                memo["hash_id_sound"] = hash_id_local
                memo["hash_id_sound"] = hash_id_local
                print("Esto es hash_id_sound: " , hash_id_local, flush=True)
                memo["hash_id_sound"] = hash_id_local
            memo["hash_id_sound"] = hash_id_local
            self.info("Everything seems good with the service.")
                
            self.team_db[self.flag] = memo
            
        

            

    def getflag(self):
        self.http_get("/")


        if self.flag not in self.team_db:
            raise BrokenServiceException("Flag not found in the DB. Something went wrong!!")

        memo = self.team_db[self.flag]

           
        self.info("Taking out the information with the flag key")

        if memo[self.flag] == "register":
            
            self.info("Getting the register pipeline")

            username = memo["usernames"][self.flag]

            self.info("Getting the username for the register flag")


            try:
                self.login_on_service(username)
            except Exception as e :
                raise BrokenServiceException("Error trying to login with old user: " + str(e))

            self.info("We logged in with the username of the register flag")

            user_profile_request = self.get_user_info()

            self.info("We get user info from service in the register flag")


            try:
                info_user = json.loads(user_profile_request.text)
            except Exception as e:
                raise BrokenServiceException("Invalid format json : " + str(e))

            self.info("We parsed json of the user in register pipeline")

            print("Here is the flag getted : " ,info_user["mobile_number"] , flush=True )

            if info_user["mobile_number"] != self.flag:
                raise BrokenServiceException("Mobile_number flag is not there")
            else:
                self.info("Everything OK with the mobile_number_flag")



        
        elif memo[self.flag] == "song_name":
            return
            self.info("Getting the username of the song_name pipeline")

            username = memo["usernames"][self.flag]
            hash_id_name = memo["hash_id_name"]

            self.info("username and hash of the song retrieved")

            try:
                self.login_on_service(username)
            except Exception as e :
                raise BrokenServiceException("Error trying to login with old user: " + str(e))

            self.info("Getting information of the song by hash on server")

            song_request_info = self.get_song_with_hashid(hash_id_name)

            self.info("Getted information song by hash from the server")

            try:
                info_song = json.loads(song_request_info.text)
            except Exception as e:
                raise BrokenServiceException("Invalid format json for the song! : " + str(e))

            if info_song["name_song"] != self.flag:
                raise BrokenServiceException("Name song flag is not there!")
            else:
                self.info("Everything OK with the name_song flag")


        elif memo[self.flag] == "song_sound":
            return
            self.info("Getting the username of the song_name pipeline")

            hash_id = memo["hash_id_sound"]
            username = memo["usernames"][self.flag]

            self.info("username and hash of the song retrieved")

            try:
                self.login_on_service(username)
            except Exception as e :
                raise BrokenServiceException("Error trying to login with old user: " + str(e))


            self.info("Downloading the song ... searching with hash_id")

            song_request_audio = self.download_song_with_hashid(hash_id)
            raw_song = song_request_audio.raw

            self.info("Song Downloaded")

            memory_song = BytesIO()
            raw_song.decode_content = True

            self.info("Decoded song")

            for chunk in song_request_audio.iter_content(1024):
                memory_song.write(chunk)

            self.info("Writing in memory the song")
        

            self.info("Hashing the binary of the song")
            hash_id_from_service = self.hash_file_binary(memory_song.getvalue())

            self.info("hash_id was calculated!")

            if hash_id_from_service != hash_id:
                raise BrokenServiceException("The song was not what I uploaded!!!")
        
            
    def putnoise(self):
        pass

    def getnoise(self):
        pass

    def havoc(self):
        random = self.generate_random_string
        user_register = self.register_service(random)
        self.info("Checker Register on service")
        self.login_on_service(user_register)
        self.debug("Checker logged in service with user object : ")
        self.info("Checker logged in")
        self.visit_my_songs()
        self.info("Checker Visiting Songs")
        self.info("It seems like the service is online!!!")
        

    def exploit(self):
        pass
            


app = ExplotifyChecker.service
if __name__ == "__main__":
    run(ExplotifyChecker)