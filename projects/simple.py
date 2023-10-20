AppName = "ROOT"
color = [187,187,187,1] #LIGHT_GRAY



class Startup:

    color = [88,196,221,0.1] #BLUE      
    s = ROOT.Startup2()
    def toto(self):
        aaaaaaaaaa()
        bbbbbbbbbb()
        cccccccccc()
        dddddddddd()
        eeeeeeeeee()
        ffffffffff()
        gggggggggg()
        #hhhhhhhhhh()
        ROOT.Startup3.toto.a111111111()
        iiiiiiiiii()
    
class Startup2:
    s = ROOT.Startup3()
    color = [88,196,221,0.1] #BLUE   
    def toto(self):
        a111111111()
        a222222222()
        a333333333()
        a444444444()
        a555555555()

class Startup3:

    color = [88,196,221,0.1] #BLUE   
    def toto(self):
        a111111111()
        a222222222()
        a333333333()
        a444444444()
        a555555555()


class Startup4:

    color = [88,196,221,0.1] #BLUE   
    def toto(self):
        a111111111()
        a222222222()
        ROOT.Startup3.toto.a333333333()
        a444444444()
        a555555555()


class MyScenario:
    def Launch(self): 
        ROOT.Startup.toto()