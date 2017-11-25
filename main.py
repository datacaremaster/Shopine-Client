from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.properties import ObjectProperty
from kivy.properties import ListProperty
from kivy.lang.builder import Builder
from kivy.uix.behaviors import ButtonBehavior 
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import urllib
import json
import urllib2


#globals
#shopping_service_url='http://localhost:8080/api/items/?'
shopping_service_url='http://datacaremaster.com/itemsapi/api/items/?'

Countries ={'U.S.': 'US','U.K.': 'GB','Canada': 'CA'}

#need set utf-8 to handle non-ascii
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class LocationDropDown(DropDown):
    pass

class SearchBox(BoxLayout):
    locationdropdown=ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SearchBox, self).__init__(**kwargs)
        Clock.schedule_once(self.init_locationdropdown, 0)

    def init_locationdropdown(self, dt=0):
        self.locationdropdown=LocationDropDown()
        btnloc=self.ids["btnlocation"]
        btnloc.bind(on_release=self.locationdropdown.open)
        self.locationdropdown.bind(on_select=lambda instance, x: setattr(btnloc, 'text', x))


    def do_search(self, keyword, maxprice, location):
        if keyword:
            searchopt = {}
            searchopt['kw'] = keyword
            if maxprice:
                searchopt['maxp'] = maxprice
            if location:
                try:
                    searchopt['loc'] = Countries[location]
                except KeyError:
                    pass
           
            shopping_service_fullurl = shopping_service_url+urllib.urlencode(searchopt)
            try:
                response=json.load(urllib2.urlopen(shopping_service_fullurl))
                #need handle no items response to avoid error
                if response and response['Item'] and response['Item']['WhadaaData'] and response['Item']['WhadaaData']['ItemList']:
                    self.parent.ids.itemsresultdisplay.opacity=1
                    self.parent.ids.noresultdisplay.opacity=0
                    self.parent.ids.itemsresultdisplay.ids.itemlistdisplay.itemlist=response['Item']['WhadaaData']['ItemList']
                else:
                    self.parent.ids.itemsresultdisplay.opacity=0
                    self.parent.ids.noresultdisplay.opacity=1
            except:
                pass
                #raise

    def do_reset(self):
        self.ids.searchkeyword.text=''
        self.ids.maxprice.text=''


class ItemListDisplay(BoxLayout):
    itemlist=ObjectProperty(None)

    item_template = StringProperty('ItemRecord')

    def __init__(self, **kwargs):
        super(ItemListDisplay, self).__init__(**kwargs)
        self.fetch_data_from_datasource()
        self.display_itemlist(self.data)

    def fetch_data_from_datasource(self):
        self.data=[]


    def display_itemlist(self, itemlist):
        self.clear_widgets()
        for item in itemlist:
            w = Builder.template(self.item_template, **item)
            self.add_widget(w)

    def on_itemlist(self, instance, value):
        self.display_itemlist(value)

class ShopineApp(App):
    def get_itemsource_image(self, srcname):
        if srcname==2:
            img ='img/amazon-icon.png'
        elif srcname==1:
            img ='img/ebay-icon.png'
        else:
            img ='img/noimage-icon.png'

        return img

if __name__=='__main__':
    ShopineApp().run()