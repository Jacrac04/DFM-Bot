<br />
<p align="center">
  <a href="https://github.com/Jacrac04/DFM-Bot">
    <img src="images/logo.jpg" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Dr Frost Maths Bot</h3>

  <p align="center">
    A Bot for drfrostmaths.com
    <br />
    <a href="https://replit.com/@Jacrac04/DFM-Bot#main.py">Try Online</a>
    ·
    <a href="https://github.com/Jacrac04/DFM-Bot/issues">Report Bug</a>
    ·
    <a href="https://github.com/Jacrac04/DFM-Bot/issues">Request Feature</a>
  </p>
</p>

# DFM V5 
Thanks to [Asad](https://github.com/Asad-K) for creating a fix for "QID" questions. The bot still doesn't work for "param" questions but a fix will likely be coming soon. For now, I recommend only using manual submit. 

<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#setup-and-use-for-windows">Setup Windows</a></li>
        <li><a href="#setup-and-use-for-repl">Setup Repl</a></li>
        <li><a href="#tips">Tips</a></li>
      </ul>
    </li>
    <li><a href="#bugs-issues-and-requests">Bugs, Issues And Requests</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#todo">Todo</a></li>
    <li><a href="#contact-me">Contact Me</a></li>
  </ol>
</details>



## About The Project
This is a Bot for [drfrostmaths.com](drfrostmaths.com). If you like this please Star it on Github, it really helps, thanks.
It was originally based of [AK163631's Answer Tool](https://github.com/AK163631/DFM-Answer-Tool). This is for educational purposes only.

### Version 4 Update!
New Features:
- Delay - You can add a delay when answering questions.
- Warnings - If you try to do something known to get you banned, it will warn you.
- Task Generator - Generate Question lists
- Update Checker - This can be disabled by changing `ENABLE_STATUS_CHECK = True` to `ENABLE_STATUS_CHECK = False` in `main.py`
- TimesTable Bot (Experimental) - Use this to get onto the timestable leaderboards!

Other Changes:
- Changed file layout




![Image of Interface](https://github.com/Jacrac04/DFM-Bot/blob/master/images/Interface.JPG)

## Getting Started
### The Interface
![Image of Annotated Interface](https://github.com/Jacrac04/DFM-Bot/blob/master/images/annotatedInterface.png)
### Setup And Use For Windows
1. Download the latest version from [Releases](https://github.com/Jacrac04/DFM-Bot/releases)
2. Run the .exe
     - If it gets blocked by your antivirus or Windows, I recommend that you DO NOT run it. Instead use repl or download the source code and run that.
4. Enter your login details - Ensure that your [Dr frost account](https://www.drfrostmaths.com/account.php) is not linked to google or another service. [(Check here)](https://www.drfrostmaths.com/account.php)
5. Enter a question url or the AAID
    - This should look like `https://www.drfrostmaths.com/do-question.php?aaid=12345678` or `12345678`
    - make sure that there is nothing else like `qnum=5` in it.
6. Select manual or auto submit.
    - Auto submit lets you enter the amount of the questions for it to answer and it will go through and answer them for you. You can enter a min and max value for delay and it will pick a random delay between them. After clicking start, if you refresh your Dr forst page you should see questions being answered.
    - Manual submit will give you the answer for the currrent question and then you can enter it yourself. 
7. Click start.


### Setup And Use For Repl
1. Go to the [replit.com site](https://replit.com/@Jacrac04/DFM-Bot#main.py) for this project and click fork. It is important you create your own version as repl shares one instance between everyone, so people may be able to get your Dr Frost password. Once you have done this you can run it.
2. Enter your login details - Ensure that your [Dr frost account](https://www.drfrostmaths.com/account.php) is not linked to google or another service. [(Check here)](https://www.drfrostmaths.com/account.php)
3. Enter a question url or the AAID.
    - This should look like `https://www.drfrostmaths.com/do-question.php?aaid=12345678` or `12345678`
    - make sure that there is nothing else like `qnum=5` in it.
4. Select manual or auto submit.
    - Auto submit lets you enter the amount of the questions for it to answer and it will go through and answer them for you. You can enter a min and max value for delay and it will pick a random delay between them. After clicking start, if you refresh your Dr forst page you should see questions being answered.
    - Manual submit will give you the answer for the currrent question and then you can enter it yourself. 
5. Click start.


The repl site works however it is slower and you will have a better user expeciernce is you run it using the exe or source code on your own machine.


### Tips
* IMPORTANT: Please read [this](https://github.com/Jacrac04/DFM-Bot/issues/1) before using
* I recommend that you change your Dr Frost password to something unique that you dont use for anything else before using this.
* If you use a 'keep going till i say' question url the only way to stop the bot is by closing the window or terminating the process
* After about 15 on one 'skill' you will reach 'master' level. You can keep answering questions on that skill but you will not gain points. So if you want to get lots of points go to on Dr frost practice --> key skills then select lots of skills which you haven't done before then practise them. 


## Bugs, Issues And Requests
Please report any issue or bugs [here](https://github.com/Jacrac04/DFM-Bot/issues/new/choose)
See the [open issues](https://github.com/Jacrac04/DFM-Bot/issues) for a list of proposed features (and known issues).

## Contributing
Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Todo 

- [x] Add Executable
- [x] Add UI
- [x] Add More Answer Functions
- [X] Auto skill selectors (maybe)
- [x] Add images to `README.md`
- [ ] Fix sample space answer

## Contact Me 
To contact me you can make an [issue](https://github.com/Jacrac04/DFM-Bot/issues/new/choose) using the Help Wanted or Question template.
