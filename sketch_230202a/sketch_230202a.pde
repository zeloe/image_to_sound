/**
 * Array Objects. 
 * 
 * Demonstrates the syntax for creating an array of custom objects. 
 */
import oscP5.*;
import netP5.*;
int unit = 50;
int count;
int posx = 0;
int posy = 0;
int qposx = 0;
int qposy = 0;
int size = 0;
int index = 0;
OscP5 oscP5;
String path = "black.png";
PImage img;
void setup() {
  size(1000, 500);
  noStroke();
  oscP5 = new OscP5(this,8000);
  background(0);
    img = loadImage(path);
  }

void oscEvent(OscMessage theOscMessage){
  if(theOscMessage.checkAddrPattern("/pos") == true)
  {
    posy = theOscMessage.get(0).intValue();
    posx = theOscMessage.get(1).intValue();
  }
  if(theOscMessage.checkAddrPattern("/img") == true)
  {
    path = theOscMessage.get(0).stringValue();
    qposy = theOscMessage.get(1).intValue();
    qposx = theOscMessage.get(2).intValue();
     img = loadImage(path);
  }
}
void draw() {
   
stroke(255,255,255);
 fill(255,255,255);
    strokeWeight(0);

  circle(posx,posy,1);
    
  image(img, 500, 0);
 
   noFill();
   stroke(255,0,0);
   strokeWeight(2);
   
  rect(qposx +500 +2, qposy, 50, 50);
  
   }
   
    
