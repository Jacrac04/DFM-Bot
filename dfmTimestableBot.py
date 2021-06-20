###############################################################################
#                            dfm Timestable Bot                               #
#                               EXPERIMENTAL                                  #
#                               Please  Read                                  #
#                          This is my first version                           #
# This will get the score you set in QNUMTODO in the timestables fixed time   # 
# comp on DFM.                                                                #
# It automatically calculates the time to wait between each question but slow # 
# networks and cpu usage spikes can slow down the proccess meaning the time   # 
# can get out.                                                                #
# I suggest that you start at 10 or another low number so you can adjust your #
# PCs EXCTIME (See how far the current duration found in the resp outputed at #
# the end is of from 30 and diveide that by the QNUMTODO and add/subract that # 
# from your current EXCTIME).                                                 #
# If you see that it has slowed down you can kill the procces by going to     #
# https://www.drfrostmaths.com/homework/process-finishtimestables.php?ttaid=  #
# and add your ttaid to the end of that to force stop the task.               #
###############################################################################

import json
from requests import Session
import time

EMAIL = 'example@example.com' # Your email
PASSWORD = 'password' # Your Password

QNUMTODO = 69 # Do not go above 69 as its currently impossible 

EXCTIME = 0.1 # How long your pc takes to run the code in the loop
TIMETOSLEEP = (29/QNUMTODO) - EXCTIME # Calculates how long to wait between questions so you stay arround 30 secs

MD5LOOKUP = {'cfcd208495d565ef66e7dff9f98764da': 0, 'c4ca4238a0b923820dcc509a6f75849b': 1, 'c81e728d9d4c2f636f067f89cc14862c': 2, 'eccbc87e4b5ce2fe28308fd9f2a7baf3': 3, 'a87ff679a2f3e71d9181a67b7542122c': 4, 'e4da3b7fbbce2345d7772b0674a318d5': 5, '1679091c5a880faf6fb5e6087eb1b2dc': 6, '8f14e45fceea167a5a36dedd4bea2543': 7, 'c9f0f895fb98ab9159f51fd0297e236d': 8, '45c48cce2e2d7fbdea1afc51c7c6ad26': 9, 'd3d9446802a44259755d38e6d163e820': 10, '6512bd43d9caa6e02c990b0a82652dca': 11, 'c20ad4d76fe97759aa27a0c99bff6710': 12, 'c51ce410c124a10e0db5e4b97fc2af39': 13, 'aab3238922bcc25a6f606eb525ffdc56': 14, '9bf31c7ff062936a96d3c8bd1f8f2ff3': 15, 'c74d97b01eae257e44aa9d5bade97baf': 16, '70efdf2ec9b086079795c442636b55fb': 17, '6f4922f45568161a8cdf4ad2299f6d23': 18, '1f0e3dad99908345f7439f8ffabdffc4': 19, '98f13708210194c475687be6106a3b84': 20, '3c59dc048e8850243be8079a5c74d079': 21, 'b6d767d2f8ed5d21a44b0e5886680cb9': 22, '37693cfc748049e45d87b8c7d8b9aacd': 23, '1ff1de774005f8da13f42943881c655f': 24, '8e296a067a37563370ded05f5a3bf3ec': 25, '4e732ced3463d06de0ca9a15b6153677': 26, '02e74f10e0327ad868d138f2b4fdd6f0': 27, '33e75ff09dd601bbe69f351039152189': 28, '6ea9ab1baa0efb9e19094440c317e21b': 29, '34173cb38f07f89ddbebc2ac9128303f': 30, 'c16a5320fa475530d9583c34fd356ef5': 31, '6364d3f0f495b6ab9dcf8d3b5c6e0b01': 32, '182be0c5cdcd5072bb1864cdee4d3d6e': 33, 'e369853df766fa44e1ed0ff613f563bd': 34, '1c383cd30b7c298ab50293adfecb7b18': 35, '19ca14e7ea6328a42e0eb13d585e4c22': 36, 'a5bfc9e07964f8dddeb95fc584cd965d': 37, 'a5771bce93e200c36f7cd9dfd0e5deaa': 38, 'd67d8ab4f4c10bf22aa353e27879133c': 39, 'd645920e395fedad7bbbed0eca3fe2e0': 40, '3416a75f4cea9109507cacd8e2f2aefc': 41, 'a1d0c6e83f027327d8461063f4ac58a6': 42, '17e62166fc8586dfa4d1bc0e1742c08b': 43, 'f7177163c833dff4b38fc8d2872f1ec6': 44, '6c8349cc7260ae62e3b1396831a8398f': 45, 'd9d4f495e875a2e075a1a4a6e1b9770f': 46, '67c6a1e7ce56d3d6fa748ab6d9af3fd7': 47, '642e92efb79421734881b53e1e1b18b6': 48, 'f457c545a9ded88f18ecee47145a72c0': 49, 'c0c7c76d30bd3dcaefc96f40275bdc0a': 50, '2838023a778dfaecdc212708f721b788': 51, '9a1158154dfa42caddbd0694a4e9bdc8': 52, 'd82c8d1619ad8176d665453cfb2e55f0': 53, 'a684eceee76fc522773286a895bc8436': 54, 'b53b3a3d6ab90ce0268229151c9bde11': 55, '9f61408e3afb633e50cdf1b20de6f466': 56, '72b32a1f754ba1c09b3695e0cb6cde7f': 57, '66f041e16a60928b05a7e228a89c3799': 58, '093f65e080a295f8076b1c5722a46aa2': 59, '072b030ba126b2f4b2374f342be9ed44': 60, '7f39f8317fbdb1988ef4c628eba02591': 61, '44f683a84163b3523afe57c2e008bc8c': 62, '03afdbd66e7929b125f8597834fa83a4': 63, 'ea5d2f1c4608232e07d3aa3d998e5135': 64, 'fc490ca45c00b1249bbe3554a4fdf6fb': 65, '3295c76acbf4caaed33c36b1b5fc2cb1': 66, '735b90b4568125ed6c3f678819b6e058': 67, 'a3f390d88e4c41f2747bfa2f1b5f87db': 68, '14bfa6bb14875e45bba028a21ed38046': 69, '7cbbc409ec990f19c78c75bd1e06f215': 70, 'e2c420d928d4bf8ce0ff2ec19b371514': 71, '32bb90e8976aab5298d5da10fe66f21d': 72, 'd2ddea18f00665ce8623e36bd4e3c7c5': 73, 'ad61ab143223efbc24c7d2583be69251': 74, 'd09bf41544a3365a46c9077ebb5e35c3': 75, 'fbd7939d674997cdb4692d34de8633c4': 76, '28dd2c7955ce926456240b2ff0100bde': 77, '35f4a8d465e6e1edc05f3d8ab658c551': 78, 'd1fe173d08e959397adf34b1d77e88d7': 79, 'f033ab37c30201f73f142449d037028d': 80, '43ec517d68b6edd3015b3edc9a11367b': 81, '9778d5d219c5080b9a6a17bef029331c': 82, 'fe9fc289c3ff0af142b6d3bead98a923': 83, '68d30a9594728bc39aa24be94b319d21': 84, '3ef815416f775098fe977004015c6193': 85, '93db85ed909c13838ff95ccfa94cebd9': 86, 'c7e1249ffc03eb9ded908c236bd1996d': 87, '2a38a4a9316c49e5a833517c45d31070': 88, '7647966b7343c29048673252e490f736': 89, '8613985ec49eb8f757ae6439e879bb2a': 90, '54229abfcfa5649e7003b83dd4755294': 91, '92cc227532d17e56e07902b254dfad10': 92, '98dce83da57b0395e163467c9dae521b': 93, 'f4b9ec30ad9f68f89b29639786cb62ef': 94, '812b4ba287f5ee0bc9d43bbf5bbe87fb': 95, '26657d5ff9020d2abefe558796b99584': 96, 'e2ef524fbf3d9fe611d5a8e90fefdc9c': 97, 'ed3d2c21991e3bef5e069713af9fa6ca': 98, 'ac627ab1ccbdb62ec96e702f07f6425b': 99, 'f899139df5e1059396431415e770c6dd': 100, '38b3eff8baf56627478ec76a704e9b52': 101, 'ec8956637a99787bd197eacd77acce5e': 102, '6974ce5ac660610b44d9b9fed0ff9548': 103, 'c9e1074f5b3f9fc8ea15d152add07294': 104, '65b9eea6e1cc6bb9f0cd2a47751a186f': 105, 'f0935e4cd5920aa6c7c996a5ee53a70f': 106, 'a97da629b098b75c294dffdc3e463904': 107, 'a3c65c2974270fd093ee8a9bf8ae7d0b': 108, '2723d092b63885e0d7c260cc007e8b9d': 109, '5f93f983524def3dca464469d2cf9f3e': 110, '698d51a19d8a121ce581499d7b701668': 111, '7f6ffaa6bb0b408017b62254211691b5': 112, '73278a4a86960eeb576a8fd4c9ec6997': 113, '5fd0b37cd7dbbb00f97ba6ce92bf5add': 114, '2b44928ae11fb9384c4cf38708677c48': 115, 'c45147dee729311ef5b5c3003946c48f': 116, 'eb160de1de89d9058fcb0b968dbbbd68': 117, '5ef059938ba799aaa845e1c2e8a762bd': 118, '07e1cd7dca89a1678042477183b7ac3f': 119, 'da4fb5c6e93e74d3df8527599fa62642': 120, '4c56ff4ce4aaf9573aa5dff913df997a': 121, 'a0a080f42e6f13b3a2df133f073095dd': 122, '202cb962ac59075b964b07152d234b70': 123, 'c8ffe9a587b126f152ed3d89a146b445': 124, '3def184ad8f4755ff269862ea77393dd': 125, '069059b7ef840f0c74a814ec9237b6ec': 126, 'ec5decca5ed3d6b8079e2e7e7bacc9f2': 127, '76dc611d6ebaafc66cc0879c71b5db5c': 128, 'd1f491a404d6854880943e5c3cd9ca25': 129, '9b8619251a19057cff70779273e95aa6': 130, '1afa34a7f984eeabdbb0a7d494132ee5': 131, '65ded5353c5ee48d0b7d48c591b8f430': 132, '9fc3d7152ba9336a670e36d0ed79bc43': 133, '02522a2b2726fb0a03bb19f2d8d9524d': 134, '7f1de29e6da19d22b51c68001e7e0e54': 135, '42a0e188f5033bc65bf8d78622277c4e': 136, '3988c7f88ebcb58c6ce932b957b6f332': 137, '013d407166ec4fa56eb1e1f8cbe183b9': 138, 'e00da03b685a0dd18fb6a08af0923de0': 139, '1385974ed5904a438616ff7bdb3f7439': 140, '0f28b5d49b3020afeecd95b4009adf4c': 141, 'a8baa56554f96369ab93e4f3bb068c22': 142, '903ce9225fca3e988c2af215d4e544d3': 143, '0a09c8844ba8f0936c20bd791130d6b6': 144, '2b24d495052a8ce66358eb576b8912c8': 145, 'a5e00132373a7031000fd987a3c9f87b': 146, '8d5e957f297893487bd98fa830fa6413': 147, '47d1e990583c9c67424d369f3414728e': 148, 'f2217062e9a397a1dca429e7d70bc6ca': 149, '7ef605fc8dba5425d6965fbd4c8fbe1f': 150, 'a8f15eda80c50adb0e71943adc8015cf': 151, '37a749d808e46495a8da1e5352d03cae': 152, 'b3e3e393c77e35a4a3f3cbd1e429b5dc': 153, '1d7f7abc18fcb43975065399b0d1e48e': 154, '2a79ea27c279e471f4d180b08d62b00a': 155, '1c9ac0159c94d8d0cbedc973445af2da': 156, '6c4b761a28b734fe93831e3fb400ce87': 157, '06409663226af2f3114485aa4e0a23b4': 158, '140f6969d5213fd0ece03148e62e461e': 159, 'b73ce398c39f506af761d2277d853a92': 160, 'bd4c9ab730f5513206b999ec0d90d1fb': 161, '82aa4b0af34c2313a562076992e50aa3': 162, '0777d5c17d4066b82ab86dff8a46af6f': 163, 'fa7cdfad1a5aaf8370ebeda47a1ff1c3': 164, '9766527f2b5d3e95d4a733fcfb77bd7e': 165, '7e7757b1e12abcb736ab9a754ffb617a': 166, '5878a7ab84fb43402106c575658472fa': 167, '006f52e9102a8d3be2fe5614f42ba989': 168, '3636638817772e42b59d74cff571fbb3': 169, '149e9677a5989fd342ae44213df68868': 170, 'a4a042cf4fd6bfb47701cbc8a1653ada': 171, '1ff8a7b5dc7a7d1f0ed65aaa29c04b1e': 172, 'f7e6c85504ce6e82442c770f7c8606f0': 173, 'bf8229696f7a3bb4700cfddef19fa23f': 174, '82161242827b703e6acf9c726942a1e4': 175, '38af86134b65d0f10fe33d30dd76442e': 176, '96da2f590cd7246bbde0051047b0d6f7': 177, '8f85517967795eeef66c225f7883bdcb': 178, '8f53295a73878494e9bc8dd6c3c7104f': 179, '045117b0e0a11a242b9765e79cbf113f': 180, 'fc221309746013ac554571fbd180e1c8': 181, '4c5bde74a8f110656874902f07378009': 182, 'cedebb6e872f539bef8c3f919874e9d7': 183, '6cdd60ea0045eb7a6ec44c54d29ed402': 184, 'eecca5b6365d9607ee5a9d336962c534': 185, '9872ed9fc22fc182d371c3e9ed316094': 186, '31fefc0e570cb3860f2a6d4b38c6490d': 187, '9dcb88e0137649590b755372b040afad': 188, 'a2557a7b2e94197ff767970b67041697': 189, 'cfecdb276f634854f3ef915e2e980c31': 190, '0aa1883c6411f7873cb83dacb17b0afc': 191, '58a2fc6ed39fd083f55d4182bf88826d': 192, 'bd686fd640be98efaae0091fa301e613': 193, 'a597e50502f5ff68e3e25b9114205d4a': 194, '0336dcbab05b9d5ad24f4333c7658a0e': 195, '084b6fbb10729ed4da8c3d3f5a3ae7c9': 196, '85d8ce590ad8981ca2c8286f79f59954': 197, '0e65972dce68dad4d52d063967f0a705': 198, '84d9ee44e457ddef7f2c4f25dc8fa865': 199}

def postAnswer(ttaid, ans, qnum):
    data = {'ttaid': ttaid, 'answer': ans, 'qnum': qnum}
    print(data)
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                ' Chrome/87.0.4280.141 Safari/537.36'}
    sesh.post('https://www.drfrostmaths.com/homework/process-incrementtimestablescore.php', headers=headers, data=data)


sesh = Session()
login_url = 'https://www.drfrostmaths.com/process-login.php?url='
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/87.0.4280.141 Safari/537.36'}
data = {'login-email': EMAIL, 'login-password': PASSWORD}

sesh.post(login_url, headers=headers, data=data)

resp = sesh.get('https://www.drfrostmaths.com/homework/process-starttimestables.php',headers=headers) # Start Timetable
resp = json.loads(resp.text)
ttaid = resp['ttaid']
dfmData = resp['data']
print(ttaid)
qnum = 1

for dfmD in dfmData:
    if qnum > QNUMTODO:
        break 
    encryptedAns = dfmD['a'] # Finds the encrypted answer in the data
    ans = MD5LOOKUP[encryptedAns] # Finds the answer by looking up the hash in a hash dictionary
    postAnswer(ttaid, ans, qnum)
    qnum+=1
    time.sleep(TIMETOSLEEP) # The code in this loop takes about 0.1 secs to execute for me

time.sleep(1)

resp = sesh.get('https://www.drfrostmaths.com/homework/process-finishtimestables.php?ttaid='+str(ttaid),headers=headers) #Ends Timetables
print(resp.text) 
# Example Resp outputed at the end: {"prev":{"score":68,"total":266,"points":200,"duration":28.15},"current":{"score":69,"total":266,"points":200,"duration":29.97},"trophies":[],"timemultipler":0,"scoremultiplier":0,"numquestions":12}
# Adjust the EXCTIME based on the current duration found in the resp outputed at the end