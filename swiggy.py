#-------------------------------------------------------------------------------
# Name:        Swiggy Order
# Purpose:
#
# Author:      Arvind Kumar
#
# Created:     11th May 2019
# Copyright:
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# coding= utf-8

import Selenium2Library,os

class swiggy():
    #####################Contructor#####################################
    def __init__(self):
        self.obj = Selenium2Library.Selenium2Library()
        self.obj._info('init function')
        #self.parser = ConfigParser.SafeConfigParser()
        self.pythonpath = os.environ['PYTHONPATH']
        #self.objectConfigFile = self.pythonpath + "\Configuration\objectIdentifier.conf"
        #self.found = self.parser.read(self.objectConfigFile)
        self.obj._info(self.pythonpath)
        #self.obj._info(self.objectConfigFile)
        self.obj.set_selenium_speed(2)

# This Fucntion will launch browser, Part of setup
    def launch_Browser(self,url):
        try:
            self.obj.open_browser(url,browser='chrome')
            self.obj.maximize_browser_window()
            self.obj.go_to(url)
        except:
            raise Exception('Error')

# This Fucntion will close all browser. Part of teardown
    def close_Browser(self):
        try:
            self.obj.close_all_browsers()
            self.obj._info('Browsers closed')
        except:
            try:
                self.obj.close_all_browsers()
                self.obj._info('Browsers closed in expect')
            except:
                pass

# This Fucntion will enter locationa nd choose exact one
    def choose_exact_location(self,loc):
        self.obj._info('Entering location as %s'%loc)
        exact_location= str(loc)+', Karnataka, India'
        self.obj._info('Exact Location:-%s'%exact_location)

        self.obj.input_text("id=location",loc)
        xpath= "xpath= //div[@class='_3lmRa']//span[@class='_2W-T9'][contains(text(),'"+exact_location+"')]"   #Enter and choose exact location
        self.obj._info('Waiting for first option to be visible and then select it-%s'%xpath)
        self.obj.wait_until_element_is_visible(xpath)

        self.obj.click_element(xpath)
        self.obj._info('Wait until search icon is present and visible')
        xpath= "xpath= //span[contains(text(),'Search')]"
        self.obj.wait_until_element_is_visible(xpath,timeout=90)
        self.obj.element_should_be_visible(xpath)

# This Fucntion will search restaurent name
    def search_restaurent(self,restaurent_name):
        self.obj._info('Searching for restaurent name')
        xpath= "xpath= //span[contains(text(),'Search')]"
        self.obj.wait_until_page_contains_element(xpath,timeout=90)          #Wait till Search option comes up
        self.obj.click_element(xpath)
        xpath= "xpath=//input[@placeholder='Search for restaurants or dishes']"          #Write name of restaurent
        self.obj.wait_until_page_contains_element(xpath,timeout=90)
        self.obj.wait_until_element_is_visible(xpath,timeout=90)
        self.obj.element_should_be_visible(xpath)
        self.obj.input_text("xpath=//input[@placeholder='Search for restaurants or dishes']",restaurent_name)

        xpath= "xpath= //div[contains(text(),'"+restaurent_name+"')]"
        self.obj.wait_until_page_contains_element(xpath,timeout=90)
        self.obj.wait_until_element_is_visible(xpath,timeout=90)
        #Click on restaurent name
        xpath= "xpath=//div[contains(text(),'"+restaurent_name+"')]"
        self.obj.click_element(xpath)
        xpath= "xpath= //h2[contains(text(),'Recommended')]"           #Wait till text is shown and loaded fully
        self.obj.wait_until_page_contains_element(xpath,timeout=90)
        self.obj.wait_until_element_is_visible(xpath,timeout=90)

# This Fucntion will select items which will order
    def select_items_to_order(self,item,item_cnt):
        self.obj._info('Choose item to add-%s-%s'%(item,item_cnt))
        xpath= "xpath=//div[@class='_2SyqU'][contains(text(),'"+item+"')]/../../../../div[3]/div[2]/div[text()='ADD']"     #Click on Add button
        self.obj._info('Adding Item with xpath-%s'%xpath)
        self.obj.wait_until_page_contains_element(xpath,timeout=90)
        self.obj.click_element(xpath)
        xpath= "//div[@class='_2SyqU'][contains(text(),'"+item+"')]/../../../../div[3]/div[2]/div[4]"   #Get cake count, Will use it to order
        count= self.obj.get_text(xpath)
        self.obj._info('count is:%s'%count)
        if int(item_cnt)>int(count):
            loop_cnt= int(item_cnt)-int(count)
            plus_xpath= "xpath=//div[@class='_2SyqU'][contains(text(),'"+item+"')]/../../../../div[3]/div[2]/div[2]"      #Click on + sign to add
            self.obj._info(plus_xpath)
            for c in range(int(loop_cnt)):
                self.obj._info('Click plus sign-%s'%c)
                self.obj.click_element(plus_xpath)

# This Fucntion will input all text during signup#
    def checkout_and_get_all_items_on_checkout_page(self):
        self.obj._info('Checkout now..')
        xpath= "xpath= //div[@class='_1gPB7']"        #click on checkout button
        self.obj.click_element(xpath)
        xpath= "//div[@class='_2pdCL']/div"
        self.obj._info(xpath)
        self.obj.wait_until_page_contains_element(xpath,timeout=90)     #Wait until checkout done and moved to next page
        count_of_itemtype= self.obj.get_matching_xpath_count(xpath)
        self.obj._info(count_of_itemtype)
        i= 1
        self.item_hash= {}
        baseurl= "xpath=//div[@class='_2pdCL']"
        while i<=int(count_of_itemtype):
            itemurl= baseurl+"/div["+str(i)+"]/div[1]/div[2]"                    #Get name of item
            self.obj.wait_until_page_contains_element(itemurl,timeout=90)
            itemname= self.obj.get_text(itemurl)
            itemurlcount= baseurl+"/div["+str(i)+"]/div[2]/div/div[1]/div[4]"    #Get count of item
            self.obj.wait_until_page_contains_element(itemurlcount,timeout=90)
            itemcount= self.obj.get_text(itemurlcount)
            #create a hash
            self.item_hash[itemname]= itemcount                          #create hash with item and count
            i= i+1
        self.obj._info('Hash of items and count on checkout page-%s'%self.item_hash)

# This Fucntion will verify items on checkout page#
    def verify_items_on_checkout_page(self,item,item_cnt):
        self.obj._info('Verify item count on checkout page for:-%s'%item)
        self.obj._info('Expected count-%s Actual count-%s'%(item_cnt,self.item_hash[item]))
        if int(item_cnt)!=int(self.item_hash[item]):
            raise Exception('Item count not matching for %s .. Failure...'%item)
        else:
            self.obj._info('Item count matching for %s .. Great...'%item)

# This Fucntion will input all text during signup#
    def signup(self,mobileno,name,email,password):
        self.obj._info('Sign up..')
        xpath= "xpath=//div[contains(text(),'SIGN UP')]"      #Click on signup button, class is static/constant
        self.obj._info(xpath)
        self.obj.click_element(xpath)
        #Input mobile number
        self.obj.input_text("id=mobile",mobileno)
        self.obj.input_text("id=name",name)
        self.obj.input_text("id=email",email)
        self.obj.input_text("id=password",password)
        #Click on referal code
        xpath= "xpath=//div[@class='_3GOZo']"                 #click on referal code icon, class is static/constant
        self.obj._info('Xpath is:%s'%xpath)
        self.obj.wait_until_page_contains_element(xpath,timeout=90)
        self.obj.click_element(xpath)
        #click on continue signup
        xpath= "xpath=//a[@class='_2REYC']"                   #click on continue button, class is static/constant
        self.obj._info('Xpath is:%s'%xpath)
        self.obj.wait_until_page_contains_element(xpath,timeout=90)
        self.obj.click_element(xpath)
        xpath= "xpath=//input[@id='email']/../label"
        self.obj.wait_until_page_contains_element(xpath,timeout=90)  #Wait till message inside email text box not visible
        label= self.obj.get_text(xpath)
        self.obj._info(label)

# This Fucntion will check error message while doing signup#
    def verify_email_error_and_take_screenshot(self):
        xpath= "xpath=//input[@id='email']/../label"
        self.obj.wait_until_page_contains_element(xpath,timeout=90)  #Wait till message inside email text box not visible
        label= self.obj.get_text(xpath)
        self.obj._info(label)
        if str(label)=='Invalid email address':                      #Compare email box error label
            self.obj._info("seems Error message related to email field")
            #Capture screenshot
            self.obj.capture_page_screenshot()

# This Fucntion will update cart items on checkout page#
    def update_items_during_checkout(self,item,item_cnt):
        self.obj._info('Choose item to update with count-%s-%s'%(item,item_cnt))
        xpath= "//div[contains(text(),'"+item+"')]/../../div[2]/div/div[1]/div[4]"   #xpath used to count no of items in checkout page
        count= self.obj.get_text(xpath)
        self.obj._info('count is:%s'%count)
        if int(count)>int(item_cnt):
            loop_cnt= int(count)-int(item_cnt)
            minus_xpath= "xpath=//div[contains(text(),'"+item+"')]/../../div[2]/div/div[1]/div[3]"    #Update item count in cart
            self.obj._info(minus_xpath)
            for c in range(int(loop_cnt)):
                self.obj._info('Click Minus sign during checkout-%s'%c)
                self.obj.click_element(minus_xpath)
        #Wait until loading is done if any
        xpath= "//div[contains(text(),'"+item+"')]/../../div[2]/div/div[1]/div[4]"
        self.obj.wait_until_page_contains_element(xpath,timeout=90)
        self.obj._info('Capture current screenshot & close Browser')
        self.obj.capture_page_screenshot()

