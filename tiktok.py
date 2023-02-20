#Developed by github.com/useragents
#This script was made for educational purposes. I am not responsible for your actions using this script. This code is a few months old, hence why it may not appear as professional but still works to this day.
try:
    from selenium import webdriver
    import time, os, ctypes, requests
    from colorama import Fore, init
    import warnings, selenium, platform
except ImportError:
    input("Error while importing modules. Please install the modules in requirements.txt")

init(convert = True, autoreset = True)
warnings.filterwarnings("ignore", category=DeprecationWarning)

clear = "clear"
if platform.system() == "Windows":
    clear = "cls"

os.system(clear)

ascii_text = f"""{Fore.RED}
                ████████▀▀▀████
                ████████────▀██
                ████████──█▄──█
                ███▀▀▀██──█████
                █▀──▄▄██──█████
                █──█████──█████
                █▄──▀▀▀──▄█████
                ███▄▄▄▄▄███████ github.com/shezan78
"""

class automator:
    
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.xpaths = {
            "followers": "/html/body/div[4]/div[1]/div[3]/div/div[1]/div/button",
            "likes": "/html/body/div[4]/div[1]/div[3]/div/div[2]/div/button",
            "views": "/html/body/div[4]/div[1]/div[3]/div/div[4]/div/button",
            "shares": "/html/body/div[4]/div[1]/div[3]/div/div[5]/div/button"
        }
        try:
            self.driver = webdriver.Chrome(options = options)
        except Exception as e:
            self.error(f"Error trying to load web driver: {e}")
        self.status = {}
        self.sent = 0
        self.cooldowns = 0
        self.ratelimits = 0

    def check_status(self):
        for xpath in self.xpaths:
            value = self.xpaths[xpath]
            element = self.driver.find_element_by_xpath(value)
            if not element.is_enabled():
                self.status.update({xpath: "[OFFLINE]"})
            else:
                self.status.update({xpath: ""})
    
    def check_for_captcha(self):
        while True:
            try:
                if "Enter the word" not in self.driver.page_source:
                    return
            except:
                return
            os.system(clear)
            print(ascii_text)
            print(f"{self.console_msg('Error')} Complete the CAPTCHA in the driver.")
            time.sleep(1)

    def console_msg(self, status):
        colour = Fore.RED
        if status == "Success":
            colour = Fore.GREEN
        return f"                {Fore.WHITE}[{colour}{status}{Fore.WHITE}]"
    
    def update_ascii(self):
        options = f"""
{self.console_msg("1")} Follower Bot {Fore.RED}{self.status["followers"]}
{self.console_msg("2")} Like Video Bot {Fore.RED}{self.status["likes"]}
{self.console_msg("3")} View Bot {Fore.RED}{self.status["views"]}
{self.console_msg("4")} Share Bot {Fore.RED}{self.status["shares"]}
        """
        return ascii_text + options
    
    def check_url(self, url):
        redirect = True
        if "vm.tiktok.com/" in url:
            redirect = False
        if redirect:
            if "/video/" not in url:
                return False
        session = requests.Session()
        r = session.get(url, allow_redirects=redirect)
        if redirect:
            if r.status_code == 200:
                return True
            return False
        location = r.headers["Location"]
        if "/video" in location:
            return True
        return False

    def convert(self, min, sec):
        seconds = 0
        if min != 0:
            answer = int(min) * 60
            seconds += answer
        seconds += int(sec) + 15
        return seconds

    def check_submit(self, div):
        remaining = f"/html/body/div[4]/div[{div}]/div/div/h4"
        try:
            element = self.driver.find_element_by_xpath(remaining)
        except:
            return None, None
        if "READY" in element.text:
            return True, True
        if "seconds for your next submit" in element.text:
            output = element.text.split("Please wait ")[1].split(" for")[0]
            minutes = element.text.split("Please wait ")[1].split(" ")[0]
            seconds = element.text.split("(s) ")[1].split(" ")[0]
            sleep_duration = self.convert(minutes, seconds)
            return sleep_duration, output
        return element.text, None
    
    def update_cooldown(self, sleep_time, bot, rl = False):
        cooldown = sleep_time
        while True:
            time.sleep(1)
            try:
                cooldown -= 1
            except TypeError:
                break
            self.update_title(bot, cooldown, rl)
            if cooldown == 0:
                break
    
    def wait_for_ratelimit(self, arg, div):
        time.sleep(1)
        duration, output = self.check_submit(div)
        if duration == True:
            return
        if output == None:
            time.sleep(0.7)
            self.wait_for_ratelimit(arg, div)
        self.cooldowns += 1
        self.update_cooldown(duration, arg)

    def send_bot(self, video_url, bot, div):
        try:
            self.driver.find_element_by_xpath(self.xpaths[bot]).click()
            time.sleep(0.5)
        except:
            pass
        enter_link_xpath = f"/html/body/div[4]/div[{div}]/div/form/div/input" 
        link = self.driver.find_element_by_xpath(enter_link_xpath)
        link.clear()
        link.send_keys(video_url)
        self.driver.find_element_by_xpath(f"/html/body/div[4]/div[{div}]/div/form/div/div/button").click() #Search button
        time.sleep(0.8)
        send_button_xpath = f"/html/body/div[4]/div[{div}]/div/div/div[1]/div/form/button"
        try:
            self.driver.find_element_by_xpath(send_button_xpath).click() 
        except selenium.common.exceptions.NoSuchElementException:
            self.wait_for_ratelimit(bot, div)
            self.driver.find_element_by_xpath(f"/html/body/div[4]/div[{div}]/div/form/div/div/button").click() #Search button
            time.sleep(0.8)
            self.driver.find_element_by_xpath(send_button_xpath).click()
        time.sleep(3)
        try:
            s = self.driver.find_element_by_xpath(f"/html/body/div[4]/div[{div}]/div/div/span")
            if "Too many requests" in s.text:
                self.ratelimits += 1
                self.update_cooldown(50, bot, True)
                self.send_bot(video_url, bot, div)
            elif "sent" in s.text:
                sent = 100
                if bot == "likes":
                    try:
                        sent = int(s.text.split(" Hearts")[0])
                    except IndexError:
                        sent = 30
                if bot == "views":
                    sent = 2500
                if bot == "shares":
                    sent = 500
                self.sent += sent
            else:
                print(s.text)
        except:
            self.sent += sent
        self.update_title(bot, "0")
        self.wait_for_ratelimit(bot, div)
        self.send_bot(video_url, bot, div)

    def update_title(self, bot, remaining, rl = False):
        if clear == "cls":
            os.system(clear)
            ctypes.windll.kernel32.SetConsoleTitleW(f"TikTok Automated | Sent: {self.sent} | Cooldown: {remaining}s | Developed by @shezan78 on Github")
            print(ascii_text)
            print(self.console_msg(self.sent) + f" Sent {bot}")
            rl_cooldown = "0"
            cooldown = "0"
            if rl:
                rl_cooldown = remaining
            else:
                cooldown = remaining
            print(self.console_msg(self.cooldowns) + f" Cooldowns {Fore.WHITE}[{Fore.RED}{cooldown}s{Fore.WHITE}]")
            print(self.console_msg(self.ratelimits) + f" Ratelimits {Fore.WHITE}[{Fore.RED}{rl_cooldown}s{Fore.WHITE}]")

    def main(self):
        if clear == "cls":
            ctypes.windll.kernel32.SetConsoleTitleW("TikTok Automated | Developed by @shezan78 on Github")
        self.driver.get("https://zefoy.com/")
        time.sleep(2)
        if "502 Bad Gateway" in self.driver.page_source:
            os.system(clear)
            print(ascii_text)
            input(f"{self.console_msg('Error')} This website does not allow VPN or proxy services.")
            os._exit(0)
        self.check_for_captcha()
        self.check_status()
        self.start()
    
    def error(self, error):
        print(ascii_text)
        print(f"{self.console_msg('Error')} {error}")
        time.sleep(5)
        os._exit(0)
    
    def start(self):
        os.system(clear)
        print(self.update_ascii())
        try:
            option = int(input(f"                {Fore.RED}> {Fore.WHITE}"))
        except ValueError:
            self.start()
        if option == 1:
            if self.status["followers"] != "":
                return self.start()
            div = 2
            ver = "followers"
            username = str(input(f"\n{self.console_msg('Console')} TikTok Username: @"))
            print()
            self.send_bot(username, ver, div)
            return
        elif option == 2:
            if self.status["likes"] != "":
                return self.start()
            div = 3
            ver = "likes"
        elif option == 3:
            if self.status["views"] != "":
                return self.start()
            div = 5
            ver = "views"
        elif option == 4:
            if self.status["shares"] != "":
                return self.start()
            div = 6
            ver = "shares"
        else:
            return self.start()
        video_url = str(input(f"\n{self.console_msg('Console')} #TikTok Botter
import time
from colorama import Fore, init
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from os import system, get_terminal_size

init()
system("mode 800")
system("title TikTok Botter -By neoN#6035")

def color(str, color):
    if color.lower() == "green":
        result = f"{Fore.WHITE}[{Fore.LIGHTGREEN_EX}{str}{Fore.WHITE}]{Fore.LIGHTGREEN_EX}"

    elif color.lower() == "red":
        result = f"{Fore.WHITE}[{Fore.LIGHTRED_EX}{str}{Fore.WHITE}]{Fore.LIGHTRED_EX}"

    return result

def align(str):
    lines = str.splitlines( )
    greatest = []
    for i in lines:  
        greatest.append(len(i))

    for i in lines:
        length = round(int(greatest[-1])/2)
        print(f"{' '*round(get_terminal_size().columns/2-length)}{i}")

class printing():

    def __init__(self, a, b, c, d):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def text():
        text = f"""{Fore.LIGHTMAGENTA_EX}
\t\t\t\t\t▄▄▄▄▄▄▪  ▄ •▄ ▄▄▄▄▄      ▄ •▄     ▄▄▄▄·       ▄▄▄▄▄▄▄▄▄▄▄▄▄ .▄▄▄  
\t\t\t\t\t  ██  ██ █▌▄▌▪•██  ▪     █▌▄▌▪    ▐█ ▀█▪▪     •██  •██  ▀▄.▀·▀▄ █·
\t\t\t\t\t  ▐█.▪▐█·▐▀▀▄· ▐█.▪ ▄█▀▄ ▐▀▀▄·    ▐█▀▀█▄ ▄█▀▄  ▐█.▪ ▐█.▪▐▀▀▪▄▐▀▀▄ 
\t\t\t\t\t  ▐█▌·▐█▌▐█.█▌ ▐█▌·▐█▌.▐▌▐█.█▌    ██▄▪▐█▐█▌.▐▌ ▐█▌· ▐█▌·▐█▄▄▌▐█•█▌
\t\t\t\t\t  ▀▀▀ ▀▀▀·▀  ▀ ▀▀▀  ▀█▄▀▪·▀  ▀    ·▀▀▀▀  ▀█▄▀▪ ▀▀▀  ▀▀▀  ▀▀▀ .▀  ▀
"""
        text = text.replace('▪', f'{Fore.GREEN}▪{Fore.LIGHTMAGENTA_EX}')
        text = text.replace('•', f'{Fore.GREEN}•{Fore.LIGHTMAGENTA_EX}')
        text = text.replace('·', f'{Fore.GREEN}·{Fore.LIGHTMAGENTA_EX}')
        text = text.replace('.', f'{Fore.GREEN}.{Fore.LIGHTMAGENTA_EX}')
        align(text)

    def info():
        align(f"""{Fore.WHITE}
╔═══════════════════════════════════════════════════════════════════════════════════╗
║                                                                                   ║
║          {color(">", "green")} About: {Fore.LIGHTMAGENTA_EX}This Tool Uses Zefoy To Bot TikTok Stats.{Fore.WHITE}                     ║
║          {color(">", "green")} Updates: {Fore.LIGHTMAGENTA_EX}Error Fix & Adjustment --4/15/2022{Fore.WHITE}                          ║
║          {color(">", "green")} Made By: {Fore.LIGHTMAGENTA_EX}neoN#6035{Fore.WHITE}                                                ║
║          {color(">", "green")} Github: {Fore.LIGHTMAGENTA_EX}https://github.com/shech24{Fore.WHITE}                             ║
║          {color(">", "green")} Download Chrome Driver: {Fore.LIGHTMAGENTA_EX}https://chromedriver.chromium.org/downloads{Fore.WHITE}  ║
║                                                                                   ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
""")

    def options():
        align(f"""{Fore.WHITE}
╔═══════════════════════════════╗
║                               ║
║          {color("1", "green")} {Fore.LIGHTMAGENTA_EX}Start{Fore.WHITE}            ║
║          {color("2", "green")} {Fore.LIGHTMAGENTA_EX}Info{Fore.WHITE}             ║
║          {color("3", "green")} {Fore.LIGHTMAGENTA_EX}Options{Fore.WHITE}          ║
║          {color("4", "green")} {Fore.LIGHTMAGENTA_EX}Clear{Fore.WHITE}            ║
║          {color("5", "green")} {Fore.LIGHTMAGENTA_EX}Exit{Fore.WHITE}             ║
║                               ║
╚═══════════════════════════════╝
""")

    def botOptions():
        align(f"""{Fore.WHITE}
╔═══════════════════════════════╗
║                               ║
║          {color("1", "green")} {Fore.LIGHTMAGENTA_EX}Follows{Fore.WHITE}          ║
║          {color("2", "green")} {Fore.LIGHTMAGENTA_EX}Hearts{Fore.WHITE}           ║
║          {color("3", "green")} {Fore.LIGHTMAGENTA_EX}Views{Fore.WHITE}            ║
║          {color("4", "green")} {Fore.LIGHTMAGENTA_EX}Shares{Fore.WHITE}           ║
║          {color("5", "green")} {Fore.LIGHTMAGENTA_EX}All{Fore.WHITE}              ║
║                               ║
╚═══════════════════════════════╝
""")

    def cooldowns(self):
        align(f"""{Fore.WHITE}
╔═══════════════════════════════╗
║          {color(">", "green")} {Fore.LIGHTMAGENTA_EX}Cool Downs {color("<", "green")}║
║          {color(">", "green")} {Fore.LIGHTMAGENTA_EX}Follows: {Fore.LIGHTCYAN_EX}{self.a}s{Fore.WHITE}             ║
║          {color(">", "green")} {Fore.LIGHTMAGENTA_EX}Hearts: {Fore.LIGHTCYAN_EX}{self.b}s{Fore.WHITE}              ║
║          {color(">", "green")} {Fore.LIGHTMAGENTA_EX}Views: {Fore.LIGHTCYAN_EX}{self.c}s{Fore.WHITE}               ║
║          {color(">", "green")} {Fore.LIGHTMAGENTA_EX}Shares: {Fore.LIGHTCYAN_EX}{self.d}s{Fore.WHITE}              ║
║                               ║
╚═══════════════════════════════╝
""")

    def refresh():
        system("cls")
        printing.text()
        align(f"\n\n\t\t\t{color('>', 'green')} Made By: {Fore.LIGHTMAGENTA_EX}neoN#6035 {color('<', 'green')}")
        align(f"\t\t\t\t{color('>', 'green')} {Fore.LIGHTGREEN_EX}Github: {Fore.LIGHTMAGENTA_EX}https://github.com/shech24 {color('<', 'green')}")
        printing.options()

def start(video, botChoice):

    option = webdriver.ChromeOptions()
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    try:
        service = Service(executable_path="C:\\Users\\YOUR\\PATH\\HERE\\chromedriver.exe")
        driver = webdriver.Chrome(service=service, options=option)
    except Exception as DriverError:
        print(f"{color('>', 'red')} {Fore.LIGHTRED_EX}Error: {DriverError}")
        input(f"{color('>', 'red')} {Fore.LIGHTRED_EX}Press Enter to Exit")
        exit()

    driver.get("https://zefoy.com")
    
    if driver.title == "zefoy.com | 502: Bad gateway":
            print(f"{color('>', 'red')} Zefoy Is Down... Attempting To Fix.\n")
            while driver.title == "zefoy.com | 502: Bad gateway":
                time.sleep(20)
                driver.refresh()
                if driver.title != "zefoy.com | 502: Bad gateway":
                    print(f"\n{color('>', 'red')} Fixed! Zefoy is Back Up. Starting Now.\n")
                    break
    else:
        print(f"\n{color('>', 'green')} Zefoy Is Up!\n")
    
    captchaCheck = input(f"{color('>>>', 'green')} Type \"y\" Once You Finished The Captcha: {Fore.LIGHTMAGENTA_EX}")
    captchaFinish = False

    if captchaCheck == "y":
        while captchaFinish != True:
            try:
                driver.find_element(By.XPATH, "/html/body/div[4]/div[1]/div[3]/div/div[1]/div/h5")
                captchaFinish = True
            except:
                print(f"\n{color('>', 'red')} You Didn't Finish The Captcha.")
                input(f"{color('>>>', 'green')} Type \"y\" Once You Finished The Captcha: {Fore.LIGHTMAGENTA_EX}")

    #Defining Find Cooldown
    def findCooldown(xpath):
        cooldown = driver.find_element(By.XPATH, xpath).text

        #String Slicing For Minutes
        minute1 = cooldown.find("wait") + 4
        minute2 = minute1
        while True:
            minute2 += 1
            if cooldown[minute2] == "m":
                break

        #String Slicing For Seconds
        second1 = cooldown.find(")") + 1
        second2 = second1
        while True:
            second2 += 1
            if cooldown[second2] == "s":
                break
        
        #Returning Minutes & Second Added
        return (int(cooldown[minute1:minute2])*60) + int(cooldown[second1:second2])

    print(f"\n{color('>', 'green')} Captcha is Finished, Starting...\n")

    #Defining Xpaths
    home = "/html/body/nav/ul/li/a"

    views_enter = "/html/body/div[4]/div[1]/div[3]/div/div[4]/div/button"
    views_input = "/html/body/div[4]/div[5]/div/form/div/input"
    views_search = "/html/body/div[4]/div[5]/div/form/div/div/button"
    views_submit = "/html/body/div[4]/div[5]/div/div/div[1]/div/form/button"
    views_cooldowns = "/html/body/div[4]/div[5]/div/div/h4"

    shares_enter = "/html/body/div[4]/div[1]/div[3]/div/div[5]/div/button"
    shares_input = "/html/body/div[4]/div[6]/div/form/div/input"
    shares_search = "/html/body/div[4]/div[6]/div/form/div/div/button"
    shares_submit = "/html/body/div[4]/div[6]/div/div/div[1]/div/form/button"
    shares_cooldowns = "/html/body/div[4]/div[6]/div/div/h4"

    hearts_enter = "/html/body/div[4]/div[1]/div[3]/div/div[2]/div/button"
    hearts_input = "/html/body/div[4]/div[3]/div/form/div/input"
    hearts_search = "/html/body/div[4]/div[3]/div/form/div/div/button"
    hearts_submit = "/html/body/div[4]/div[3]/div/div/div[1]/div/form/button"
    hearts_cooldowns = "/html/body/div[4]/div[3]/div/div/h4"

    follows_enter = "/html/body/div[4]/div[1]/div[3]/div/div[1]/div/button"
    follows_input = "/html/body/div[4]/div[2]/div/form/div/input"
    follows_search = "/html/body/div[4]/div[2]/div/form/div/div/button"
    follows_submit = "/html/body/div[4]/div[2]/div/div/div[1]/div/form/button"
    follows_cooldowns = "/html/body/div[4]/div[2]/div/div/h4"

    #List of Xpaths for the Bot All
    enterList = [
        [follows_enter, follows_input, follows_search, follows_submit, follows_cooldowns, "Follows"],
        [views_enter, views_input, views_search, views_submit, views_cooldowns, "Views"],
        [hearts_enter, hearts_input, hearts_search, hearts_submit, hearts_cooldowns, "Hearts"],
        [shares_enter, shares_input, shares_search, shares_submit, shares_cooldowns, "Shares"],
    ]

    #Defining Cool-downs
    follows_cooldown = 0
    hearts_cooldown = 0
    views_cooldown = 0
    shares_cooldown = 0

    #Defining Boolean
    continue1 = False
    continue2 = False

    time.sleep(5)

    #Defining Botting Function, Uses XPaths as parameters
    def bot(which, enter, input, search, submit, con1, con2, cooldownText, cooldownTime):
        amount = 0
        while captchaFinish:
            driver.refresh()

            #Checks If Zefoy Down
            if driver.title == "zefoy.com | 502: Bad gateway":
                print(f"{color('>', 'red')} Zefoy Is Down... Attempting To Fix.\n")
                while driver.title == "zefoy.com | 502: Bad gateway":
                    time.sleep(20)
                    driver.refresh()
                    if driver.title != "zefoy.com | 502: Bad gateway":
                        print(f"\n{color('>', 'red')} Fixed! Zefoy is Back Up. Starting Now.\n")
                        break

            print(f"{color('>', 'green')} Sending {which}...")
            try:
                driver.find_element(By.XPATH, enter).click()
                time.sleep(1)
                driver.find_element(By.XPATH, input).send_keys(video)
                con1 = True
            except:
                con1 = False
                print(f"\n{color('>', 'red')} {which} Page is Down on Zefoy.")
                print(f"{color('>', 'red')} Stopped.")
                time.sleep(1000000)
            if con1 == True:
                time.sleep(2)
                driver.find_element(By.XPATH, search).click()
                time.sleep(3)
                try:
                    driver.find_element(By.XPATH, submit).click()
                    con2 = True
                    print(f"{color('>', 'green')} Sent {which}, Getting Cool Down\n")
                except:
                    con2 = False
                    print(f"{color('>', 'red')} {which} Cool Down Isn't Finished, Getting Cool Down.\n")
                    time.sleep(5)
                    cooldownTime += findCooldown(cooldownText)
                if con2 == True:
                    time.sleep(5)
                    cooldownTime += findCooldown(cooldownText)
                else:
                    pass
            else:
                pass

            amount += 1
            driver.find_element(By.XPATH, home).click()
            print(f"{color('>', 'green')} Completed {Fore.LIGHTCYAN_EX}{amount} {Fore.LIGHTGREEN_EX}Time.")
            print(f"{color('>', 'green')} Cooldown: {Fore.LIGHTCYAN_EX}{cooldownTime}s\n")
            for i in range(10):
                time.sleep(cooldownTime/10)
                driver.refresh()
                print(f"{color('>', 'green')} Cool-Down: {Fore.LIGHTCYAN_EX}{i+1}/10")

            print(f"\n{color('>', 'green')} Finished Cool Down, Restarting...\n")
            time.sleep(5)

    def botAll(boolean):
        amount = 0
        while True:

            #Checks If Zefoy Down
            if driver.title == "zefoy.com | 502: Bad gateway":
                print(f"{color('>', 'red')} Zefoy Is Down... Attempting To Fix.\n")
                while driver.title == "zefoy.com | 502: Bad gateway":
                    time.sleep(20)
                    driver.refresh()
                    if driver.title != "zefoy.com | 502: Bad gateway":
                        print(f"\n{color('>', 'red')} Fixed! Zefoy is Back Up. Starting Now.\n")
                        break

            driver.refresh()
            cooldownList = []
            if boolean:
                for i in enterList:
                    time.sleep(3)
                    print(f"{color('>', 'green')} Sending {i[5]}...")
                    try:
                        driver.find_element(By.XPATH, i[0]).click()
                        time.sleep(1)
                        driver.find_element(By.XPATH, i[1]).send_keys(video)
                        continue1 = True
                    except:
                        print(f"{color('>', 'red')} {i[5]} Page is Down on Zefoy.\n")
                        cooldownList.append(0)
                        continue1 = False
                        driver.find_element(By.XPATH, home)

                    if continue1 == True:
                        time.sleep(2)
                        driver.find_element(By.XPATH, i[2]).click()
                        time.sleep(3)

                        try:
                            driver.find_element(By.XPATH, i[3]).click()
                            continue2 = True
                            print(f"{color('>', 'green')} Sent {i[5]}, Getting Cool Down.\n")
                        except:
                            print(f"{color('>', 'red')} {i[5]} Cool Down Isn't Finished, Getting Cool Down.\n")
                            time.sleep(5)
                            cooldownList.append(findCooldown(i[4]))
                            driver.find_element(By.XPATH, home).click()
                            continue2 = False

                        if continue2 == True:
                            time.sleep(5)
                            cooldownList.append(findCooldown(i[4]))
                            driver.refresh()
                    else:
                        pass
                else:
                    pass
                
                amount +=1
                cooldownList.sort()


                print(f"{color('>', 'green')} Completed {amount} Time.")
                print(f"{color('>', 'green')} Cooldown: {Fore.LIGHTCYAN_EX}{cooldownList[-1]}s\n")

                for i in range(10):
                    time.sleep(cooldownList[-1]/10)
                    driver.refresh()
                    print(f"{color('>', 'green')} Cool-Down: {Fore.LIGHTCYAN_EX}{i+1}/10")

            time.sleep(5)
            print(f"\n{color('>', 'green')} Finished Cool Down, Restarting...\n")
            driver.refresh()

    if botChoice == 1:
        bot("Follows", follows_enter, follows_input, follows_search, follows_submit, continue1, continue2, follows_cooldowns, follows_cooldown)
    elif botChoice == 2:
        bot("Hearts", hearts_enter, hearts_input, hearts_search, hearts_submit, continue1, continue2, hearts_cooldowns, hearts_cooldown)
    elif botChoice == 3:
        bot("Views", views_enter, views_input, views_search, views_submit, continue1, continue2, views_cooldowns, views_cooldown)
    elif botChoice == 4:
        bot("Shares", shares_enter, shares_input, shares_search, shares_submit, continue1, continue2, shares_cooldowns, shares_cooldown)
    elif botChoice == 5:
        botAll(True)

printing.refresh()

while True:
    choice = input(f"{color('>>>', 'green')} Choice: {Fore.LIGHTMAGENTA_EX}")
    if choice == "1":
        video = input(f"{color('>>>', 'green')} TikTok Video URL: {Fore.LIGHTMAGENTA_EX}")
        printing.botOptions()
        option = input(f"\n{color('>>>', 'green')} Which to Bot: {Fore.LIGHTMAGENTA_EX}")
        start(video, int(option))
        break

    elif choice == "2":
        printing.info()
    elif choice == "3":
        printing.options()
    elif choice == "4":
        printing.refresh()
    elif choice =="5":
        exit(): "))
        print()
        check = self.check_url(video_url)
        if not check:
            return self.error("This URL does not exist.")
        self.send_bot(video_url, ver, div)

obj = automator()
obj.main()
