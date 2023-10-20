from opengl.Shape import *
import pygame as pg
import pygame.freetype

class Text(Shape):
    def __init__(self, text, size):
        super().__init__(False)
        self.text = text
        self.size = size       
        self.tex = self.genTextureForText(text, None, 0)
        #self.genTextureForText(text, None, 1)
        #self.genTextureForText(text, None, 2)
        #self.genTextureForText(text, None, 3)

        
    def genTextureForText(self, text, existingTexture, level):
        font = pygame.freetype.SysFont('Times New Roman', 256/pow(2,level))
        textSurface = font.render(text, (255,255,255,255), (255,0,0,0))[0]
        w = textSurface.get_width()
        h = textSurface.get_height()   
        self.aspect = w/h
        image = pg.image.tobytes(textSurface, "RGBA", True)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        if existingTexture==None:
            texture = glGenTextures(1)
        else:
            texture=existingTexture
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexImage2D(GL_TEXTURE_2D, level, GL_RGBA, w, h, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_BLEND)  
        glGenerateMipmap(GL_TEXTURE_2D) #??
        glActiveTexture(GL_TEXTURE0)
     
        return texture
    
    def getMinX(self):
        return -self.size*self.aspect*0.5
    def getMaxX(self):
        return self.size*self.aspect*0.5
    def getMinY(self):
        return -self.size*0.5
    def getMaxY(self):
        return self.size*0.5

    
    def drawGeometry(self, wireframe):                
        glDisable(GL_TEXTURE_2D)
        glColor4f(1,0,1,0); 

        glEnable(GL_TEXTURE_2D)
        glBindTexture (GL_TEXTURE_2D, self.tex)
        glColor4f(1,1,1,1); 
       
        glBegin (GL_QUADS)
        glTexCoord2f (0,0)
        glVertex2f (self.getMinX(), self.getMinY())

        glTexCoord2f (1, 0)
        glVertex2f (self.getMaxX(), self.getMinY())
        
        glTexCoord2f (1,1)
        glVertex2f (self.getMaxX(), self.getMaxY())

        glTexCoord2f (0, 1)
        glVertex2f (self.getMinX(), self.getMaxY())
        glEnd()

        glDisable(GL_TEXTURE_2D)